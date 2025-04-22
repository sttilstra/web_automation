# web_automation
This project was created to interact with a website as the data needed from this site was not available through an API.
It interacts with and downloads zip files from the website, extracts and renames the zip file content, uploads them to Azure blob storage and sends alert messages to a Microsoft Teams Channel via a webhook.
It utilizes headless chrome portable in order to avoid incompatible chrome driver issues due to organizational updates.

The script runs as an exectuable file on a virtual machine kicked off with windows task scheduler. Both the website and VM do not have the best peformance, so the browser implicit wait and page load timeout options are set to longer. Additionally there are several areas throughout the script were time.sleep is invoked to allow time for the website to catch up and the VM to finish processing before moving on to another process.

Downstream from this process, the data from the files are copied to a Sql Database via an Azure Datafactory Pipeline and then processed further for consumption in a web application.

Please note that sensitiive/site specific information has been generalized.
