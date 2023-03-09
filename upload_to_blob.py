from azure.storage.blob import BlobClient


# this function creates a blob storage client and uploads a file to the azure files container
def upload_to_blob(filename):
    storage_account_key = "<accountKey>"
    storage_account_name = "<accountName>"
    container_name = "<containerName>"
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

    blob_client = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=f"{filename}.csv")

    with open(rf"C:\filepath\Downloads\{filename}.csv", "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    return


