import random


def generate_random_phone_number(message):
    formats = [
        '+1 (###) ###-####',
        '###-###-####',
        '### ### ####',
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


def generate_random_other_number(message, type=[0,1,2,3,4,5]):
    formats = [
        '1###-1###',  # year span
        '###-###=###', # math
        '#####-####+###=####',  #math
        'www.yle.fi/#######/',  # web page
        'https://www.hs.fi/####-###'
    ]

    format_str = random.choice([formats[t] for t in type])
    phone_number = ''.join([random.choice('0123456789') if char == '#' else char for char in format_str])
    
    return message.replace("#",phone_number)

possible_phone_number_messages = [
    'Please contact me immediately by phone. #.',
    'My phone number is #! Call as soon as you can.',
    'To get more information call:#',
    '# is the number I call when I need pest control',
    '#. #.',
    'Contact information: phone: # email: ...'
]

possible_other_number_messages = [
    ('This # is substraction and should not be removed!',[1,2]),
    ('In the years # the largest floods ever recorded occured.',[0]),
    ('# do not correct this',[0,1,2,3,4]),
    ('=># this right here',[0,1,2,3,4]),
    ('# and #/#',[0,1,2,3,4])
]

for i in range(20):
    m = random.choice(possible_phone_number_messages)
    print(generate_random_phone_number(m))

for i in range(20):
    m,i = random.choice(possible_other_number_messages)
    print(generate_random_other_number(m, type=i))