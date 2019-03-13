from tkinter import *
from tkinter.ttk import *
from QueryModule import *
from functools import partial

window=Tk()

window.title("Searcher Window")
rows=0
lbl=Label(window, text="Filter options: ")
lbl.grid(column=0,row=rows)
rows += 1

def clearCBox(cbox):
	cbox.set('')

labelsDict = {}
CBoxDict = {}
clearButtonDict = {}

filterDict = obtainFilterDict()

for (tableName,filterName) in filterDict:
	labelsDict[(tableName,filterName)] = Label(window, text=filterName)
	CBoxDict[(tableName,filterName)] = Combobox(window,state="readonly", values=filterDict[(tableName,filterName)])
	clearButtonDict[(tableName,filterName)] = Button(window, text='Clear', command=partial(clearCBox,CBoxDict[(tableName,filterName)]))

	labelsDict[(tableName,filterName)].grid(column=0, row=rows, pady=5)
	CBoxDict[(tableName,filterName)].grid(column=1, row=rows, pady=5, padx=10)
	clearButtonDict[(tableName,filterName)].grid(column=2, row=rows, pady=5)

	rows += 1

def obtainSearchDict(CBoxDict):
	searchDict = {}
	for (tableName,filterName) in CBoxDict:
		filterValue = CBoxDict[(tableName,filterName)].get()
		if filterValue != '':
			searchDict[(tableName,filterName)] = filterValue
	return searchDict
	

def search():
	searchDict = obtainSearchDict(CBoxDict)
	print(searchDict)
	searchResult = querySearch(searchDict)
	lbl4=Label(window, text=str(searchResult))
	lbl4.grid(column=0, row=rows, pady=10)


button2=Button(window, text="Search", command=search)
button2.grid(column=1, row=rows, pady=10)
rows += 1
window.mainloop()