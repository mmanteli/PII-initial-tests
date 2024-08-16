import re
import phonenumbers
from dateutil.parser import parse as dateparse
import random
from pii_manager import PiiEnum
from pii_manager.api import PiiManager
from pii_manager.lang import COUNTRY_ANY



# BLOOM TOOL
# Define language, country(ies) and PII tasks
lang = 'en'
country = ['US', 'GB', 'FR','IT','DE','SP','FI']
tasklist = (PiiEnum.IP_ADDRESS, PiiEnum.EMAIL_ADDRESS, PiiEnum.PHONE_NUMBER)
proc = PiiManager(lang, country, tasks=tasklist)


def check_phonenumber(n, line):
    # Skip dates and numbers too small to count (5 digit phone numbers only in Samoa, Faroe and Cook Islands,
    # French Guinea, Greenland and Tanzania have 6)
    if len([i for i in n if i.isdigit()])<=6:
        return str(n)
    # see for spans of years => Very common!
    a =  re.search(r'\d{4}[-]\d{4}', n)
    if a !=None and a.group()==n:
        return str(n)
    try:
        d = dateparse(n)
        return str(n)
    except:
        # escape web addresses and doi etc. => punct on both sides
        # also math, like +:/= => "+" cannot be at the front
        match = line.index(n)
        if match > 1 and match+len(n) < len(line) and line[match-1] in "=\/:;." and line[match+len(n)] in "\/:;.+=":
            return str(n)
        # finally check for phone number compatibility
        regions = ["US", "FR", "SP", "GB", "DE", "IT"]
        if any([phonenumbers.is_possible_number_string(n, r) for r in regions]):
            return "<PHONE_NUMBER>"
        else:
            return str(n)

def replace_number_me(line):
    """
    This finds all that /might/ be phone numbers and uses phonenumbers pakage to detect if 
    a phone number was actually found -> Deletes arithmetic only in very weird instances!
    Added [^/\n:;\+a-zA-Z] -> Dates etc. not recognized as numbers.
    => this was also supposed to fix the unicode problem but it did not.
    """
    return re.sub(r'(?:\+\d{1,3}[ -])?([\(]\d{1,4}[\)][ -])?(\d{1,10}[^:;/+a-zA-Z.,\n\\]){2,6}\d+', lambda x: check_phonenumber(x.group(),line), line)


#def replace_number_bloom(line):
#    # This is for us? But does not even recognize them? cONFUSION
#    return re.sub(r'(?:\+|00)(?:9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)[-\x20\.]?(?:\d{2,3}[-\x20]?){3,4}',"<PHONE_NUMBER>", line)

def replace_number_bloom(line):
    return proc(line)

def generate_random_phone_number(message):
    formats = [
        '+1 (###) ###-####',
        '04#-###-####',
        '0## ### ####',
        '+33 ## ## ## ## ##', # French format with 
        '04 ## ## ## ##',  # French format
        '+39 ## ### ####', # Italian format
        '(###) ###-####',   # US format with hyphen
        '(###) ########',   # US format without hyphen
        '+299 ## ## ##',    # Greenland 
        '(3###) ##-####',   # Some German
    ]

    format_str = random.choice(formats)
    phone_number = ''.join([random.choice('0123456789') if char == '#' else char for char in format_str])
    
    return message.replace("#",phone_number)

def generate_random_other_number(message):
    formats = [
        '####-####',  # year span
        '###-###=###', # math
        '#####-####+###=####',
        'www.yle.fi/#######/'  # web page
    ]

    format_str = random.choice(formats)
    phone_number = ''.join([random.choice('0123456789') if char == '#' else char for char in format_str])
    
    return message.replace("#",phone_number)


text = "Hi! My phone number is # and my email is myname@gmail.com. Contact me asap!"
text = generate_random_phone_number(text)
print(replace_number_bloom(text))
exit()

for i in range(100):
    message = "to contact, please dial # and remember to also send an email."
    gen = generate_random_phone_number(message)
    a = replace_number_bloom(gen)
    if "<PHONE_NUMBER>" in a:
        print(gen)
        print(a)
        print("--------------------------------")
    #print("ME:    ",replace_number_me(gen))
exit()
for i in range(5):
    message = "this is not a number: #"
    gen = generate_random_other_number(message)
    print(gen)
    print("BLOOM: ",replace_number_bloom(gen))
    #print("ME:    ",replace_number_me(gen))
    print("--------------------------------")