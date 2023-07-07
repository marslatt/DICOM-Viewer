'''
DICOM Standard Browser: https://dicom.innolitics.com/ciods
https://groups.google.com/g/comp.protocols.dicom/c/xh0ogPv31aI
'''


class DicomSeries(object):

    def __init__(self, dcm):
        super().__init__()
        # NB: May also include StudyInstanceUID - Identifier of the study or scanning session.
        # NB: SeriesInstanceUID is the same within a series acquired in one scan.
        self.serId = str(dcm.SeriesInstanceUID)
        self.pxlData = {}
        self.attribData = {}

        # NB: Images in pxlData and pxlDataMod are ordered by SOPInstanceUID, which should be unique for any image.
        self.addImage(dcm)
        self.setAttributeData(dcm)

    def getSerId(self):
        return self.serId

    def setSerId(self, sid):
        self.serId = sid

    def getImageData(self):
        return self.pxlData.values()

    def addImage(self, dcm):
        img = dcm.pixel_array.astype(float)
        imgId = str(dcm.SOPInstanceUID)
        self.pxlData[imgId] = img

    def getPreviewImageData(self):
        return list(self.pxlData.values())[0]

    def getPreviewImageName(self):
        return self.ptnData['Modality']

    def anonymizePatientData(self):
        self.attribData['PatientName'] = ''
        self.attribData['PatientID'] = ''
        self.attribData['PatientSex'] = ''
        self.attribData['PatientBirthDate'] = ''

    def getAttributeData(self):
        return self.attribData.values()

    def setAttributeData(self, dcm):
        # TODO AttributeError: 'FileDataset' object has no attribute 'MediaStorageSOPClassUID'
        # self.attribData['MediaStorageSOPClassUID'] = str(dcm.MediaStorageSOPClassUID)
        # TODO AttributeError: 'FileDataset' object has no attribute 'MediaStorageSOPInstanceUID'
        # self.attribData['MediaStorageSOPInstanceUID'] = str(dcm.MediaStorageSOPInstanceUID)
        # TODO AttributeError: 'FileDataset' object has no attribute 'TransferSyntaxUID'
        # self.attribData['TransferSyntaxUID'] = str(dcm.TransferSyntaxUID)
        self.attribData['SOPClassUID'] = str(dcm.SOPClassUID)
        self.attribData['InstanceNumber'] = str(dcm.InstanceNumber)
        self.attribData['PatientName'] = str(dcm.PatientName)
        self.attribData['PatientID'] = str(dcm.PatientID)
        self.attribData['PatientSex'] = str(dcm.PatientSex)
        self.attribData['PatientBirthDate'] = str(dcm.PatientBirthDate)
        # TODO AttributeError: 'FileDataset' object has no attribute 'AcquisitionDate'
        # self.ptnData['AcquisitionDate'] = str(dcm.AcquisitionDate)
        # TODO  AttributeError: 'FileDataset' object has no attribute 'AcquisitionNumber'
        # self.ptnData['AcquisitionNumber'] = str(dcm.AcquisitionNumber)
        self.attribData['Modality'] = str(dcm.Modality)
        self.attribData['Manufacturer'] = str(dcm.Manufacturer)
        # self.attribData['StudyDescription'] = str(dcm.StudyDescription)
        self.attribData['SeriesNumber'] = str(dcm.SeriesNumber)

        for element in dcm:  # TODO | TEST
            print(element)

    def getStrAttributeData(self):
        txt = ''
        for i in self.attribData:
            txt += i + ": " + self.attribData[i] + '\n\n'
        return txt
