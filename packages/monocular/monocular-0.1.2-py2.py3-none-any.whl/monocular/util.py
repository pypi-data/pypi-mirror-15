import re
import os
import imghdr
from PIL import Image as PILImage
from StringIO import StringIO

SUCCESS_CODES = [200, 201, 204]
VALID_TYPES = ['JPEG', 'PNG', 'BMP']

def validate_image(image):
    try:
        # Image is valid (return True) if it is a PIL Image of valid type, or an iamge file
        if isinstance(image, PILImage.Image) and image.format in VALID_TYPES:
            return True
        elif isinstance(image, str) and os.path.isfile(image):
            try:
                file_type = imghdr.what(image)
                if file_type and file_type.upper() in VALID_TYPES:
                    return True
                else:
                    return False
            except IOError:
                return False
        else:
            return False
    except ImportError:
        return False

def check_status(status):
    if status in SUCCESS_CODES:
        return True
    else:
        return False

def produce_request_image(image):
    if os.path.isfile(image):
        return open(image, 'rb')
    else:
        image_file = StringIO()
        image.save(image_file, image.format)
        image_file.seek(0)

    return image_file
