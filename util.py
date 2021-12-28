import re
# print('hello')
def is_short_date_format(date_string):
    if len(date_string) != 5:
        # print('len must == 5')
        return False
    if date_string[2] != '-':
        # print('3rd char must be -')
        return False
    if not date_string[:2].isnumeric() or int(date_string[:2]) not in range(1,13):
        # print()
        # print('month out of range')
        return False
    if not date_string[3:].isnumeric() or int(date_string[3:]) not in range(1,32):
        # print('day out of range')
        return False
    # print('True')
    return True

def is_short_time_format(time_string):
    if len(time_string) != 5:
        # print('len must == 5')
        return False
    if time_string[2] != ':':
        # print('3rd char must be -')
        return False
    if not time_string[:2].isnumeric() or int(time_string[:2]) not in range(0,24):
        # print()
        # print('month out of range')
        return False
    if not time_string[3:].isnumeric() or int(time_string[3:]) not in range(0,60):
        # print('day out of range')
        return False
    return True

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)