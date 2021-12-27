from util import is_short_date_format, is_short_time_format


#Test short-date-strings
str="12-22-2022"
assert(is_short_date_format(str)==False)
str="22-12"
assert(is_short_date_format(str)==False)
str="1222"
assert(is_short_date_format(str)==False)
str="12-22-"
assert(is_short_date_format(str)==False)
str="12-22"
assert(is_short_date_format(str)==True)

#Test short time strings
str="12:13"
assert(is_short_time_format(str)==True)
str="23:59"
assert(is_short_time_format(str)==True)
str="00:00"
assert(is_short_time_format(str)==True)
str="24:00"
assert(is_short_time_format(str)==False)
str="01:60"
assert(is_short_time_format(str)==False)
str="s1:32"
assert(is_short_time_format(str)==False)
str="1234"
assert(is_short_time_format(str)==False)
str="21:0t"
assert(is_short_time_format(str)==False)