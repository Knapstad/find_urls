from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from os import listdir 


kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


class AddButton(Button):
    pass


class SubtractButton(Button):
    pass


class Container(GridLayout):
    pass


class MainApp(App):

    def build(self):
        self.title = 'Finn alle sider - OBOS'
        return Container()

if __name__ == "__main__":
    app = MainApp()
    app.run()