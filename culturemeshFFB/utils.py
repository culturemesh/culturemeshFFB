#
# This file contains utility functions.
#

import config
import calendar
import datetime
import pytz
from dateutil.parser import parse

####### Date Utils #######

def str2date(str_):
  return datetime.datetime.strptime(str_, config.DATETIME_FMT_STR)

def get_month(date):
  return calendar.month_name[date.month]

def get_month_abbr(date):
  return calendar.month_abbr[date.month]

def get_weekday(date):
  return calendar.day_name[date.weekday()]

def get_weekday_abbr(date):
  return calendar.day_abbr[date.weekday()]

ERROR_DATE = "1970-01-01 00:00:00"
def parse_date(str_):
  try:
    # First let's try this format
    date = str2date(str_)
  except ValueError:
    # Otherwise best guess
    try:
      date = parse(str_)
    except:
      # Give up, and return the first date.
      data_err = parse_date(ERROR_DATE)
      return pytz.UTC.localize(data_err)
  return date

def enhance_event_date_info(event):
  date = parse_date(event['event_date'])

  event['month'] = get_month(date)
  event['month_abbr'] = get_month_abbr(date)
  event['weekday'] = get_weekday(date)
  event['weekday_abbr'] = get_weekday_abbr(date)
  event['year'] = date.year
  event['day'] = date.day

  hr = date.hour
  pod = " AM"
  if hr == 0:
    hr = 12
  elif hr >= 12:
    pod = " PM"
    hr -= 12
    if hr == 0:
      hr = 12

  hr = str(hr)
  minute = date.minute
  minute = "{0:0=2d}".format(minute)

  event['time'] = hr + ":" + minute + pod
