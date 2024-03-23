#+++++++++++srource files
from os.path import isdir, isfile
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
            yield Container(Button("do it",id="doit_b",disabled=True),Button('config',id="config-b"),Button("add",id="addb"),id="bbox")
        #-------------------------
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None | object:
        button_id = event.button.id
        if button_id == "doit_b":
            for item in data['options']:
                for source in item['sources']:
                    copyProcess.copy(source[0], item['destination'], source[1])

        if button_id == "config-b":
             self.push_screen(ConfigScreen(pk=(self.sB.highlighted)or 0))
        if button_id == "addb":
             self.push_screen(AddScreen())
    @on(SelectionList.SelectedChanged)
    def update_selected_view(self) -> None:
        if len(self.sB.selected) == 0:
            self.query_one("Button#doit_b").disabled = True;
        else:
            self.query_one("Button#doit_b").disabled = False;

class copyProcess():
    @staticmethod
    def copy(origin:str,destination:str,filename:str):
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
             if os.path.isfile(origin):
                  shutil.copy2(origin, os.path.join(destination,filename))
             elif os.path.isdir(origin):
                  shutil.copytree(origin, os.path.join(destination,filename))




class ConfigScreen(ModalScreen[bool]):  

    def __init__(self, pk:int,name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.pk = pk
        self.data:dict = data["options"][pk]
    def compose(self) -> ComposeResult:
        yield Grid(
            Input(str(self.data['title']),placeholder="write a origin file or directory or url",id="input_title_conf",classes="input"),
            Input(str(self.data['description']),placeholder="write a origin file or directory or url",id="input_description_conf",classes="input"),
            Input(str(self.data['sources']),placeholder="write a origin file or directory or url",id="input_ori_conf",classes="input"),
            Input(str(self.data['destination']),placeholder="write a destination directory",id="input_des_conf",classes="input"),
            Horizontal(Button("save", variant="default", id="save_b"),
            Button("delete",variant="default",id="delete_b"),
            id="dialog",
        ))

    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_b":
            data['options'][self.pk]['destination'] = self.query_one('#input_des_conf').value
            list_of_lists = ast.literal_eval(self.query_one('#input_ori_conf').value)
            data['options'][self.pk]['sources'] = list_of_lists
            data['options'][self.pk]['title'] = self.query_one("#input_title_conf").value
            data['options'][self.pk]['description'] = self.query_one('#input_description_conf').value
            with open('data.json','w') as file:
                json.dump(data,file)
        if event.button.id == "delete_b":
            data['options'].pop(self.pk)
        self.dismiss(True)
        refresh()


    

class AddScreen(ModalScreen[bool]):  

    def __init__(self,name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
    def compose(self) -> ComposeResult:
        yield Grid(
            Input(placeholder="inter title",id="input_title_add",classes="input"),
            Input(placeholder="inter description",id="input_description_add",classes="input"),
            Input(placeholder="write a origin file or directory or url",id="input_ori_add",classes="input"),
            Input(placeholder="write a destination directory",id="input_des_add",classes="input"),
            
            Container(Button("save", variant="default", id="save_b_add"),
            id="dialog",
        ))

    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_b_add":
            des = self.query_one('#input_des_add').value
            title = self.query_one('#input_title_add').value
            description = self.query_one('#input_description_add').value
            listOfsources = ast.literal_eval(self.query_one('#input_ori_add').value)
            new_dict = {"title": title,"description": description,"sources": listOfsources,"destination": des}
            data["options"].append(new_dict)
            with open('data.json','w') as file:
                json.dump(data,file)
        self.dismiss(True)


    

def refresh():
       app.sB.clear_options()
       for i in range(0,len(data['options'])):
            app.sB.add_option(Selection(data['options'][i]['title'],i))
            

if __name__ == "__main__":
    global app;
    app = Cloner()
    app.run()

