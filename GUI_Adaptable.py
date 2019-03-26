from tkinter import *
from tkinter.ttk import *
#from QueryModule import *
from functools import partial
import ast

root=Tk()
myframe=Frame(root)
myframe.pack(expand = True) #Expandeix el primer frame

canvas=Canvas(myframe)
window=Frame(canvas,width=768, height=2000)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)


myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left",expand = True) #Expandeix el canvas
canvas.create_window((0,0),window=window,anchor='nw')
window.bind("<Configure>")
window.pack(expand = True) #Expandeix la llista pero es carrega la scrollbar!!


root.title("Searcher Window")
rows=0
lbl=Label(window, text="Filter options: ")
lbl.grid(column=0,row=rows)
rows += 1

def clearCBox(cbox):
	cbox.set('')

labelsDict = {}
CBoxDict = {}
clearButtonDict = {}

filterDict = ast.literal_eval(open("filterDict2.txt", "r").read())
#filterDict = obtainFilterDict()

for (tableName,filterName) in filterDict:
	labelsDict[(tableName,filterName)] = Label(window, text=filterName)
	CBoxDict[(tableName,filterName)] = Combobox(window,state="readonly", values=filterDict[(tableName,filterName)])
	clearButtonDict[(tableName,filterName)] = Button(window, text='Clear', command=partial(clearCBox,CBoxDict[(tableName,filterName)]))

	labelsDict[(tableName,filterName)].grid(column=0, row=rows, pady=5)
	CBoxDict[(tableName,filterName)].grid(column=1, row=rows, pady=5, padx=10)
	clearButtonDict[(tableName,filterName)].grid(column=2, row=rows, pady=5)

	rows += 1

canvas.configure(scrollregion=canvas.bbox("all"))

lbl4=Label(window, text='')
lbl4.grid(column=0, row=rows, pady=10)

def obtainSearchDict(CBoxDict):
	searchDict = {}
	for (tableName,filterName) in CBoxDict:
		filterValue = CBoxDict[(tableName,filterName)].get()
		if filterValue != '':
			searchDict[(tableName,filterName)] = filterValue
	return searchDict
	

def search():
#	searchDict = obtainSearchDict(CBoxDict)
#	searchResult = querySearch(searchDict)
	lbl4.config(text=str(searchResult))


button2=Button(window, text="Search", command=search)
button2.grid(column=1, row=rows, pady=10)
rows += 1
root.mainloop()