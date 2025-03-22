from pydicom.dataset import FileDataset 
from typing import Dict
 
class DicomSeries():
    '''
    Parse a DICOM Series dataset stored in accordance with the DICOM file format
    NB: All transformations and filters are applied to the whole series!
    '''
    def __init__(self, dcm: FileDataset):            
        # NB: SeriesInstanceUID is the same within a series acquired in one scan. 
        self.serId = str(dcm.SeriesInstanceUID)
        # NB: Attributes in attribData are currently the same for all images in the series. # TODO
        self.attribData = self.readAttributeData(dcm) # TODO
        self.imgData = {}  
 
    def readAttributeData(self, dcm: FileDataset) -> Dict[str, str]:        
        '''
        attrib: Dict[str, str] = {} 
        for tag, elem in dcm.items(): 
            name = dcm.dir().get(tag)                
            if tag_name:
                attrib[name] = str(elem) 
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

    def getAttributeData(self):
        return self.attribData.values()

    def getStrAttributeData(self):
        return '\n\n'.join(f"{key}: {value}" for key, value in self.attribData.items()) 
  
    def anonymizePatientData(self):
        self.attribData['PatientName'] = ''
        self.attribData['PatientID'] = ''
        self.attribData['PatientSex'] = ''
        self.attribData['PatientBirthDate'] = ''


