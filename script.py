import os

# load openslide
# The path can also be read from a config file, etc.
OPENSLIDE_PATH = os.path.join(os.getcwd(), 'openslide-win64/bin')

import os
if hasattr(os, 'add_dll_directory'):
    # Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide

from openslide.deepzoom import DeepZoomGenerator
from openslide import OpenSlideUnsupportedFormatError


def get_dicom_image(filename):
    try:
        return get_slide(filename)
    except OpenSlideUnsupportedFormatError as e:
        print(f'{filename} is not WSI')


def get_slide(filename):
    slide = openslide.OpenSlide(filename)
    level = slide.level_count-1

    tiles = DeepZoomGenerator(slide, tile_size=256, overlap=0, limit_bounds=False)

    # Get the dimensions for this level
    level_dimension = slide.level_dimensions[level]

    # Read a region from the slide
    # Note that the region is defined at level 0 coordinates,
    # so we need to adjust if working with a different level
    region = slide.read_region((0, 0), level, level_dimension)

    prop = slide.properties

    return (slide, level_dimension, region, prop, tiles)

    # load the DICOM file with openslide for WSI(Whole Slide Images)
    # # this file often captured from scanner
    # slide = openslide.OpenSlide(filename)
    # # desired width is 1200, height is 1200
    # dicom_dict = {}
    # dicom_dict['filename'] = filename
    # dicom_dict['width'] = 1200
    # dicom_dict['height'] = 1200
    # thumbnail = slide.get_thumbnail(size=(dicom_dict['width'], dicom_dict['height']))
    # dicom_dict['data'] = np.array(thumbnail)
    # dicom_dict['type'] = 'wsi'
    # slide.get_thumbnail(size=(1200, 1200))
    # return dicom_dict