import re
import sys
import json
import string
#from email_validator import validate_email
from pii_manager import PiiEnum
from pii_manager.api import PiiManager
from pii_manager.lang import COUNTRY_ANY
# Define language, country(ies) and PII tasks
lang = 'es'
#country = ['US', 'GB', 'AU', 'SP']
tasklist = (PiiEnum.IP_ADDRESS, PiiEnum.EMAIL_ADDRESS, PiiEnum.PHONE_NUMBER)


proc = PiiManager(lang, COUNTRY_ANY, tasks=tasklist)

for line in sys.stdin:
    j = json.loads(line)
    text = j["raw_content"]
    j["redacted"] = proc(text)
    print(json.dumps({"redacted":j["redacted"], "original":j["raw_content"]}))


