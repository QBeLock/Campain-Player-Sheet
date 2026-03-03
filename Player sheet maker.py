import json
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Player sheet maker")




class zakladni_riadok():
    data = {}
    riadok = -1
    def __init__(self, nazov, grid_velkost = riadok):
        zakladni_riadok.riadok += 1
        self.nazov = tk.Label(root, text=nazov)
        self.nazov.grid(row=zakladni_riadok.riadok, column=0, pady=(0,grid_velkost))
        zakladni_riadok.data.update({nazov: ""})

class textovi_vstup(zakladni_riadok):
    text = tk.StringVar()

    def __init__(self, nazov, grid_velkost = 0):
        super().__init__(nazov,grid_velkost)
        self.okno = tk.Entry(root, textvariable=zakladni_riadok.data[nazov], width=50)
        self.okno.grid(row=zakladni_riadok.riadok, column=1, pady=(0,grid_velkost))

    def get(self):
        return self.text.get()

class session_choice_bool(zakladni_riadok):
    def __init__(self, nazov,grid_velkost = 0):
        super().__init__(nazov,grid_velkost)
        zakladni_riadok.data[nazov] = []
        self.session_input = []
        self.frame = tk.Frame(root)
        for i in range(3):
            zakladni_riadok.data[nazov].append(tk.BooleanVar())
            self.session_input.append(tk.Checkbutton(self.frame, variable=zakladni_riadok.data[nazov][i]))
            self.session_input[i].grid(row=0, column=i + 1, padx=20)
        self.frame.grid(row=zakladni_riadok.riadok, column=1, pady=(0,grid_velkost))

class session_choice_int(zakladni_riadok):


    def __init__(self, nazov, grid_velkost = 0):
        super().__init__(nazov, grid_velkost)
        zakladni_riadok.data[nazov] = []
        self.session_input = []
        self.frame = tk.Frame(root)
        for i in range(3):
            zakladni_riadok.data[nazov].append(tk.IntVar())
            self.session_input.append(tk.Entry(self.frame, textvariable=zakladni_riadok.data[nazov][i], width=1))
            self.session_input[i].grid(row=0, column=i + 1, padx=30, pady=0)
        self.frame.grid(row=zakladni_riadok.riadok, column=1, pady=(0,grid_velkost))


meno = textovi_vstup("Meno", 10)

meno_postavi = textovi_vstup("Meno Postavi")
podstatne_pre_postavu = textovi_vstup("Podstatne Pre-Postavi",10)

plot_twist = textovi_vstup("Plot Twist")
session_choice_bool("Plot twist")
dalsie_plani = textovi_vstup("Dalšie Pláni")
session_choice_int("Minor eventi")
session_choice_bool("Major eventi")


def save():
    file_path = filedialog.askopenfilename(title="Select Profile Picture", filetypes=[("JSON", ('*.json'))], defaultextension=".json")



def load():
    file_path = filedialog.askopenfilename(title="Select Profile Picture", filetypes=[("JSON", ('*.json'))])
    with open(file_path) as json_file:
        data = json.load(json_file)


load = tk.Button(root, text="Load", command=load)
load.grid(row=6, column=2)
save = tk.Button(root, text="Save", command=save)
save.grid(row=7, column=2)


root.mainloop()