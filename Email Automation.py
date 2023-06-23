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

# Example usage
send_email('Test Email', 'This is a test email.', 'recipient@example.com')
process_incoming_emails()
search_emails('SUBJECT "Important"')
delete_emails('SUBJECT "Spam"')