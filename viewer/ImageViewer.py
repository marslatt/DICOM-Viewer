from PIL import Image, ImageFilter, ImageOps
from tkinter import Menubutton, Frame, Menu, PhotoImage, Label, Button
from tkinter import LEFT, TOP, X, FLAT, RAISED, BOTH, Y 
from tkinter import filedialog as fd 
from tkinter import ttk
from threading import Timer
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
        self.master.title("DICOM Viewer")
        self.master.state('zoomed')
        self.master.overrideredirect(False)
        self.master.bind("<Escape>", lambda event: self.master.quit())
        self.loadIcons()
        self.loadMenu()

        # DICOM images Preview bar
        self.previewbar = Frame(self.master, bd=1, relief=RAISED)
        self.previewbar.pack(side=LEFT, fill=Y)

    def loadIcons(self): 
        icons = ['addimg', 'expimg', 'editimg', 'zoomin', 'zoomout', 'histogram', 'help', 'details', 'animate', 'revert'] # 'anonymize'
        for icon in icons:
            self.icons[icon] = PhotoImage(file=os.path.join(ICONPATH, f"{icon}.png"))
 
    def loadMenu(self):
        # Main menu
        self.menubar = Frame(self.master, bd=1, relief=RAISED)
        self.menubar.pack(side=TOP, fill=X)

        # Open
        btnOpen = Menubutton(self.menubar, relief=FLAT, compound=TOP, text="Open", image=self.icons['addimg'])
        btnOpen.pack(side=LEFT, padx=0, pady=0)
        menuOpen = Menu(btnOpen, tearoff=0)
        menuOpen.add_command(label="Open DICOM Image", command=self.onOpenDICOM)
        menuOpen.add_command(label="Open ZIP File", command=self.onOpenZIP)
        btnOpen.config(menu=menuOpen)

        # Export
        btnExport = Menubutton(self.menubar, relief=FLAT, compound=TOP, text="Export", image=self.icons['expimg'])
        btnExport.pack(side=LEFT, padx=0, pady=0)
        menuExport = Menu(btnExport, tearoff=0)
        menuExport.add_command(label="Export Current Image", command=self.onExportImg)
        menuExport.add_command(label="Export Current Series", command=self.onExportSeries)
        btnExport.config(menu=menuExport)

        # Edit
        btnEdit = Menubutton(self.menubar, relief=FLAT, compound=TOP, text="Edit", image=self.icons['editimg'])
        btnEdit.pack(side=LEFT, padx=0, pady=0)
        menuEdit = Menu(btnEdit, tearoff=0)
        menuEdit.add_command(label='Sharpen', command=self.onSharpenImg)
        menuEdit.add_command(label='Smooth', command=self.onSmoothImg)
        menuEdit.add_separator()
        menuEdit.add_command(label="Rotate 90' CW", command=self.onRotateRight90Img)
        menuEdit.add_command(label="Rotate 180' CW", command=self.onRotateRight180Img)
        menuEdit.add_separator()
        menuEdit.add_command(label="Flip Horizontal", command=self.onFlipHorzImg)
        menuEdit.add_command(label="Flip Vertical", command=self.onFlipVertImg)
        btnEdit.config(menu=menuEdit)

        # Revert Image
        btnRevert = Button(self.menubar, relief=FLAT, compound=TOP, text="Revert", image=self.icons['revert'],
                           command=self.onRevertImg, pady=5)
        btnRevert.pack(side=LEFT, padx=0, pady=0)

        separator1 = ttk.Separator(self.menubar, orient='vertical')
        separator1.pack(side=LEFT, padx=2, pady=0, fill='y')

        # Zoom In
        btnZoomIn = Button(self.menubar, relief=FLAT, compound=TOP, text="Zoom In", image=self.icons['zoomin'],
                           command=self.onZoomIn, pady=5)
        btnZoomIn.pack(side=LEFT, padx=0, pady=0)

        # Zoom Out
        btnZoomOut = Button(self.menubar, relief=FLAT, compound=TOP, text="Zoom Out", image=self.icons['zoomout'],
                            command=self.onZoomOut, pady=5)
        btnZoomOut.pack(side=LEFT, padx=0, pady=0)

        # Information / Annotations
        btnInfo = Button(self.menubar, relief=FLAT, compound=TOP, text="Annotations", image=self.icons['details'],
                         command=self.onAnnotation, pady=5)
        btnInfo.pack(side=LEFT, padx=0, pady=0)

        separator2 = ttk.Separator(self.menubar, orient='vertical')
        separator2.pack(side=LEFT, padx=2, pady=0, fill='y')

        # Histogram Equalization
        btnHistogram = Button(self.menubar, relief=FLAT, compound=TOP, text="Equalize", image=self.icons['histogram'],
                              command=self.onEqualizeImg, pady=5)
        btnHistogram.pack(side=LEFT, padx=0, pady=0)

        # Animate
        btnAnimate = Button(self.menubar, relief=FLAT, compound=TOP, text="Animate", image=self.icons['animate'],
                            command=self.onAnimate, pady=5)
        btnAnimate.pack(side=LEFT, padx=0, pady=0)

        separator3 = ttk.Separator(self.menubar, orient='vertical')
        separator3.pack(side=LEFT, padx=2, pady=0, fill='y')

        # Help
        btnHelp = Button(self.menubar, relief=FLAT, compound=TOP, text="Help", image=self.icons['help'],
                         command=self.onDocumentation, pady=5)
        btnHelp.pack(side=LEFT, padx=0, pady=0)

    def reloadPreviewBar(self):
        # Clear all previously loaded images
        for c in filter(None, self.previewbar.winfo_children()):
            c.destroy()

        for ds in self.controller.getData():
            sid = ds.getSerId() 
            # Generate tkinter-friendly sid as name           
            name = sid.replace('.', "_") 
            # Create preview image
            self.previews.append(self.controller.generatePreview(sid))
            label = Label(self.previewbar, image=self.previews[-1], name=name)
            label.pack(side=TOP, padx=5, pady=5, fill='x')
            label.bind("<Button-1>", lambda e: self.onOpenImgCanvas(e))
            # Create image series
            self.images[sid] = self.controller.generateImages(sid)
            # Create series description
            self.descr[sid] = self.controller.generateAttributeData(sid)

    def onOpenImgCanvas(self, e):
        if self.canvas:
            self.canvas.destroy()
        # Get sid out of widget name 
        self.imgkey = str(e.widget)[str(e.widget).rfind('.') + 1:].replace('_', '.')
        self.canvas = ImageCanvas(self.master, self.images[self.imgkey], self.descr[self.imgkey])
        self.canvas.pack(fill=BOTH, expand=True)

    def onOpenDICOM(self):
        self.controller.clearData()
        files = fd.askopenfilenames(parent=self.master, title='Choose a DICOM File', filetypes=[("DICOM", ".dcm .DCM")])
        self.controller.readData(files)

        if self.canvas:
            self.canvas.destroy()
        self.reloadPreviewBar()

    def onOpenZIP(self):
        self.controller.clearData()
        file = fd.askopenfilename(parent=self.master, title='Choose a Zip File', filetypes=[("ZIP", ".zip .ZIP")])
        self.controller.readData(file)

        if self.canvas:
            self.canvas.destroy()
        self.reloadPreviewBar()

    def onExportImg(self):
        pass
        # TODO

    def onExportSeries(self):
        pass
        # self.controller.writeData(path, ds)
        # TODO

    def onSmoothImg(self):
        if self.imgkey:
            self.images[self.imgkey] = [i.filter(ImageFilter.GaussianBlur) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()

    def onSharpenImg(self):
        if self.imgkey:
            self.images[self.imgkey] = [i.filter(ImageFilter.SHARPEN) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()

    def onRotateRight90Img(self):
        if self.imgkey:
            self.images[self.imgkey] = [i.rotate(90, expand=1) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()

    def onRotateRight180Img(self):
        if self.imgkey:
            self.images[self.imgkey] = [i.rotate(180, expand=1) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()

    def onFlipHorzImg(self):
        if self.imgkey:
            self.images[self.imgkey] = [i.transpose(Image.FLIP_LEFT_RIGHT) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()

    def onFlipVertImg(self):
        if self.imgkey:
            self.images[self.imgkey] = [i.transpose(Image.FLIP_TOP_BOTTOM) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()

    def onRevertImg(self):
        if self.imgkey:
            self.images[self.imgkey] = self.controller.generateImages(self.imgkey)
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()

    def onZoomIn(self):
        if self.canvas:
            self.canvas.zoomin()

    def onZoomOut(self):
        if self.canvas:
            self.canvas.zoomout()

    def onAnnotation(self):
        if self.canvas:
            self.canvas.description()

    def onEqualizeImg(self):
        if self.imgkey:
            self.images[self.imgkey] = [ImageOps.autocontrast(i, cutoff=2, ignore=2) for i in self.images[self.imgkey]]
            self.images[self.imgkey] = [ImageOps.equalize(i, mask=None) for i in self.images[self.imgkey]]
            self.canvas.reset(self.images[self.imgkey])
            self.canvas.redraw()

    def onAnimate(self):
        ''' 
        Animate DCOM Series 
        '''
        class RepeatTimer(Timer):
            def run(self):
                try:
                    while not self.finished.wait(self.interval):
                        self.function()
                except Exception as e:
                    # User has selected another image thumbnail from preview bar
                    self.cancel()

        if self.canvas:
            timer = RepeatTimer(0.5, self.canvas.reindex)
            timer.start()

    def onDocumentation(self):
        webbrowser.open(DOCURL)

    def onExit(self):
        self.quit()