from os import sep
from DicomIO import DicomIO
from DicomSeries import DicomSeries
from PIL import Image, ImageTk
import zipfile


class DicomController(object):

    def __init__(self):
        super().__init__()
        # Dictionary containing all opened DicomSeries
        self.data = {}

    def readData(self, path):
        self.data = DicomIO.readZIP(path) if zipfile.is_zipfile(str(path)) else DicomIO.readDICOM(path)

    def writeData(self, ds, path):
        self.data = DicomIO.writeDICOM(path, ds)

    def generatePreview(self, sid):
        prev = None

        try:
            arr = self.data[sid].getPreviewImageData()
            img = Image.fromarray(arr)  # TypeError: Cannot handle this data type
            if img.mode != 'RGB':
                img = img.convert('RGB')  # for PET, SPECT, etc.
            img = img.resize((150, 150))
            prev = ImageTk.PhotoImage(image=img)
        except TypeError as e:
            print(e)
        finally:
            return prev

    def generateImages(self, sid):
        images = []

        try:
            for img in self.data[sid].getImageData():
                img = Image.fromarray(img)
                if img.mode != 'RGB':
                    img = img.convert('RGB')  # for PET, SPECT, etc.
                images.append(img)
        except TypeError as e:
            print(e)
        finally:
            return images

    def generateAttributeData(self, sid):
        return self.data[sid].getStrAttributeData()

    def removeDICOM(self, ds):
        self.data.remove(ds)

    def getData(self):
        return self.data.values()

    def clearData(self):
        self.data.clear()
