#!/usr/bin/env python

# TODO: Add more data
# TODO: Test Performance
# TODO: Push to git

import requests
from dateutil import rrule, relativedelta
import random
import math
import json
from datetime import timedelta, date, datetime
import calendar
import argparse

maximum_dist = 31
mult_dist = [0]*maximum_dist
locations = {}

#######################################

def run():
    st = datetime.now()
    human_resolution = 'Daily'

    # Get and parse the command line inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('-sd', '--start_date', help='pass the start date for the weather you want to view ("YYYY-MM-DD")', type=lambda d: datetime.strptime(d, '%Y-%m-%d'), default=datetime.now() - timedelta(365/12))
    parser.add_argument('-ed', '--end_date', help='pass the end date for the weather you want to view, will default to today if not supplied ("YYYY-MM-DD")', type=lambda d: datetime.strptime(d, '%Y-%m-%d'), default=datetime.now())
    parser.add_argument('-r', '--resolution', help='add the resolution of the data you want ("h" for hourly, "d" for days or "m" for months)"', default='d', choices=['h','d','m'])
    args = parser.parse_args()

    start_date = args.start_date
    end_date = args.end_date
    resolution = args.resolution

    if start_date > end_date:
        print("Cheeky... Let's just swap those two round")
        temp_date = end_date
        end_date = start_date
        start_date = temp_date

    human_resolution = ('Hourly' if resolution == 'h' else human_resolution)
    human_resolution = ('Monthly' if resolution == 'm' else human_resolution)

    print('Start_date: {}\nEnd_date: {}\nwith a resolution of {}'.format(start_date, end_date, human_resolution))

    # Loop through the dates and locations and write each line to disk
    sample_size = 10
    i = 0
    print ('Sample data for the following locations: \n\t{}'.format('\n\t'.join(locations)))
    
    fname = 'output-{}.txt'.format(datetime.now().strftime('%Y%m%d%H%M'))
    with file(fname, 'w') as f:
        for single_date in daterange(start_date, end_date, resolution):
            for locale, data in locations.iteritems():
                i += 1
                li = get_line_item(locale, single_date)
                if (i<10):
                    print ('{0}|{1}|{2}|{3}|{4:.2f}|{5:.2f}|{6:.2f}'.format(data['IATA'], data['LatLong'], single_date.strftime('%Y-%m-%dT%H:%M:%SZ'), li['conditions'], li['temp'], li['pressure'], li['humidity']))
                f.write('{0}|{1}|{2}|{3}|{4:.2f}|{5:.2f}|{6:.2f}\n'.format(data['IATA'], data['LatLong'], single_date.strftime('%Y-%m-%dT%H:%M:%SZ'), li['conditions'], li['temp'], li['pressure'], li['humidity']))

    et = datetime.now()
    rd = relativedelta.relativedelta (et, st)
    print ('Finished, test data written to {} in {}.{} seconds'.format(fname, rd.seconds, rd.microseconds))

#######################################

def get_line_item(loc, date):
    #step 0 - get the month from the date
    month = date.strftime("%B")
    loc_month = locations[loc][month]
    
    # step 1 - get the temp for the loc_month
    temp = get_num_within_range(loc_month['MaxMaxTemp'], loc_month['MeanMaxTemp'], loc_month['MinMaxTemp'])

    # step 2 - get the humidity for the loc month
    humidity = get_num_within_range(loc_month['MaxHumidity'], loc_month['MeanHumidity'], loc_month['MinHumidity'])

    # step 3 - get the barometric pressure for the loc month
    pressure = get_num_within_range(loc_month['MaxPressure'], loc_month['MeanPressure'], loc_month['MinPressure'])

    # step 4 - get the conditions based on the above information
    total_month_days = calendar.monthrange(int(date.strftime('%Y')), int(date.strftime('%m')))[1]
    conditions = get_conditions(temp, humidity, pressure, loc_month['RainyDays'], loc_month['SunnyDays'], loc_month['CloudyDays'],total_month_days - sum([loc_month['RainyDays'], loc_month['SunnyDays'], loc_month['CloudyDays']]))

    return {
        'temp':temp,
        'humidity':humidity,
        'pressure':pressure,
        'conditions':conditions
    }

#######################################

# TODO: add tests
def get_conditions(temp, humidity, pressure, rainy_days, sunny_days, cloudy_days, other_days):

    # terms taken from: http://www.farmonlineweather.com.au/help/article.jsp?id=72

    # get conditions based on the number of rainy days, sunny days and cloudy days as per the locations data.
    cond = random.randint(1,sum([rainy_days, sunny_days, cloudy_days, other_days]))

    if cond <= rainy_days:
        if temp <= 0:
            return random.choice(['Snow', 'Blizzard', 'Late Snow'])
        else:
            if pressure < 900:
                return 'Thunderstorms'
            else:
                return random.choice(['Rain', 'Thunderstorms', 'Possible Showers', 'Rain Developing', 'Drizzle', 'Heavy Showers', 'Scattered Showers'])
    elif cond > rainy_days and cond <= sum([rainy_days, sunny_days]):
        if temp > 30:
            conditions = random.choice(['Hot, Sunny', 'Hot', 'Sunny', 'Clear'])
        else: 
            conditions = random.choice(['Sunny', 'Mostly Sunny', 'Clear'])
        if humidity > 68:
            conditions += ' and Humid'
        else:
            conditions += ' and Dry'

        return conditions
    elif cond > sum([rainy_days, sunny_days]) and cond < sum([rainy_days, sunny_days, cloudy_days]):
        return random.choice(['Overcast', 'Cloudy', 'Mostly Cloudy', 'Hazy', 'Cloud Increasing'])
    else:
        return random.choice(['Late Thunder', 'Possible Thuderstorms', 'Isolated Showers', 'Early Fog', 'Windy'])

#######################################

# TODO: add tests
def daterange(start_date, end_date, resolution):
    if resolution == 'd':
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)
    elif resolution == 'm':
        for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            yield dt
    elif resolution == 'h':
        for n in range(int ((end_date - start_date).days)*24):
            yield start_date + timedelta(hours=n)

#######################################

def get_locations_from_disk():
    global locations
    with file('locations.json', 'r') as f:
        locations = json.load(f)

#######################################

# TODO: add tests
# return a random number which given enough calls will approximate a bell curve
def get_distributed_number():
    global mult_dist
    vals = []
    for x in range(6):
        vals.append(random.randint(0,5))

    mult_dist[sum(vals)]
    return sum(vals)

#######################################

# TODO: add tests
# get a random number given boundaries and an average that will over time tend towards a bell curve of results
def get_num_within_range(high, avg, low):
    half_size = maximum_dist/2
    top_range = (high - avg) / half_size
    bot_range = (avg - low) / half_size

    multiplier = get_distributed_number()

    dev = abs(half_size - multiplier)

    if multiplier > half_size:
        initial_number = avg + (dev * top_range)
        temp = random.uniform(initial_number - top_range, min(initial_number + top_range, high))
    else:
        initial_number = avg - (dev * bot_range)
        temp = random.uniform(max(initial_number - bot_range, low), initial_number + bot_range)

    return temp

#######################################

get_locations_from_disk()

run()