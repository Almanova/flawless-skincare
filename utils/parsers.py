from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser
from django.http.multipartparser import MultiPartParserError,\
    MultiPartParser as DjangoMultiPartParser


class MultipleFilesParser(BaseParser):
    media_type = 'multipart/form-data'

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        request = parser_context['request']
        encoding = parser_context.get('encoding',
                                      settings.DEFAULT_CHARSET)
        meta = request.META.copy()
        meta['CONTENT_TYPE'] = media_type
        upload_handlers = request.upload_handlers
        parsed = []
        try:
            parser = DjangoMultiPartParser(meta, stream,
                                           upload_handlers,
                                           encoding)
            _, files = parser.parse()
            for file in files.values():
                parsed.append({'image': file})
            return parsed
        except MultiPartParserError as e:
            raise ParseError(str(e))
