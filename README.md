# Salesforce Data Export Tool

## Overview
This tool is ued for exporting data from Salesforce using Salesforce Data Export API. It allows users to auto download all backup ZIPS.

## Features
- **Login**: Log in to Salesforce org using provided credentials.
- **Export Data**: Retrieve a link to the exported data file from Salesforce.
- **Download Data**: Download the exported data file to a local directory.

## Usage
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Create a `config.json` file with your Salesforce credentials and configuration.
    ```json
    {
      "username": "your_username",
      "password": "your_password",
      "security_token": "your_security_token",
      "auth_url": "your_auth_url",
      "org_url": "your_org_url"
    }
    ```
4. Run the script using `python run.py`.
![image](https://github.com/psagredo99/autoBackupDownload/assets/72439144/a6635ecf-1369-4b29-bf31-001493404024)

## Configuration
- **config.json**: Contains Salesforce login credentials and configuration.
- **login.xml**: Template for the SOAP login request.

## Output
The downloaded data file will be saved in the "downloads" directory within the project folder.

## Dependencies
- [Requests](https://docs.python-requests.org/en/latest/)
- [tqdm](https://github.com/tqdm/tqdm)


