import re
from datetime import datetime, timedelta

month_delta = -1
month = (datetime.now() + timedelta(month_delta)).strftime("%Y%m")
print(month)

my = re.search(r"(?P<y>\d{4})(?P<m>\d{1,2})", month)
year_todelete = my.group("y")
month_todelete = my.group("m")

datetime.now()-timedelta(mo)
