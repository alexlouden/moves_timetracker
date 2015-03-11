import json
from dateutil import parser
from collections import defaultdict
import datetime
from pprint import pprint


WEEKDAY = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}


def parse():
    with open('moves.json') as f:
        data = json.load(f)

    data = data['export']
    places = defaultdict(list)

    for row in data:
        row['date'] = parser.parse(row['date'])

        if row['segments'] is None:
            continue

        for seg in row['segments']:

            if 'place' not in seg or 'name' not in seg['place']:
                continue

            place = seg['place']['name']

            start = parser.parse(
                seg['startTime']) + datetime.timedelta(hours=8)
            end = parser.parse(seg['endTime']) + datetime.timedelta(hours=8)
            time = end - start

            places[place].append(
                {
                    "week": start.isocalendar()[1],
                    "day": start.weekday(),
                    "date": start.date(),
                    "duration": time,
                    "start": start,
                    "end": end
                }
            )

    return data, places


def analyse(place):

    data = defaultdict(lambda: defaultdict(datetime.timedelta))
    dates = defaultdict(lambda: defaultdict(list))

    for row in place:
        data[row['week']][row['day']] += row['duration']
        dates[row['week']][row['day']].append(row)

    days = [
        (
            weeknum,
            daynum,
            data[weeknum][daynum].total_seconds() / 60 / 60,
            dates[weeknum][daynum][0]['start'],
            dates[weeknum][daynum][-1]['end']
        )
        for weeknum in sorted(data.keys())
        for daynum in sorted(data[weeknum].keys())
    ]

    weeks = defaultdict(float)
    for w, d, h, start, end in days:
        weeks[w] += h

    return data, dates, days, weeks


def td_to_hours(td):
    return td.total_seconds() / 60 / 60


def prettyprint(placedata, dates, weeks):

    hours = 0
    count = 0

    for weeknum, week in placedata.iteritems():
        print
        print '-' * 20
        print 'Week {}'.format(weeknum)
        print '-' * 20

        for daynum, time in week.iteritems():
            end = dates[weeknum][daynum][-1]['end']
            start = dates[weeknum][daynum][0]['start']
            print '{day} {start:{dfmt}}'.format(
                day=WEEKDAY[daynum],
                start=start,
                dfmt='%Y/%m/%d',
            )
            print '{start:{fmttime}} - {end:{fmttime}} = {total:.1f}'.format(
                start=start,
                end=end,
                fmttime='%H:%M:%S',
                hours=td_to_hours(time),
                total=td_to_hours(end - start)
            )

        print 'Total: {:.2f}'.format(weeks[weeknum])
        print 'Average: {:.2f}'.format(weeks[weeknum] / len(week))

        hours += weeks[weeknum]
        count += len(week)

    print
    print '=' * 20
    print 'Hours: {}'.format(hours)
    print 'Days: {}'.format(count)
    print 'Average: {:.2f}'.format(hours / count)

if __name__ == '__main__':
    data, places = parse()

    print places.keys()

    home = places['Cranked']
    placedata, dates, days, weeks = analyse(home)

    prettyprint(placedata, dates, weeks)
