from util import is_short_date_format

str="12-22-2022"
assert(is_short_date_format(str)==False)

str="12-22"
assert(is_short_date_format(str)==True)

str="22-12"
assert(is_short_date_format(str)==False)

str="1222"
assert(is_short_date_format(str)==False)

str="12-22-"
assert(is_short_date_format(str)==False)