import datetime
import hashlib
import os


def _upload_path(tag):
    def _upload_path_tagged(instance, filename):
        now = datetime.datetime.now()
        path = os.path.join(now.strftime('%Y'), now.strftime('%m'),
                            now.strftime('%d'))
        hashed_filename = (hashlib.md5(filename +
                           str(now.microsecond)).hexdigest())
        __, extension = os.path.splitext(filename)
        return os.path.join(tag, path, hashed_filename + extension)
    return _upload_path_tagged
