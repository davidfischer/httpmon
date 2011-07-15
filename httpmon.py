#!/usr/bin/env python26
import smtplib
import urllib2
from email.mime.text import MIMEText

URLS = []
TIMEOUT = 30
_OK = 200

# SMTP settings
#SMTPUSER = ''
#SMTPPASS = ''
#SMTPSERVER = ''
#SMTPPORT = 25

# who to address the email to and from
TO = 'you@gmail.com'
FROM = 'httpmon@localhost'

def main():
    for url in URLS:
    
        try:
            f = urllib2.urlopen(url, timeout=TIMEOUT)
            code = f.code
            body = str(f.headers)
            msg = f.msg
            f.close()
        except (urllib2.URLError, urllib2.HTTPError), e:
            msg = 'Unknown'
            body = str(getattr(e, 'reason', '?'))
            code = getattr(e, 'code', 0)
    
        print "%s - %s" %(msg, url)
    
        if code != _OK:
            subject = '[DOWNTIME NOTIFY] %s' %url
            msg = '%s - %s\n%s\n' %(code, msg, body)
            email_notify(subject, msg)

def email_notify(subject, txt):
    msg = MIMEText(txt)
    msg['Subject'] = subject
    msg['From'] = FROM
    msg['To'] = list().append(TO)

    # Send the email via our own SMTP server.
    s = smtplib.SMTP(SMTPSERVER, SMTPPORT)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(SMTPUSER, SMTPPASS)
    s.sendmail(FROM, TO, msg.as_string())
    s.quit()

if __name__ == '__main__':
    main()
