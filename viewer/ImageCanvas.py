from tkinter import Canvas, Frame
from tkinter import LEFT, BOTH, NW
from PIL import Image, ImageTk 

class ImageCanvas(Frame):
    def __init__(self, master, imgArr, descr=""):
        super().__init__(master)     
        self.maxh = master.winfo_screenheight() - 200  # MAX image heigth 
        self.minw = 250  # MIN image width 
        self.descr = descr
        self.descrShow = True
        self.images = imgArr
        self.currimg = None
        self.index = 0
        self.display = Canvas(self, bd=0, highlightthickness=0, bg='#000')
        self.display.pack(side=LEFT, fill=BOTH, expand='y')
        self.bind("<Configure>", self.resize)
        self.bind_all("<MouseWheel>", self.reindex) 
        self.bind("<Key>", self.zoom)        
        self.focus_set() # Make sure the frame can receive focus

    def reset(self, images):
        self.images = images

    def description(self):
        self.descrShow = not self.descrShow
        self.redrawAll()

    def zoom(self, event): 
        if event.keysym == "equal" and (event.state & 0x0004):  # 0x0004 is the modifier for Ctrl            
            self.zoomin()
        if event.keysym == "minus" and (event.state & 0x0004): 
            self.zoomout()     

    def zoomin(self):
        h = self.currimg.height()
        if h < self.maxh:
            w = self.currimg.width()
            self.rw = int(w * 1.5)
            self.rh = int(h * 1.5)
            self.redrawAll()

    def zoomout(self):
        w = self.currimg.width()
        if w > self.minw:  
            h = self.currimg.height()
            self.rw = int(w / 1.5)
            self.rh = int(h / 1.5)
            self.redrawAll()

    def resize(self, event):
        w, h = self.images[0].size  # original image size
        ratio = min(event.width / w, event.height / h)
        self.rw = int(w * ratio)
        self.rh = int(h * ratio)
        self.redrawAll()

    def reindex(self, event=None):
        self.index = self.index + 1 if self.index < len(self.images) - 1 else 0
        self.redraw()  # TODO Error _tkinter.TclError: invalid command name ".!imagecanvas.!canvas"

    def redrawAll(self):
        resized = self.images[self.index].resize((self.rw, self.rh), Image.ADAPTIVE)
        self.currimg = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(0, 0, image=self.currimg, anchor=NW, tags="IMG")
        self.display.delete("DSC")
        if self.descrShow:
            self.display.create_text(self.rw + 200, 200, text=self.descr, fill="white", font=("Ariel", 11), tags="DSC")

    def redraw(self):
        resized = self.images[self.index].resize((self.rw, self.rh), Image.ADAPTIVE)
        self.currimg = ImageTk.PhotoImage(resized)
        self.display.delete("IMG") # TODO Error _tkinter.TclError: invalid command name ".!imagecanvas.!canvas"
        self.display.create_image(0, 0, image=self.currimg, anchor=NW, tags="IMG")

# TODO Error _tkinter.TclError: invalid command name ".!imagecanvas.!canvas"
# self.tk.call((self._w, 'delete') + args)