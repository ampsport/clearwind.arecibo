import os
import sys

from AccessControl import getSecurityManager
from ZODB.POSException import ConflictError
from lib.arecibo import ThreadedHTTPPost
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component.hooks import getSite

from clearwind.arecibo.interfaces import IAreciboConfiguration

from logging import getLogger
log = getLogger('Plone')

headers = ['HOME', 'HTTP_ACCEPT', 'HTTP_ACCEPT_ENCODING',
           'HTTP_ACCEPT_LANGUAGE', 'HTTP_CONNECTION', 'HTTP_HOST', 'LANG',
           'PATH_INFO', 'QUERY_STRING', 'REQUEST_METHOD', 'SCRIPT_NAME',
           'SERVER_NAME', 'SERVER_PORT', 'SERVER_PROTOCOL', 'SERVER_SOFTWARE']

try:
    import site_configuation
    from site_configuration import config
    log("Arecibo configuration read from: %s" % os.path.abspath(site_configuration.__file__))
except:
    # please don't override this here, look in site_configuration.py for a chance to
    # overload this, details are there too
    config = {
        "account": "",
        "transport": "http",
        "priorities": {
            404: 5,
            403: 3,
            500: 1,
        },
        "default-priority": 3,
        "ignores": ["Redirect", ]
    }


def get(context):
    # pull first from our default settings above
    # the from site_configuration
    # and finally from the Plone Control Panel
    cfg = config.copy()
    registry = getUtility(IRegistry)
    try:
        arecibo_settings = registry.forInterface(IAreciboConfiguration)
    except KeyError:
        return cfg

    if arecibo_settings.account_number:
        cfg["account"] = arecibo_settings.account_number
    if arecibo_settings.app_name:
        cfg["app_name"] = arecibo_settings.app_name
    if arecibo_settings.transport == "smtp":
        cfg["transport"] = "smtp"
    cfg["ignore_localhost"] = arecibo_settings.ignore_localhost

    return cfg


def arecibo(context, **kw):
    cfg = get(context)
    if kw.get("error_type") in cfg["ignores"]:
        return

    if not cfg["account"]:
        msg = "There is no account number configured so that the error can be sent to Arecibo"
        log.error('Arecibo: %s', msg)
        return

    req = context.REQUEST
    error = ThreadedHTTPPost()

    error.posturl = "http://%s.appspot.com/v/1/" % cfg["app_name"]
    error.smtp_to = "django-%s@%s.appspotmail.com" % (cfg["account"], cfg["app_name"])
    site = getSite()
    if not site:
        return 
    error.smtp_from = site.portal_properties.email_from_address

    try:
        mail_possible = not not context.MailHost.smtp_host
        if mail_possible and cfg["transport"] == "smtp":
            error.transport = "smtp"
    except: # no mailhost on file
        log.error('Not in the context of a mail host. passing.')
        return 

    errorType = kw.get("error_type")
    try:
        ignoredExceptions = getSite().error_log._ignored_exceptions
        if errorType in ignoredExceptions:
            log.debug('Error is in list of ignored exceptions, not forwarding to arecibo')
            return
    except:  # don't want to kill error reporting if someone's config is amuck.
        pass

    if errorType == 'NotFound':
        status = 404
    elif errorType == 'Unauthorized':
        status = 403
    else:
        status = 500

    priority = cfg["priorities"].get(status, cfg["default-priority"])

    error.set("account", cfg["account"])
    error.set("priority", priority)
    error.set("user_agent", req.get('HTTP_USER_AGENT', ""))

    if req.get("QUERY_STRING"):
        error.set("url", "%s?%s" % (req['ACTUAL_URL'], req['QUERY_STRING']))
    else:
        error.set("url", req['ACTUAL_URL'])

    if kw.get("error_log_id"):
        error.set("uid", kw.get("error_log_id"))

    ip = req.get("X_FORWARDED_FOR", req.get('REMOTE_ADDR', ''))
    # don't forward errors from developer instances
    if ip == "127.0.0.1" and cfg["ignore_localhost"]:
        log.debug('Error is from localhost, not forwarding to arecibo')
        return

    error.set("ip", ip)
    error.set("type", kw.get("error_type"))
    error.set("status", status)
    error.set("request", "\n".join(["%s: %s" % (k, req[k]) for k in headers if req.get(k)]))

    if status != 404:
        # lets face it the 404 tb is not useful
        error.set("traceback", kw.get("error_tb"))

    usr = getSecurityManager().getUser()
    error.set("username", "%s (%s)" % (usr.getId(), usr.getUserName()))
    error.set("msg", kw.get("error_msg"))

    if error.transport == "http":
        try:
            error.send()
        except ConflictError:
            raise
        except:
            exctype, value = sys.exc_info()[:2]
            msg = "There was an error posting that error to Arecibo via http %s, %s" % (exctype, value)
            log.error('Arecibo: %s', msg)
    elif error.transport == "smtp":
        # use the MailHost to send out which is configured by the site
        # administrator, and has more functionality than straight smtplib
        try:
            context.MailHost.send(error._msg_body(), mto=error.smtp_to, mfrom=error.smtp_from)
        except ConflictError:
            raise
        except:
            exctype, value = sys.exc_info()[:2]
            msg = "There was an error posting that error to Arecibo via smtp %s, %s" % (exctype, value)
            log.error('Arecibo: %s', msg)
