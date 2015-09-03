#!/usr/bin/env python
# coding: utf-8

import logging
from google.appengine.api import mail
from google.appengine.runtime.apiproxy_errors import OverQuotaError
from google.appengine.ext import deferred


def send_mail(to, subject, text):
    """
    Sendet ein Text-E-Mail
    """

    # Parameter
    if isinstance(to, basestring):
        recipients = [to]
    else:
        recipients = to

    # bawomail als Absender, da er gerold.penz (vielleicht wegen dem Punkt) nicht annimmt
    sender = "bawomail@immoads.at"
    if not mail.is_email_valid(sender):
        logging.error(u"sender address not valid")
        logging.error(u"sender: {sender}".format(sender = sender))
        logging.error(u"recipients: {recipients}".format(recipients = recipients))
        logging.error(u"subject: {subject}".format(subject = subject))
        logging.error(u"body: {body}".format(body = text))
        raise RuntimeError("sender address not valid")

    for recipient in recipients:
        if not mail.is_email_valid(recipient):
            logging.error(u"recipient address not valid")
            logging.error(u"sender: {sender}".format(sender = sender))
            logging.error(u"recipient: {recipient}".format(recipient = recipient))
            logging.error(u"subject: {subject}".format(subject = subject))
            logging.error(u"body: {body}".format(body = text))
            raise RuntimeError("recipient address not valid")

    try:
        mail.send_mail(sender, to, subject, text)
    except OverQuotaError:
        logging.error(u"OverQuotaError - E-mail not sent.")
        logging.error(u"sender: {sender}".format(sender = sender))
        logging.error(u"recipients: {recipients}".format(recipients = recipients))
        logging.error(u"subject: {subject}".format(subject = subject))
        logging.error(u"body: {body}".format(body = text))


def send_mail_to_admins(subject, text):
    """
    Sendet ein E-Mail an alle eingestellten Admins
    """

    # bawomail als Absender, da er gerold.penz (vielleicht wegen dem Punkt) nicht annimmt
    sender = "bawomail@immoads.at"
    if not mail.is_email_valid(sender):
        logging.error("sender address not valid")
        logging.error("sender: {sender}".format(sender = sender))
        logging.error("subject: {subject}".format(subject = subject))
        logging.error("body: {body}".format(body = text))
        raise RuntimeError("sender address not valid")

    try:
        mail.send_mail_to_admins(sender, subject, text)
    except OverQuotaError:
        logging.error("OverQuotaError - E-mail not sent.")
        logging.error("sender: {sender}".format(sender = sender))
        logging.error("subject: {subject}".format(subject = subject))
        logging.error("body: {body}".format(body = text))


def send_mail_defered(to, subject, text):
    """
    Übergibt das Senden des E-Mails an einen neuen Task
    """

    deferred.defer(
        send_mail,
        to = to,
        subject = subject,
        text = text
    )


class GaeSmtpHandler(logging.Handler):
    """
    A handler class which sends an SMTP email for each logging event.
    """

    def __init__(self, subject):

        logging.Handler.__init__(self)
        self.subject = subject


    def emit(self, record):
        try:
            send_mail_defered(
                to = u"gerold.penz@immoads.at",
                subject = self.subject,
                text = self.format(record)
            )
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

