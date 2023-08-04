import os
import pypandoc
import shutil
import time
import pickle
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from tkinter import Tk
from tkinter.filedialog import askdirectory
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField

Window.size = (Window.width, Window.height / 2)  # Make the window shorter

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: [30, 10, 30, 10]
    spacing: 10
    pos_hint: {'center_y': 0.5}
    BoxLayout:
        size_hint_x: 0.8
        MDTextField:
            id: root_dir_input
            hint_text: "Root directory"
            mode: "rectangle"
        MDIconButton:
            icon: "folder"
            on_release: app.open_filechooser('root_dir_input')
    BoxLayout:
        size_hint_x: 0.8
        MDTextField:
            id: new_dir_input
            hint_text: "New directory"
            mode: "rectangle"
        MDIconButton:
            icon: "folder"
            on_release: app.open_filechooser('new_dir_input')
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        spacing: '12dp'
        MDRaisedButton:
            text: "Sync"
            size_hint_x: None
            width: 300
            font_size: '18sp'
            pos_hint: {'center_x': 0.5}
            on_release: app.sync()

'''

target_subdirectory = 'College Essay\/'

class SyncApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # Use dark mode
        self.theme_cls.primary_palette = "Blue"  # Set primary color to blue
        return Builder.load_string(KV)

    def open_filechooser(self, target):
        self.target = target
        Tk().withdraw()  # Hide the root Tk window
        selected_path = askdirectory()  # Open the file dialog
        self.root.ids[self.target].text = selected_path

    def sync(self):
        root_dir = self.root.ids.root_dir_input.text
        new_dir = self.root.ids.new_dir_input.text

        try:
            with open('last_sync_time.pkl', 'rb') as f:
              last_sync_time = pickle.load(f)
        except FileNotFoundError:
            last_sync_time = 0

        # Walk through the directory structure
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                md_file = os.path.join(dir_path, file_name)
                # Ignore .canvas files and files modified before the last sync
                if not file_name.endswith('.canvas') and os.path.getmtime(md_file) > last_sync_time:
                    # For each .md file, convert it to .docx
                    if file_name.endswith('.md'):
                        docx_file = file_name.replace('.md', '.docx')
                        # create corresponding directory structure in the new directory
                        new_dir_path = dir_path.replace(root_dir, new_dir)
                        if not os.path.exists(new_dir_path):
                            os.makedirs(new_dir_path)
                        # Convert md to docx using pandoc
                        print('Converting to ' + os.path.join(new_dir_path, docx_file))
                        output = pypandoc.convert_file(md_file, 'docx', outputfile=os.path.join(new_dir_path, docx_file), extra_args=['--reference-doc', 'template-modern.docx'])
                        assert output == ""
                else:
                    print_string = os.path.join(dir_path, file_name)
                    index = print_string.find(target_subdirectory)
                    if index != -1:
                        print(print_string[index:])
                    else:
                        print("Couldn't find target subdirectory in path")
        with open('last_sync_time.pkl', 'wb') as f:
            pickle.dump(time.time(), f)
        print('done')

SyncApp().run()
