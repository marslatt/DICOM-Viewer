from PIL import Image, ImageOps
from tkinter import Frame, PhotoImage, Button 
from tkinter import LEFT, TOP, X, FLAT, RAISED, BOTH, Y 
from tkinter import filedialog as fd 
from tkinter import ttk 
from dicom import DicomIO
from viewer import ImageCanvas
from viewer.SideBar import SideBar
import webbrowser
import os

DOCPATH = os.path.join(os.getcwd(), "data", "docs", "Documentation.pdf")
DOCURL = f"file:///{DOCPATH}"
ICONPATH = os.path.join(".", "viewer", "icons")

class MainFrame(Frame):
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
        self.loadUI()
 
    def loadUI(self):
        self.master.title("DICOM AI Lab")
        self.master.state('zoomed')
        self.master.overrideredirect(False)
        self.master.bind("<Escape>", lambda event: self.master.quit())
        self.loadIcons()
        self.loadMenu()
        self.loadSideBars()  

    def loadSideBars(self):
        self.previewBar = SideBar(self.master, side="left", width=180)
        self.tagBar = SideBar(self.master, side="right", width=350)   

    def loadIcons(self): 
        icons = ['openseries', 'exportimg', 'anonymize',                   
                 'rotate', 'flipvert', 'fliphoriz', 'histogram', 'revert',
                 'analyze', 'segmentation', 'noisereduct', 'edgedetect',
                 'help' ]    
        self.icons = {icon: PhotoImage(file=os.path.join(ICONPATH, f"{icon}.png")) for icon in icons}
 
    def loadMenu(self): 
        self.menubar = Frame(self.master, bd=1, relief=RAISED)
        self.menubar.pack(side=TOP, fill=X)

        button_data = [
            ("Open", 'openseries', self.onOpen),  # Open Series
            ("Export", 'exportimg', self.onExport),  # Export Image
            ("Anonymize", 'anonymize', self.onAnonymize),  # Export Image
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
            button.pack(side="left", padx=0, pady=0)

            if text in ["Anonymize", "Revert", "Extract Edges"]: 
                separator = ttk.Separator(self.menubar, orient='vertical')
                separator.pack(side=LEFT, padx=2, pady=0, fill='y')

    def reloadPreviewBar(self):
        self.previewBar.clear()
        # Add list of preview images
        for ds in self.controller.getData():
            sid = ds.getSerId() 
            # Generate tkinter-friendly name from sid           
            name = sid.replace('.', "_") 
            # Create and add preview
            self.previews.append(self.controller.generatePreview(sid))
            self.previewBar.addLabel(image=self.previews[-1], name=name, bindFunc=self.showImgCanvas) 
            # Create image series
            self.images[sid] = self.controller.generateImages(sid)
            # Create description
            self.descr[sid] = self.controller.generateTagData(sid)              
        # self.previewBar.refresh()   # TODO Does NOT recalculate size after adding children!

    def showImgCanvas(self, e):
        if self.canvas:
            self.canvas.destroy()
        # Get sid out of widget name 
        self.imgkey = str(e.widget)[str(e.widget).rfind('.') + 1:].replace('_', '.')
        self.canvas = ImageCanvas(self.master, self.images[self.imgkey]) # , self.descr[self.imgkey]) # TODO ADD img specific descr
        self.canvas.pack(fill=BOTH, expand=True)
        self.showImgTags(self.imgkey)  
        
    def showImgTags(self, sid): 
        self.tagBar.clear()  
        self.tagBar.addLabel(text=self.descr[sid])
        # self.tagBar.refresh()  # TODO Does NOT recalculate size after adding children!
 
    def onOpen(self):
        self.controller.clearData()
        files = fd.askopenfilenames(
            parent=self.master,
            title='Choose a DICOM File',
            filetypes=[("Files", "*.dcm;*.DCM")]
        )
        if files:
            self.controller.readData(files)
            # Clear view
            self.tagBar.clear()
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
        self.flip(Image.FLIP_LEFT_RIGHT)  

    def onFlipVertical(self):
        self.flip(Image.FLIP_TOP_BOTTOM) 

    def flip(self, direction):
        if self.imgkey:
            self.images[self.imgkey] = [i.transpose(direction) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()
            
    def onRevert(self):
        if self.imgkey:
            self.images[self.imgkey] = self.controller.generateImages(self.imgkey)
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()  
 
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
            # TODO Create segmentation result img of self.images[self.imgkey], add to previewbar and open in ImgCanvas  
            pass    

    def onNoiseReduct(self):
        if self.imgkey:
            # TODO Create noise reduction result img of self.images[self.imgkey], add to previewbar and open in ImgCanvas 
            pass     

    def onEdgeDetect(self):
        if self.imgkey:
            # TODO Create edge detection result img of self.images[self.imgkey], add to previewbar and open in ImgCanvas 
            pass   

    def onAnonymize(self):
        if self.imgkey: 
            pass     

    def onDocumentation(self):
        webbrowser.open(DOCURL)

    def onExit(self):
        self.quit()
