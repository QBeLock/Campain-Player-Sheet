import json
import os
from tkinter import filedialog
import random

dirname = os.path.dirname(__file__)
config_path = os.path.join(dirname, 'csp_config.json')

config_dir = {}

sheets = {}
session = -1
hraci = []
kandidati = []


def kontrola_riadku(hrac,riadok,varenie=True):
    if hrac[riadok] == "":
        print(riadok + ": chíba")
    if len(hrac[riadok]) > 100 and varenie:
        print(f"{riadok}: {hrac["Meno"].upper()} VARÍ")
    else:
        print(riadok + ": v pohode")

with open(config_path) as json_file:
    json_data = json.load(json_file)
    for key in json_data:
        sheet_file = open(json_data[key])
        sheets.update({key: json.loads(sheet_file.read())})


while True:
    command = input("zadanie: ")
    match command:
        case "load":
            file_path = filedialog.askopenfilename(title="Load", filetypes=[("CPS",("*.cps")),("JSON", ('*.json')),("All files", "*.*")], defaultextension=".json")
            with open(file_path) as json_file:
                currrent_sheet = json.loads(json_file.read())
                if currrent_sheet["Meno"] in sheets:
                    sheets[currrent_sheet["Meno"]] = currrent_sheet
                    print(currrent_sheet["Meno"] + " sheet updatnuti")
                else:
                    sheets.update({currrent_sheet["Meno"]: currrent_sheet})
                    print(currrent_sheet["Meno"] + " sheet pridani")
                    config_dir.update({currrent_sheet["Meno"]: file_path})
                    with open(config_path, "w") as config:
                        config.write(json.dumps(config_dir))
        case "list":
            print(list(sheets.keys()))
        case "hrac":
            try:
                hrac = sheets[input("meno: ")]
                while True:
                    command = input("sub-zadanie: ")
                    match command:
                        case "kontrola" | "k" | "test" | "t":
                            kontrola_riadku(hrac,"Meno Postavi",varenie=False)
                            kontrola_riadku(hrac,"Podstatne Pre Postavu")
                            kontrola_riadku(hrac,"Ďalšie Pláni")
                            if True in hrac["Major eventi"]:
                                print("Major eventi: v pohode")
                            else:
                                print("Major eventi: chiba")
                            minor_eventi = 0
                            for i in hrac["Minor eventi"]:
                                minor_eventi += i
                            print("Minor eventi: " + str(minor_eventi))
                        case "plot twist" | "pt":
                            print("Plot twist: " + str(len(hrac["Plot twist"] )))
                            if True in hrac["Plot twist session"]:
                                print("session: v pohode")
                            else:
                                print("session: chiba")
                        case "kringe tester" | "kt":
                            if hrac["Meno"].lower() in ["maco", "tvoje meno debil"]:
                                print("kringe")
                            else:
                                print("based")
                        case "vimaz":
                            sheets.pop(hrac["Meno"])
                            config_dir.pop(hrac["Meno"])
                            print(hrac["Meno"] + " sheet odstraneni")
                            with open(config_path, "w") as config:
                                config.write(json.dumps(config_dir))
                        case "spet" | "s" | "end":
                            break
            except KeyError:
                print("meno neni loadnute")
        case "help":
            print("""load
list
hrac
  - kontrola | k | test | t
  - plot twist | pt
  - kringe tester | kt
  - vimaz
  - spet | s | end
kontrola | k | test | t
help
session | s
DM | dm
debil selector | ds | db
end""")
        case "kontrola" | "k" | "test" | "t":
            event_counter = [0,0,0]
            for i in sheets.values():
                for j in range(3):
                    event_counter[j] += int(i["Major eventi"][j])
            print(event_counter)
        case "session" | "s":
            viber = input("session: ")
            if viber == "nove" or viber == "n":
                session += 1
            else:
                try:
                    if int(viber) > 3 or int(viber) < 1:
                        raise ValueError
                    session = int(viber) - 1
                except ValueError:
                    print("zli vstup")
            kandidati.clear()
            hraci.clear()
            for i in sheets.values():
                if i["Major eventi"][session]:
                    kandidati.append(i["Meno"])
                hraci.append(i["Meno"])
            random.shuffle(hraci)
            random.shuffle(kandidati)
        case "DM" | "dm":
            try:
                if (len(kandidati) == 1 and len(hraci) == len(sheets)) or len(kandidati) == 0:
                    DM = hraci[0]
                else:
                    DM = kandidati[0]
                print(DM)
                if hraci != []:
                    hraci.remove(DM)
                if kandidati != []:
                    kandidati.remove(DM)
                else:
                    for i in sheets.keys():
                        hraci.append(i)
                    random.shuffle(hraci)
            except IndexError:
                print("session nebol inicializovani")
        case "debil selektor" | "ds" | "db":
            print(random.choice(list(sheets.keys())))
        case "end":
            break