import os

# load libvips
add_dll_dir = getattr(os, "add_dll_directory", None)
vipsbin = r"vips-dev-8.15\bin"  # LibVIPS binary dir
os.environ['PATH'] = vipsbin + ';' + os.environ['PATH']

import pyvips

from pathlib import Path

# convert wsi to dzi
def convert_wsi_to_dzi(src_file):
    """
    Convert WSI (DICOM) file to DZI format for OpenSeadragon
    Returns the path to the generated DZI file
    """
    src_path = Path(src_file)
    dzi_file = src_path.stem  # filename without extension
    
    try:
        # Load the DICOM file
        image = pyvips.Image.new_from_file(src_file, access='sequential')
        
        # Convert to DZI format
        image.dzsave(dzi_file, layout='dz')
        
        # Return the path to the DZI file
        dzi_path = f"{dzi_file}.dzi"
        return dzi_path
        
    except Exception as e:
        print(f"Error converting {src_file} to DZI: {e}")
        return None

def file_exists(file_path):
    """Check if a file exists"""
    return Path(file_path).exists()

def get_dzi_path_for_dcm(dcm_file):
    """Get the expected DZI file path for a given DCM file"""
    dcm_path = Path(dcm_file)
    dzi_file = f"{dcm_path.stem}.dzi"
    return dzi_file

def dzi_exists_for_dcm(dcm_file):
    """Check if DZI file already exists for the given DCM file"""
    dzi_path = get_dzi_path_for_dcm(dcm_file)
    return file_exists(dzi_path)