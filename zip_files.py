from zipfile import ZipFile
import os

filepath = r"<C:\filepath\Downloads\filename.zip>"
download_folder_path = r"<C:\filepath\Downloads>"


# this function extracts the downloaded zip file contents, renames the csv and deletes zip file
def extract_and_delete(new_name):
    with ZipFile(filepath) as zip_object:
        original_filename = zip_object.namelist()

    with ZipFile(filepath) as zip_object:
        zip_object.extractall(download_folder_path)

    os.rename(rf"{download_folder_path}\{original_filename[0]}", rf"{download_folder_path}\{new_name}.csv")
    os.remove(filepath)

    return
