import numpy as np # linear algebra
import pandas
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import csv
from datetime import datetime

# This function filters rows from 'train.csv' where the 'units' column is not equal to 0,
# and saves the filtered dataset as 'train_filtered.csv'.
# Input : train.csv
# Output : train_filtered.csv
def filter_train():
    with open('./Unfiltered_Data/train.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)
        with open('./Data_Processing/train_filtered.csv', 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(headers)

            for row in csv_reader:
                units_data = row[3]
                if int(units_data) != 0:
                    csv_writer.writerow(row)

# Rearranges the columns of a CSV file so that the last column (units) becomes the first column.
# Want to make crossreferencing based on units.
# Input : train_filtered.csv
# Output : train_filtered2.csv
def reorganize_train():
    with open('./Data_Processing/train_filtered.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # Read the header row

        # Rearrange headers: last column becomes first, followed by the rest
        new_headers = [headers[-1]] + headers[:-1]

        with open('./Data_Processing/train_filtered2.csv', 'w', newline='') as csv_output:
            csv_writer = csv.writer(csv_output)
            csv_writer.writerow(new_headers)  # Write the new headers

            for row in csv_reader:
                # Rearrange row data: last column becomes first, followed by the rest
                new_row = [row[-1]] + row[:-1]
                csv_writer.writerow(new_row)

# This function enriches the 'train_filtered2.csv' dataset by adding a 'station' column,
# using a mapping of store IDs to station IDs from 'key.csv'.
# Input : train_filtered2.csv
# Output : train_filtered3.csv

def store_station():
    # stations = pd.read_csv('./key.csv', index_col=0)
    store_station = None
    with open('./Unfiltered_Data/key.csv', 'r') as key_file:
        file_reader = csv.reader(key_file)
        headers = next(file_reader)
        store_station = dict(file_reader)

    with open('./Data_Processing/train_filtered2.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)
        with open('./Data_Processing/train_filtered3.csv', 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)

            headers.append('station_nbr')
            csv_writer.writerow(headers)

            for row in csv_reader:
                store_id = row[2]
                station_id = store_station[store_id]
                new_row = row
                new_row.append(station_id)
                csv_writer.writerow(new_row)

# This function adds a 'dayNum' column to the 'weather.csv' dataset, representing the day of the week (values 1-7)
# for each date in the second column, and saves the result as 'weather_with_day_of_week.csv'.
# Input : weather.csv
# Output : weather_with_day_of_week.csv
def day_of_week():
    format = '%Y-%m-%d'
    with open('./Unfiltered_Data/weather.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)

        with open('./Data_Processing/weather_with_day_of_week.csv', 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)

            headers.append('dayNum')
            csv_writer.writerow(headers)
            for row in csv_reader:
                date_data = row[1]
                datetime_obj = datetime.strptime(date_data, format)
                day = datetime_obj.isoweekday()
                new_row = row
                new_row.append(day)
                csv_writer.writerow(new_row)

# This function adds 'weekday' and 'weekend' columns to the 'weather_with_day_of_week.csv' dataset,
# classifying each day as a weekday (1) or weekend (0), and saves the result as 'weather_with_weekday_weekend.csv'.
# Input : weather_with_day_of_week.csv
# Output : weather_with_weekday_weekend.csv
def weekday_weekend():
    with open('./Data_Processing/weather_with_day_of_week.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)
        with open('./Data_Processing/weather_with_weekday_weekend.csv', 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)

            headers.append('weekday')
            headers.append('weekend')
            csv_writer.writerow(headers)
            for row in csv_reader:
                day = row[20]
                new_row = row
                if int(day) <= 5:
                    new_row.append('1')
                    new_row.append('0')
                else:
                    new_row.append('0')
                    new_row.append('1')
                csv_writer.writerow(new_row)

# This function adds one-hot encoded columns for each weather code in 'weather_with_weekday_weekend.csv',
# indicating the presence (1) or absence (0) of each code, and saves the result as 'weather_with_weather_codes.csv'.
# Input : train_filtered3.csv
# Output : weather_with_weather_codes.csv
def weather_codes():
    code_types = ["FC+", "FC", "TS", "GR", "RA", "DZ","SN","SG", "GS","PL","IC", "FG+", "FG", "BR", "UP","HZ", "FU", "VA", "DU", "DS", "PO", "SA", "SS", "PY", "SQ","DR","SH", "FZ", "MI", "PR", "BC", "BL","VC"]

    with open('./Data_Processing/weather_with_weekday_weekend.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)
        with open('./Data_Processing/weather_with_weather_codes.csv', 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            new_headers = headers + code_types
            csv_writer.writerow(new_headers)

            for row in csv_reader:
                weathercodes = row[12]
                current_codes = weathercodes.split()
                processed_codes = []
                onehotencoding = []
                for code in current_codes:
                    if len(code) == 4:
                        processed_codes.append(code[:2])
                        processed_codes.append(code[-2:])
                    elif len(code) < 4:
                        processed_codes.append(code)
                    # else:
                        # print(code)

                for type in code_types:
                    if type in processed_codes:
                        onehotencoding.append('1')
                    else:
                        onehotencoding.append('0')

                new_row = row + onehotencoding
                csv_writer.writerow(new_row)

# Filtering out irrelevant data
def filter_weather_codes():
    df = pd.read_csv('./Data_Processing/weather_with_weather_codes.csv')

    # List of columns to drop
    columns_to_keep = [
        'station_nbr', 'date', 'tavg', 'dayNum', 'weekday', 'weekend', 
        'FC+', 'FC', 'TS', 'GR', 'RA', 'DZ', 'SN', 'SG', 'GS', 'PL', 
        'IC', 'FG+', 'FG', 'BR', 'UP', 'HZ', 'FU', 'VA', 'DU', 'DS', 
        'PO', 'SA', 'SS', 'PY', 'SQ', 'DR', 'SH', 'FZ', 'MI', 'PR', 
        'BC', 'BL', 'VC'
    ]

    # Drop the specified columns
    df_filtered = df[columns_to_keep]

    # Save the filtered DataFrame to a new CSV file
    df_filtered.to_csv('./Data_Processing/weather_with_weather_codes2.csv', index=False)


# This function combines data from 'train_filtered3.csv' and 'weather_with_weather_codes2.csv'
# based on matching 'date' and 'station_nbr', and saves the result as 'train_filtered4.csv'.
# Input : train_filtered3.csv & weather_with_weather_codes2.csv
# Output : train_filtered4.csv
# OUTDATED - Use combine() instead
def combine_train_with_weather():
    with open('./Data_Processing/train_filtered3.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)
        new_headers= ['tavg','dayNum', 'weekday', 'weekend',
                       "FC+", "FC", "TS", "GR", "RA", "DZ","SN","SG",
                       "GS","PL","IC", "FG+", "FG", "BR", "UP","HZ",
                       "FU", "VA", "DU", "DS", "PO", "SA", "SS", "PY",
                       "SQ","DR","SH", "FZ", "MI", "PR", "BC", "BL","VC"]
        headers = headers + new_headers

        with open('./Data_Processing/weather_with_weather_codes2.csv', 'r') as weather_file:
            csv_reader2 = csv.reader(weather_file)
            next(csv_reader2)
            with open('./Data_Processing/train_filtered4.csv', 'w', newline='') as output_file:
                csv_writer = csv.writer(output_file)
                csv_writer.writerow(headers)

                for row in csv_reader2:
                    date = row[1]
                    station_nbr = row[0]
                    for inner_row in csv_reader:
                        inner_date = inner_row[1]
                        inner_station_nbr = inner_row[4]
                        if date == inner_date and station_nbr == inner_station_nbr:
                            new_row = row+inner_row[2:]
                            csv_writer.writerow(new_row)

# This function combines data from 'train_filtered3.csv' and 'weather_with_weather_codes2.csv'
# based on matching 'date' and 'station_nbr', and saves the result as 'train_filtered4.csv'.
# Input : train_filtered3.csv & weather_with_weather_codes2.csv
# Output : merged_data.csv
def combine():
    data = pd.read_csv('./Data_Processing/train_filtered3.csv')
    weather = pd.read_csv('./Data_Processing/weather_with_weather_codes2.csv')
    # print(data.info())
    merged_df = pd.merge(data, weather, on=['date', 'station_nbr'])
    # print(merged_df.head(5))

    file_name = './Data_Processing/merged_data.csv'
    merged_df.to_csv(file_name)


# This code creates a 'label' column by combining 'store_nbr', 'item_nbr', and 'date',
# drops the original columns, and saves the modified dataset as 'train_data.csv'.
# Input : merged_data.csv
# Output : train_data
def combine_train():
    test = pd.read_csv("./Data_Processing/merged_data.csv", index_col=False)
    test['label'] = test.apply(lambda x: str(x['store_nbr']) + '_' + str(x['item_nbr']) + '_' + str(x['date']), axis=1)
    test = test.drop(['store_nbr', 'item_nbr', 'date'], axis=1)
    test.to_csv("./Model_Training/train_data.csv", index=False)


# Filter weather data
def filter_weather():
    # Filtering out irrelevant data
    df = pd.read_csv('./Data_Processing/weather_with_weekday_weekend.csv')

    # List of columns to drop
    columns_to_keep = [
        'station_nbr', 'date', 'tmax', 'tmin', 'dayNum', 'weekday', 'weekend'
    ]

    # Drop the specified columns
    df_filtered = df[columns_to_keep]

    # Save the filtered DataFrame to a new CSV file
    df_filtered.to_csv('./Data_Processing/weather_training.csv', index=False)


# This code enriches the 'sampleSubmission.csv' dataset with weather data from 'weather_training.csv',
# using 'key.csv' to map stores to stations, and saves the result as 'testing_data.csv'.
# Input : key.csv & sampleSubmission.csv
# Output : testing_data.csv
def combine_test():
    key_df = pd.read_csv("./Unfiltered_Data/key.csv")
    # Store : Station
    store_station_dict = dict(zip(key_df['store_nbr'], key_df['station_nbr']))

    # Y_Labels
    sample_df = pd.read_csv("./Unfiltered_Data/sampleSubmission.csv", index_col=False)
    sample_df = sample_df.drop(['units'], axis=1)

    weather_df = pd.read_csv("./Data_Processing/weather_training.csv", index_col=False)
    data_test = pd.DataFrame()

    last_station = None
    last_date = None
    last_row = None
    counter = 0
    for index1, row1 in sample_df.iterrows():
        # print(counter)
        counter += 1
        t = row1['id']
        data = row1['id'].split("_")
        store_id = int(data[0])
        station_id = store_station_dict[store_id]
        date_id = data[2]

        if None in (last_station, last_date):
            row_index = weather_df.index[(weather_df['date'] == date_id) & (weather_df['station_nbr'] == station_id)].tolist()
            new_row = weather_df.loc[row_index, :]
            new_row['id'] = t
            data_test = new_row

            last_station = station_id
            last_date = date_id
            last_row = new_row

        else:
            if (last_station == station_id) & (last_date == date_id):
                new_row = last_row.copy()
                new_row['id'] = t
                data_test = pd.concat([data_test, new_row])
            else:
                row_index = weather_df.index[(weather_df['date'] == date_id) & (weather_df['station_nbr'] == station_id)].tolist()
                new_row = weather_df.loc[row_index,:]
                new_row['id'] = t
                data_test = pd.concat([data_test, new_row])

                last_station = station_id
                last_date = date_id


    # print()
    data_test.to_csv("./Model_Training/testing_data.csv", encoding='utf-8', index=False)


    # for index1, row1 in sample_df.iterrows():
    #     data = row1['id'].split("_")
    #     store_id = int(data[0])
    #     station_id = store_station_dict[store_id]
    #     date_id = data[2]
    #     for index2, row2 in weather_df.iterrows():
    #         station_id2 = row2["station_nbr"]
    #         date_id2 = row2[1]
    #         if str(station_id) == str(station_id2) and str(date_id) == str(date_id2):
    #             temp = [row1["id"],row2["tmax"],row2["tmin"],row2["dayNum"],row2["weekday"],row2["weekend"]]
    #             data_test.append(temp)
    #
    # np_data_test = np.array(data_test)
    # index_list = ["id","tmax", "tmin", "dayNum", "weekday", "weekend"]
    # df = pandas.DataFrame(np_data_test, index=index_list)

    # df.to_csv("final_test.csv", encoding='utf-8', index=False)

    # sampleSubmission_df = pd.read_csv("sampleSubmission.csv", index_col=False)
    # train_labels = sampleSubmission_df['id'].values
    # test_labels = []
    # for value in train_labels:
    #     data = value.split("_")
    #     store_nbr = data[0]
    #     date = data[2]
    #     temp = [store_nbr, date]
    #     test_labels.append(temp)

def main():
    # filter_train()
    # reorganize_train()
    # store_station()
    # day_of_week()
    # weekday_weekend()
    # weather_codes()
    # filter_train()
    # filter_weather_codes()
    # filter_weather()
    # combine_train_with_weather()
    # combine()
    # combine_train()
    print("Starting")
    combine_test()
    print("Ending")

if __name__ == "__main__":
    main()

# data = pd.read_csv('./train.csv')
# weather = pd.read_csv('./weather.csv')


