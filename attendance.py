### ATTENDANCE LIST FOR EACH DAY ###

import pandas as pd
import math

### RESET ###
attendance_file = pd.read_csv("attendance_ref.csv")

ls = []
for i in attendance_file["Index"]:
    ls.append(i)
    if math.isnan(i):
        ls.remove(i)

index_num = []
namelist = []
for index, rows in attendance_file.iterrows():
    if math.isnan(rows["Index"]):
        attendance_file = attendance_file.drop(index, axis=0)
    else:
        index_num.append(rows["Index"])
        namelist.append(rows["Name"])
data = {"Index": index_num, "Name": namelist}
df = pd.DataFrame(data, columns=["Index", "Name"])
df.to_csv("Attendance_Namelist.csv", columns=["Index", "Name"], index=False)
print("Reset \n")

### INPUT READ AND WRITE FILES ###

num = input("Which class: ")
filename_head = "swift-accelerator-2019-"
filename_attendance = "_entries.csv"
filename_exit = "-exit-survey_entries.csv"
attendance_survey = pd.read_csv(
    filename_head + num + filename_attendance, index_col="Index Number"
)
exit_survey = pd.read_csv(filename_head + num + filename_exit, index_col="Index Number")
Attendance_Namelist = pd.read_csv("Attendance_Namelist.csv")

### MANAGING ATTENDANCE ###

attendance = []
for i in Attendance_Namelist["Index"]:
    if i in list(attendance_survey.index):
        attendance.append(1)
    else:
        attendance.append("")

### CHECKING REPEATS FOR SURVEY ###
def get_repeats(survey):
    index_list = list(survey.index)
    repeats = []
    for index in index_list:
        if index_list.count(index) > 1:
            repeats.append(index)
    for repeat in repeats:
        index_list.remove(repeat)

    for i in repeats:
        if repeats.count(i) > 1:
            repeats.remove(i)

    repeats.sort()
    return (repeats, index_list)


(attendance_repeats, _) = get_repeats(attendance_survey)
(exit_repeats, index_list) = get_repeats(exit_survey)

### ADDING SURVEY RESULTS ###

able_to_follow = []
able_to_complete = []
comments = []

for i in Attendance_Namelist["Index"]:
    if i in index_list:
        able_to_follow.append(exit_survey.loc[i][9])
        able_to_complete.append(exit_survey.loc[i][11])
        comments.append(exit_survey.loc[i][12])
    else:
        able_to_follow.append(math.nan)
        able_to_complete.append(math.nan)
        comments.append(math.nan)

### WRITING TO FILE ###

attendance_entry = pd.DataFrame({num: attendance})
able_to_follow_entry = pd.DataFrame(
    {"I managed to follow what was taught": able_to_follow}
)
able_to_complete_entry = pd.DataFrame(
    {"I managed to complete the work that was given": able_to_complete}
)
comments_entry = pd.DataFrame({"Other Comments": comments})
Attendance_Namelist = pd.concat(
    [
        Attendance_Namelist,
        attendance_entry,
        able_to_follow_entry,
        able_to_complete_entry,
        comments_entry,
    ],
    axis=1,
)
Attendance_Namelist.to_csv("attendance.csv", index=False)

print(
    "Repeated entries for attendance, please check!\n",
    attendance_repeats,
    "\nRepeated entries for exit, please check!\n",
    exit_repeats,
)

import os

os.system("open attendance.csv")
