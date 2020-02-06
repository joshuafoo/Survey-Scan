from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
Window.size = (1000, 800)
#Window.clearcolor = (1, 1, 1, 1)
class Item(GridLayout):
    def spinnerchange(a,b):
        pass
#        print(a,b)
    pass
kv = """
<StockList>: # RecycleView
    viewclass: 'Item'
    data: self.getData()
    RecycleBoxLayout:
        orientation: 'vertical'
        default_size: None, dp(300)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height

<Item>:
    name: 'init value'
    info: 'init value'
    default: 'init value'
    row_count: 'init value'
    cols: 1
    Label:
        text: root.name
    
    Spinner:
    
        size_hint: 0.8, 0.5
        size: 100, 44
        pos_hint: {'center': (.5, .5)}
        text: root.default
        values: 'Multiple-Choice', 'Strongly Agree/Disagree', 'Scale Rating (1 to 10)', 'Open Ended'
        on_text:root.spinnerchange(root.row_count)

BoxLayout:
    StockList:

"""

# Builder.load_file('gui/stockList.kv')


class StockList(RecycleView):

  def getData(self):
    data = []
    for i in range(0,10):
      add = {}
      add['info'] = 'Onn kit ' + str(i)
      add['name'] = 'item ' + str(i)
      add['default'] = 'item ' + str(i)
      add['row_count'] = str(i)
      data.append(add)
#    print(datxa)
    return data

class TestApp(App):
  def build(self):
    return Builder.load_string(kv)


if __name__ == '__main__':
  TestApp().run()
