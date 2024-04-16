import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Install necessary packages
# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
# For sending email, no additional installations are required as smtplib and email modules are part of Python standard library.

# Google Drive API credentials
credentials = service_account.Credentials.from_service_account_file('credentials.json')
drive_service = build('drive', 'v3', credentials=credentials)

def upload_file_to_drive(archive_path, folder_id=None):
    file_metadata = {'name': os.path.basename(archive_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(archive_path, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    # Set the permission to make the file accessible to anyone with the link
    drive_service.permissions().create(fileId=file.get('id'), body={'role': 'reader', 'type': 'anyone'}).execute()
    
    return file.get('id')


def get_shareable_link(file_id):
    return drive_service.files().get(fileId=file_id, fields='webViewLink').execute()['webViewLink']

def send_email(username, app_name, client_email, archive_path):    
    # Folder ID in Drive where the file will be uploaded (optional, set to None if uploading to root)
    folder_id = None

    # Upload the file to Google Drive
    file_id = upload_file_to_drive(archive_path, folder_id)

    # Get shareable link of the uploaded file
    shareable_link = get_shareable_link(file_id)

    # Email details
    sender_email = 'vallivn18@gmail.com'
    sender_password = 'hsig xnka zcmp ntsl'
    subject = f'Your {app_name} app files is ready for download!'
    body = f'Hey {username}, \n\nThanks for using Appify for creating your {app_name} app. You can download your {app_name} app\'s AAB and APK files from the following link\n{shareable_link}\n\nTeam Appify'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = client_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    try:
        server.sendmail(sender_email, client_email, text)
        server.quit()
        print("Email Sent Successfully!!!")
        return True
    except smtplib.SMTPException as e:
        print("failed to Send Email :", e)
        server.quit()
        return False

