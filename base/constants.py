from collections import namedtuple

IMAGES_EXTENSIONS = ["png", "jpg ", "gif"]

ImageSize = namedtuple("ImageSize", ["width", "height"])
MAX_IMAGE_SIZE = ImageSize(320, 240)

DOC_EXTENSIONS = ["txt"]
MAX_DOC_SIZE = 100 * 1024



ALLOWED_TAGS = {
    'a': {'href', 'title'},
    'code': set(),
    'i': set(),
    'strong': set(),
}