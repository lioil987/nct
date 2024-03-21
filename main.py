#+++++++++++srource files
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Button, Label, Header, Footer, Static, SelectionList
from textual.containers import Container
from textual.widgets.selection_list import Selection
#-----------
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
        sel_list = SelectionList()
        sel_list.add_option(Selection('hi',1))
        yield Container(sel_list)

if __name__ == "__main__":
    app = Cloner()
    app.run()

