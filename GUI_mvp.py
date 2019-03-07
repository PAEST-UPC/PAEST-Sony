from tkinter import *
from tkinter.ttk import *
window=Tk()

window.title("Searcher Window")
# window.geometry('350x400') # Mida per defecte, si no es posa s'obre una finestra per a que es vegi tot

lbl=Label(window, text="Escull: ")
lbl.grid(column=0,row=0)
lbl2=Label(window, text="Audio Language: ")
lbl3=Label(window, text="Subtitles Language")
lbl4=Label(window, text="Els resultats de la cerca son: ")
# lst=['Audio Language', 'Subtitles Language', 'Video Quality']
# lstbox=Listbox(window)
# lst2=['Country','File size','Date']
# lstbox2=Listbox(window)
# 
# for item in lst:
# 	lstbox.insert(END,item)
# 	
# for item in lst2:
# 	lstbox2.insert(0,item)
# 	
# txtbox=Entry(window)


#chk_state = BooleanVar()
#chk_state.set(True) #set check state
#chk = Checkbutton(window, text='Checkbutton', var=chk_state)
#chk.grid(column=1, row=1)

desplegable=Combobox(window,state="readonly")
desplegable['values']=("--", "Català", "Español de España no Latino")
desplegable.current(0)

desplegable2=Combobox(window,state="readonly")
desplegable2['values']=desplegable['values']
desplegable2.current(0)

def desplega():
	lbl.configure(text="Els desplegables son: ")
	lbl2.grid(column=0, row=1, padx=5)
	lbl3.grid(column=0, row=2, padx=5)
	desplegable.grid(column=1,row=1, sticky='news', pady=5)
	desplegable2.grid(column=1,row=2)

def cerca():
	lbl4.grid(column=0, row=3, pady=20)
	
# rad1 = Radiobutton(window,text='Llista', value=1, command=llista)
# rad2 = Radiobutton(window,text='Desplegable', value=2, command=desplega)
# rad3 = Radiobutton(window,text='Textbox', value=3, command=textbx)

# rad1.grid(column=1,row=0)
# rad2.grid(column=2,row=0)
# rad3.grid(column=3,row=0)

button1=Button(window, text='Mostra els desplegables', command=desplega)
button1.grid(column=1, row=0, sticky='news')
button2=Button(window, text='Cerca', command=cerca)
button2.grid(column=1, row=3)
window.mainloop()