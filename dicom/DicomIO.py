import pydicom as pd
# from pd.dataset import FileDataset, FileMetaDataset
from pydicom.filereader import InvalidDicomError
from zipfile import ZipFile, BadZipfile 
from dicom import DicomSeries, DicomDir  
from PIL import Image, ImageTk
from typing import Dict
import zipfile
import os

# https://pydicom.github.io/pynetdicom/dev/examples/storage.html
# TODO https://pydicom.github.io/pynetdicom/dev/service_classes/storage_service_class.html#storage-sops

TMPDIR = os.path.join('.', 'data', 'tmp')

class DicomIO():
    '''
    DICOM IO Controller
    '''
    def __init__(self):       
        self.data: Dict[str, DicomSeries] = {}  # Dictionary containing all opened DicomSeries 
    
    def readData(self, path: str):
        self.readZIP(path) if zipfile.is_zipfile(str(path)) else self.readDICOM(path)
        # TODO add readDICOMDIR(path)    

    def getData(self):
        return self.data.values()
    
    def clearData(self):
        self.data.clear()
 
    def readDICOM(self, path: str):
        try:
            for file in path:
                dcm = pd.dcmread(file)  # pydicom.dataset.FileDataset object
                sid = str(dcm.SeriesInstanceUID)
                if sid not in self.data:
                    self.data[sid] = DicomSeries(dcm)
                self.data[sid].addImage(dcm) 
        except InvalidDicomError as e:  # non-dicom file
            print(e)   
        except AttributeError as e:  # no-SUID kind of dicom file
            print(e)
        except Exception as e:
            print(e)
                   
    def removeDICOM(self, sid: str):
        self.data.remove(sid) 

    def readDICOMDIR(self, path: str):
        # TODO
        pass   
           
    def readZIP(self, path: str): 
        try:
            with ZipFile(path, 'r') as zf:
                zf.extractall(TMPDIR)
                zippath = [os.path.join(TMPDIR, file) for file in os.listdir(TMPDIR)]            
            return self.readDICOM(zippath)
        except BadZipfile as e:
            print(e)                
        except Exception as e:
            print(e)
        finally:
            for file in zippath:
                os.remove(file)  # Clean up extracted files   

    def writeDICOM(self, path: str, ds: DicomSeries):
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

    def generateAttributeData(self, sid: str):
        return self.data[sid].getStrAttributeData()





