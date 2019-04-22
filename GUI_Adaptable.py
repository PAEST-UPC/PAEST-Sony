from tkinter import *
from tkinter.ttk import *
from QueryModule import *
from functools import partial
import ast

root=Tk()
myframe=Frame(root)#,width=1500, height=1200)

canvas=Canvas(myframe,width=600, height=500)
window=Frame(canvas, height=1300)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

canvas.create_window((0,0),window=window,anchor='nw')#,width=1500, height=1200)
window.bind("<Configure>")

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

#filterDict = ast.literal_eval(open("filterDict2.txt", "r").read())
filterDict = obtainFilterDictMT()
conversionDict = obtainConversionDict()
invConversionDict = obtainInvConversionDict()

for (tableName,filterName) in filterDict:
    labelsDict[(tableName,filterName)] = Label(window, text=filterName)
    values = []
    for tupled_value in filterDict[(tableName,filterName)]:
        for value in tupled_value:
            if (tableName,filterName,value) in conversionDict:
                values.append(conversionDict[(tableName,filterName,value)])
            else:
                values.append(value)
    
    CBoxDict[(tableName,filterName)] = Combobox(window,state="readonly", width=50, values=values)
    clearButtonDict[(tableName,filterName)] = Button(window, text='Clear', command=partial(clearCBox,CBoxDict[(tableName,filterName)]))

    labelsDict[(tableName,filterName)].grid(column=0, row=rows, pady=5)
    CBoxDict[(tableName,filterName)].grid(column=1, row=rows, pady=5, padx=10)
    clearButtonDict[(tableName,filterName)].grid(column=2, row=rows, pady=5)

    rows += 1

myframe.pack()
canvas.pack(side="left",expand = True)
myscrollbar.pack(side="right",fill="y")

canvas.configure(scrollregion=canvas.bbox("all"))

lbl4=Label(window, text='')
lbl4.grid(column=0, row=rows, pady=10)

def obtainSearchDict(CBoxDict):
    searchDict = {}
    for (tableName,filterName) in CBoxDict:

        filterValue = CBoxDict[(tableName,filterName)].get()
        if filterValue != '':
            if filterValue in invConversionDict:
                searchDict[(tableName,filterName)] = invConversionDict[filterValue]
            else:
                searchDict[(tableName,filterName)] = filterValue

    return searchDict
    

def search():
    searchDict = obtainSearchDict(CBoxDict)
    searchResult = querySearchMT(searchDict)
    print(searchResult)
#   lbl4.config(text=str(searchResult))


button2=Button(window, text="Search", command=search)
button2.grid(column=1, row=rows, pady=10)
rows += 1
root.mainloop()