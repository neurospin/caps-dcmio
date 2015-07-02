# Diverse dicom reading functions to extract precise information

import dicom


def get_date_scan(path_to_dicom):
    """
    return session date as string
    """
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        value = dataset[0x0008, 0x0022].value
    except:
        logging.warning("WARNING: no AcquisitionDate field")
        value = '0'
    return value


def get_repetition_time(path_to_dicom):
    """
    return the repetition time as string
    """
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        value = dataset[0x0018, 0x0080].value
    except:
        logging.warning("WARNING: no RepetitionTime field")
        value = '0'
    return value


def get_echo_time(path_to_dicom):
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        value = dataset[0x0018, 0x0081].value
    except:
        logging.warning("WARNING: no EchoTime field in {0}".format(
            path_to_dicom))
        value = -1
    return value


def get_SOP_storage_type(path_to_dicom):
    """
    return True for Enhanced storage, False otherwise
    """
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        value = dataset[0x0008, 0x0016].value
        if "Enhanced" in str(value):
            return True
        else:
            return False
    except:
        logging.warning("WARNING: no 'SOPClassUID' field")
        return False


def get_Raw_Data_Run_Number(path_to_dicom):
    """
    return value field
    WARNING: private field: designed for GE scan (LONDON IOP centre)
    """
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        return int(dataset[0x0019, 0x10a2].value)
    except:
        print "WARNING: no 'RawDataRunNumber' field"
        return -1

def get_number_of_slices_philips(path_to_dicom):
    """ return value of "NumberOfSlicesMR" field
    """
    try:
        # run dcmdump and read number of slices inside. pydicom is unable
        # to extract the information
        temporary_text_file = os.path.join(os.path.dirname(path_to_dicom),
                                           "temp.txt")
        os.system("dcmdump {0} > {1}".format(path_to_dicom,
                                             temporary_text_file))
        # load text file
        buff = open(temporary_text_file, "r")
        for line in buff.readlines():
            if "StackNumberOfSlices" in line:
                temp = line
                break
        buff.close()
        # Remove temp file
        os.remove(temporary_text_file)
        # Now we have the line, remove spaces
        value = temp.replace(' ', '')
        # return the last 2 character as integer (we assume that there will
        # always be more than 9 slices)
        return int(value.split('#')[0][-2:])
    except:
        logging.warning("WARNING: no 'NumberOfSlicesMR' field")
        return 0

def get_sequence_number(path_to_dicom):
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        serie_number = dataset[0x0020, 0x0011].value
    except:
        logging.warning("WARNING: no 'SeriesNumber' field")
        serie_number = '0'
    return serie_number


def get_nb_slices(path_to_dicom):
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        volume_number = dataset[0x0020, 0x1002].value
    except:
        try:
            volume_number = dataset[0x2001, 0x1018].value
        except:
            logging.debug("WARNING: no 'ImagesInAcquisition' field")
            volume_number = -1
    return int(volume_number)


def get_nb_temporal_position(path_to_dicom):
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        volume_number = dataset[0x0020, 0x0105].value
    except:
        logging.warning("WARNING: no 'NumberOfTemporalPositions' field")
        volume_number = 0
    return int(volume_number)


def get_sequence_name(path_to_dicom):
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        serie_descr = dataset[0x0008, 0x103e].value
        serie_descr = serie_descr.replace(" ", "_")
    except:
        logging.warning("WARNING: no 'SerieDescription' field")
        serie_descr = "Unknown"
    return serie_descr


def get_protocol_name(path_to_dicom):
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        protocol_name = dataset[0x0018, 0x1030].value
        protocol_name = protocol_name.replace(" ", "_")
    except:
        logging.warning("WARNING: no 'ProtocolName' field")
        protocol_name = "Unknown"
    return protocol_name


def get_serie_serieInstanceUID(path_to_dicom):
    try:
        dataset = dicom.read_file(path_to_dicom, force=True)
        serie_UID = dataset[0x0020, 0x000e].value
        serie_UID = serie_UID.replace(" ", "_")
    except:
        print "WARNING: no 'SeriesInstanceUID' field"
        serie_UID = "Unknown"
    return serie_UID
