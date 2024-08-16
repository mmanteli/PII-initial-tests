import re
import sys
import json
import string
import phonenumbers
from email_validator import validate_email
from dateutil.parser import parse as dateparse



#---------------------------------REGEX ONLY-------------------------------------#
def replace_email(line):
    return re.sub(r'[\w.+-]+@[\w-]+\.[\w-]+', "<EMAIL>", line)

def replace_number(line):
    """
    This finds all phone numbers in the standard format, except it sometimes misses singular digits
    and deletes one white space.
    -> unfortunately in the rp2 data many numbers are not in the standard format
    -> some aritmetic, e.g. 142-12-100 might be removed
    """
    return re.sub(r'((?:\+\d{1,3})|)?(([ ]\d{2,10}){2,5}|(?:\+\d{10,12})|([-]\d{2,7}){2,3})|(?:\(\d{3}\))[ ]\d{2,3}[-]\d{2,4}', "<NUMBER>", line)


#---------------------------------REGEX+TOOL-------------------------------------#

def replace_IP(line):
    return re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', "<IP_ADDRESS>", line)


def check_email(e):
    try:
        validate_email(e, check_deliverability=False)
        return "<EMAIL>"
    except:
        return str(e)
    

def replace_email2(line):
    return re.sub(r'\b\S*@\S*\b', lambda x: check_email(x.group()), line)


def check_phonenumber(n, line):
    # Skip dates and numbers too small to count (5 digit phone numbers only in Samoa, Faroe and Cook Islands,
    # French Guinea, Greenland and Tanzania have 6)
    if len([i for i in n if i.isdigit()])<=6:
        return str(n)
    # see for spans of years
    a =  re.search(r'\d{4}[-]\d{4}', n)
    if a !=None and a.group()==n:
        return str(n)
    try:
        d = dateparse(n)
        return str(n)
    except:
        # escape web addresses and doi etc. => punct on both sides
        match = line.index(n)
        if match > 1 and match+len(n) < len(line) and line[match-1] in "\/:;." and line[match+len(n)] in "\/:;.":
            return str(n)
        # finally check for phone number compatibility
        regions = ["US", "FR", "SP", "GB", "DE", "IT"]
        if any([phonenumbers.is_possible_number_string(n, r) for r in regions]):
            return "<PHONE_NUMBER>"
        else:
            return str(n)


def replace_number2(line):
    """
    This finds all that /might/ be phone numbers and uses phonenumbers pakage to detect if 
    a phone number was actually found -> Deletes arithmetic only in very weird instances!
    Added [^/\n:;\+a-zA-Z] -> Dates etc. not recognized as numbers.
    => this was also supposed to fix the unicode problem but it did not.
    """
    return re.sub(r'(?:\+\d{1,3}[ -]|[\(]\d{1,3}[\)][ -])?(\d{1,10}[^/\n:;\+a-zA-Z.]){2,5}\d+', lambda x: check_phonenumber(x.group(),line), line)


for line in sys.stdin:
    j = json.loads(line)
    text = j["raw_content"]
    text = replace_email2(text)
    text = replace_IP(text)
    j["redacted"] = replace_number2(text)
    print(json.dumps({"redacted":j["redacted"], "original":j["raw_content"]}))

# The unicode problem
# n = "\u4201 34819"
# >>> '䈁 34819'
# [phonenumbers.is_possible_number_string(n, r) for r in regions] 
# >>> [False, True, False, True, False, False]
# -> makes 
