#Write a Python program to subtract five days from current date.
"""import datetime

today = datetime.date.today()
five_days_ago = today - datetime.timedelta(days=5)

print(five_days_ago)"""


#Write a Python program to print yesterday, today, tomorrow.
"""import datetime
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)"""


#Write a Python program to drop microseconds from datetime.
"""import datetime

now = datetime.datetime.now()
drop_microseconds = now.replace(microsecond=0)

print(drop_microseconds)"""


#Write a Python program to calculate two date difference in seconds.
import datetime

date1 = datetime.datetime(2026, 9, 28, 10, 0, 0)
date2 = datetime.datetime(2026, 9, 28, 12, 30, 0)

difference = date2 - date1

seconds = difference.total_seconds()

print(seconds)