#+++++++++++srource files
from os.path import exists, isdir, isfile, join
from sys import path
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Button, Label, Header, Footer, Placeholder, ProgressBar, Static, SelectionList, Input,Checkbox
from textual.events import Mount
from textual import on
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.widgets.selection_list import Selection
from textual.screen import ModalScreen
import json
import shutil
import requests
from urllib.parse import urlparse
import os
import ast
#-----------
data =None
style_file=os.path.join(os.path.abspath(__file__+"/.."),"styles.tcss")
data_file=os.path.join(os.path.abspath(__file__+"/.."),"data.json")

with open(data_file) as f:
    temp = json.load(f)
    data=temp;

class Cloner(App):
    CSS_PATH = style_file
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
            yield Horizontal(Vertical(Button("select all",id="select_all_btn"),Button("reset all",id="reset_all_btn")),sB,id="all_b")
            yield Container(Button("clone",id="clone_b",disabled=True),Button('config',id="config_b",disabled=True),Button("add",id="addb"),id="bbox")
        #-------------------------
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None | object:
        button_id = event.button.id
        if button_id == "select_all_btn":
            self.sB.select_all()
        if button_id == "reset_all_btn":
            self.sB.deselect_all()

        if button_id == "clone_b":
            for i in self.sB.selected:
                for source in data["options"][i]['sources']:
                    copyProcess.copy(source[0], data["options"][i]['destination'], source[1])

        if button_id == "config_b":
             self.push_screen(ConfigScreen(pk=(self.sB.highlighted)or 0))
        if button_id == "addb":
             self.push_screen(AddScreen())
    @on(SelectionList.SelectedChanged)
    def update_selected_view(self) -> None:
        if self.sB.selected:
            self.query_one("Button#clone_b").disabled = True;
        else:
            self.query_one("Button#clone_b").disabled = False;

    def on_selection_list_selection_highlighted(self):
        if type(self.sB.highlighted) == int:
            self.query_one("Button#config_b").disabled = False;
        else:
            self.query_one("Button#config_b").disabled = True;
            


class copyProcess():
    @staticmethod
    def copy(origin:str,destination:str,filename:str):
        os.makedirs(destination,exist_ok=True)
        if copyProcess.is_valid_url(origin):
            copyProcess.download_web(origin,destination,filename)
        else:
            copyProcess.local_copy(origin,destination,filename)
    @staticmethod
    def download_web(url:str,destination:str,filename:str):
        response = requests.get(url)
        open(os.path.join(destination,filename), "wb").write(response.content)
    @staticmethod
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    @staticmethod
    def local_copy(origin:str,destination:str,filename:str):
        if os.path.exists(origin):
             if os.path.isfile(origin) and not os.path.exists(os.path.join(destination,filename)):
                  shutil.copy2(origin, os.path.join(destination,filename))
             elif os.path.isdir(origin) and not os.path.exists(os.path.join(destination,filename)):
                  shutil.copytree(origin, os.path.join(destination,filename))




class ConfigScreen(ModalScreen[bool]):  

    def __init__(self, pk:int,name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.pk = pk
        self.data:dict = data["options"][pk]
    def compose(self) -> ComposeResult:
        yield Grid(
            Vertical(Label("title:"),Input(self.data['title'],placeholder="inter a title",id="input_title_conf",classes="input")),
            Vertical(Label("description:"),Input(self.data['description'],placeholder="inter description",id="input_description_conf",classes="input")),
            Vertical(Label("sources:"),Input(str(self.data['sources']),placeholder="write an origin file or directory or url",id="input_ori_conf",classes="input")),
            Vertical(Label("destination:"),Input(self.data['destination'],placeholder="write a destination directory",id="input_destination_conf",classes="input")),
            

            Horizontal(Button('save',id="save_b"),Button('delete',id="delete_b")),
            id="dialog"
        )


    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_b":
            data['options'][self.pk]['destination'] = self.query_one('#input_destination_conf').value
            list_of_lists = ast.literal_eval(self.query_one('#input_ori_conf').value)
            data['options'][self.pk]['sources'] = list_of_lists
            data['options'][self.pk]['title'] = self.query_one("#input_title_conf").value
            data['options'][self.pk]['description'] = self.query_one('#input_description_conf').value
            with open(data_file,'w') as file:
                json.dump(data,file)
                
            refresh()
            self.dismiss()
        if event.button.id == "delete_b":
            data['options'].pop(self.pk)
            with open(data_file,'w') as file:
                json.dump(data,file)
            refresh()
            self.dismiss(True)


    

class AddScreen(ModalScreen[bool]):  

    def __init__(self,name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
    def compose(self) -> ComposeResult:
        yield Grid(
            Vertical(Label("title:"),Input(placeholder="inter title",id="input_title_add",classes="input")),
            Vertical(Label("description:"),Input(placeholder="inter description",id="input_description_add",classes="input")),
            Vertical(Label("sources:"),Input(placeholder="write a origin file or directory or url",id="input_ori_add",classes="input")),
            Vertical(Label("destination:"),Input(placeholder="write a destination directory",id="input_des_add",classes="input")),
            
            
            Horizontal(Button("save", variant="default", id="save_b_add"),
                      Button("cancel",variant="default",id="cancel_b_add"),
            id="dialog"
        ))

    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_b_add":
            des = self.query_one('#input_des_add').value
            title = self.query_one('#input_title_add').value
            description = self.query_one('#input_description_add').value
            listOfsources = ast.literal_eval(self.query_one('#input_ori_add').value)
            new_dict = {"title": title,"description": description,"sources": listOfsources,"destination": des}
            data["options"].append(new_dict)
            with open(data_file,'w') as file:
                json.dump(data,file)
            refresh()
            self.dismiss(True)
        if event.button.id == "cancel_b_add":
            self.dismiss(True)


    

def refresh():
       app.sB.clear_options()
       for i in range(0,len(data['options'])):
            app.sB.add_option(Selection(data['options'][i]['title'],i))
            

if __name__ == "__main__":
    global app;
    app = Cloner()
    app.run()

