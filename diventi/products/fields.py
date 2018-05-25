from django.db.models.fields.files import FileField, FieldFile
from django.http import HttpResponse
from django.core.files.storage import get_storage_class


class ProtectedFileField(FileField):

    # attr_class = ProtectedFieldFile

    """
    A FileField that gives the 'private' ACL to the files it uploads to S3, instead of the default ACL.
    """
    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, **kwargs):
        if storage is None:
            storage = get_storage_class()(acl='private')
        super(ProtectedFileField, self).__init__(verbose_name=verbose_name,
                name=name, upload_to=upload_to, storage=storage, **kwargs)