import csv
import re
import sys
import os
import pandas as pd
from typing import Any

FILTERING = "filtering"
SORTING = "sorting"

if len(sys.argv) == 1:
    sys.stdout.write("Usage: %s <nginx.log> <accesslog.csv>\n" % sys.argv[0])
    sys.exit(0)

path = os.path.abspath("nginx.log")
csv_file_name = sys.argv[1]

pattern = re.compile(
    r'(?P<ip>\S+) (?P<http_auto>.) (?P<http_auto2>.) \[(?P<time>\S+ \+[0-9]{4})] \"(?P<request>.*)\" (?P<status>\S+) (?P<size>[0-9]+) \"(?P<referer>.*)\" \"(?P<user_agent>.*)\" (?P<somenumber>[0-9]+) (?P<somenumber2>\S+) (?P<ipadress_port>\S+) \[] (?P<host2>\S+) (?P<status2>[0-9]+) (?P<somenumber3>\S+) (?P<status3>[0-9]+) (?P<sometext>\S+)')

file = open(path)

with open(csv_file_name, 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['ip', 'http_auto', 'http_auto2', 'time', 'request', 'response_status', 'bytes_from_server', 'referer', 'user_agent', 'bytes_from_server_2',
                     'response_time', 'monitoring_system', 'ipadress_port', 'bytes_from_server_3', 'response_time_2', 'response_status_2', 'key'])

    for line in file:
        m = pattern.match(line)
        result = m.groups()
        csv_out.writerow(result)

# Reading the file

data_frame = pd.read_csv(csv_file_name)

with open(csv_file_name) as f:
    first_line = f.readline()
header = [first_line]

# User choose what he want to do with the log file

method = input(
    f"Please write down what do you want to do with log file: {FILTERING}, {SORTING} or nothing(just press Enter)?\n")

if method == FILTERING:
    # Storing input values from user
    filtering_array = []

    column_filtering = input(
        "Please write columns you want to filter, for example ip,response_status.\nHere are the available headers: " + ",".join(header))

    for a in column_filtering.split(","):
        filtering_array.append(a)

    data_filtered = data_frame.filter(items=filtering_array)

    value_filtering_answer = input(
        "Do you want to find exactly value in the filtered logs?\nY/y or N/n : ")
    if value_filtering_answer.lower() == "y":
        value_filter = input(
            "Please write what value you want to find in filtered columns: ")
        value_filter_data = data_filtered.filter(like=value_filter, axis=0)
        question_filtering_and_finding = input(
            "Do you want to sort it?\nY/y or N/n : ")
        if question_filtering_and_finding.lower() == "y":
            value_filter_data.sort_values(
                by=filtering_array, axis=0, ascending=True, inplace=True, na_position='first')
            value_filter_data.to_csv(
                column_filtering + value_filter + '_filtered_and_sorted_and_finded.csv', index=False)
            print("Your log file is filtered by exact value and sorted successfully!")

        elif question_filtering_and_finding.lower() == "n":
            value_filter_data.to_csv(
                column_filtering + '_just_filtered_and_finded.csv', index=False)
            print("Your log file is filtered and finded the exact value successfully!")

    elif value_filtering_answer.lower() == "n":
        question_filtering = input(
            "Do you want to sort it?\nY/y or N/n : ")
        if question_filtering.lower() == "y":
            data_filtered.sort_values(
                by=filtering_array, axis=0, ascending=True, inplace=True, na_position='first')
            data_filtered.to_csv(
                column_filtering + '_just_filtered_and_sorted.csv', index=False)
            print("Your log file is filtered and sorted successfully!")

        elif question_filtering.lower() == "n":
            print("Your log file was filtered successfully!")
            data_filtered.to_csv(
                column_filtering + '_just_filtered.csv', index=False)

# Sorting method
elif method == SORTING:

    # Sorting file by the input value
    value_sort = input(
        "Please input columns separated by comma which you want sort it by, for example status,ip : " + ",".join(header))

    sorting_array = []
    for f in value_sort.split(","):
        sorting_array.append(f)

    data_frame.sort_values(by=sorting_array, axis=0, ascending=True,
                           inplace=True, na_position='first')

    # Saving the new file
    data_frame.to_csv(value_sort + '_sorted.csv', index=False)
    print("Your data after sorting was saved in new csv file successfully!")

    # If user press just Enter
elif method == "" or "nothing":
    data_frame.to_csv('accesslog.csv', index=False)
    print("Your log file is ready to read in csv format!")
