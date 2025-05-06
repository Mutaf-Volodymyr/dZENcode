from django.core.exceptions import ValidationError
from PIL import Image
import mimetypes
from io import BytesIO
from base.constants import (
    IMAGES_EXTENSIONS,
    MAX_IMAGE_SIZE,
    MAX_DOC_SIZE,
    DOC_EXTENSIONS,
)


class FileValidator:
    def __init__(self):
        self.max_image_width, self.max_image_height = MAX_IMAGE_SIZE
        self.max_doc_size = MAX_DOC_SIZE
        self.doc_extensions = DOC_EXTENSIONS
        self.image_extensions = IMAGES_EXTENSIONS

    def __call__(self, file):
        mime_type, _ = mimetypes.guess_type(file.name)
        mime_type, file_extension = mime_type.split('/')

        if "image" == mime_type:
            if file_extension not in self.image_extensions:
                raise ValidationError(
                    f'The wrong image format. Permissible formats:'
                    f' {", ".join(self.image_extensions)}')
            self.validate_image(file)
        elif "text" == mime_type:
            if file_extension not in self.doc_extensions:
                raise ValidationError(
                    f'The wrong format of the document. Permissible formats:'
                    f' {", ".join(self.doc_extensions)} ')
            self.validate_text_file(file)
        else:
            raise ValidationError(
                "The wrong file format. Only images and text files are acceptable.")

    def validate_image(self, file):
        try:
            img = Image.open(file)
            if img.width > self.max_image_width or img.height > self.max_image_height:
                img.thumbnail((self.max_image_width, self.max_image_height))
                img_io = BytesIO()
                img.save(img_io, img.format)
                img_io.seek(0)
                file.file = img_io

        except Exception as e:
            raise ValidationError(f"Image processing error: {str(e)}")

    def validate_text_file(self, file):
        if file.size > self.max_doc_size:
            raise ValidationError(
                f"The size of the text file should not exceed {self.max_doc_size / 1024} KB.")

    def deconstruct(self):
        return (
            "base.custom_validators.FileValidator",  # Полный путь к классу
            [],
            {}
        )