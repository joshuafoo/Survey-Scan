from functools import partial
import matplotlib.pyplot as plt
import numpy as np

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
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
from kivy.uix.togglebutton import ToggleButton
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

kv = """
<Questionlist>: # RecycleView
    viewclass: 'Item2'
    data: self.getData()
    RecycleBoxLayout:
        orientation: 'vertical'
        default_size: None, dp(100)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        scroll_type: ['bars']
        bar_width: 25
<Item2>:
    cols: 1
    name: 'init value'
    row_count: 'init value'
    RoundedButton:
        size_hint:(0.9, 0.9)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        markup: True
        text: "[size=30]       " + root.name
        text_size: self.size     
        halign: 'left'
        valign: 'center'
        on_release: root.fire_popup(root.name)

#:import Window kivy.core.window    
<MyPopup@Popup>:
    auto_dismiss: 
    pos_hint: {'center_x': .5, 'center_y': .5}
    size_hint: .8, .8
    title:"Question 1"
            

BoxLayout:
    orientation:"vertical"
    size_hint:(1, 0.97)

    BoxLayout:
        size_hint:(0.95, None)
        pos_hint: {'center_x': .5, 'center_y': .5}
        orientation:"horizontal"

        RoundedButton:
            size_hint:(0.8, None)
            pos_hint: {'y': .25}
            text:"Back"
            on_press:#root.manager.current =  "first"

        FloatLayout:#padding

        Label:
            markup: True
            pos_hint: {'y': .25}
            text:"[size=45][b]Question Overview[/b]"

        FloatLayout:

        RoundedButton:
            size_hint:(0.8, None)
            pos_hint: {'y': .25}
            text:"Save"
            on_press:#root.export()


    Questionlist:
        id:rv

<RoundedButton@Button>:
    background_color: 0,0,0,0  # the last zero is the critical on, make invisible
    canvas.before:
        Color:
            rgba: (.4,.4,.4,1) if self.state=='normal' else (0,.7,.7,1)  # visual feedback of press
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [50,]
"""


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
            Fl.remove_widget(self.current_segement)
            self.current_segement = globals()[name.replace(" ", "_")]()
            Fl.add_widget(self.current_segement)
            Fl.remove_widget(btn)
            Fl.add_widget(btn)
            print(name + " selected")

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
        self.size_hint = (0.9, 0.9)
        self.pos_hint ={'center_y': 0.45, 'center_x': 0.5}#left right top bottom

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

class Statistics(StackLayout):
    def __init__(self, **kwargs):
        super(Statistics, self).__init__(**kwargs)
        self.orientation = "tb-lr"
        self.size_hint = (0.9, 0.9)
        self.pos_hint ={'center_y': 0.5, 'center_x': 0.5}#left right top bottom
        for i in range(7):
            
            l = Label(
                text='Stats stuff ' + str(i),
                font_size='15sp',
                size_hint = (None,None))
            
            self.add_widget(l)
        
    

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': "Button " + str(x+1),"row":str(x)} for x in range(30)]


class TestApp(App):
  def build(self):
    return Builder.load_string(kv)


if __name__ == '__main__':
  TestApp().run()

