# Test-Weather #

## Purpose ##

The purpose of this exercise was to be able to demonstrate my ability to understand the problem space and build a technical solution that achieved the goal of the project. 

I had a lot of fun (and wasted far too much time) exploring certain aspects of this project, for instance, how to go about creating a random number within a known set of boundaries that would tend towards a bell curve.

As with most of these sorts of exercises I'm happy with it for the most part as it does what it's supposed to, but I would have loved to have been able to spend more time on this to improve the accuracy and performance.

## How It Works ##

- The user passes in (optionally) a start date, and end date and a resolution (Hourly, Daily, Monthly) and the programme will create line items for each location on that resolution for the date range.
- The locations themselves are in a text field and also supply the details of the IATA, lat long and elevation and details of monthly weather metrics
- The figures (pressure, temperature and humidity) are effectively random numbers within a set of boundaries (boundaries are effectively set from within the text file of locations) tending towards a bell curve
- The conditions are derived from a prescribed set of conditions using the temp, pressure and humidity as inputs.
- When the application runs it will print to screen upto the first ten records created and all of the data will be written to disk in the same location as the application iteself using the file naming convention 'output-[YYYYmmddHHMM].txt'

## How To Run It ##

- Download the repo
- From the command line cd into the src directory
- Run `pip install --user pipenv`
- Run `pipenv install requests`
- Run `pipenv run python ./weathergenerator.py`
- Run `pipenv run python ./weathergenerator.py -r h -sd 2018-01-01 -ed 2018-08-15` hourly resolution between those two dates (sd = start date and ed = end date)
- Run `pipenv run python ./weathergenerator.py -h` for help

## Known Shortcomings ##

- Accurate seed data. I wish I had more time to curate more and more accurate data
- The standard distribution of temperatures is not accurate because I was unwilling to spend the time modeling accurate bell curves
- I found it difficult to find accurate information on humidity maximum / minimum and pressure maximum / minimum so those figures are not entirely accurate and are using a standard bell curve around those contrived boundaries
- I wanted to build this to scale nicely but ran out of time to add in any form of parallelisation