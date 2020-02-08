from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
Window.size = (1000, 800)
# Window.clearcolor = (1, 1, 1, 1)
class Item(GridLayout):pass
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

    name: 'init value'
    row_count: 'init value'
    b1_state: 'init value'
    b2_state: 'init value'
    b3_state: 'init value'
    b4_state: 'init value'
    
    cols: 1
    Label:
        text: root.name
    BoxLayout:
        size_hint_y: None
        height: "40dp"
        ToggleButton:
            text:"Multiple-Choice"
            id: b1
            group: root.row_count
            #state:root.b1_state
            on_release: app.StockList.adjust_data(app.StockList,root.row_count,id)
            allow_no_selection:False

        ToggleButton:
            text:"Strongly Agree/Disagree"
            id: b2
            group: root.row_count
            #state:root.b2_state
            on_release: app.StockList.adjust_data(app.StockList,root.row_count,id)
            allow_no_selection:False

        ToggleButton:
            text:"Scale Rating (1 to 10)"
            id: b3
            group: root.row_count
            #state:root.b3_state
            on_release: app.StockList.adjust_data(app.StockList,root.row_count,id)
            allow_no_selection:False
        ToggleButton:
            text:"Open Ended"
            id: b4
            group: root.row_count
            #state:root.b4_state
            on_release: app.StockList.adjust_data(app.StockList,root.row_count,id)
            allow_no_selection:False
        
BoxLayout:
    StockList:

"""

class TestApp(App):
    class StockList(RecycleView):
        toggle_states = [["normal" for i in range(4)] for i in range(10)]
        data = []
        def getData(self):
            data = []
            for i in range(0,10):
                add = {}
                add['name'] = 'item ' + str(i)
                add['b1_state'] = self.toggle_states[i][0]
                add['b2_state'] = self.toggle_states[i][1]
                add['b3_state'] = self.toggle_states[i][2]
                add['b4_state'] = self.toggle_states[i][3]
                add['row_count'] = str(i)
                data.append(add)
            print(data)
            return data
        def adjust_data(self, rvRow,button_name):
            for d in self.data:
                if d['row_count'] == rvRow:
                        if(d[button_name] == "normal"):d[button_name] = "down"; print("DOWN")
                        elif(d[button_name] == "down"):d[button_name] = "normal"; print("UP")
                        break
            print(self.data)

            
    def build(self):
        return Builder.load_string(kv)


if __name__ == '__main__':
  TestApp().run()
