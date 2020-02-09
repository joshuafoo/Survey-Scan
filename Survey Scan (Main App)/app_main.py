#--------Import all required packages--------#
try:
    import kivy
except ImportError:
    raise ImportError("This script requires Kivy to be installed.")

from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition
from kivy.config import Config
Config.set('graphics', 'resizable', False)
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

class First(Screen):
    def on_enter(self):Window.size = (500, 100)
    def __init__(self, **kwargs):
        super(First, self).__init__(**kwargs)
        
        #--------Create ui elements--------#

        # creating Floatlayout 
        Fl = FloatLayout()
        
        #"Enter file name" label
        l = Label(
            text='Enter File Name :',
            font_size='15sp',pos_hint ={'center_y': .5, 'center_x': .2},
            size_hint = (.3, .25))

        #Error label
        self.err = Label(
            text='Error:Invalid file name',
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
                                   hint_text='File Name',
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
                else:raise Error("Please enter a file name.")
                    
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
        
kv = """
<StockList>: # RecycleView
    viewclass: 'Item'
    data: self.getData()
    RecycleBoxLayout:
        orientation: 'vertical'
        default_size: None, dp(150)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        scroll_type: ['bars']
        bar_width: 25
<Item>:
    cols: 1
    name: 'init value'
    row_count: 'init value'
    b1state: 'normal'
    b2state: 'normal'
    b3state: 'normal'
    b4state: 'normal'
    
    Label:
        markup: True
        text: "[size=30]" + root.name
        
    BoxLayout:
        size_hint_y: None
        size_hint_x: .8
        height: "40dp"
        
        FloatLayout:
            size_hint: 0.1, 0.1
            
        ToggleButton:
            text:"Multiple-Choice"
            id: b1
            group: root.row_count
            state: root.b1state
            on_release:root.adjust_data(root.row_count,0,self.state,root)
            allow_no_selection:False
            
        ToggleButton:
            text:"Strongly Agree/Disagree"
            id: b2
            group: root.row_count
            state:root.b2state
            on_release:root.adjust_data(root.row_count,1,self.state,root)
            allow_no_selection:False
            
        ToggleButton:
            text:"Scale Rating (1 to 10)"
            id: b3
            group: root.row_count
            state:root.b3state
            on_release:root.adjust_data(root.row_count,2,self.state,root)
            allow_no_selection:False
            
        ToggleButton:
            text:"Open Ended"
            id: b4
            group: root.row_count
            state:root.b4state
            on_release:root.adjust_data(root.row_count,3,self.state,root)
            allow_no_selection:False
            
        FloatLayout:
            size_hint: 0.1, 0.1
            
<Second>:
    name: 'second'
    id : why

    BoxLayout:
        orientation:"vertical"
        size_hint:(1, 0.97)

        BoxLayout:
            size_hint:(0.95, None)
            pos_hint: {'center_x': .5, 'center_y': .5}
            orientation:"horizontal"

            RoundedButton:
                size_hint:(0.8, None)
                text:"Back"
                on_press:root.manager.current =  "first"
                    
            FloatLayout:#padding
            
            Label:
                markup: True
                text:"[size=45][b]Question Overview[/b]"
                
            FloatLayout:
            
            RoundedButton:
                size_hint:(0.8, None)
                text:"Export data"
                on_press:root.export()
                
            
        StockList:
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
        Window.size = (1000, 800)#set size of window after transtion to this screen
        

class Thrid(Screen):
    def on_enter(self):
        Window.size = (1000, 800)#set size of window after transtion to this screen
    
      

# Scene manager class 
class MyApp(App):
    
    Builder.load_string(kv)#load kv string
    sm = ScreenManager(transition=NoTransition())#declare scenemanger with no transtion set as default
    #--------Add screens to Scene manager--------#     
    sm.add_widget(First(name ='first'))
    sm.add_widget(Second(name ='second'))
    sm.add_widget(Thrid(name ='third'))
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
