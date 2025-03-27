from pydicom.dataset import FileDataset 
from typing import Dict
from pydicom.datadict import keyword_for_tag
from pydicom.pixels import pixel_array
from pydicom.multival import MultiValue
import numpy as np
 
class DicomSeries():
    '''
    Parse a DICOM Series dataset stored in accordance with the DICOM file format
    NB: All transformations and filters are applied to the whole series!
    '''
    def __init__(self, dcm: FileDataset):            
        # SeriesInstanceUID is the same within a series acquired in one scan. 
        self.serId = str(dcm.SeriesInstanceUID)
        # TODO Attributes in attribData are currently the same for all images in the series. 
        self.tagData = self.readTagData(dcm) # TODO
        self.imgData = {}  
 
    def readTagData(self, dcm: FileDataset) -> Dict[str, str]:        
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
        # Images in imgData are ordered by SOPInstanceUID, which should be unique for every image. 
        imgId = str(dcm.SOPInstanceUID) 
        imgArr = pixel_array(dcm)
 
        # Some DICOM images pixel values may be stored in a scaled format - using "rescale slope" and "rescale intercept" values.
        # Adjust with slope/intercept for displaying the pixel values correctly.
        slope = dcm.RescaleSlope if 'RescaleSlope' in dcm else 1
        intercept = dcm.RescaleIntercept if 'RescaleIntercept' in dcm else 0
        imgArr = slope * imgArr + intercept   

        # PhotometricInterpretation tag specifies how to interpret pixel data in terms of color or grayscale representation. 
        # MONOCHROME1: Negative pixel values = white (bright), positive pixel values = black (dark).
        # MONOCHROME2: Positive pixel values = white (bright), negative pixel values = black (dark).
        # RGB: For true color images
        # YBR_FULL or YBR_PARTIAL: For images in YCbCr color space (used for some color images)
        photometricIntr = dcm.PhotometricInterpretation 
        if photometricIntr == "MONOCHROME1":  
            imgArr = np.max(imgArr) - imgArr # Negative values indicate white

        # Windowing = Adjusting the Range of Pixel Intensities, applying a "window center" and "window width" to calculate 
        # the displayed intensity range.       
        winCenter = dcm.get("WindowCenter") if 'WindowCenter' in dcm else None
        winWidth = dcm.get("WindowWidth") if 'WindowWidth' in dcm else None
        if winCenter and winWidth:
            winCenter = winCenter[0] if isinstance(winCenter, MultiValue) else winCenter
            winWidth = winWidth[0] if isinstance(winWidth, MultiValue) else winWidth
            lowerBound = winCenter - winWidth // 2
            upperBound = winCenter + winWidth // 2
            # Clip the pixel data to the window range
            imgArr = np.clip(imgArr, lowerBound, upperBound)
            # Normalize to 0-255 for display purposes
            imgArr = ((imgArr - lowerBound) / (upperBound - lowerBound) * 255).astype(np.uint16)  

        self.imgData[imgId] = imgArr 

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


