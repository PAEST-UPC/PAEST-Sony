from tkinter import *
from tkinter.ttk import *
import QueryModule

window=Tk()

window.title("Searcher Window")
# window.geometry('350x400') # Mida per defecte, si no es posa s'obre una finestra per a que es vegi tot
rows=0
lbl=Label(window, text="Els desplegables son: ")
lbl.grid(column=0,row=rows)
rows += 1
lbl4=Label(window, text="Els resultats de la cerca son: ")

labelsDic = {}
CBoxDic = {}

filterDict = QueryModule.obtainFilterDict()

for filterName in filterDict:
	labelsDic[filterName] = Label(window, text=filterName)
	CBoxDic[filterName] = Combobox(window,state="readonly", values=filterDict[filterName])
	labelsDic[filterName].grid(column=0, row=rows, pady=5)
	CBoxDic[filterName].grid(column=1, row=rows, pady=5, padx=10)
	rows += 1

	
	
def cerca():
	lbl4.grid(column=0, row=rows, pady=10)
button2=Button(window, text="Cerca", command=cerca())
button2.grid(column=1, row=rows, pady=10)
rows += 1
window.mainloop()