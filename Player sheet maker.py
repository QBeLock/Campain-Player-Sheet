import json
import tkinter as tk
from abc import ABC, abstractmethod
from asyncio.windows_events import NULL
from tkinter import filedialog

root = tk.Tk()
root.title("Player sheet maker")


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text,
                      background="#ffffe0", borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

class zakladni_riadok(ABC):
    riadky = []
    def __init__(self, nazov, tooltip, grid_velkost = 0,viska =0):
        zakladni_riadok.riadky.append(self)
        self.nazov = nazov
        self.lbl = tk.Label(root, text=nazov)
        self.lbl.grid(row=len(zakladni_riadok.riadky) - 1, column=0, pady=(0,grid_velkost))
        CreateToolTip(self.lbl, tooltip)
        self._grid_velkost = grid_velkost

    def _init_end(self):
        self.okno.grid(row=len(zakladni_riadok.riadky) - 1, column=1, pady=(0,self._grid_velkost))

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self, value):
        pass

class textovi_vstup(zakladni_riadok):


    def __init__(self, nazov, tooltip, grid_velkost = 0):
        super().__init__(nazov,tooltip,grid_velkost)
        self._data = tk.StringVar()
        self.okno = tk.Entry(root, textvariable=self._data, width=50)
        self._init_end()

    def get(self):
        return self._data.get()

    def set(self, value):
        self._data.set(value)



class session_choice_base(zakladni_riadok, ABC):

    @abstractmethod
    def create_session(self, session_id):
        pass

    def __init__(self, nazov, tooltip, grid_velkost=0):
        super().__init__(nazov,tooltip,grid_velkost)
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

    def set(self, value):
        for i in range(3):
            self.session[i].set(value[i])


class session_choice_bool(session_choice_base):
    def create_session(self, session_id):
        self.session.append(tk.BooleanVar())
        return tk.Checkbutton(self.okno, variable=self.session[session_id])



class session_choice_int(session_choice_base):
    def create_session(self, session_id):
        self.session.append(tk.IntVar())
        return tk.Entry(self.okno, textvariable=self.session[session_id], width=1)

class rozdelovac(zakladni_riadok):
    def __init__(self,tooltip = "", grid_velkost):
        super().__init__("",tooltip,grid_velkost)
        self.okno = tk.Label(root)
        self._init_end()
    def get(self):
        return NULL
    def set(self, value):
        pass





meno = textovi_vstup("Meno","Tvoje meno debil", 10)

postavi_sekcia = rozdelovac()
meno_postavi = textovi_vstup("Meno Postavi", "daj dáke cool meno nemusíš nam ho potom ani povedať podla roleplayu")
podstatne_pre_postavu = textovi_vstup("Podstatne Pre Postavi","Načom tvojej postave záleží. niečo čo ked sa stane tak na to bude reagovať.",10)

plot_sekcia = rozdelovac()
plot_twist = textovi_vstup("Plot twist", "niečo vimislíš")
session_choice_bool("Plot twist session", "kedi sa stane/ú tvoj(e) plot twisti. Každé okienko je session z lava do prava.")
dalsie_plani = textovi_vstup("Ďalšie Pláni", "Rôzne eventi, situacie alebo miesta ktore sa mozu obiavit v kampani")
session_choice_int("Minor eventi", "kedi sa stanú predom pripravené veci ktoré si vimislel ale len na velmi kráatko napr: najdeme zbran.\n Každé okienko je session z lava do prava napíš tam kolko sa ich má stať za daní session.")
session_choice_bool("Major eventi", "Rovnako ako minor eventi ale tieto môžu zabrať aj pol sessionu")



def konvertovat_data():
    konvertovane = {}
    for i in zakladni_riadok.riadky:
        if i.get():
            konvertovane.update({i.nazov: i.get()})
    return konvertovane


file_path = ""

def save():
    print(file_path + "---")
    if file_path == "":
        save_as()
    else:
        with open(file_path, "w") as json_file:
            json_file.write(json.dumps(konvertovat_data()))
            json_file.close()

def save_as():
    try:
        file_path = filedialog.asksaveasfilename(title="Save as", filetypes=[("JSON", ('*.json'))], defaultextension=".json", initialfile=zakladni_riadok.riadky[0].get()+" sheet")
        with open(file_path, "w") as json_file:
            json_file.write(json.dumps(konvertovat_data()))
            json_file.close()
            print(file_path)
    except FileNotFoundError:
        pass

def load():
    file_path = filedialog.askopenfilename(title="Load", filetypes=[("JSON", ('*.json')),("All files", "*.*")], defaultextension=".json")
    with open(file_path) as json_file:
        json_dir = json.loads(json_file.read())
        for i in zakladni_riadok.riadky:
            i.set(json_dir[i.nazov])
        json_file.close()
        print(file_path)

load_btn = tk.Button(root, text="Load", command=load)
load_btn.grid(row=5, column=2)
save_btn = tk.Button(root, text="Save", command=save)
save_btn.grid(row=6, column=2)
save_as_btn = tk.Button(root, text="Save as", command=save_as)
save_as_btn.grid(row=7, column=2)


root.mainloop()