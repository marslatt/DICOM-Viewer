from tkinter import Frame, Canvas, Scrollbar, Label

# TODO Fix width of sidebars! Fix height of scrollbar after adding children!

class SideBar(Frame):
    def __init__(self, master, side="left", width=0):
        super().__init__(master)  

        # Main frame
        self.sidebar = Frame(master, bd=1, relief="raised", width=width) 
        self.sidebar.pack(side=side, fill="y", padx=5, pady=5) 

        # Scrolling 
        self.canvas = Canvas(self.sidebar)
        self.canvas.pack(side="left", fill="both", expand=True) 

        self.scrollbar = Scrollbar(self.sidebar, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y", expand=True) 

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Content
        self.content = Frame(self.canvas)
        self.content.pack_propagate(True)   
        self.canvas.create_window((0, 0), window=self.content, anchor="nw") 
 
    def addLabel(self, text="", image=None, name="", bindFunc=None): 
        label = Label(self.content, image=image, name=name, text=text, anchor="nw", wraplength=300)
        label.bind("<Button-1>", lambda e: bindFunc(e))  #  TODO TypeError: 'NoneType' object is not callable witth some images
        label.pack(padx=10, pady=10, anchor="nw")  

    def refresh(self):    
        # TODO Recalculate size! Scrollbar works if app window gets minimized/maximized/restored though
        pass
        #self.content.pack(fill="both", expand=True) 
        #self.scrollbar.pack(side="right", fill="y") 
        #self.canvas.pack(side="left", fill="y", expand=True) 
        #self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

    def clear(self):
        for c in filter(None, self.content.winfo_children()):
            c.destroy() 