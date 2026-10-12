import datetime 

current = datetime.date.today()
endOfYear = datetime.date(2026,12,31)

diff = str(endOfYear - current)

diff = int(diff[0:2]) / 7



print(round(diff))

