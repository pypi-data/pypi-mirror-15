import hashlib
from distutils.filelist import findall
from zipfile import ZipFile

from os.path import relpath, dirname


def get_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as file_:
        batch_size = 4096
        chunk = file_.read(batch_size)
        while chunk:
            md5_hash.update(chunk)
            chunk = file_.read(batch_size)

        return hashlib.md5(file_.read()).hexdigest()


def zip_dir(path, zip_name=None):
    zip_name = zip_name or '{}.zip'.format(path)
    with ZipFile(zip_name, 'w') as zip_file:
        for file in findall(path):
            zip_file.write(file, relpath(file, dirname(path)))

