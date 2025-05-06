from django.core.exceptions import ValidationError
from base.constants import (
    IMAGES_EXTENSIONS,
    MAX_DOC_SIZE,
    DOC_EXTENSIONS, ALLOWED_TAGS,
)
from base.utils.file_manager import get_extensions_and_type
from lxml import etree


class FileValidator:
    def __init__(self):
        self.max_doc_size = MAX_DOC_SIZE
        self.doc_extensions = DOC_EXTENSIONS
        self.image_extensions = IMAGES_EXTENSIONS

    def __call__(self, file):
        file_extension, mime_type = get_extensions_and_type(file.name)

        if "image" == mime_type:
            if file_extension not in self.image_extensions:
                raise ValidationError(
                    f'The wrong image format. Permissible formats:'
                    f' {", ".join(self.image_extensions)}')

        elif "text" == mime_type:
            if file_extension not in self.doc_extensions:
                raise ValidationError(
                    f'The wrong format of the document. Permissible formats:'
                    f' {", ".join(self.doc_extensions)} ')
            self.validate_text_file_size(file)
        else:
            raise ValidationError(
                "The wrong file format. Only images and text files are acceptable.")


    def validate_text_file_size(self, file):
        if file.size > self.max_doc_size:
            raise ValidationError(
                f"The size of the text file should not exceed {self.max_doc_size / 1024} KB.")

    def deconstruct(self):
        return (
            self.__class__.__module__ + '.' + self.__class__.__name__,
            [],
            {}
        )


class TextValidator:
    def __call__(self, text: str) -> None:
        text =  f"<div>{text}</div>"
        try:
            parser = etree.XMLParser(recover=False)
            root = etree.fromstring(text, parser=parser)
        except etree.XMLSyntaxError as e:
            raise ValidationError("Wrong XHTML")
        for elem in root.iter():
            if elem.tag == 'div':
                continue
            if elem.tag not in ALLOWED_TAGS:
                raise ValidationError(f"Impermissible HTML тег <{elem.tag}>.")
            allowed_attrs = ALLOWED_TAGS[elem.tag]
            for attr in elem.attrib:
                if attr not in allowed_attrs:
                    raise ValidationError(
                        f"An unacceptable attribute'{attr}' for tag <{elem.tag}>."
                    )


    def deconstruct(self):
        return (
            self.__class__.__module__ + '.' + self.__class__.__name__,
            [],
            {},
        )