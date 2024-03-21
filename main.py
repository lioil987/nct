#+++++++++++srource files
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Button, Label, Header, Footer, Static, SelectionList
from textual.containers import Container, Vertical, Horizontal
from textual.widgets.selection_list import Selection
import json
#-----------
data =None
with open('./data.json') as f:
    temp = json.load(f)
    data=temp;

class Cloner(App):
    CSS_PATH = "./styles.tcss"
    TITLE = "Cloner"
    SUB_TITLE = "clone framework"

    def compose(self,) -> ComposeResult:
        yield Header()
        yield Expander()
        yield Footer()
    


class Expander(Widget):
    def compose(self) -> ComposeResult:
        sB = SelectionList(id='cL')
        for i in range(0,len(data['options'])):
            sB.add_option(Selection(data['options'][i]['title'],i))
        with Vertical():
            yield Container(Static("hello",id="text"),id="sBox")
            yield Container(sB,id="cBox")
            yield Container(Button("do it"), id="bbox")
        
if __name__ == "__main__":
    app = Cloner()
    app.run()

