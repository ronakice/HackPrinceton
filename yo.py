from tkinter import *
from tkinter import Tk
fields = 'Keyword 1', 'Keyword 2', 'Keyword 3', 'Keyword 4', 'Starting date [YYYY-MM-DD]','End date [YYYY-MM-DD]'
l1=[]
Starting=""
Ending=""
def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print(field[0])
      l1.append(text.replace(" ","%20"))
      print('%s: "%s"' % (field, text))

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=30, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

if __name__ == '__main__':
	root = Tk()
	ents = makeform(root, fields)
	root.bind('<Return>', (lambda event, e=ents: fetch(e)))
	b1 = Button(root, text='Show', command=(lambda e=ents: fetch(e)))
	b1.pack(side=LEFT, padx=5, pady=5)
	b2 = Button(root, text='Quit', command=root.quit)
	b2.pack(side=LEFT, padx=5, pady=5)
	root.mainloop()

print(l1)
