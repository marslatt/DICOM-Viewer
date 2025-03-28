from pydicom.dataset import FileDataset 
from pydicom.sequence import Sequence
from pydicom.datadict import keyword_for_tag
from pydicom.pixels import pixel_array
from pydicom.multival import MultiValue
from monai.transforms import ToTensor #, Compose, Resize
import numpy as np 
# import re
 
class DicomSeries():
    '''
    Parse a DICOM Series dataset stored in accordance with the DICOM file format
    NB: All transformations and filters are applied to the whole series!
    '''
    def __init__(self, dcm: FileDataset):            
        # SeriesInstanceUID is the same within a series acquired in one scan. 
        self.serId = str(dcm.SeriesInstanceUID)
        self.imgData = {} 
        self.tagData = {}
        self.readTagData(dcm)         
        self.addImage(dcm) 
 
    # TODO Listed tags in tagData are currently not images-specific. Divide tags into sections.
    def readTagData(self, dcm: FileDataset):
        for tag, elem in dcm.items(): 
            key = keyword_for_tag(tag) or "UnknownTag"             
            if key not in ['PixelData', 'IconImageSequence']:
                name = f"{tag} {key}" 
                value = self.formatTagValue(dcm[tag].value)
                self.tagData[name] = value             
    
    def formatTagValue(self, value): 
        if isinstance(value, str):
          return value.strip()    
        elif isinstance(value, Sequence):
            strValue = '\n'.join(str(x) for x in value)
            # strValue = re.sub(r"\s+", "  ", strValue)
            return f"[\n{strValue.strip()}\n]"   

    def addImage(self, dcm: FileDataset):
        '''
        Add new image to the series
        '''  
        try:
            # Images in imgData are ordered by SOPInstanceUID, which should be unique for every image. 
            imgId = str(dcm.SOPInstanceUID) 
            imgArr = pixel_array(dcm)
    
            # Some DICOM images may have pixel values stored in a scaled format - using "rescale slope" and "rescale intercept" values.
            # Adjust with slope/intercept for displaying the pixel values correctly.
            slope = float(dcm.RescaleSlope) if 'RescaleSlope' in dcm else 1  # float
            intercept = float(dcm.RescaleIntercept) if 'RescaleIntercept' in dcm else 0 # float
            imgArr = slope * imgArr + intercept   

            # PhotometricInterpretation tag specifies how to interpret pixel data in terms of color or grayscale representation. 
            # MONOCHROME1: Negative pixel values = white (bright), positive pixel values = black (dark).
            # MONOCHROME2: Positive pixel values = white (bright), negative pixel values = black (dark).
            # RGB: For true color images
            # YBR_FULL or YBR_PARTIAL: For images in YCbCr color space (used for some color images)
            photometricIntr = dcm.PhotometricInterpretation 
            if photometricIntr == "MONOCHROME1":  
                imgArr = np.max(imgArr) - imgArr # Negative values indicate white

            # Windowing = Adjusting the Range of Pixel Intensities, applying "window center" and "window width" to calculate 
            # the displayed intensity range.       
            winCenter = dcm.WindowCenter if 'WindowCenter' in dcm else None
            winWidth = dcm.WindowWidth if 'WindowWidth' in dcm else None
            if winCenter and winWidth:
                winCenter = float(winCenter[0]) if isinstance(winCenter, MultiValue) else float(winCenter)
                winWidth = float(winWidth[0]) if isinstance(winWidth, MultiValue) else float(winWidth)
                lowerBound = winCenter - winWidth // 2
                upperBound = winCenter + winWidth // 2
                # Clip the pixel data to the window range
                imgArr = np.clip(imgArr, lowerBound, upperBound)
                # Normalize to 0-255 for display purposes
                imgArr = ((imgArr - lowerBound) / (upperBound - lowerBound) * 255).astype(np.uint16)  

            self.imgData[imgId] = imgArr 
        except Exception as e:
            print(e)    

    def getSerId(self):
        return self.serId 

    def getImageData(self):
        return self.imgData.values() 

    def getPreviewImageData(self):
        return next(iter(self.imgData.values()), None)

    def getTagData(self):
        return self.tagData.values()

    def getStrTagData(self):  # TODO Incorrect formating of values (bytes to utf-8, lists)
        return '\n\n'.join(f"{key}:\n{value}" for key, value in self.tagData.items())  
             
    def anonymizePatientData(self):
        self.tagData['PatientName'] = ''
        self.tagData['PatientID'] = ''
        self.tagData['PatientSex'] = ''
        self.tagData['PatientBirthDate'] = ''

    # TODO
    def transformToTensor(self): #, size: tuple):
        '''
        Convert an DICOM pixel_array into a PyTorch tensor, as expected by PyTorch-based models
        '''
        return {imgId: ToTensor(imgArr) for imgId, imgArr in self.imgData.items()} 
    
        # transform = Compose([ Resize(spatial_size=size), ToTensor() ])
        #return {imgId: transform(imgArr) for imgId, imgArr in self.imgData.items()}  
       
    

    

