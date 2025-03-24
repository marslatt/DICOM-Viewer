from PIL import Image, ImageOps
from tkinter import Frame, PhotoImage, Label, Button, Canvas
from tkinter import LEFT, RIGHT, TOP, X, FLAT, RAISED, BOTH, Y 
from tkinter import filedialog as fd 
from tkinter import ttk 
from dicom import DicomIO
from viewer import ImageCanvas
import webbrowser
import os

DOCPATH = os.path.join(os.getcwd(), "data", "docs", "Documentation.pdf")
DOCURL = f"file:///{DOCPATH}"
ICONPATH = os.path.join(".", "viewer", "icons")

class ImageViewer(Frame):
    '''
    Main app view
    '''
    def __init__(self,  master=None):
        super().__init__(master)
        self.master = master
        self.controller = DicomIO()
        self.icons = {}
        self.previews = []
        self.images = {}
        self.descr = {}
        self.canvas = None
        self.imgkey = None 
        self.initGUI()

    def initGUI(self):
        self.master.title("DICOM AI Lab")
        self.master.state('zoomed')
        self.master.overrideredirect(False)
        self.master.bind("<Escape>", lambda event: self.master.quit())
        self.loadIcons()
        self.loadMenu()

        # Zoom in/out
        self.bind("<Key>", self.onKeyPress)        
        self.focus_set() # Make sure the frame can receive focus

        # Right side bar
        self.rightBar = Frame(self.master, bd=1, relief=RAISED, width=360)
        self.rightBar.pack(side=RIGHT, fill=Y)

        # Left side bar
        self.leftBar = Frame(self.master, bd=1, relief=RAISED, width=160)
        self.leftBar.pack(side=LEFT, fill=Y)

        # DICOM images Preview bar
        self.previewBar = Frame(self.leftBar, bd=1, relief=RAISED, width=160)
        self.previewBar.pack(side=LEFT, fill=Y)  

    def onKeyPress(self, event):
        if event.keysym == "equal" and (event.state & 0x0004):  # 0x0004 is the modifier for Ctrl
            if self.canvas:
                self.canvas.zoomin()
        if event.keysym == "minus" and (event.state & 0x0004): 
            if self.canvas:
                self.canvas.zoomout() 

    def loadIcons(self): 
        icons = ['openseries', 'exportimg',                  
                 'rotate', 'flipvert', 'fliphoriz', 'histogram', 'revert',
                 'analyze', 'segmentation', 'noisereduct', 'edgedetect',
                 'help' ]    
        self.icons = {icon: PhotoImage(file=os.path.join(ICONPATH, f"{icon}.png")) for icon in icons}
 
    def loadMenu(self):
        # Main menu
        self.menubar = Frame(self.master, bd=1, relief=RAISED)
        self.menubar.pack(side=TOP, fill=X)

        button_data = [
            ("Open", 'openseries', self.onOpen),  # Open Series
            ("Export", 'exportimg', self.onExport),  # Export Image
            ("Rotate", 'rotate', self.onRotate),  # Rotate 90 CW
            ("Flip Vertical", 'flipvert', self.onFlipVertical),  # Flip Vertical
            ("Flip Horizontal", 'fliphoriz', self.onFlipHorizontal),  # Flip Horizontal
            ("Equalize", 'histogram', self.onEqualize),  # Equalize Histogram
            ("Revert", 'revert', self.onRevert),  # Revert Changes 
            ("LLM Analysis", 'analyze', self.onAnalyze),  # Analyze with LLM  
            ("Segmentation", 'segmentation', self.onSegment),  # Segmentation
            ("Denoise", 'noisereduct', self.onNoiseReduct),  # Noise Reduction
            ("Extract Edges", 'edgedetect', self.onEdgeDetect),  # Edge Detection
            ("Help", 'help', self.onDocumentation)  # Open Documentation
        ]

        for text, icon, command in button_data:
            button = Button(self.menubar, relief=FLAT, compound=TOP, text=text, image=self.icons[icon], command=command, pady=5) 
            button.pack(side=LEFT, padx=0, pady=0)

            if text in ["Export", "Revert", "Extract Edges"]:
                # Add separator after buttons (but not for the last one)
                separator = ttk.Separator(self.menubar, orient='vertical')
                separator.pack(side=LEFT, padx=2, pady=0, fill='y')

    def reloadPreviewBar(self):
        # Clear all previously loaded images
        for c in filter(None, self.previewBar.winfo_children()):
            c.destroy()

        for ds in self.controller.getData():
            sid = ds.getSerId() 
            # Generate tkinter-friendly name for sid           
            name = sid.replace('.', "_") 
            # Create preview image
            self.previews.append(self.controller.generatePreview(sid))
            label = Label(self.previewBar, image=self.previews[-1], name=name)
            label.pack(side=TOP, padx=5, pady=5, fill='x')
            label.bind("<Button-1>", lambda e: self.onOpenImgCanvas(e))
            # Create image series
            self.images[sid] = self.controller.generateImages(sid)
            # Create description
            self.descr[sid] = self.controller.generateAttributeData(sid)

    def onOpenImgCanvas(self, e):
        if self.canvas:
            self.canvas.destroy()
        # Get sid out of widget name 
        self.imgkey = str(e.widget)[str(e.widget).rfind('.') + 1:].replace('_', '.')
        self.canvas = ImageCanvas(self.master, self.images[self.imgkey], "") # self.descr[self.imgkey])
        self.canvas.pack(fill=BOTH, expand=True)
        self.onShowDICOMData(self.imgkey)

    def onOpen(self):
        self.controller.clearData()
        files = fd.askopenfilenames(
            parent=self.master,
            title='Choose a DICOM File',
            filetypes=[("Files", "*.dcm;*.DCM")]
        )
        self.controller.readData(files)
        
        for c in filter(None, self.rightBar.winfo_children()):  # TODO
            c.destroy()
        if self.canvas:
            self.canvas.destroy()
        self.reloadPreviewBar()
 
    def onExport(self):
        pass
        # TODO self.controller.writeData(path, ds) 
 
    def onRotate(self):
        if self.imgkey:
            self.images[self.imgkey] = [i.rotate(90, expand=1) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()

    def onFlipHorizontal(self):
        if self.imgkey:
            self.images[self.imgkey] = [i.transpose(Image.FLIP_LEFT_RIGHT) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()

    def onFlipVertical(self):
        if self.imgkey:
            self.images[self.imgkey] = [i.transpose(Image.FLIP_TOP_BOTTOM) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()
            
    def onRevert(self):
        if self.imgkey:
            self.images[self.imgkey] = self.controller.generateImages(self.imgkey)
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()  
    
    def onShowDICOMData(self, sid):  # TODO
        # Clear all previously loaded elements
        for c in filter(None, self.rightBar.winfo_children()):
            c.destroy()

        # Create a Canvas widget
        canvas = Canvas(self.rightBar, width=350, height=500)
        canvas.pack(side=TOP, padx=5, pady=5, fill='both', expand=True) 
        canvas.create_text(175, 150, text=self.descr[sid], font=("Arial", 10), fill="black", anchor="center")
 
    def onAnalyze(self):
        if self.imgkey:
            # TODO Analyze with LLM the content of self.images[self.imgkey] 
            pass              
 
    def onEqualize(self):
        # TODO https://pdf.sciencedirectassets.com/280203/1-s2.0-S1877050919X00198/1-s2.0-S1877050919321519
        # Possible aproach with OpenCV
        # Draw new image in separate ImageCanvas tab  
        if self.imgkey:
            self.images[self.imgkey] = [ImageOps.autocontrast(i, cutoff=2, ignore=2) for i in self.images[self.imgkey]]
            self.images[self.imgkey] = [ImageOps.equalize(i, mask=None) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()    

    def onSegment(self):
        if self.imgkey:
            # TODO Create segmentation of self.images[self.imgkey] and open it in separate ImageCanvas tab 
            # self.canvas.reset(self.images[self.imgkey])
            # self.canvas.redraw()     
            pass    

    def onNoiseReduct(self):
        if self.imgkey:
            # TODO Do noise reduction on self.images[self.imgkey] and open it in separate ImageCanvas tab 
            # self.canvas.reset(self.images[self.imgkey])
            # self.canvas.redraw()     
            pass     

    def onEdgeDetect(self):
        if self.imgkey:
            # TODO Do edge detection on self.images[self.imgkey] and open it in separate ImageCanvas tab 
            # self.canvas.reset(self.images[self.imgkey])
            # self.canvas.redraw()     
            pass   
                 
    def onDocumentation(self):
        webbrowser.open(DOCURL)

    def onExit(self):
        self.quit()