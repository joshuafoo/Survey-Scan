## © Copyright 2020 by Joshua and Yan En. All Rights Reserved.
## SURVEY SCAN VER 3.2

### Try Importing All Required Packages ###
try:
    #python pre-installed libraries
    import math
    import time
    import sys
    import os
    import operator
    import statistics
    import csv
    from functools import partial
    from threading import Thread
    from os import listdir
    from os.path import isfile, join
    import traceback

    #External libraries
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats
    from textblob import TextBlob
    import kivy

    #have to set config before other kivy pakages are imported
    from kivy.config import Config
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'default_font','AvenirNext-Regular')
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

    #kivy pakages

    from kivy.app import App
    from kivy.core.window import Window
    from kivy.core.text import FontContextManager as FCM
    from kivy.graphics import Color
    from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
    from kivy.properties import StringProperty
    from kivy.clock import Clock
    from kivy.lang import Builder
    from kivy.uix.button import Button
    from kivy.uix.textinput import TextInput
    from kivy.uix.label import Label
    from kivy.uix.popup import Popup
    from kivy.uix.recycleview import RecycleView
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.stacklayout import StackLayout
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.togglebutton import ToggleButton
    from kivy.uix.spinner import Spinner
    from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition

except ImportError:
    raise ImportError("Some Packages were not installed properly. Please install them and try again")

# Declare Global Variables, Classes, Data Handling
questioninfo = []
toggle_states = [] # Stores Toggle States of Toggle Buttons
directstate = []
notallowed = ["Index", "Entry Id", "Date Created", "Created By", "Date Updated", "Updated By", "IP Address", "Last Page Accessed","Completion Status,", "Index Number", "Name", "Gender", "Age (This Year)", "School", "Completion Status"]
file_path = ""
displayarr = [] # For Data Processing from Second Screen to Third Screen
selectedButton = "NA"
filename = ''
surveyfile = None

class Question:
    def __init__(self, name, data, type, minval, maxval, mean, median, mode, standarddev, iqr, uq, lq, totalresponses, anomdata, freqdata, sentidata, isValidRow):
        self.name = name
        self.data = data
        self.type = type
        self.minval = minval
        self.maxval = maxval
        self.mean = mean
        self.median = median
        self.mode = mode
        self.standarddev = standarddev
        self.iqr = iqr
        self.uq = uq
        self.lq = lq
        self.totalresponses = totalresponses
        self.anomdata = anomdata
        self.freqdata = freqdata
        self.sentidata = sentidata
        self.isValidRow = isValidRow

### User Interface ###
def find_anomalies(data):
    anomalies = []
    # Set upper and lower limit to 3 standard deviation
    data_std = np.std(data)
    data_mean = np.mean(data)
    anomaly_cut_off = data_std * 3

    lower_limit  = data_mean - anomaly_cut_off
    upper_limit = data_mean + anomaly_cut_off
    # Generate outliers
    for index, outlier in enumerate(data):
        if outlier > upper_limit or outlier < lower_limit:
            anomalies.append((outlier, index))
    return anomalies

class NoTitleDialog(Popup): # ALERT CLASS
    # e.g to show an alert with message "WHY" and a ok button, call
    #dialog = NoTitleDialog()
    #dialog.label_text = "WHY"
    #dialog.open()

    def __init__(self, **kwargs):
        super(NoTitleDialog, self).__init__(**kwargs)
        self.label_text = "Error"

class First(Screen):
    def on_enter(self):
        Window.size = (600, 200)

    def __init__(self, **kwargs):
        super(First, self).__init__(**kwargs)
        ## Creating UI Elements ##
        # Creating Float Layout
        Fl = FloatLayout()

        # Creating reload image button
        reload_btn = Button(
            text="",
            background_normal="reload_sprite.png",
            background_down="reload_sprite_2.png",
            pos_hint ={'center_y': .65, 'center_x': .67},size_hint = (.06, .18))

        # Creating "Enter file name" label
        l = Label(
            text='Select file from directory',
            font_size='15sp',pos_hint ={'center_y': .85, 'center_x': .5},
            size_hint = (.3, .25))

        # Creating Error Label, Set to Hidden
        self.err = Label(
            text='Error: Invalid File Selected',
            font_size='13sp',pos_hint ={'center_y': .2, 'center_x': .5},
            size_hint = (.3, .25),
            color=[1, .8, .8, 0])

#################### Generate Spinner Values################
        cwd = os.getcwd() # Get Current Working Directory (CWD)
        self.files = []
        for f in listdir(cwd):
            if isfile(join(cwd, f)):

                # Check if File Extension is ".csv" (Is it a csv file?)
                if(f.replace(" ", "")[-4:] == ".csv"):
                    self.files.append(f)

        # If .csv files are not found in directory, display error
        if(len(self.files)== 0):
            self.files = ["No .csv files found in directory"]


        # Truncate all values that exceed spinner, display new values
        self.modfiles = self.files[::] # Create new instance of files called "modfiles"

        for i, item in enumerate(self.modfiles):
            if(len(item) > 40):
                self.modfiles[i] = item[:40] + "..."
        print(self.files)

        #Create spinner
        self.spinner = Spinner(
            text="Select File",
            values=set(self.modfiles),
            size_hint=(.6, .2),
            pos_hint ={"center_y": .65, "center_x": .4})

        # Create Import Button
        btn = Button(text ="Import",
                     size_hint =(.2, .2),
                     background_color =(.3, .6, .7, 1),
                     pos_hint ={"center_y": .65, "center_x": .8})

## ACTIONS/TRIGGERS AND BINDINGS ##
        # Function: When Button Pressed
        def on_button(instance):
            Window.left = 250
            Window.top = 40
            global questioninfo
            print(self.files,self.modfiles)
            try:
                ## NOTE: self.spinner.text will give you the value that is selected in the spinner
                try:
                    file = self.files[self.modfiles.index(self.spinner.text)]
                except ValueError:
                    file = "Select File"
                print('File Selected (via Spinner on First Screen): ', file)
                # Useless Data Validation (If Value Filepath)
                if not(os.path.isfile(file)):
                    raise Error("Please Select a valid .csv file")

                # Data Validation (If Default "Select" value)
                if(file != "Select File" or file != "No .csv files found in directory"):
                    questioninfo = []
                    # FILE DATA HANDLING
                    global surveyfile
                    surveyfile = pd.read_csv(file)
                    global filename
                    filename = file
                    questions = list(surveyfile.columns.values)
                    global notallowed
                    for question in questions:
                        isInvalid = False
                        for restricted in notallowed: # CANNOT USE QUESTION.LOWER() IN NOT ALLOWED
                            if question.lower() == restricted.lower():
                                isInvalid = True
                                break
                        if not isInvalid:
                            questioninfo.append(Question(question, list(surveyfile[question]),'', '', '', '', '', '', '', '', '', '', '', '', '', '', False))
                    # REMOVING UNWANTED VALUES
                    for validquestiondata in questioninfo:
                        rowisvalid = False
                        for response in validquestiondata.data:
                            try:
                                print(response)
                                if str(response).strip().lower() == "nil" or str(response).strip().lower() == "na" or str(response).strip() == ""  or response == [] or (type(response) == float and math.isnan(response)) : #(isinstance(response, float) and math.isnan(float(response))
                                    print("BAD")
                                    validquestiondata.data.remove(response)
                                else:
                                    print("{} is normal valid".format(response))
                                    rowisvalid = True
                            except:
                                print("{} is valid".format(response))
                                rowisvalid = True
                                pass
                        if rowisvalid:
                            print(validquestiondata.name)
                            validquestiondata.isValidRow = True

                    if len(questioninfo) == 0:
                        raise Error("Please Select a valid .csv file")
                    else:
                        selectedButton = questioninfo[0]
                    ## ANALYSING OF DATA ##
                    # TOGGLE STATES MODIFICATION
                    global toggle_states
                    global directstate
                    directstate = []
                    toggle_states = []
                    agreearray = ['agree', 'strongly agree', 'disagree', 'strongly disagree', 'neutral']
                    for item in questioninfo:
                        if item.isValidRow:
                            dataArray = {}
                            for value in item.data: # NOTE: Already Sorted, Remove Whitespace if There
                                # NOTE: FOR DEBUG PURPOSES
                                # print(str(value).lower().strip())
                                # print(dataArray.keys())
                                if str(value).lower().strip() in dataArray.keys():
                                    dataArray[str(value).lower().strip()] += 1
                                else:
                                    dataArray[str(value).lower()] = 1
                            # DATA ANALYSIS (Multiple-Choice, Strongly Agree/Disagree, Scale Rating (1 to 10), Open Ended)
                            print(item.name)
                            hasAppended = False
                            ## CHECK FOR STRONGLY AGREE/DISAGREE
                            if len(dataArray) <= 5 and any(elem in agreearray for elem in dataArray.keys()):
                                hasAppended = True
                                print("SA/SD")
                                toggle_states.append(['normal','down','normal','normal']) # Strongly Agree/Disagree Question
                                directstate.append("Strongly Agree/Disagree")
                            ## CHECK FOR SCALE RATING
                            elif len(dataArray) <= 10:
                                isValidQuestion = True
                                for value in dataArray:
                                    try:
                                        x = 0
                                        for i in range(10):
                                            x += 1
                                            if not(int(value) > 0 and int(value) <= 10):
                                                isValidQuestion = False
                                                raise TypeError()
                                    except:
                                        if x < 9:
                                            break # Data is not valid type
                                        else:
                                            pass
                                if isValidQuestion:
                                    hasAppended = True
                                    print("SCALER")
                                    toggle_states.append(['normal','normal','down','normal']) # Scale Rating Question
                                    directstate.append("Scale Rating (1 to 10)")
                            ## CHECK FOR MULTIPLE CHOICE
                            if hasAppended == False:
                                if len(dataArray) <= 4:
                                    print("MCQ")
                                    toggle_states.append(['down','normal','normal','normal']) # Multiple Choice Question
                                    directstate.append("Multiple-Choice")
                                ## CHECK FOR OPEN ENDED
                                else:
                                    print("OE")
                                    toggle_states.append(['normal','normal','normal','down']) # Open Ended Question
                                    directstate.append("Open Ended")


                    # CHANGE SCREEN
                    self.manager.current =  "second"
                    self.err.color = [1, .8, .8, 0]
                    #Window.size = (1000, 800)#set window size


            # Error Handling
            except Error as e:
                self.err.text = str(e)
                self.err.color = [1, .8, .8, 1] # Make error text visible
                Window.left = 420
                Window.top = 250
            except Exception:
                print("Something went wrong,this is the error")
                traceback.print_exc()

        btn.bind(on_press=on_button)

        def reload_spinner(instance):
            self.spinner.text="Select File"
            cwd = os.getcwd() # Get Current Working Directory (CWD)
            self.files = []
            for f in listdir(cwd):
                if isfile(join(cwd, f)):
                    # Check if File Extension is ".csv" (Is it a csv file?)
                    if(f.replace(" ", "")[-4:] == ".csv"):
                        self.files.append(f)

            # If .csv files are not found in directory, display error
            if(len(self.files)== 0):
                self.files = ["No .csv files found in directory"]

            # Truncate all values that exceed spinner, display new values
            self.modfiles = self.files[::] # Create new instance of files called "modfiles"

            for i, item in enumerate(self.modfiles):
                if(len(item) > 40):
                    self.modfiles[i] = item[:40] + "..."
            print(self.modfiles)

            self.spinner.values = set(self.modfiles)

        reload_btn.bind(on_press=reload_spinner)


        ## Add widgets to screen ##
        Fl.add_widget(btn)
        Fl.add_widget(self.spinner)
        Fl.add_widget(l)
        Fl.add_widget(reload_btn)
        Fl.add_widget(self.err)
        self.add_widget(Fl)

class Item(GridLayout):

    def adjust_data(self, rvRow,button_index,state,refff):
        # NOTE: Function called when any toggle button is toggled
        toggle_states[int(rvRow)] = ["normal" for i in range(4)] # Set all toggle buttons to normal
        toggle_states[int(rvRow)][int(button_index)] = str(state) # Set toggle button toggled to down
        options = ["Multiple-Choice", "Strongly Agree/Disagree", "Scale Rating (1 to 10)", "Open Ended"]
        directstate[int(rvRow)] = options[int(button_index)]
        root = App.get_running_app().root # Scenemanger
        root.get_screen('second').ids.rv.data = root.get_screen('second').ids.rv.getData() # Reload data
        # Update toggle button states
        refff.b1state = refff.ids.b1.state
        refff.b2state = refff.ids.b2.state
        refff.b3state = refff.ids.b3.state
        refff.b4state = refff.ids.b4.state



class StockList(RecycleView):
    def getData(self):
        data = []
        global questioninfo
        global toggle_states
        print(len(questioninfo))
        print(len(toggle_states))
        print(toggle_states)
        i = 0
        for item in questioninfo:
            if item.isValidRow:
                print(i, item.name)
                print(item.isValidRow)
                add = {}
                #Truncate logic
                if(len(str(item.name)) > 240):
                    add['name'] = str(item.name.replace("	"," "))[:240] + "..."
                else:
                    add['name'] = str(item.name.replace("	"," "))
                item.name = add['name']
                add['b1state'] = toggle_states[i][0]
                add['b2state'] = toggle_states[i][1]
                add['b3state'] = toggle_states[i][2]
                add['b4state'] = toggle_states[i][3]
                add['row_count'] = str(i)
                data.append(add)
                i+=1
        return data



class Second(Screen):
    def goback(self): # When back button is clicked
        Window.left = 420
        Window.top = 250
        self.manager.current =  "first" # Transition to third scene

    def export(self): # When export data button is clicked
        global directstate
        global questioninfo
        ZDEAlert, OEAlert, OEMAlert = False, False, False
        ## DATA HANDLING ##
        global selectedButton
        try:
            selectedButton = questioninfo[0]
        except:
            pass
        index = 0
        for question in questioninfo:
            if question.isValidRow:
                question.type = directstate[index]
                frequency = {}
                maxval = minval = mean = median = mode = standarddev = iqr = uq = lq = totalresponses = 0
                global displayarr
                if question.type == "Open Ended":
                    question.totalresponses = len(question.data)
                    if question.totalresponses > 10 and OEMAlert == False:
                        OEMAlert = True
                        dialog = NoTitleDialog()
                        dialog.label_text = "PLEASE NOTE:\nSome Data for Open Ended Questions may be ommitted due to the large size of the data"
                        dialog.open()
                    polarityarray = []
                    for response in question.data:
                        temp = []
                        ## Advanced Data Processing
                        # Statistics Calculation (Minimum Sentiment, Maximum Sentiment, Mean/Average Sentiment, Mode Sentiment(s), Median Sentiment(s), Sentiments' Standard Deviation, Sentiments' Interquartile Range, Upper Quartile of Sentiments, Lower Quartile of Sentiments, Total No. Responses)
                        text = TextBlob(str(response))
                        # text = text.correct() ## EXPERIMENTAL: AUTOCORRECT FEATURE
                        for item in text.tags:
                            if item[1] == 'JJ' or item[1] == 'JJR' or item[1] == 'JJS':
                                if str(item[0]) in frequency.keys():
                                    frequency[str(item[0])] += 1
                                else:
                                    frequency[str(item[0])] = 1

                        # Conduct Sentiment Analysis on Data
                        for sentence in text.sentences:
                            temp.append(sentence.sentiment.polarity)
                        polarityarray.append(temp)

                    # Total No. Responses
                    totalresponses = len(polarityarray)

                    ## NUMPY ARRAY FOR STATISTIC VALUES
                    nparray = np.array([value for subarray in polarityarray for value in subarray])

                    # Mean/Average InitConfigs
                    totalvalue = 0
                    for sentiset in polarityarray:
                        for subsentiment in sentiset:
                            totalvalue += subsentiment
                    try:
                        # Mode
                        question.mode = stats.mode(nparray)[0]

                        # Mean
                        question.mean = totalvalue/totalresponses

                        # Median
                        question.median = np.median(nparray)

                        # Upper Quartile
                        question.uq = np.median(nparray[10:])

                        # Lower Quartile / 1st Quartile
                        question.lq = np.median(nparray[:10])

                        # Interquartile range
                        question.iqr = abs(uq-lq)

                        # Standard Deviation
                        question.standarddev = np.std(nparray)

                        # Minimum and Maximum
                        question.minval = min(nparray)
                        question.maxval = max(nparray)

                        # Anomalies
                        question.anomdata = find_anomalies(nparray)
                        print(question.anomdata)

                    except ZeroDivisionError:
                        ## RAISE ERROR
                        print("ER0")
                        print(question.name)
                        question.mean = question.mode = question.median = question.standarddev = question.uq = question.lq = question.iqr = question.minval = question.maxval = question.anomdata = "NA"
                        if ZDEAlert == False:
                            ZDEAlert = True
                            dialog = NoTitleDialog()
                            dialog.label_text = "ALERT:\nNo Responses were found for one/some question(s). Statistics will not be shown for that/those question(s). "
                            dialog.open()
                        pass

                    ## SAVE THE CALCULATED DATA
                    question.freqdata = frequency
                    question.sentidata = polarityarray

                else: # If NOT OPEN ENDED
                    ## Normal Data Processing
                    ## DATA HANDLING ##
                    ## Statistics Input (Minimum, Maximum Mean/Average, Mode, Median, Standard Deviation, Interquartile Range, Upper Quartile, Lower Quartile, Total No. Responses)
                    for response in question.data:
                        if str(response) in frequency.keys():
                            frequency[str(response)] += 1
                        else:
                            frequency[str(response)] = 1
                    try:
                        # Total No. Responses
                        question.totalresponses = len(question.data)
                        print(question.totalresponses)

                        ## NUMPY ARRAY FOR STATISTIC VALUES
                        nparray = np.array([value for value in question.data])

                        # Mode
                        question.mode = stats.mode(nparray)[0]

                        # Frequency Table
                        question.freqdata = frequency

                        if question.type == "Strongly Agree/Disagree" or question.type == "Multiple-Choice":
                            currcount = 1
                            freq2 = {}
                            for item in frequency:
                                freq2[currcount] = frequency[item]
                                currcount += 1

                            ## CALCULATE DATA FOR SPECIAL CASES
                            # Mean
                            nparray = np.array([int(freq2[x]) for x in freq2.keys()])
                            totalvalue = sum([int(freq2[x]*x) for x in freq2.keys()])

                            question.mean = list(frequency.keys())[int(round(totalvalue/question.totalresponses))]

                            # Median
                            question.median = list(frequency.keys())[int(round(np.median(nparray)))] ## FIX THIS: CURRENT RETURNS MEDIAN OF GIVEN ARRAY, NOT BASED ON WEIGHTED VALUES

                            # Upper Quartile
                            question.uq = list(frequency.keys())[int(round(np.median(sorted(nparray)[10:])))]

                            # Lower Quartile / 1st Quartile
                            question.lq = list(frequency.keys())[int(round(np.median(sorted(nparray)[:10])))]

                            # Interquartile range
                            question.iqr = list(frequency.keys())[int(round(abs(uq-lq)))]

                            # Standard Deviation
                            question.standarddev = list(frequency.keys())[int(np.std(nparray))]

                            # Minimum and Maximum
                            question.minval = list(frequency.keys())[int(round(min(nparray)))]
                            question.maxval = list(frequency.keys())[int(round(max(nparray)))]

                        else:
                            # Mean
                            totalvalue = sum([int(x) for x in question.data])
                            question.mean = totalvalue/question.totalresponses

                            # Median
                            question.median = np.median(nparray)

                            # Upper Quartile
                            question.uq = np.median(nparray[10:])

                            # Lower Quartile / 1st Quartile
                            question.lq = np.median(nparray[:10])

                            # Interquartile range
                            question.iqr = abs(uq-lq)

                            # Standard Deviation
                            question.standarddev = np.std(nparray)

                            # Minimum and Maximum
                            question.minval = min(nparray)
                            question.maxval = max(nparray)

                            # Anomalies
                            question.anomdata = find_anomalies(nparray)
                            print(question.anomdata)

                    except ZeroDivisionError:
                        ## RAISE ERROR
                        print("ZDE2")
                        print(question.name)
                        question.mean = question.median = question.standarddev = question.uq = question.lq = question.iqr = question.minval = question.maxval = "NA"
                        if ZDEAlert == False:
                            ZDEAlert = True
                            dialog = NoTitleDialog()
                            dialog.label_text = "ALERT:\nNo Responses were found for one/some question(s). Statistics will not be shown for that/those question(s). "
                            dialog.open()
                        pass

                    except ValueError: # ValueError or IndexError
                        ## RAISE NOTIF
                        #print(question.totalresponses, question.mode[0])
                        #print(question.name)
                        question.mean = question.median = question.uq = question.lq = question.iqr = question.standarddev = question.minval = question.maxval = "NA"
                        question.anomdata = "No Anomalies will be displayed for Multiple Choice and Strongly Agree/Disagree Questions"
                        if OEAlert == False:
                            OEAlert = True
                            dialog = NoTitleDialog()
                            dialog.label_text = "PLEASE NOTE:\nNo Mean, Median, Upper Quartile, Lower Quartile, Interquartile Range, Standard Deviation, Anomalies, Minval and Maxval will be shown for Multiple Choice and Strongly Agree/Disagree Questions."
                            dialog.open()
                        ## CONVERT ALL STRONGLY AGREE AND DISAGREE VALUES // MULTIPLE CHOICE VALUES TO SCALE DEGREE
                        pass

                    except IndexError:
                        ## RAISE NOTIF
                        #print(question.totalresponses, question.mode[0])
                        #print(question.name)
                        question.mean = question.median = question.uq = question.lq = question.iqr = question.standarddev = question.minval = question.maxval = question.anomdata ="NA"
                        if OEAlert == False:
                            OEAlert = True
                            dialog = NoTitleDialog()
                            dialog.label_text = "PLEASE NOTE:\nNo Mean, Median, Upper Quartile, Lower Quartile, Interquartile Range, Standard Deviation, Anomalies, Minval and Maxval will be shown for Multiple Choice and Strongly Agree/Disagree Questions."
                            dialog.open()
                        ## CONVERT ALL STRONGLY AGREE AND DISAGREE VALUES // MULTIPLE CHOICE VALUES TO SCALE DEGREE
                        pass
                    # except:
                    #     pass
                index += 1
        self.manager.current =  "third" # Transition to third scene

    def quit_app(self):
        MyApp.get_running_app().stop()

    def on_enter(self):
        Window.size = (950, 700) # Set size of window after transtion to this screen
        self.ids.rv.data = self.ids.rv.getData() # Reload data

    def proccess_csv(self,filepath):
        print(filepath)

class third(Screen):
    def search(self,arr,text,state_arr):
        result = []
        state_result = []
        text = text.lower()
        for i,item in enumerate(arr):
            if(text in item.lower()):
                result.append(item)
                state_result.append(state_arr[i])
        return [result,state_result]


    def search_bar_changed(self,text):
        global questioninfo
        global directstate
        arr = self.search([str(item.name) for item in questioninfo],text,directstate)
        root = App.get_running_app().root # Scenemanger
        data=[]
        for i, item in enumerate(arr[0]):
            add = {}
            add['name'] = str(item)
            add['row_count'] = str(i)
            add['question_type'] = arr[1][i]
            data.append(add)
        root.get_screen('third').ids.rv.data = data # set data

    def save(self):# Save button pressed
        dialog = NoTitleDialog()
        dialog.label_text = "Saving File and Exiting Application..."
        dialog.open()
        ## SAVE FILE AS CSV ##
        csv_columns = ['Index', 'Name', 'Type', 'Minimum Value', 'Maximum Value', 'Mean', 'Median', 'Mode', 'Standard Deviation', 'Interquartile Range', 'Upper Quartile', 'Lower Quartile', 'Total Responses', 'Anomalies']
        dict_data = []
        for index, question in enumerate(questioninfo):
            temp = {}
            # 16 Fields
            print(question.name)
            temp["Index"] = index+1
            temp["Name"] = question.name
            temp["Type"] = question.type
            temp["Minimum Value"] = question.minval
            temp["Maximum Value"] = question.maxval
            temp["Mean"] = question.mean
            temp["Median"] = question.median
            temp["Mode"] = question.mode
            temp["Standard Deviation"] = question.standarddev
            temp["Interquartile Range"] = question.iqr
            temp["Upper Quartile"] = question.uq
            temp["Lower Quartile"] = question.lq
            temp["Total Responses"] = question.totalresponses
            temp["Anomalies"] = question.anomdata
            dict_data.append(temp)

        print(dict_data)
        global filename
        csv_file = "evaluated-{}".format(filename)
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_data:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
        os.system("open {}".format(csv_file))
        MyApp.get_running_app().stop() # STOPS APPLICATION

    def on_enter(self):
        Window.size = (950, 700) # Set size of window after transtion to this screen
        self.ids.rv.data = self.ids.rv.getData() # Reload data

class MyLayout():pass

class MyPopup(Popup):pass

class Questionlist(RecycleView):
    def getData(self):
        data=[]
        global questioninfo
        global directstate

        for i, item in enumerate(questioninfo):
            add = {}
            if(len(str(item.name)) >180):

                add['name'] = str(item.name.replace("	"," "))[:150] + "..."
            else:
                add['name'] = str(item.name.replace("	"," "))
            add['row_count'] = str(i)
            add['question_type'] = directstate[i]
            data.append(add)
        return data

class Item2(FloatLayout):
    def __init__(self, **kwargs):
        super(Item2, self).__init__(**kwargs)
        # Define variables
        global selectedButton
        print(selectedButton.type)
        self.array = ["Statistics","Pie Chart","Bar Chart","Anomalies"]
        self.current_segement = globals()[self.array[0].replace(" ", "_")]()

    def fire_popup(self,name,question_type):
        ## Set Button Selected ##
        for item in questioninfo:
            if str(item.name) == str(name):
                global selectedButton
                selectedButton = item
                if selectedButton.type == "Open Ended":
                    self.array = ["Sentiment Data","Pie Chart","Bar Chart","Anomalies"]
                else:
                    self.array = ["Statistics","Pie Chart","Bar Chart","Anomalies"]

        ## Creates popup widget ##
        self.current_segement = globals()[self.array[0].replace(" ", "_")]()
        pops = MyPopup()

        if(len(name)>105):# Check if name is more than 2 lines
            pops.title = name[:105] + "..."# Truncate name
        else:
            pops.title = name

        pops.title_size = 40

        ## Create UI Elements ##
        # Creating Floatlayout
        Fl = FloatLayout()
        Bl = BoxLayout(size_hint_y= None,
                       size_hint_x= .95,
                       height= "30dp",
                       pos_hint = {'center_y': .95, 'center_x': .5})

        # Toggle button events
        def change_type(name,foo):
            # Unloads previous tab and load new tab
            plt.close() # Close mathplot figure
            Fl.remove_widget(self.current_segement)
            self.current_segement = globals()[name.replace(" ", "_")]()
            Fl.add_widget(self.current_segement)
            Fl.remove_widget(btn)
            Fl.add_widget(btn)

        # Setup toggle buttons
        toggle_arra = []
        for i in self.array:
            Tb = ToggleButton(text=i,
                              group = "joshua",
                              state = "normal",
                              allow_no_selection = False)

            Tb.bind(on_release = partial(change_type,i))
            toggle_arra.append(Tb)
            Bl.add_widget(Tb)

        toggle_arra[0].state = "down" # Set first toggle button to be default selected

        # "Dismiss" button
        btn = Button(text ='Dismiss',
                     size_hint =(.2, .1),
                     background_color =(.3, .6, .7, 1),
                     pos_hint ={'center_y': 0.05, 'center_x': .5},
                     on_press = lambda *args: pops.dismiss())


        ## Add Widgets to Popup ##
        Fl.add_widget(self.current_segement)
        Fl.add_widget(Bl)
        Fl.add_widget(btn)

        pops.add_widget(Fl)
        pops.open()

class Anomalies(StackLayout):
    def __init__(self, **kwargs):
        super(Anomalies, self).__init__(**kwargs)
        global questioninfo
        ## Set constraints of view ##
        self.orientation = "tb-lr" # FORMAT: Left Right Top Bottom
        self.size_hint = (0.9, 0.8)
        self.pos_hint ={'center_y': 0.5, 'center_x': 0.5}

## Create Scrollable Label


        long_text = ""
        print(selectedButton.anomdata)
        if(selectedButton.anomdata != "NA"):
            for num,i in enumerate(selectedButton.anomdata):
                name = "Joshua"
                index = str(i[1])
                response = str(i[0])
                long_text+='\n Response {} with name {} has response: "{}" '.format(index,name,response)
                long_text+="\n"
        else:
            long_text = "NA"
        if(long_text == ""):long_text = "NA"

        l = ScrollableLabel(text=long_text)

        # Add scrollable label to self
        self.add_widget(l)


class Pie_Chart(BoxLayout):
    def __init__(self, **kwargs):
        super(Pie_Chart, self).__init__(**kwargs)
        self.size_hint = (0.92, 0.9)
        self.pos_hint ={'center_y': 0.45, 'center_x': 0.5}

## Create Pie Chart ##

        plt.clf() # Clear All
        # plt.gca().axis("equal")
        # pie = plt.pie(total, startangle=0)
        plt.rcParams['font.size'] = 19.0 # Set Font Size of Words
        fig, ax = plt.subplots(figsize=(100, 5), subplot_kw=dict(aspect="equal"))
        default_arr = selectedButton.freqdata
        #remove @ entry if exists
        if("@" in default_arr):
            del default_arr["@"]

        #Limits data to max 5
        sorted_arr = sorted(default_arr, key=default_arr.get, reverse=True)
        frequencyarr = {}
        count = 0
        #others_count = 0
        for i in sorted_arr:
            if(count <=5):
                frequencyarr[i] = selectedButton.freqdata[i]
                count+=1

        data = [frequencyarr[x] for x in frequencyarr]
        keys = [str(x) for x in frequencyarr.keys()]

        global index
        index = 0

        def func(pct, allvals):
            global index
            absolute = data[index]  # int(math.ceil(pct/100.*np.sum(allvals)))
            index += 1
            return "{:.1f}%\n({} responses)".format(pct, absolute)

        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                          textprops=dict(color="w"))

        ax.legend(wedges, keys,
                  title="Responses",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=20, weight="bold")
        #plt.subplots_adjust(left=0.0, bottom=0.1, right=0.5)
        ax.set_title("Percentage of Responses")
        ax.autoscale(enable=True)
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))
class Bar_Chart(BoxLayout):
    def __init__(self, **kwargs):
        super(Bar_Chart, self).__init__(**kwargs)

## Set View Constraints ##
        self.size_hint = (0.8, 0.8)
        self.pos_hint ={'center_y': 0.503, 'center_x': 0.5}#left right top bottom

## Create Graph ##
        plt.clf() # Clear all
        plt.rcParams['font.size'] = 25.0 # Set Font Size of Words
        print(selectedButton.freqdata)
        default_arr = selectedButton.freqdata
        #remove @ entry if exists
        if("@" in default_arr):
            del default_arr["@"]

        #Limits data to max 5
        sorted_arr = sorted(default_arr, key=default_arr.get, reverse=True)
        frequencyarr = {}
        count = 0
        #others_count = 0
        for i in sorted_arr:
            if(count <=5):
                frequencyarr[i] = selectedButton.freqdata[i]
                count+=1
           #else:
                #others_count+=selectedButton.freqdata[i]
        #if(len(sorted_arr)>5):
            #frequencyarr["others"] = others_count

        objects = []
        performance = []
        for item in frequencyarr.keys():
            objects.append(item)
            performance.append(frequencyarr[item])
        objects = tuple(objects)
        y_pos = np.arange(len(objects))


        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Responses')
        plt.title('Amount of Responses')

## Add Graph to Self ##
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class Sentiment_Data(StackLayout):
    def __init__(self, **kwargs):
        super(Sentiment_Data, self).__init__(**kwargs)
        ## Set Constraints of view ##
        self.orientation = "tb-lr" # FORMAT: Left Right Top Bottom
        self.size_hint = (0.9, 0.8)
        self.pos_hint ={'center_y': 0.5, 'center_x': 0.5}

        ## Create Scrollable Label
        global selectedButton
        lmode = ''
        question = selectedButton
        for index, smode in enumerate(question.mode):
            try:
                lmode += str(int(smode))
            except:
                lmode += '\"' + str(smode) + '\"'
            if index != len(question.mode)-1:
                lmode += ', '

        long_text = """\
        Perception Mean/Average: {}
        Perception Mode(s): {}
        Perception Median: {}
        Perception Standard Deviation: {}
        Perception Interquartile Range: {}
        Perception Upper Quartile: {}
        Perception Lower Quartile: {}
        Perception Total No. Responses: {}
        Lowest Perception Response(s): {}
        Highest Perception Response(s): {}
        """.format(question.mean,lmode,question.median,question.standarddev,question.iqr,question.uq,question.lq, question.totalresponses, question.minval, question.maxval)

        l = ScrollableLabel(text=long_text)

        # Add scrollable label to self
        self.add_widget(l)

class Statistics(StackLayout):
    def __init__(self, **kwargs):
        super(Statistics, self).__init__(**kwargs)
        ## Set Constraints of view ##
        self.orientation = "tb-lr" # FORMAT: Left Right Top Bottom
        self.size_hint = (0.9, 0.8)
        self.pos_hint ={'center_y': 0.5, 'center_x': 0.5}

        ## Create Scrollable Label
        global selectedButton
        lmode = ''
        question = selectedButton
        for index, smode in enumerate(question.mode):
            try:
                lmode += str(int(smode))
            except:
                lmode += '\"' + str(smode) + '\"'
            if index != len(question.mode)-1:
                lmode += ', '

        long_text = """\
        Mean/Average: {}
        Mode(s): {}
        Median: {}
        Standard Deviation: {}
        Interquartile Range: {}
        Upper Quartile: {}
        Lower Quartile: {}
        Total No. Responses: {}
        Lowest Valued Response(s): {}
        Highest Valued Response(s): {}
        """.format(question.mean,lmode,question.median,question.standarddev,question.iqr,question.uq,question.lq, question.totalresponses, question.minval, question.maxval)

        l = ScrollableLabel(text=long_text)

        # Add scrollable label to self
        self.add_widget(l)

class RV(RecycleView):pass


# Scene manager class
class MyApp(App):
    Builder.load_file("main.kv") # Load .kv file
    sm = ScreenManager(transition=NoTransition()) # Declare scenemanger with no transtion set as default
    ## Add Screens to Scene Manager
    sm.add_widget(First(name ='first'))
    sm.add_widget(Second(name ='second'))
    sm.add_widget(third(name ='third'))
    sm.current = "first" # Set default screen (first)\

    def build(self):
        self.icon = 'Survey Scan Logo.png'
        self.title = 'Survey Scan'
        Window.left = 420
        Window.top = 250
        return self.sm

#error class
class Error(Exception):
    pass

# Run the Application
if __name__ == "__main__":
    MyApp().run()
