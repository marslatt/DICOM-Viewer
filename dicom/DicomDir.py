class DicomDir():
    '''
    Parse a DICOMDIR object stored in accordance with the DICOM file format
    '''
# TODO
pass


# DICOM Standard Browser: https://dicom.innolitics.com/ciods
# https://groups.google.com/g/comp.protocols.dicom/c/xh0ogPv31aI

'''
Common DICOM Fields

# Patient Information:

PatientName (0010,0010): The patient's name.

PatientID (0010,0020): Unique identifier for the patient.

PatientBirthDate (0010,0030): The patient's birth date.

PatientSex (0010,0040): The sex of the patient (M, F, O, etc.).

PatientAge (0010,1010): The age of the patient.

PatientWeight (0010,1030): The weight of the patient.

PatientAddress (0010,1040): The address of the patient.

PatientTelephoneNumbers (0010,2154): The phone number(s) of the patient.

# Study Information:

StudyInstanceUID (0020,000D): A unique identifier for the study.

StudyDate (0008,0020): The date the study was performed.

StudyTime (0008,0030): The time the study was performed.

StudyDescription (0008,1030): The description of the study.

StudyID (0020,0010): A unique identifier for the study.

AccessionNumber (0008,0050): A unique identifier for the study, used by the institution.

ReferringPhysicianName (0008,0090): The name of the physician who referred the patient for the study.

InstitutionName (0008,0080): The name of the institution where the study was performed.

StudyDate (0008,0020): Date of the study.

StudyTime (0008,0030): Time of the study.

StationName (0008,1010): The name of the station where the image was taken.

PerformingPhysicianName (0008,1050): The name of the physician who performed the study.

DeviceID (0032,1010): Unique identifier for the device that performed the study.

# Series Information:

SeriesInstanceUID (0020,000E): A unique identifier for the series.

SeriesNumber (0020,0011): The number of the series in the study.

SeriesDescription (0008,103E): The description of the series.

Modality (0008,0060): The type of imaging modality (e.g., CT, MRI, X-ray).

BodyPartExamined (0018,0015): The part of the body examined (e.g., head, chest).

ContrastBolusAgent (0018,1040): The name of the contrast agent used.

# Image Information:

SOPInstanceUID (0008,0018): A unique identifier for the specific image or instance.

InstanceNumber (0020,0013): A number identifying the instance within a series.

Rows (0028,0010): The number of rows in the image.

Columns (0028,0011): The number of columns in the image.

PixelSpacing (0028,0030): The spacing between pixels in the image (in millimeters).

ImagePositionPatient (0020,0032): The position of the image in the patient’s body (X, Y, Z).

ImageOrientationPatient (0020,0037): The orientation of the image relative to the patient.

SliceThickness (0018,0050): The thickness of the slice in the image.

StudyDate (0008,0020): The date the study was performed.

PatientPosition (0018,5100): The position of the patient during the scan (e.g., supine, prone).

# Technical Information:

Manufacturer (0008,0070): The manufacturer of the imaging equipment.

DeviceSerialNumber (0018,1000): The serial number of the imaging device.

SoftwareVersion (0018,1020): The software version of the imaging device.

SlicingThickness (0018,0050): The thickness of each slice in the 3D imaging.

ExposureTime (0018,1150): The time the imaging system exposed the sensor.

XRayTubeCurrent (0018,1151): The current used in the X-ray tube.

KVP (0018,0060): The peak kilovoltage used in the imaging process.

'''