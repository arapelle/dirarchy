import datetime


class VariablesDict(dict):
    def __missing__(self, key):
        match key:
            case "$YEAR":
                return f"{datetime.date.today().year}"
            case "$MONTH":
                return f"{datetime.date.today().month:02}"
            case "$DAY":
                return f"{datetime.date.today().day:02}"
            case "$DATE_YMD":
                today = datetime.date.today()
                return f"{today.year}{today.month:02}{today.day:02}"
            case "$DATE_Y_M_D":
                today = datetime.date.today()
                return f"{today.year}-{today.month:02}-{today.day:02}"
            case _:
                raise KeyError(key)
