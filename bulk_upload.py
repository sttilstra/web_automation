from azure.storage.blob import BlobClient


# this function creates a blob storage client and uploads a file to the ahri files container
def upload_to_blob(filename):
    storage_account_key = "<accountKey>"
    storage_account_name = "<accountName>"
    container_name = "<containerName>"
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

    blob_client = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=f"{filename}.csv")

    with open(rf"C:\filepath\Downloads\{filename}.csv", "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    return


# this function loops through the file directory and calls the upload to blob function for each file and then removes the file from the local directory
def bulk_upload():
    download_folder_path = r"<folderpath>"
    files = os.listdir(download_folder_path)

    for file in files:
        if file == "desktop.ini":
            files.remove(file)

        upload_to_blob(file)
        os.remove(rf"{download_folder_path}\{file}")

    return

