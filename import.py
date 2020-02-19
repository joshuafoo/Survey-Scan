### ATTENDANCE LIST FOR EACH DAY ###

import pandas as pd
import math

### RESET ###
surveyfile = pd.read_csv("attendance_ref.csv")
# print(list(surveyfile["Fairly meaningless points"]))
columnheaders = list(surveyfile.columns.values)
for columnname in columnheaders:

print(columnheaders)

ls = []
for i in surveyfile["Index"]:
    ls.append(i)
    if math.isnan(i):
        ls.remove(i)
columnheads = list(surveyfile.columns.values)
print(columnheads)
