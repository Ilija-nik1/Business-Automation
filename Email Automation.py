import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
smtp_server = 'your_smtp_server'
smtp_port = 587
imap_server = 'your_imap_server'
imap_port = 993
email_address = 'your_email_address'
email_password = 'your_email_password'

def send_email(subject, body, recipient, sender=email_address):
    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject

    # Add body to the email
    message.attach(MIMEText(body, 'plain'))

    try:
        # Create SMTP connection
        smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
        smtp_conn.starttls()
        smtp_conn.login(email_address, email_password)

        # Send email
        smtp_conn.send_message(message)
        print("Email sent successfully.")

        # Close SMTP connection
        smtp_conn.quit()
    except Exception as e:
        print("An error occurred while sending the email:", str(e))

def process_incoming_emails():
    try:
        # Create IMAP connection
        imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap_conn.login(email_address, email_password)

        # Select the mailbox to process
        imap_conn.select('INBOX')

        # Search for emails based on criteria
        _, data = imap_conn.search(None, 'ALL')

        # Iterate through email IDs
        for email_id in data[0].split():
            _, email_data = imap_conn.fetch(email_id, '(RFC822)')
            raw_email = email_data[0][1].decode('utf-8')

            # Process the email as needed
            # Example: Print email subject
            message = email.message_from_string(raw_email)
            subject = message['Subject']
            print("Received email with subject:", subject)

            # Mark the email as seen (optional)
            imap_conn.store(email_id, '+FLAGS', '\\Seen')

        # Close IMAP connection
        imap_conn.close()
        imap_conn.logout()
    except Exception as e:
        print("An error occurred while processing the emails:", str(e))

def search_emails(criteria):
    try:
        # Create IMAP connection
        imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap_conn.login(email_address, email_password)

        # Select the mailbox to search
        imap_conn.select('INBOX')

        # Search for emails based on criteria
        _, data = imap_conn.search(None, criteria)

        # Iterate through email IDs
        for email_id in data[0].split():
            _, email_data = imap_conn.fetch(email_id, '(RFC822)')
            raw_email = email_data[0][1].decode('utf-8')

            # Process the email as needed
            # Example: Print email subject
            message = email.message_from_string(raw_email)
            subject = message['Subject']
            print("Found email with subject:", subject)

        # Close IMAP connection
        imap_conn.close()
        imap_conn.logout()
    except Exception as e:
        print("An error occurred while searching emails:", str(e))

def delete_emails(criteria):
    try:
        # Create IMAP connection
        imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap_conn.login(email_address, email_password)

        # Select the mailbox to delete emails from
        imap_conn.select('INBOX')

        # Search for emails based on criteria
        _, data = imap_conn.search(None, criteria)

        # Iterate through email IDs and delete emails
        for email_id in data[0].split():
            imap_conn.store(email_id, '+FLAGS', '\\Deleted')

        # Expunge deleted emails
        imap_conn.expunge()

        # Close IMAP connection
        imap_conn.close()
        imap_conn.logout()

        print("Emails deleted successfully.")
    except Exception as e:
        print("An error occurred while deleting emails:", str(e))

def get_email_body(email_id):
    try:
        # Create IMAP connection
        imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap_conn.login(email_address, email_password)

        # Select the mailbox to fetch email from
        imap_conn.select('INBOX')

        # Fetch the email data
        _, email_data = imap_conn.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1].decode('utf-8')

        # Process the email body
        message = email.message_from_string(raw_email)
        if message.is_multipart():
            # If the email has multiple parts, iterate through them
            for part in message.get_payload():
                if part.get_content_type() == 'text/plain':
                    return part.get_payload()
        else:
            # If the email is not multipart, return the body directly
            return message.get_payload()
    except Exception as e:
        print("An error occurred while retrieving the email body:", str(e))

def get_email_sender(email_id):
    try:
        # Create IMAP connection
        imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap_conn.login(email_address, email_password)

        # Select the mailbox to fetch email from
        imap_conn.select('INBOX')

        # Fetch the email data
        _, email_data = imap_conn.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1].decode('utf-8')

        # Process the email sender
        message = email.message_from_string(raw_email)
        return message['From']
    except Exception as e:
        print("An error occurred while retrieving the email sender:", str(e))

def move_emails(criteria, destination_mailbox):
    try:
        # Create IMAP connection
        imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap_conn.login(email_address, email_password)

        # Select the source mailbox to move emails from
        imap_conn.select('INBOX')

        # Search for emails based on criteria
        _, data = imap_conn.search(None, criteria)

        # Iterate through email IDs and move emails
        for email_id in data[0].split():
            imap_conn.copy(email_id, destination_mailbox)
            imap_conn.store(email_id, '+FLAGS', '\\Deleted')

        # Expunge deleted emails
        imap_conn.expunge()

        # Close IMAP connection
        imap_conn.close()
        imap_conn.logout()

        print("Emails moved successfully.")
    except Exception as e:
        print("An error occurred while moving emails:", str(e))

def mark_email_as_unread(email_id):
    try:
        # Create IMAP connection
        imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap_conn.login(email_address, email_password)

        # Select the mailbox to modify email flags
        imap_conn.select('INBOX')

        # Mark the email as unread
        imap_conn.store(email_id, '-FLAGS', '\\Seen')

        # Close IMAP connection
        imap_conn.close()
        imap_conn.logout()

        print("Email marked as unread successfully.")
    except Exception as e:
        print("An error occurred while marking the email as unread:", str(e))

def get_email_attachments(email_id):
    try:
        # Create IMAP connection
        imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap_conn.login(email_address, email_password)

        # Select the mailbox to fetch email from
        imap_conn.select('INBOX')

        # Fetch the email data
        _, email_data = imap_conn.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]

        # Process the email attachments
        message = email.message_from_bytes(raw_email)
        attachments = []

        for part in message.iter_attachments():
            attachment_data = part.get_payload(decode=True)
            attachment_name = part.get_filename()
            attachments.append((attachment_name, attachment_data))

        # Close IMAP connection
        imap_conn.close()
        imap_conn.logout()

        return attachments
    except Exception as e:
        print("An error occurred while retrieving the email attachments:", str(e))

# Example usage
send_email('Test Email', 'This is a test email.', 'recipient@example.com')
process_incoming_emails()
search_emails('SUBJECT "Important"')
delete_emails('SUBJECT "Spam"')

# Additional function usage
email_id = '12345'  # Replace with the actual email ID
body = get_email_body(email_id)
print("Email Body:", body)

sender = get_email_sender(email_id)
print("Email Sender:", sender)

move_emails('SUBJECT "Archive"', 'Archive')

mark_email_as_unread(email_id)

attachments = get_email_attachments(email_id)
for attachment in attachments:
    attachment_name, attachment_data = attachment
    with open(attachment_name, 'wb') as file:
        file.write(attachment_data)