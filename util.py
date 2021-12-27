def is_short_date_format(date_string):
    if len(date_string) != 5:
        # print('len must == 5')
        return False
    if date_string[2] != '-':
        # print('3rd char must be -')
        return False
    if int(date_string[:2]) not in range(0,13):
        # print()
        # print('month out of range')
        return False
    if int(date_string[3:]) not in range(0,32):
        # print('day out of range')
        return False
    return True