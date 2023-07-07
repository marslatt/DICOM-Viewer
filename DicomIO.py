''' TODO Write documentaion here '''

import pydicom as pd
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.filereader import InvalidDicomError
from zipfile import ZipFile, BadZipfile
from os import sep, listdir, remove
from DicomSeries import DicomSeries


class DicomIO(object):

    TMPDIR = '.' + sep + 'data' + sep + 'tmp'

    @staticmethod
    def readDICOM(path):
        data = {}

        try:
            for file in path:
                dcm = pd.dcmread(file)  # pydicom.dataset.FileDataset object
                sid = str(dcm.SeriesInstanceUID)
                if sid in data:
                    data[sid].addImage(dcm)  # TODO Sort data[sid]?
                else:
                    data[sid] = DicomSeries(dcm)
        except InvalidDicomError as e:  # non-dicom file
            print(e)  # TODO Log errors
        except AttributeError as e:  # TODO no-SUID kind of dicom file
            print(e)
        except Exception as e:
            print(e)
        finally:
            return data

    @staticmethod
    def readZIP(path):
        data = {}
        zippath = []

        try:
            zf = ZipFile(path, 'r')
            zf.extractall(DicomIO.TMPDIR)
            for file in listdir(DicomIO.TMPDIR):
                zippath.append(DicomIO.TMPDIR + sep + file)
            data = DicomIO.readDICOM(zippath)
        except BadZipfile as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            zf.close()
            for file in listdir(DicomIO.TMPDIR):
                remove(DicomIO.TMPDIR + sep + file)
            return data

    @staticmethod
    def writeDICOM(path, ds):
        '''
        meta = FileDataset(path)
        # https://pydicom.github.io/pynetdicom/dev/examples/storage.html
        # The Storage Service Class defines an application-level class-of-service that facilitates the simple transfer
        # of information Instances (objects). It allows one DICOM AE to send images, waveforms, etc., to another.
        # TODO https://pydicom.github.io/pynetdicom/dev/service_classes/storage_service_class.html#storage-sops
        # meta.MediaStorageSOPClassUID = pd._storage_sopclass_uids.generate_uid().MRImageStorage
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
        pass
        

