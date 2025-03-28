from pydicom import dcmread
# from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.filereader import InvalidDicomError 
from dicom import DicomSeries, DicomDir  
from PIL import Image, ImageTk 
import os

# https://pydicom.github.io/pynetdicom/dev/examples/storage.html
# TODO https://pydicom.github.io/pynetdicom/dev/service_classes/storage_service_class.html#storage-sops

TMPDIR = os.path.join('.', 'data', 'tmp')

class DicomIO():
    '''
    DICOM IO Controller
    '''
    def __init__(self):       
        self.data = {}  # Dictionary containing all opened DicomSeries 
    
    def readData(self, path: tuple):
        self.readDICOM(path)  
        # TODO add readDICOMDIR(path)    

    def getData(self):
        return self.data.values()
    
    def clearData(self):
        self.data.clear() 
 
    def readDICOM(self, path: tuple):
        try:
            for file in path:
                dcm = dcmread(file)  # pydicom.dataset.FileDataset object
                sid = str(dcm.SeriesInstanceUID) 
                if not sid:
                    raise Exception("SeriesInstanceUID value is empty or invalid.") 
                if sid not in self.data:
                    self.data[sid] = DicomSeries(dcm)
                else:
                    self.data[sid].addImage(dcm) 
        except InvalidDicomError as e:  # non-dicom file
            print(e)   
        except AttributeError as e:  # no-SeriesInstanceUID kind of dicom file
            print(e)
        except Exception as e:
            print(e)
                   
    def removeDICOM(self, sid: str):
        self.data.remove(sid) 

    def readDICOMDIR(self, path: tuple):
        # TODO
        pass   
 
    def writeDICOM(self, path: tuple, ds: DicomSeries):  
        '''
        meta = FileDataset(path)
        meta.MediaStorageSOPClassUID = pd._storage_sopclass_uids.generate_uid().MRImageStorage
        meta.MediaStorageSOPInstanceUID = pd.uid.generate_uid()
        meta.TransferSyntaxUID = pd.uid.ExplicitVRLittleEndian

        dcm = FileDataset(path)
        dcm.file_meta = meta
        dcm.is_little_endian = True
        dcm.is_implicit_VR = False

        img = dcm.pixel_array.astype(float)
        imgId = str(dcm.SOPInstanceUID)
        dcm.pxlData[imgId] = img

        dcm.save_as(path)
        '''

        ''''
        ds.getImageData()
        new_image = Image.fromarray(array)
        new_image.save('new.png')
        '''
        # TODO
        pass
  
    def generatePreview(self, sid: str): 
        try:
            arr = self.data[sid].getPreviewImageData()
            img = Image.fromarray(arr)   
            if img.mode != 'RGB':
                img = img.convert('RGB')  # for PET, SPECT, etc.
            img = img.resize((150, 150))
            prev = ImageTk.PhotoImage(image=img)
            return prev
        except TypeError as e:
            print(e)          

    def generateImages(self, sid: str):
        images = []
        try:
            for img in self.data[sid].getImageData():
                img = Image.fromarray(img)
                if img.mode != 'RGB':
                    img = img.convert('RGB')  # for PET, SPECT, etc.
                images.append(img)
            return images
        except TypeError as e:
            print(e)            

    def generateTagData(self, sid: str):
        return self.data[sid].getStrTagData()





