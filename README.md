# web_automation_no_api
This project was created to interact with a website since the data needed from this site was not available through an API.
It interacts with and downloads zip files from the website, extracts and renames the zip file content, uploads them to Azure blob storage and sends alert messages to a Microsoft Teams Channel via a webhook.

Update
------------------
I refactored the code so that the upload to blob storage action does not take place in the for loop which downloads the given files. These two actions are now seperate - the script will download all the files first and after the webscraping is done and the browser closed, the script will upload the files to blob storage and remove the extracted files from the directory.


