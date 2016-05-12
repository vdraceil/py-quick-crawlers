import re
import string


class Scrapy(object):
    SCRAPY_STATE_DIRS = ['./requests.queue']
    SCRAPY_STATE_FILES = ['./requests.seen', './spider.state']


class Regex(object):
    PT_COMPLETE_URL = re.compile(r'^https?://[^/]+(/.*)?')
    PT_DOMAIN_FROM_URL = re.compile(
        r'^https?://([\w\-]+\.)*([\w\-]+)\.(\w{2,3}\.\w{2}|\w{2,4})/?'
    )

    PT_HTML_TAGS = re.compile(r'<[^>]+>')
    PT_PUNCTUATIONS = re.compile('[%s0-9]' % re.escape(string.punctuation))
    PT_NON_ENG_CHARS = re.compile(r'[^A-Za-z\s]+')
    PT_NON_PRINTABLE_CHARS = re.compile('[\x00-\x01](?![\x00-\x0f])')

    PT_EMAIL = re.compile(r'[a-zA-Z0-9_\.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+')
