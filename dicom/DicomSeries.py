from pydicom.dataset import FileDataset 
from typing import Dict
from pydicom.datadict import keyword_for_tag
 
class DicomSeries():
    '''
    Parse a DICOM Series dataset stored in accordance with the DICOM file format
    NB: All transformations and filters are applied to the whole series!
    '''
    def __init__(self, dcm: FileDataset):            
        # NB: SeriesInstanceUID is the same within a series acquired in one scan. 
        self.serId = str(dcm.SeriesInstanceUID)
        # NB: Attributes in attribData are currently the same for all images in the series. # TODO
        self.tagData = self.readTagData(dcm) # TODO
        self.imgData = {}  
 
    def readTagData(self, dcm: FileDataset) -> Dict[str, str]:   
        '''
        data: Dict[str, str] = {}    
        # NB: StudyInstanceUID: Unique identifier of the study or scanning session.        
        # data['StudyInstanceUID'] = str(dcm.StudyInstanceUID)  
        # data['StudyDescription'] = str(dcm.StudyDescription)
        data['SOPClassUID'] = str(dcm.SOPClassUID)        
        data['SeriesNumber'] = str(dcm.SeriesNumber)
        data['InstanceNumber'] = str(dcm.InstanceNumber)
        data['PatientName'] = str(dcm.PatientName)
        data['PatientID'] = str(dcm.PatientID)
        data['PatientSex'] = str(dcm.PatientSex)
        data['PatientBirthDate'] = str(dcm.PatientBirthDate)
        data['Modality'] = str(dcm.Modality)
        data['Manufacturer'] = str(dcm.Manufacturer)
        return data  
        '''     
        data: Dict[str, str] = {} 
        for tag, elem in dcm.items(): 
            name = keyword_for_tag(tag)                
            if name not in ['PixelData', 'IconImageSequence']:
                data[name] = str(elem.value).strip()  # TODO bytes to str: elem.value.decode('utf-8'))              
        return data  # TODO some elem.value contain list
            
    def addImage(self, dcm: FileDataset):
        '''
        Add new image to the series
        '''  
        # NB: Images in imgData are ordered by SOPInstanceUID, which should be unique for every image. 
        imgId = str(dcm.SOPInstanceUID)
        self.imgData[imgId] = dcm.pixel_array.astype(float)

    def getSerId(self):
        return self.serId
    
    def getImgId(self):
        return self.imgId

    def getImageData(self):
        return self.imgData.values() 

    def getPreviewImageData(self):
        return next(iter(self.imgData.values()), None)

    def getPreviewImageName(self):
        return self.ptnData['Modality']

    def getTagData(self):
        return self.tagData.values()

    def getStrTagData(self):  # TODO Incorrect formating of values (bytes to utf-8, lists)
        return '\n\n'.join(f"{key}: {value}" for key, value in self.tagData.items())  
             
    def anonymizePatientData(self):
        self.tagData['PatientName'] = ''
        self.tagData['PatientID'] = ''
        self.tagData['PatientSex'] = ''
        self.tagData['PatientBirthDate'] = ''


