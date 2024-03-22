#+++++++++++srource files
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Button, Label, Header, Footer, Placeholder, Static, SelectionList, Input
from textual.events import Mount
from textual import on
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.widgets.selection_list import Selection
from textual.screen import ModalScreen
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
        #+++++++++++++++++++++++++
        sB = SelectionList(id='cL')
        self.sB = sB
        for i in range(0,len(data['options'])):
            sB.add_option(Selection(data['options'][i]['title'],i))
            
        with Vertical():
            yield Container(Static("choose item an create theme",id="text"),id="sBox")
            yield Container(sB,id="cBox")
            yield Container(Button("do it",id="doit_b",disabled=True),Button('config',id="config-b"), id="bbox")
        #-------------------------
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None | object:
        button_id = event.button.id
        if button_id == "config-b":
             self.push_screen(QuitScreen())
    @on(SelectionList.SelectedChanged)
    def update_selected_view(self) -> None:
        if len((self.query_one('SelectionList')).selected) == 0:
            self.query_one("Button#doit_b").disabled = True;
        else:
            self.query_one("Button#doit_b").disabled = False;




class QuitScreen(ModalScreen[bool]):  


    def compose(self) -> ComposeResult:
        yield Grid(
            Static("Are you sure you want to quit?"),
            Input(placeholder="write a origin file or directory or url"),
            Input(placeholder="write a destination directory"),
            
            Container(Button("save", variant="default", id="save_b"),
            id="dialog",
        ))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)


    




if __name__ == "__main__":
    app = Cloner()
    app.run()

