# Install necessary libraries
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

# Authenticate using Service Account
SERVICE_ACCOUNT_FILE = 'authtest-448709-424a7e65caa5.json'  # Path to your service account JSON file
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

def generate_google_docs_requests_from_markdown(markdown_notes):
    """Convert markdown content to Google Docs API requests.

    Args:
        markdown_notes (str): Raw markdown content to be converted.

    Returns:
        list: A list of Google Docs API requests for document formatting.
    """
    requests = []
    current_index = 1 

    lines = markdown_notes.splitlines()

    def get_indent_level(line):
        """Determine indentation level based on leading spaces."""
        return len(line) - len(line.lstrip())

    def get_bullet_preset(indent_level):
        """Map indentation levels to appropriate bullet presets."""
        presets = [
            'BULLET_DISC_CIRCLE_SQUARE',   # First nested level
            'BULLET_ARROW_DIAMOND_DISC'   # Third nested level
        ]
        return presets[min(indent_level // 2, len(presets) - 1)]


    for line in lines:

        # Main Title (Heading 1)
        if line.startswith("# "):
            title_text = line[2:]
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': title_text + "\n"
                }
            })
            current_index += len(title_text) + 1
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_index - len(title_text) - 1, 'endIndex': current_index},
                    'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                    'fields': 'namedStyleType'
                }
            })

        # Section Headers (Heading 2)
        elif line.startswith("## "):
            section_text = line[3:]
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': section_text + "\n"
                }
            })
            current_index += len(section_text) + 1
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_index - len(section_text) - 1, 'endIndex': current_index},
                    'paragraphStyle': {'namedStyleType': 'HEADING_2'},
                    'fields': 'namedStyleType'
                }
            })

        # Sub-section Headers (Heading 3)
        elif line.startswith("### "):
            subsection_text = line[4:]
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': subsection_text + "\n"
                }
            })
            current_index += len(subsection_text) + 1
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_index - len(subsection_text) - 1, 'endIndex': current_index},
                    'paragraphStyle': {'namedStyleType': 'HEADING_3'},
                    'fields': 'namedStyleType'
                }
            })
        
        # Sub-section Headers (Heading 4)
        elif line.startswith("#### "):
            subsection_text = line[5:]
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': subsection_text + "\n"
                }
            })
            current_index += len(subsection_text) + 1
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_index - len(subsection_text) - 1, 'endIndex': current_index},
                    'paragraphStyle': {'namedStyleType': 'HEADING_4'},
                    'fields': 'namedStyleType'
                }
            })

        # Checkboxes
        elif line.startswith("- [ ]"):
            checkbox_text = line[6:]
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': checkbox_text + "\n"
                }
            })
            current_index += len(checkbox_text) + 1
            requests.append({
                'createParagraphBullets': {
                    'bulletPreset': 'BULLET_CHECKBOX',
                    'range': {
                        'startIndex': current_index - len(checkbox_text) - 1,
                        'endIndex': current_index
                    }
                }
            })
            
            # Handle mentions within checkbox text
            matches = re.finditer(r"@(\w+):", checkbox_text)
            for match in matches: 
                mention_start = current_index - len(checkbox_text) + match.start() - 1
                mention_end = current_index - len(checkbox_text) + match.end()
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': mention_start, 'endIndex': mention_end},
                        'textStyle': {'bold': True, 'foregroundColor': {'color': {'rgbColor': {'blue': 1}}}},
                        'fields': 'bold,foregroundColor'
                    }
                })

        elif re.match(r"^\s*[*-]\s+", line):
            # Remove bullet markers and leading/trailing whitespace
            bullet_text = re.sub(r"^\s*[*-]\s+", "", line).strip()
            
            # Determine indentation level
            indent_level = get_indent_level(line)
            
            # Insert text request
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': bullet_text + "\n"
                }
            })
            
            # Create paragraph bullets request with appropriate preset
            requests.append({
                'createParagraphBullets': {
                    'range': {
                        'startIndex': current_index,
                        'endIndex': current_index + len(bullet_text) + 1
                    },
                    'bulletPreset': get_bullet_preset(indent_level)
                }
            })
            
            # Add indentation with progressive offset
            if indent_level > 0:
                requests.append({
                    'updateParagraphStyle': {
                        'range': {
                            'startIndex': current_index,
                            'endIndex': current_index + len(bullet_text) + 1
                        },
                        'paragraphStyle': {
                            'indentFirstLine': {'magnitude': indent_level * 12, 'unit': 'PT'},
                            'indentStart': {'magnitude': (indent_level - 1) * 12, 'unit': 'PT'}
                        },
                        'fields': 'indentFirstLine,indentStart'
                    }
                })
            
            # Update current index
            current_index += len(bullet_text) + 1

        

        # General Paragraph or Footer
        elif line:
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': line + "\n"
                }
            })
            current_index += len(line) + 1
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': current_index - len(line) - 1, 'endIndex': current_index},
                    'textStyle': {'fontSize': {'magnitude': 10, 'unit': 'PT'}, 'foregroundColor': {'color': {'rgbColor': {'red': 0.5}}}},
                    'fields': 'fontSize,foregroundColor'
                }
            })

    
    return requests
# Initialize Google Docs API service
def initialize_google_docs_service():
    """Initialize and return a Google Docs API service object.

    Returns:
        Resource: A Google Docs API service object.

    Raises:
        google.auth.exceptions.DefaultCredentialsError: If credentials are invalid.
    """
    try:
        return build('docs', 'v1', credentials=credentials)
    except Exception as e:
        print(f"Failed to initialize Google Docs service: {e}")
        raise

def initialize_google_drive_service():
    """Initialize and return a Google Drive API service object.

    Returns:
        Resource: A Google Drive API service object.

    Raises:
        google.auth.exceptions.DefaultCredentialsError: If credentials are invalid.
    """
    try:
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        print(f"Failed to initialize Google Drive service: {e}")
        raise

# Function to share the Google Doc
def share_google_doc(doc_id, email=None, role="writer"):
    """
    Share the Google Doc with a specific email or make it public.

    Args:
        doc_id (str): The ID of the Google Doc to share.
        email (str): The email address to share the document with (optional).
        role (str): The role to assign ('writer' or 'reader'). Defaults to 'writer'.
    """
    drive_service = initialize_google_drive_service()
    try:
        if email:
            # Share with a specific user
            permissions = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }
        else:
            # Make the document public
            permissions = {
                'type': 'anyone',
                'role': 'reader'
            }
        
        drive_service.permissions().create(
            fileId=doc_id,
            body=permissions,
            fields='id'
        ).execute()
        if email:
            print(f"Document shared successfully with {email}")
        else:
            print("Document is now publicly accessible.")
    except Exception as e:
        print(f"An error occurred while sharing the document: {e}")

# Function to create a Google Doc from Markdown
def create_google_doc_from_markdown(markdown_content, title="Meeting Notes", email=None):
    """Create a new Google Doc from markdown content.

    Args:
        markdown_content (str): The markdown content to convert.
        title (str, optional): The title for the new document. Defaults to "Meeting Notes".

    Returns:
        str: The URL of the created Google Doc.

    Raises:
        Exception: If document creation or sharing fails.
    """
    try:
        service = initialize_google_docs_service()
        
        document = service.documents().create(body={'title': title}).execute()
        document_id = document.get('documentId')
        
        requests = generate_google_docs_requests_from_markdown(markdown_content)

        service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()

        share_google_doc(doc_id=document_id, email=email)
        doc_url = f"https://docs.google.com/document/d/{document_id}/edit"
        print(f"Document created successfully: {doc_url}")
        return doc_url
    except Exception as e:
        print(f"Failed to create Google Doc: {e}")
        raise

def read_and_create_google_doc(file_path, title="Some Title", email=None):
    """Read markdown content from a file and create a Google Doc.

    Args:
        file_path (str): The path to the markdown file.
        email (str, optional): The email to share the document with. Defaults to None.
    """
    try:
        with open(file_path, 'r') as file:
            markdown_notes = file.read()
            create_google_doc_from_markdown(markdown_notes, title=title, email=email)
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    read_and_create_google_doc('./data/input.md', title="Some title", email="ndsjrrr@gmail.com")