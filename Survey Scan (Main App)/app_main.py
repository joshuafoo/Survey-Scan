#--------Import all required packages--------#
try:
    import kivy
    import pandas as pd
    import math
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    raise ImportError("Some Packages were not installed properly. Please install them and try again")

from functools import partial
from textblob import TextBlob
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import StringProperty
from kivy.uix.togglebutton import ToggleButton

# Class for Data Import
class Question:
    def __init__(self, name, data):
        self.name = name
        self.data = data

class First(Screen):
    def on_enter(self):Window.size = (500, 100)
    def __init__(self, **kwargs):
        super(First, self).__init__(**kwargs)

        #--------Create ui elements--------#

        # creating Floatlayout
        Fl = FloatLayout()

        #"Enter file name" label
        l = Label(
            text='Enter File Path:',
            font_size='15sp',pos_hint ={'center_y': .5, 'center_x': .2},
            size_hint = (.3, .25))

        #Error label
        self.err = Label(
            text='Error: Invalid file Path',
            font_size='13sp',pos_hint ={'center_y': .2, 'center_x': .5},
            size_hint = (.3, .25),
            color=[1, .8, .8, 0])

        #"Import button" button
        btn = Button(text ='Import',
                     size_hint =(.2, .25),
                     background_color =(.3, .6, .7, 1),
                     pos_hint ={'center_y': 0.5, 'center_x': .8})

        #Textfield with 'File Name' placeholder
        self.textinput = TextInput(text = "",
                                   hint_text='File Path',
                                   pos_hint ={'center_y': 0.489, 'center_x': .5},
                                   size_hint = (.3, .25),
                                   multiline=False)


        #--------Actions/triggers and bindings--------#

        #Function called when button pressed
        def on_button(instance):
            try:
                print('Import button clicked.Text = ', self.textinput.text)

                if(self.textinput.text != ""):
                    self.manager.current =  "second"
                    self.err.color = [1, .8, .8, 0]
                    #Window.size = (1000, 800)#set window size
                else:raise Error("Please enter a file path.")

            except Error as e:
                self.err.text = str(e)
                self.err.color = [1, .8, .8, 1]#make error text visible
            except:pass

        btn.bind(on_press=on_button)



        #--------Add widgets to screen--------#
        Fl.add_widget(btn)
        Fl.add_widget(self.textinput)
        Fl.add_widget(l)
        Fl.add_widget(self.err)
        self.add_widget(Fl)

toggle_states = [["normal" for i in range(4)] for i in range(10)]#stores toggle states of toggle button
default_down_states = [0,1,2,3,0,1,2,3,0,1]#default toggle states of toggle buttons

for i in range(len(default_down_states)):
    toggle_states[i][default_down_states[i]] = "down"#set toggle buttons to down

class Item(GridLayout):

    def adjust_data(self, rvRow,button_index,state,refff):
        #Function called when any toggle button is toggled#
        toggle_states[int(rvRow)] = ["normal" for i in range(4)]#set all toggle buttons to normal
        toggle_states[int(rvRow)][int(button_index)] = str(state)#set toggle button toggled to down

        root = App.get_running_app().root#scenemanger

        root.get_screen('second').ids.rv.data = root.get_screen('second').ids.rv.getData()#reload data
        #Update toggle button states
        refff.b1state = refff.ids.b1.state
        refff.b2state = refff.ids.b2.state
        refff.b3state = refff.ids.b3.state
        refff.b4state = refff.ids.b4.state

class StockList(RecycleView):
    def getData(self):
        #data source for recycleview
        number_of_elements = 10
        data = []
        for i in range(number_of_elements):
            add = {}
            add['name'] = 'item ' + str(i)
            add['b1state'] = toggle_states[i][0]
            add['b2state'] = toggle_states[i][1]
            add['b3state'] = toggle_states[i][2]
            add['b4state'] = toggle_states[i][3]
            add['row_count'] = str(i)
            data.append(add)
        return data

class Second(Screen):
    def export(self):#export data button is clicked
        print(toggle_states)
        self.manager.current =  "third"# transition to third scene

    def on_enter(self):
        Window.top -= 30#Change position of window so it does not touch the bottom of the screen
        Window.size = (1000, 700)#set size of window after transtion to this screen


class Third(Screen):
    def save(self):#save button pressed
        print("Save to file enter logic here")
    def on_enter(self):
        Window.size = (1000, 800)#set size of window after transtion to this screen

class MyLayout():pass

class MyPopup(Popup):pass

class Questionlist(RecycleView):
    number_of_elements = 10
    def getData(self):
        data=[]

        for i in range(self.number_of_elements):
            add = {}
            add['name'] = 'Question ' + str(i)
            add['row_count'] = str(i)
            data.append(add)

        return data
class Item2(FloatLayout):

    def __init__(self, **kwargs):
        super(Item2, self).__init__(**kwargs)
        #define variables
        self.array = ["Statistics","Pie Chart","Bar Chart","Anomalies"]
        self.current_segement = globals()[self.array[0].replace(" ", "_")]()

    def fire_popup(self,name):
        #--------Creates popup widget--------#
        self.current_segement = globals()[self.array[0].replace(" ", "_")]()
        pops = MyPopup()

        if(len(name)>105):#check if name is more than 2 lines
            pops.title = name[:105] + "..."#Truncate name
        else:
            pops.title = name

        pops.title_size = 40

        #--------Create ui elements--------#

        # creating Floatlayout
        Fl = FloatLayout()
        Bl = BoxLayout(size_hint_y= None,
                       size_hint_x= .95,
                       height= "30dp",
                       pos_hint = {'center_y': .95, 'center_x': .5})

        #Toggle button events
        def change_type(name,foo):
            #unloads previous tab and load new tab
            plt.close()#close mathplot figure
            Fl.remove_widget(self.current_segement)
            self.current_segement = globals()[name.replace(" ", "_")]()
            Fl.add_widget(self.current_segement)

            Fl.remove_widget(btn)
            Fl.add_widget(btn)
            print(name + " selected")#debug

        #setup toggle buttons

        toggle_arra = []
        for i in self.array:
            Tb = ToggleButton(text=i,
                              group = "1",
                              state = "normal",
                              allow_no_selection = False)

            Tb.bind(on_release = partial(change_type,i))
            toggle_arra.append(Tb)
            Bl.add_widget(Tb)

        toggle_arra[0].state = "down"#set first toggle button to be default selected


        #"Dismiss" button
        btn = Button(text ='Dismiss',
                     size_hint =(.2, .1),
                     background_color =(.3, .6, .7, 1),
                     pos_hint ={'center_y': 0.05, 'center_x': .5},
                     on_press = lambda *args: pops.dismiss())



        #--------Add widgets to popup--------#

        Fl.add_widget(self.current_segement)
        Fl.add_widget(Bl)
        Fl.add_widget(btn)

        pops.add_widget(Fl)
        pops.open()

class Anomalies(StackLayout):
    def __init__(self, **kwargs):
        super(Anomalies, self).__init__(**kwargs)
        #--------Set constraints of view--------#
        self.orientation = "tb-lr"#left right top bottom
        self.size_hint = (0.9, 0.8)
        self.pos_hint ={'center_y': 0.5, 'center_x': 0.5}

#--------create scrollable label--------#
        long_text = """There is a lot of data anomalies.There is something wong."""

        l = ScrollableLabel(text=long_text)

        #add scrollable label to self
        self.add_widget(l)


class Pie_Chart(BoxLayout):
    def __init__(self, **kwargs):
        super(Pie_Chart, self).__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        self.pos_hint ={'center_y': 0.45, 'center_x': 0.5}

#--------Create pie chart--------#

        plt.clf()#clear all
        plt.rcParams['font.size'] = 25.0#set font size of words
        fig, ax = plt.subplots(figsize=(8, 5), subplot_kw=dict(aspect="equal"))

        recipe = ["375 g flour",
                  "75 g sugar",
                  "250 g butter",
                  "300 g berries"]#data

        data = [float(x.split()[0]) for x in recipe]
        ingredients = [x.split()[-1] for x in recipe]


        def func(pct, allvals):
            absolute = int(pct/100.*np.sum(allvals))
            return "{:.1f}%\n({:d} g)".format(pct, absolute)


        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                          textprops=dict(color="w"))

        ax.legend(wedges, ingredients,
                  title="Ingredients",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=20, weight="bold")

        ax.set_title("Matplotlib bakery: A pie")
        ax.autoscale(enable=True)

#--------Add pie chart to self--------#

        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))

class Bar_Chart(BoxLayout):
    def __init__(self, **kwargs):
        super(Bar_Chart, self).__init__(**kwargs)
#--------Set constraints of view--------#
        self.size_hint = (0.8, 0.8)
        self.pos_hint ={'center_y': 0.503, 'center_x': 0.5}#left right top bottom

#--------Create graph--------#

        plt.clf()#clear all
        objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
        y_pos = np.arange(len(objects))
        performance = [10,8,6,4,2,1]

        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Usage')
        plt.title('Programming language usage')

#--------Add graph to self--------#

        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class Statistics(StackLayout):
    def __init__(self, **kwargs):
        super(Statistics, self).__init__(**kwargs)
#--------Set constraints of view--------#
        self.orientation = "tb-lr"#left right top bottom
        self.size_hint = (0.9, 0.8)
        self.pos_hint ={'center_y': 0.5, 'center_x': 0.5}

#--------create scrollable label--------#
        long_text = """Mean/Average: 100000
Mode: 10000
Median: 10000
Standard Deviation: 100000000000
Interquartile Range: 10000000000
Upper Quartile: 10000000000
Lower Quartile: 10000000000
Total Responses: 1000000000000000000000000000000000000000"""

        l = ScrollableLabel(text=long_text)

        #add scrollable label to self
        self.add_widget(l)



class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': "Button " + str(x+1),"row":str(x)} for x in range(30)]

# Scene manager class
class MyApp(App):

    # Builder.load_string(kv) #load kv string
    Builder.load_file("main.kv") #load kv file
    sm = ScreenManager(transition=NoTransition())#declare scenemanger with no transtion set as default
    #--------Add screens to Scene manager--------#
    sm.add_widget(First(name ='first'))
    sm.add_widget(Second(name ='second'))
    sm.add_widget(Third(name ='third'))
    sm.current = "first"#default first scene

    def build(self):
        self.title = 'Survey Scan'
        return self.sm

#error class
class Error(Exception):
    pass
# run the App
if __name__ == "__main__":
    MyApp().run()
