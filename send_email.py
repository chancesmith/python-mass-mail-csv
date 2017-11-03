# import smtplib

# create and import your login.py (copy example_login.py)
# Import smtplib for the actual sending function
from env import email
from env import password
from env import server
from env import port
import smtplib
# Jinja2 templating
from jinja2 import Environment
# Import the email modules we'll need
from email.mime.application import MIMEApplication
# from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

def send_email(email_firstName, email_send_to, gif_path):

    msg = MIMEMultipart()

    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    textfile = 'email-template-inlined.html'
    with open(textfile, 'rb') as fp:
        # Create a text/plain message
        msg.attach(
            MIMEText(Environment().from_string(fp.read()).render(
                firstName=email_firstName
            ), 'html')
        )

    # attach gif
    # Open the files in binary mode.  Let the MIMEImage class automatically
    # guess the specific image type.
    part = ''
    with open(gif_path, 'rb') as fp:
        part = MIMEApplication(
            fp.read(),
            Name=basename('photobooth.gif')
        )
        # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="photobooth.gif"'
    msg.attach( part )

    # email headers
    msg['Subject'] = 'Your gif is ready'
    msg['From'] = email
    msg['To'] = email_send_to

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP(server,port)
    s.starttls()
    s.login(email,password)
    ## Send message
    try:
        s.sendmail(email, email_send_to, msg.as_string())
        return True
    except Exception: # try to avoid catching Exception unless you have too
        return False
    finally:
        s.quit()

# if send_email('chance@sodiumhalogen.com','files/1aff3698-7e47-4f19-9b19-ef40a7c503a5.gif','Tiny','Turner') is True:
#   print("Email sent")
# else:
#   print("No dice. Email sending failed.")