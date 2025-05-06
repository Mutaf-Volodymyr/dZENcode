import os

from PIL import Image, ImageSequence
import mimetypes
from base.constants import MAX_IMAGE_SIZE


def get_extensions_and_type(name) -> tuple[str, str] | None:
    mime_type, _ = mimetypes.guess_type(name)
    if not mime_type:
        return None
    _, ext = os.path.splitext(name)
    file_extension = ext.lower().lstrip('.')
    mime_type, _ = mime_type.split('/')
    return file_extension, mime_type


def check_image(file_path, file_extension):
    with Image.open(file_path) as img:
        if img.width <= MAX_IMAGE_SIZE.width and img.height <= MAX_IMAGE_SIZE.height:
            return
        if file_extension.lower() == 'gif':
            frames = []
            for frame in ImageSequence.Iterator(img):
                frame_copy = frame.copy()
                frame_copy.thumbnail((MAX_IMAGE_SIZE.width, MAX_IMAGE_SIZE.height))
                frames.append(frame_copy.convert("P", palette=Image.Palette.ADAPTIVE))
            if frames:
                frames[0].save(file_path, save_all=True, append_images=frames[1:], loop=0)

        else:
            img.thumbnail((MAX_IMAGE_SIZE.width, MAX_IMAGE_SIZE.height))
            img.save(file_path)
