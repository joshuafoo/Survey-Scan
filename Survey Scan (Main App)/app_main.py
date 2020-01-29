#--------Import all required packages--------#
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.button import Button 
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class First(Screen):
    def __init__(self, **kwargs):
        super(First, self).__init__(**kwargs)

        Window.size = (500, 100)#set window size
        
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
                    Window.size = (1000, 800)#set window size
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

class Second(Screen):
    def __init__(self, **kwargs):
        super(Second, self).__init__(**kwargs)
        
        #--------Create ui elements--------#
        
        
        #--------Actions/triggers and bindings--------#
        
        #--------Add widgets to screen--------#

# Scene manager class 
class MyApp(App):
    sm = ScreenManager(transition=FadeTransition())
    #--------Add screens to Scene manager--------#     
    sm.add_widget(First(name ='first'))
    sm.add_widget(Second(name ='second'))
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
