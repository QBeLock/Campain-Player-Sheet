import json
import tkinter as tk
from abc import ABC, abstractmethod
from asyncio.windows_events import NULL
from tkinter import filedialog

root = tk.Tk()
root.title("Player sheet maker")




class zakladni_riadok(ABC):
    riadky = []
    def __init__(self, nazov, grid_velkost = 0):
        zakladni_riadok.riadky.append(self)
        self.nazov = nazov
        self.lbl = tk.Label(root, text=nazov)
        self.lbl.grid(row=len(zakladni_riadok.riadky) - 1, column=0, pady=(0,grid_velkost))
        self._grid_velkost = grid_velkost

    def _init_end(self):
        self.okno.grid(row=len(zakladni_riadok.riadky) - 1, column=1, pady=(0,self._grid_velkost))

    @abstractmethod
    def get(self):
        pass

    def set(self, value):
        self._data = value

class textovi_vstup(zakladni_riadok):


    def __init__(self, nazov, grid_velkost = 0):
        self._data = tk.StringVar()
        super().__init__(nazov,grid_velkost)
        self.okno = tk.Entry(root, textvariable=self._data, width=50)
        self._init_end()

    def get(self):
        return self._data.get()



class session_choice_base(zakladni_riadok, ABC):

    @abstractmethod
    def create_session(self, session_id):
        pass

    def __init__(self, nazov, grid_velkost=0):
        super().__init__(nazov, grid_velkost)
        self._data = []
        self.session = []
        self.session_input = []
        self.okno = tk.Frame(root)
        for i in range(3):
            self._data.append(NULL)
            self.session_input.append(self.create_session(i))
            self.session_input[i].grid(row=0, column=i + 1, padx=30, pady=0)
        self._init_end()

    def get(self):
        konvertovane = []
        for i in self.session:
            konvertovane.append(i.get())
        return konvertovane


class session_choice_bool(session_choice_base):
    def create_session(self, session_id):
        self.session.append(tk.BooleanVar())
        return tk.Checkbutton(self.okno, variable=self.session[session_id])



class session_choice_int(session_choice_base):
    def create_session(self, session_id):
        self.session.append(tk.IntVar())
        return tk.Entry(self.okno, textvariable=self.session[session_id], width=1)







meno = textovi_vstup("Meno", 10)

meno_postavi = textovi_vstup("Meno Postavi")
podstatne_pre_postavu = textovi_vstup("Podstatne Pre-Postavi",10)

plot_twist = textovi_vstup("Plot Twist")
session_choice_bool("Plot twist")
dalsie_plani = textovi_vstup("Dalšie Pláni")
session_choice_int("Minor eventi")
session_choice_bool("Major eventi")



def konvertovat_data():
    konvertovane = {}
    for i in zakladni_riadok.riadky:
        konvertovane.update({i.nazov: i.get()})
    return konvertovane


file_path = ""

def save():
    if file_path == "":
        save_as()
    else:
        with open(file_path, "w") as json_file:
            json_file.write(json.dumps(konvertovat_data()))
            json_file.close()

def save_as():
    try:
        file_path = filedialog.asksaveasfilename(title="Save as", filetypes=[("JSON", ('*.json'))], defaultextension=".json")
        with open(file_path, "w") as json_file:
            json_file.write(json.dumps(konvertovat_data()))
            json_file.close()
    except FileNotFoundError:
        pouzivani_subor = open(file_path, "w")
    finally:
        print(file_path)
        zapisat_do_suboru()

def load():
    file_path = filedialog.askopenfilename(title="Load", filetypes=[("JSON", ('*.json')),("All files", "*.*")], defaultextension=".json")
    with open(file_path) as json_file:
        json_dir = json.load(json_file)
        for i in zakladni_riadok.riadky:
            i.set(json_dir[i.nazov])
        json_file.close()

load_btn = tk.Button(root, text="Load", command=load)
load_btn.grid(row=5, column=2)
save_btn = tk.Button(root, text="Save", command=save)
save_btn.grid(row=6, column=2)
save_as_btn = tk.Button(root, text="Save as", command=save_as)
save_as_btn.grid(row=7, column=2)


root.mainloop()