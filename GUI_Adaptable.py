from tkinter import *
from tkinter.ttk import *
from QueryModule import *
from functools import partial

window=Tk()

window.title("Searcher Window")
# window.geometry('350x400') # Mida per defecte, si no es posa s'obre una finestra per a que es vegi tot
rows=0
lbl=Label(window, text="Els desplegables son: ")
lbl.grid(column=0,row=rows)
rows += 1

def clearCBox(cbox):
	
	#inv_CBoxDict = {values: keys for keys, values in clearButtonDict.items()}
	#(tableName,filterName) = invCBoxDict[]
	cbox.set('')

labelsDict = {}
CBoxDict = {}
clearButtonDict = {}

#filterDict = obtainFilterDict()

filterDict = {
	("key1", "aux1") : ["value 1", "value 2", "value 3"],
	("key2", "aux2") : ["value 1", "value 2", "value 3"],
	("key3", "aux3") : ["value 1", "value 2", "value 3"],
	("key4", "aux4") : ["value 1", "value 2", "value 3"]
}


for (tableName,filterName) in filterDict:
	labelsDict[(tableName,filterName)] = Label(window, text=filterName)
	CBoxDict[(tableName,filterName)] = Combobox(window,state="readonly", values=filterDict[(tableName,filterName)])
	clearButtonDict[(tableName,filterName)] = Button(window, text='Clear', command=partial(clearCBox,CBoxDict[(tableName,filterName)]))

	labelsDict[(tableName,filterName)].grid(column=0, row=rows, pady=5)
	clearButtonDict[(tableName,filterName)].grid(column=2, row=rows, pady=5)
	#not working
	#CBoxList[rows] = 
	CBoxDict[(tableName,filterName)].grid(column=1, row=rows, pady=5, padx=10)
	############

	rows += 1

def obtainSearchDict(CBoxDict):
	searchDict = {}
	for (tableName,filterName) in CBoxDict:
		filterValue = CBoxDict[(tableName,filterName)].get()
		if filterValue != '':
			searchDict[(tableName,filterName)] = filterValue
	return searchDict


	

def cerca():
	searchDict = obtainSearchDict(CBoxDict)
	print(searchDict)
	searchResult = querySearch(searchDict)
	lbl4=Label(window, text=str(searchResult))
	lbl4.grid(column=0, row=rows, pady=10)



button2=Button(window, text="Cerca", command=cerca)
button2.grid(column=1, row=rows, pady=10)
rows += 1
window.mainloop()