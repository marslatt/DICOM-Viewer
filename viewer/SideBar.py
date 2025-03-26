from tkinter import Frame, Canvas, Scrollbar, Label

# TODO Fix aligning of text in content to the left instead of center! Fix height of canvas and scrollbar after adding children!

class SideBar(Frame):
    def __init__(self, master, side="left", width=0):
        super().__init__(master)
        self.master = master
        self.side = side
        self.width = width 
        # Sidebar frame
        self.sidebar = Frame(self.master, bd=1, relief="raised", width=self.width) 
        self.sidebar.pack(side=self.side, fill="y", padx=5, pady=5) 
        self.loadCanvas()       

    def loadCanvas(self):        
        self.canvas = Canvas(self.sidebar, width=self.width)
        self.canvas.pack(side="left", fill="both", expand=True)  # once packed, the height does not change after adding new elements
        self.scrollbar = Scrollbar(self.sidebar, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y", expand=True) 
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.content = Frame(self.canvas, width=self.width)
        self.canvas.create_window((0, 0), window=self.content, anchor="nw")     

    def clearContent(self): 
        for c in filter(None, self.content.winfo_children()):
            c.destroy()         
        self.canvas.configure(scrollregion=(0, 0, 1, 1)) # Reset scroll when there are no widgets in the canvas 
   
    def addLabel(self, text="", image=None, name="", bindFunc=None): 
        label = Label(self.content, image=image, name=name, text=text, anchor="nw", wraplength=300)
        if bindFunc:
            label.bind("<Button-1>", lambda e: bindFunc(e))  
        label.pack(padx=10, pady=10, anchor="nw")    
        # Update canvas scroll 
        self.canvas.update_idletasks()  # Ensure all widgets have been rendered before updating scroll
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))