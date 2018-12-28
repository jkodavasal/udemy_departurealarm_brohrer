import datetime
import requests
import pandas as pd
import os, time

def download_data(verbose=True):
    """
    Pull the data down from the public servers.

    Parameters
    ----------
    verbose: boolean
    
    Returns
    -------
    trips: list of dicts
        Each dictionary has a 'dep' and 'arr' field.
        indicating the departure and arrival datetimes
        for each trip.
    """
    # Harvard Square. Red line stop. outbound
    harvard_stop_id = '70068'
    # JFK / UMass. Red line stop. inbound
    jfk_stop_id = '70086'
    # Gather trip data from a time window from each day
    # over many days.
    start_time = datetime.time(7, 0)
    end_time = datetime.time(10, 0)
    start_date = datetime.date(2018, 5, 1)
    end_date = datetime.date(2018, 5, 5)

    TTravelURL = "http://realtime.mbta.com/developer/api/v2.1/traveltimes"
    TKey = "?api_key=wX9NwuHnZU2ToO7GmGR9uw"
    TFormat = "&format=json"
    from_stop = "&from_stop=" + str(jfk_stop_id)
    to_stop = "&to_stop=" + str(harvard_stop_id)

    # Cycle through all the days
    i_day = 0
    trips = []
    while True:
        check_date = start_date + datetime.timedelta(days=i_day)
        if check_date > end_date:
            break

        # Formulate the query
        from_time = datetime.datetime.combine(check_date, start_time)
        to_time  = datetime.datetime.combine(check_date, end_time)
        TFrom_time = "&from_datetime=" + str(int(from_time.timestamp()))
        TTo_time = "&to_datetime=" + str(int(to_time.timestamp()))

        SRequest = "".join([
            TTravelURL,
            TKey,
            TFormat,
            from_stop, to_stop,
            TFrom_time, TTo_time
        ])
        s = requests.get(SRequest)
        s_json = s.json()
        for trip in s_json['travel_times']:
            trips.append({
                'dep': datetime.datetime.fromtimestamp(
                    float(trip['dep_dt'])),
                'arr': datetime.datetime.fromtimestamp(
                    float(trip['arr_dt']))})
        if verbose:
            print(check_date, ':', len(s_json['travel_times']))
    
        i_day += 1
    
    return trips


if __name__ == '__main__':
    """
    added the above two lines to force python shell's timezone to US/Eastern
    note Daylight Savings is automatically accounted for
    """
    os.environ['TZ'] = 'US/Eastern'
    time.tzset()

    print('Current timezone ', time.tzname, '\n')
    print('Number of trips between 7 AM and 10 AM \npulled from MBTA database for \nMay 1, 2018 through May 5, 2018\n')
    trips_df = download_data()
# trips_df is actually a list of dictionaries, not a dataframe.

