# Weather-Sales-Predictor
Kaggle Competition for predicting how sales of weather-sensitive products are affected by snow and rain



Files

-Train.csv
Contains date, store number item number and units sold

-train_filtered.csv
Contains same as train.csv except removes all rows with units value 0

-train_filtered2.csv
Rearranges the columns of a CSV file so that the last column (units) becomes the first column.
Want to make crossreferencing based on units

-train_filtered3.csv
This function enriches the 'train_filtered2.csv' dataset by adding a 'station' column,
using a mapping of store IDs to station IDs from 'key.csv'.


-weather.csv
weather data

-weather_with_day_of_week.csv
This function adds a 'dayNum' column to the 'weather.csv' dataset, representing the day of the week (values 1-7)
for each date in the second column, and saves the result as 'weather_with_day_of_week.csv'.


-weather_with_weekday_weekend.csv
This function adds 'weekday' and 'weekend' columns to the 'weather_with_day_of_week.csv' dataset,
classifying each day as a weekday (1) or weekend (0), and saves the result as 'weather_with_weekday_weekend.csv'.

-weather_with_weather_codes2.csv
Take weather codes.csv adn remove everything except the tavg and all weather codes. so Columns C,D,F-T


- merged_data.csv
This function combines data from 'train_filtered3.csv' and 'weather_with_weather_codes2.csv'
based on matching 'date' and 'station_nbr', and saves the result as 'train_filtered4.csv'.


need to refractor all the code so it just uses PDs and doesnt have to use a million csvs


