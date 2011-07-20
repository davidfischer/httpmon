#!/usr/bin/env python26
from optparse import OptionParser
import smtplib
import urllib2
from email.mime.text import MIMEText

TIMEOUT = 30
_OK = 200

# SMTP settings
SMTPUSER = ''
SMTPPASS = ''
SMTPSERVER = 'localhost'
SMTPPORT = 25

# default from address
FROM = 'httpmon@davidfischer.github.com'

USAGE = """%prog [options] url1 url2 ...

Check the HTTP status code of each URL to verify if the site is up"""

def main():
    parser = OptionParser(USAGE)
    parser.add_option("-e", "--email", dest="address", default="",
                      help="Send email if a site is down")
    parser.add_option("-t", "--timeout", type="int", dest="timeout", 
                      default=TIMEOUT, help="timeout (seconds) [%d]" %TIMEOUT)
    parser.add_option("-s", "--tls", action="store_true", dest="tls", 
                      default=False, help="Use TLS for email")
    (options, args) = parser.parse_args()    

    # check each URL
    for url in args:
        try:
            f = urllib2.urlopen(url, timeout=options.timeout)
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
            subject = '[DOWNTIME] %s' %url
            msg = 'Status code: %s\n\n%s\n%s\n\n' %(code, msg, body)
            if len(options.address) > 0:
                email_notify(subject, msg, options.address, options.tls)

def email_notify(subject, txt, address, use_tls):
    msg = MIMEText(txt)
    msg['Subject'] = subject
    msg['From'] = FROM
    msg['To'] = list().append(address)

    # Send the email via our own SMTP server.
    s = smtplib.SMTP(SMTPSERVER, SMTPPORT)
    if use_tls:
        s.ehlo()
        s.starttls()
        s.ehlo()
    if len(SMTPUSER) > 0:
        s.login(SMTPUSER, SMTPPASS)
    s.sendmail(FROM, address, msg.as_string())
    s.quit()

if __name__ == '__main__':
    main()
