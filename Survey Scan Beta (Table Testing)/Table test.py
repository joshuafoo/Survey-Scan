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
from kivy.properties import StringProperty
Window.size = (1000, 800)
#Window.clearcolor = (1, 1, 1, 1)
toggle_states = [["normal" for i in range(4)] for i in range(10)]
class Item(GridLayout):
    def adjust_data(self, rvRow,button_index,state,refff):
        #print(rvRow,button_index,state)
        toggle_states[int(rvRow)] = ["normal" for i in range(4)]
        toggle_states[int(rvRow)][int(button_index)] = str(state)
        root = App.get_running_app().root
        root.ids.rv.data = root.ids.rv.getData()
        refff.b1state = refff.ids.b1.state
        refff.b2state = refff.ids.b2.state
        refff.b3state = refff.ids.b3.state
        refff.b4state = refff.ids.b4.state
        #root.ids.rv.refresh_from_data()
        pass
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
    b1state: 'normal'
    b2state: 'normal'
    b3state: 'normal'
    b4state: 'normal'
    
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
        
BoxLayout:
    StockList:
        id:rv

"""



class StockList(RecycleView):
    
    def getData(self):
        data = []
        for i in range(0,10):
            add = {}
            add['name'] = 'item ' + str(i)
            add['b1state'] = toggle_states[i][0]
            add['b2state'] = toggle_states[i][1]
            add['b3state'] = toggle_states[i][2]
            add['b4state'] = toggle_states[i][3]
            add['row_count'] = str(i)
            data.append(add)
        #print()
        #print(data)
        return data


class TestApp(App):
  def build(self):
    return Builder.load_string(kv)


if __name__ == '__main__':
  TestApp().run()


