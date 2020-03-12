### ATTENDANCE LIST FOR EACH DAY ###

import pandas as pd
import math

## QUESTION CLASS ##
class Question:
    def __init__(self, name, data):
        self.name = name
        self.data = data

### RESET ###
filepath = "attendance_ref.csv"
surveyfile = pd.read_csv(filepath)
questioninfo = []

# print(list(surveyfile["Fairly meaningless points"]))
columnheaders = list(surveyfile.columns.values)
for columnname in columnheaders:
    questioninfo.append(Question(columnname, list(surveyfile[columnname])))

# print(list(surveyfile.index)) # The index (row labels) of the DataFrame.
ls = []
for i in surveyfile["Index"]:
    ls.append(i)
    if math.isnan(i):
        ls.remove(i)
columnheads = list(surveyfile.columns.values)
print(columnheads)

### CHECKING REPEATS FOR SURVEY ###
# def get_repeats(survey):
#     index_list = list(survey.index)
#     repeats = []
#     for index in index_list:
#         if index_list.count(index) > 1:
#             repeats.append(index)
#     for repeat in repeats:
#         index_list.remove(repeat)
#
#     for i in repeats:
#         if repeats.count(i) > 1:
#             repeats.remove(i)
#
#     repeats.sort()
#     return (repeats, index_list)
#
#
# (attendance_repeats, _) = get_repeats(attendance_survey)
# (exit_repeats, index_list) = get_repeats(exit_survey)
