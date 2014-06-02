# Douglas Hawkey 3/1/14
#This program was made to provide an easy viewing of tab delimited files containing metatranscriptome data for students.

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter import ttk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(fill = None, expand = False)
        root.geometry("1000x500")
        self.createWidgets()


    def createWidgets(self):
        self.columns = ('Locus', 'E.C.', 'Metatranscriptome Hits', 'Reads/Nucleotide', 'Reads/Nucleotide/Depth', 
                        'MetaGenome Depth', 'COG', 'Product', 'Percent Identity', 'lineage', 'Scaffold', 'Locus Length',
                        'Start Coordinate', 'End Coordinate', 'cog ID', 'percent ID(cog)', 'alignment length(cog)',
                        'cog query start', 'cog query end', 'cog subj start', 'cog subj end', 'evalue(cog)',
                        'bit score(cog)', 'pfam ID', 'pfam % ID', 'pfman query start', 'pfam query end', 'pfam subj start',
                        'pfam subj end', 'pfam evalue', 'pfam bitscore', 'pfam alignment length')
        self.checkBool = tk.BooleanVar()
        self.comboStr = tk.StringVar()
        self.textStr = tk.StringVar()
		
        self.check = tk.Checkbutton(self, text = 'Clear Results', variable = self.checkBool, state = 'active') 
        self.textbox = tk.Text(self, width = 20, height = 1)
        self.button = tk.Button(self, text = "Search", command = self.Search)      
        self.exportButton = tk.Button(self, text = 'Export results to file', command = self.Export)
        
        self.comboBox = ttk.Combobox(self, textvariable= self.comboStr, state = 'readonly')
        self.comboBox.bind("<<ComboboxSelected>>", self.updateCombo)	
        self.comboBox['values'] = self.columns
        self.comboBox.current(0)
		
        self.textbox.grid(row = 1, column = 1)
        self.comboBox.grid(row=0, column=1)
        self.button.grid(row=0, column=3)
        self.check.grid(row = 0, column = 4)
        self.exportButton.grid(row = 0, column = 5)
        
        #The first display of data that contains all items
        self.frame = tk.Frame()
        self.tree = ttk.Treeview(self.frame, columns = self.columns, show = 'headings')
        for item in self.columns:
            self.tree.heading(item, text = item, anchor = 'center')
            self.tree.column(item, anchor = 'center')
        self.ysb = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.xsb = ttk.Scrollbar(self.frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll= self.ysb.set, xscroll= self.xsb.set)
		
      
		#The second display of data that shows the filtered results
        self.frame2 = tk.Frame()
        self.searchTree = ttk.Treeview(self.frame2, columns = self.columns, show = 'headings')
        for item in self.columns:
            self.searchTree.heading(item, text = item, anchor = 'center')
            self.searchTree.column(item, anchor = 'center')
        self.ysb2 = ttk.Scrollbar(self.frame2, orient='vertical', command=self.searchTree.yview)
        self.xsb2 = ttk.Scrollbar(self.frame2, orient='horizontal', command=self.searchTree.xview)
        self.searchTree.configure(yscroll= self.ysb2.set, xscroll= self.xsb2.set)
        
		#Positions all the the elements of the first treeview
        self.xsb.pack(side = 'bottom', fill = 'x', expand = False)
        self.ysb.pack(side = 'right', fill = 'y', expand = False)
        self.tree.pack(fill = 'both', expand = True)
        self.frame.pack(side ="top", expand = True, fill = 'x')
		
		#Positions all the the elements of the second treeview
        self.xsb2.pack(side = 'bottom', fill = 'x', expand = False)
        self.ysb2.pack(side = 'right', fill = 'y', expand = False)
        self.searchTree.pack(fill = 'both', expand = True)
        self.frame2.pack(side ="right", expand = True, fill = 'both')



    def updateCombo(self, event):
         self.comboStr = self.comboBox.get()
		
	#Finds any item that contains the given string and adds it to the list to be displayed on the second treeview		
    def Search(self,  item=''):
        if self.checkBool.get() == True:
            try:
                children = self.searchTree.get_children(item)
                for child in children:
                    self.searchTree.delete(child)
            except:
                print('list void')
        searchText = self.textbox.get('1.0', 'end')
        searchText = searchText.rstrip()
        comboIndex = self.comboBox.current()
        children = self.tree.get_children(item)
        for child in children:
            text = self.tree.item(child, 'values')
            selectedColumn = text[comboIndex]
            valueString = str(text)
            indexnum = selectedColumn.find(searchText)
            if indexnum is not -1:
                self.searchTree.insert('', 'end', iid= None, values = text)
        return True
				
	#Exports the results from the second treeview to a text file to allow for easy compilation of selected items
    def Export(self, item=''):
        saveFile = asksaveasfile(defaultextension = '.tab')
        try:
            children = self.searchTree.get_children(item)
            for child in children:
                valueTuple = self.searchTree.item(child, 'values')
                saveFile.write(valueTuple[0])
                for item in valueTuple[1:]:
                    saveFile.write( '\t' + item)
            saveFile.close()
        except:
            print()	

        
root = tk.Tk()
root.wm_title('Dataviewer')
app = Application(master=root)
filename = askopenfilename()  

#Loads the tab delimited file into the treeview     
with open(filename) as file:
    for line in file:
        colData = line.split('\t')
        colData[-1].rstrip()
        app.tree.insert('', 'end', iid= None, values = colData)
    del colData
    file.close()
	
app.textbox.focus_set()
app.mainloop()

