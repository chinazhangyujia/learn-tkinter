from re import A
import tkinter as tk
from tkinter import RIGHT, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES

window_width = 1000
window_height = 600

class Window(TkinterDnD.Tk):
    options = ('Option 1', 'Option 2')

    def __init__(self):
        super().__init__()
        self.title('Diagram Generator')
        self.geometry(f'{window_width}x{window_height}+50+50')
        self.resizable(False, False)

        self.option_var = tk.StringVar(self)

        self.columnconfigure(1, weight=1)
        self._create_drop_zone().grid(column=0, row=0, sticky=tk.NW, padx=10, pady=10)
        self._create_display_panel().grid(column=1, row=0, sticky=tk.NW, padx=10, pady=10)


    def _create_drop_zone(self):
        frame = ttk.Frame(self)

        ttk.Label(frame, text='Drop your csv').pack()

        listbox_frame = ttk.Frame(frame)
        listbox = tk.Listbox(listbox_frame, selectmode='extended', width=40)
        listbox.drop_target_register(DND_FILES)
        listbox.dnd_bind("<<Drop>>", self._drop_inside_file_list)
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, )
        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview)
        scrollbar.pack(side=RIGHT, fill=tk.Y)
        listbox.pack()
        listbox_frame.pack()

        remove_button = ttk.Button(frame, text='Remove', command=self._remove_files)
        remove_button.pack(side=tk.LEFT)

        self.file_list_box = listbox

        return frame
    
    def _remove_files(self):
        selected_items = self.file_list_box.curselection()
        for i in selected_items[::-1]:
            self.file_list_box.delete(i)

    def _drop_inside_file_list(self, event):
        file_names = []
        if ' ' in event.data:
            file_names = event.data.split(' ')
        else:
            file_names.append(event.data)

        self.file_list_box.insert("end", *file_names)
    
    def _remove_files_from_list(self, event):
        for i in self.file_list_box.curselection():
            self.file_list_box.delete(i)

    def _create_display_panel(self):
        frame = ttk.Frame(self)

        option_menu = ttk.OptionMenu(
            frame,
            self.option_var,
            self.options[0],
            *self.options,
            command=self._option_changed)
        
        option_menu.grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)
        return frame
    
    def _option_changed(self, *args):
        print(self.option_var.get())

