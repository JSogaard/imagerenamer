#!/usr/bin/env python3
import os
import glob
import pendulum as pm
import exifread
import click
from tqdm import tqdm
from dataclasses import dataclass


def find_ctime(path):
    """Finds the creation date AND time of an image file EXIF.
    Arguments: path
    Dependencies: ExifRead
    """
    with open(path, "rb") as file:
        exif = exifread.process_file(file)
        cdate = pm.parse(str(exif["Image DateTime"]))
    return cdate


@dataclass
class File:
    path: str
    ext: str
    ctime: pm.DateTime = None
    xmp: str = None



@click.command()
@click.argument("directory")
@click.option(
    "-e",
    "--extentions",
    "file_exts",
    default=["NEF"],
    show_default=True,
    multiple=True,
    help="File Extensions to find and rename. Can be used multiple times.",
)
@click.option(
    "-x",
    "--xmp",
    "xmp_pairing",
    is_flag=True,
    default=True,
    help="If enabled, the program will find .XMP files with the same name as an image file and rename them the same.",
)
def main(directory, file_exts, xmp_pairing=True):
    """Searches folder non-recursively for file with given
    file extensions, retrieves EXIF dates and renames files.
    If XMP pairing is enabled, rename them with same
    as paired file"""
    # Get list of image files in directory
    files = []

    if xmp_pairing:
        xmps = glob.glob(f"{directory}/*.xmp")
        for ext in file_exts:
            for file in glob.glob(f"{directory}/*.{ext}"):
                file_name = file.rsplit(".", 1)[:-1][0]
                # Add paired XMP to file property list
                if (xmp := file_name + ".xmp") in xmps:
                    files.append(File(path=file, ext=ext, xmp=xmp))
                else:
                    files.append(File(path=file, ext=ext))

    else:
        for ext in file_exts:
            for file in glob.glob(f"{directory}/*.{ext}"):
                files.append(File(path=file, ext=ext))

    # Add creation date to file property list
    for file in tqdm(files, desc="1/2 - Retrieving EXIF"):
        file.ctime = find_ctime(file.path)

    # Sort file list by creation time at last index (ctime)
    files.sort(key=lambda x: x.ctime)

    # Determining the left zero padding for the file name iterater
    padding = len(str(len(files)))

    # Loop through each image file and rename to YY-mm-dd - 000 format.
    for iter, img in tqdm(enumerate(files), desc="2/2 - Renaming files"):
        cdate = img.ctime.to_date_string()
        file_ext = img.ext
        new_path = f"{directory}/{cdate} - {str(iter).zfill(padding)}.{file_ext}"
        os.rename(img.path, new_path)
        if img.xmp:
            xmp_path = f"{directory}/{cdate} - {str(iter).zfill(padding)}.xmp"
            os.rename(img.xmp, xmp_path)


if __name__ == "__main__":
    main()
