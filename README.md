# Markdown to Google Docs Converter

[Public GitHub repository link](https://github.com/ndsjrrr/markdown-to-gdocs): https://github.com/ndsjrrr/markdown-to-gdocs

A Python script that converts Markdown files to Google Docs while preserving formatting, including headers, bullet points, checkboxes, and @mentions. The tool automatically creates a new Google Doc and makes it publicly accessible.

## Features

- Converts Markdown files to Google Docs format
- Supports multiple heading levels (H1-H4)
- Handles bullet points and checkboxes
- Supports @mentions with blue highlighting
- Automatically shares the created document
- Preserves document structure and formatting

## Prerequisites

- Python 3.6 or higher
- Google Cloud Project with Google Docs API enabled
- Service Account credentials with appropriate permissions

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd markdown-to-gdocs
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Cloud Project:
   - Create a new project in Google Cloud Console
   - Enable the Google Docs API and Google Drive API
   - Create a Service Account and download the credentials JSON file
   - Rename the credentials file to `authtest-448709-424a7e65caa5.json` and place it in the project root

## Usage

1. Place your Markdown file in the `data` directory as `input.md`

2. Run the converter:
   ```bash
   python mdToGoogle.py
   ```

3. The script will create a new Google Doc and print its URL in the console

## Google Colab Usage

0. (Optional) Create a new project in Google Cloud Console
   - Enable the Google Docs API and Google Drive API
   - Create a Service Account and download the credentials JSON file
   - Rename the credentials file to `my_auth.json`
1. Open the provided `mdToGoogleDocs.ipynb` in Google Colab
2. (Optional) Upload your service account credentials file my_auth.json and place it in the project root and comment out these two line and add my_auth.json here.
```python
# SERVICE_ACCOUNT_FILE_ENC = 'auth.json.enc'
# encrypt_auth.decrypt_auth_file(SERVICE_ACCOUNT_FILE_ENC)
SERVICE_ACCOUNT_FILE = 'my_auth.json'
```
3. (Optional) Input your email and your desired google docs title if you want edit access: process_markdown_file('./data/input.md', title="Meeting Notes", email="your_email@gmail.com")
4. Run all cells in the notebook 
5. The script will create a new Google Doc and print its URL in the console 
