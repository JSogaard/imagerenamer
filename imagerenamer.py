#!/usr/bin/env python3
import os
import glob
import pendulum as pm
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
        cdate = pm.parse(str(exif["Image DateTime"]))
    return cdate


def find_ctime(path):
    """Finds the creation date AND time of an image file EXIF.
    Arguments: path
    Dependencies: ExifRead
    """
    with open(path, "rb") as file:
        exif = exifread.process_file(file)
        cdate = pm.parse(str(exif["Image DateTime"]))
    return cdate


def non_recursive(directory, file_exts=['NEF'], xmp_pairing=True):
    """Searches folder non-recursively for file with given
    file extensions, retrieves EXIF dates and renames files.
    If XMP pairing is enabled, rename them with same
    as paired file"""
    # Get list of image files in directory
    files = []
    exts = []

    if xmp_pairing:
        xmps = glob.glob(f"{directory}/*.xmp")
        for ext in file_exts:
            for file in glob.glob(f"{directory}/*.{ext}"):
                file_name = file.split('.')[:-1]
                # Add paired XMP to file property list
                if file_name in xmps:
                    xmp = file_name + '.xmp'
                    files.append([file, ext, xmp])
                else:
                    files.append([file, ext])

    else:
        for ext in file_exts:
            for file in glob.glob(f"{directory}/*.{ext}"):
                files.append([file, ext])


    # Add creation date to file property list
    for file in tqdm(files, desc='1/2 - Retrieving EXIF'):
        file.append(find_ctime(file[0]))

    # Sort file list by creation time at last index (ctime)
    files.sort(key=lambda x: x[-1])

    # Determining the left zero padding for the file name iterater
    padding = len(str(len(files)))

    # Loop through each image file and rename to YY-mm-dd - 000 format.
    for iter, img in tqdm(enumerate(files), desc='2/2 - Renaming files'):
        cdate = img[-1].to_date_string()
        file_ext = img[1]
        newpath = f"{directory}/{cdate} - {str(iter).zfill(padding)}.{file_ext}"
        os.rename(img[0], newpath)


def main():
    fire.Fire(non_recursive)

if __name__ == '__main__':
    main()