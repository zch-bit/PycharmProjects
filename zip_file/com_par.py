# Given two archive files (pick any kind: tar, zip, etc.), write a script to tell which files are in conflict, i.e., which files are present in both archives, but with different content.
# in a.tar: a.txt (contents "foo"), b.txt (contents "bar")
# in b.tar: a.txt (contents "baz"), c.txt (different from a.txt in a.tar, but ignored)
# output: a.txt

import glob
import hashlib
import os
import zipFile

zipfiles = ['tar1.zip', 'tar2.zip']

path1 = os.getcwd() + 'tar1'
path2 = os.getcwd() + 'tar1'


def unzip(files):
    for zip in files:
        zip = zipFile.ZipFile(zip)
        zip.extractall()
        zip.close()


def get_file_list(filename):
    file_list = glob.glob(os.getcwd() + filename)
    return file_list


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def compare(file1, file2):
    return md5(file1) == md5(file2)


if __name__ == "__main__":
    file_list_1 = get_file_list('1.zip')
    file_list_2 = get_file_list('2.zip')

    for file in file_list_1:
        for item in file_list_2:
            if file.split('/')[-1] == item.split('/')[-1] and \
                    compare(file, item):
                print file
