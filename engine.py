#!/usr/bin/env python3

import datetime
import csv
import os, re


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    END = '\033[0m'


def startup():
    name1 = f'{os.getcwd()}/db.txt'
    name2 = f'{os.getcwd()}/temp.txt'
    with open(name1, 'r', encoding='utf-8') as inFile, \
            open(f'{os.getcwd()}/temp.txt', 'w', encoding='utf-8') as outFile:
        for line in inFile:
            if line.strip():
                outFile.write(line)
    os.remove(name1)
    os.rename(name2, name1)


def mothers_day(year):
    # """Return datetime.date for monthly option expiration given year and
    # month
    # >>> print(mothers_day(2020))
    # 2020-05-10
    # >>> print(mothers_day(2021))
    # 2021-05-09
    # >>> print(mothers_day(2019))
    # 2019-05-12
    # >>> print(mothers_day(1998))
    # 1998-05-10
    # """

    # The month in which mothers day is
    month = 5
    # If we assume monday == 0, then sunday happens on the 6th day
    day = 6
    # The lowest number date in the second week is th e 8th.
    lowest = 8
    # Setting the lowest date of chosen week.
    second = datetime.date(year, month, lowest)
    # What day of the week is the lowest?
    w = second.weekday()
    # If weekday is not day we need, replace that date
    if w != day:
        # Replace just the day (of month)
        second = second.replace(day=(lowest + (day - w) % 7))
    return second


def fathers_day(year):
    # """Return datetime.date for monthly option expiration given year and
    # month
    # >>> print(fathers_day(2020))
    # 2020-06-21
    # >>> print(fathers_day(2021))
    # 2021-06-20
    # >>> print(fathers_day(2019))
    # 2019-06-16
    # >>> print(fathers_day(1998))
    # 1998-06-21
    # """

    # The month in which fathers day is
    month = 6
    # If we assume monday == 0, then sunday happens on the 6th day
    day = 6
    # The lowest number date in the second week is th e 8th.
    lowest = 15
    # Setting the lowest date of chosen week.
    third = datetime.date(year, month, lowest)
    # What day of the week is the lowest?
    w = third.weekday()
    # If weekday is not day we need, replace that date
    if w != day:
        # Replace just the day (of month)
        third = third.replace(day=(lowest + (day - w) % 7))
    return third


def getBirthdays():
    today = datetime.date.today()

    mothers_date = mothers_day(today.year)
    fathers_date = fathers_day(today.year)

    if (mothers_date - today).days < 0:
        next_year = today.year + 1
        mothers_date = mothers_day(next_year)

    if (fathers_date - today).days < 0:
        next_year = today.year + 1
        fathers_date = fathers_day(next_year)

    db = []
    with open(f'{os.getcwd()}/db.txt', encoding='utf8') as f:
        reader = csv.reader(f)
        for line in reader:
            db += [line]

    db.pop(0)
    db.pop(0)

    db.append(['Mothers Day', ' ' + str(mothers_date.strftime('%d%m%Y'))])
    db.append(['Fathers Day', ' ' + str(fathers_date.strftime('%d%m%Y'))])

    db = [line for line in db if line != ['', ' ']]

    dates = []
    for i in range(len(db)):
        person = datetime.date(year=today.year, month=int(db[i][1][3:5]), day=int(db[i][1][0:3]))
        days_to_birthday = person - today
        year_diff = today.year - int(db[i][1][5:9])
        if days_to_birthday.days >= 0:
            dates.append([days_to_birthday, db[i][0], year_diff])

        else:
            dates.append([days_to_birthday + datetime.timedelta(days=365), db[i][0], year_diff + 1])

    dates.sort(reverse=False)

    birthdayList = []

    for i in range(len(dates)):
        left_aligned = f"{dates[i][1]}"
        center = f"{dates[i][0].days}"
        right_aligned = f"({dates[i][2]})"

        if dates[i][0].days == 1:
            center = f"{dates[i][0].days}"

        elif dates[i][0].days == 0:
            center = 0

        if dates[i][0].days <= 5:
            birthdayList.append([left_aligned, center, right_aligned, 0])

        elif 5 < dates[i][0].days <= 15:
            birthdayList.append([left_aligned, center, right_aligned, 1])

        elif 15 < dates[i][0].days <= 30:
            birthdayList.append([left_aligned, center, right_aligned, 2])

        else:
            birthdayList.append([left_aligned, center, right_aligned, 3])
        # birthdayList.append(f"{left_aligned:<25}{center:^10}{right_aligned:>10}")
    return birthdayList


def deleteLine(name):
    with open(f'{os.getcwd()}/db.txt', "r", encoding='utf8') as f:
        lines = f.readlines()
    with open(f'{os.getcwd()}/db.txt', "w", encoding='utf8') as f:
        for line in lines:
            string2 = line.strip("\n")
            checked = re.findall('([a-zA-Z ]*)\d*.*', string2)[0]
            if checked.strip() != name.strip():
                f.write(line)
            else:
                pass


if __name__ == "__main__":
    import doctest

    doctest.testmod()
