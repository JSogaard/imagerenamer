#!/usr/bin/env python3
import os
import glob
import datetime as dt
import exifread
import fire
from tqdm import tqdm


def find_cdate(path):
    """Finds the creation date (without time of day) of an image file from EXIF.
    Arguments: path
    Dependencies: ExifRead
    """
    with open(path, "rb") as file:
        exif = exifread.process_file(file)
        cdate = str(exif["Image DateTime"]).split(" ")[0].replace(":", "-")
    return cdate


def find_ctime(path):
    """Finds the creation date AND time of an image file EXIF.
    Arguments: path
    Dependencies: ExifRead
    """
    with open(path, "rb") as file:
        exif = exifread.process_file(file)
        cdate = str(exif["Image DateTime"])
    return cdate


def non_recursive(directory, file_exts=['.NEF']):
    # Get list of .NEF files in directory
    files = []
    for ext in file_exts:
        files.extend(glob.glob(f"{directory}/*{ext}"))

    # Create new list with tuplets of the path and time of creation for files.
    file_list = []
    for file in tqdm(files, desc='1/2 - Getting EXIF'):
        file_list.append((file, find_ctime(file)))

    # Create new list sorted by creation time at index 1
    file_list_sort = sorted(file_list, key=lambda x: x[1])

    # Loop through each image file and rename to YY-mm-dd - 000 format. Iterate up.
    for iter, img in tqdm(enumerate(file_list_sort), desc='2/2 - Renaming files'):
        cdate = img[1].split(' ')[0].replace(':', '-')
        file_ext = img[0].split('.')[-1]
        newpath = f"{directory}/{cdate} - {iter:03}.{file_ext}"
        os.rename(img[0], newpath)


def main():
    fire.Fire(non_recursive)

if __name__ == '__main__':
    main()