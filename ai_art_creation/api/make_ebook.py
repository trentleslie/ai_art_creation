import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors, discovery
from googleapiclient.discovery import build
import os
import sys
import json
from ebooklib import epub

# Set up your Google API credentials
creds = None
if os.path.exists("token.json"):
    with open("token.json", "r") as token:
        creds = google.oauth2.credentials.Credentials.from_authorized_user_info(info=json.load(token))

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"]
        )
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

drive_service = build("drive", "v3", credentials=creds)
docs_service = build("docs", "v1", credentials=creds)

def concatenate_google_docs(folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.document'"
    results = drive_service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get("files", [])

    if not items:
        print("No Google Doc files found.")
        sys.exit(1)

    # Add a leading zero to chapter numbers from 1 to 9
    for item in items:
        item_name = item["name"]
        if "Chapter " in item_name:
            chapter_num = item_name.split("Chapter ")[1].split(":")[0]
            if chapter_num.isdigit() and 1 <= int(chapter_num) <= 9:
                item["name"] = item_name.replace(f"Chapter {chapter_num}", f"Chapter 0{chapter_num}")

    # Sort the items alphabetically
    items = sorted(items, key=lambda x: x["name"])

    ebook = epub.EpubBook()
    ebook.set_identifier("id123456")
    ebook.set_title("Whispers of the Lost City DRAFT v0.1")
    ebook.set_language("en")
    ebook.add_author("Jerome Dixon")

    spine = ['nav']
    for item in items:
        doc_id = item["id"]
        doc_name = item["name"]

        try:
            doc = docs_service.documents().get(documentId=doc_id).execute()
            doc_elements = doc.get("body", {}).get("content", [])

            section = epub.EpubHtml(title=doc_name, file_name=f"{doc_name}.xhtml", lang="en")
            content = ""
            for element in doc_elements:
                if "paragraph" in element:
                    text_run = element.get("paragraph", {}).get("elements", [])[0].get("textRun", {})
                    content += text_run.get("content", "")
            section.content = content

            ebook.add_item(section)
            ebook.toc.append(section)
            spine.append(section)

        except errors.HttpError as error:
            print(f"An error occurred: {error}")

    ebook.add_item(epub.EpubNcx())
    ebook.add_item(epub.EpubNav())
    ebook.spine = spine

    return ebook

# Use the function
folder_id = "1BcFn1rubER0q0FPepEeDEwh-cy_OUFoX"
ebook_content = concatenate_google_docs(folder_id)

# Save the eBook content to a text file
#with open("ebook.txt", "w", encoding='utf-8') as ebook_file:
#    ebook_file.write(ebook_content)

# Save the eBook content to an EPUB file
epub.write_epub("ebook.epub", ebook_content)

