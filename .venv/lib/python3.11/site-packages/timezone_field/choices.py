import datetime

from timezone_field.backends import get_tz_backend


def standard(timezones):
    """
    Given a list of timezones (either strings of timezone objects),
    return a list of choices with
        * values equal to what was passed in
        * display strings as the timezone name without underscores
    """
    choices = []
    for tz in timezones:
        tz_str = str(tz)
        choices.append((tz, tz_str.replace("_", " ")))
    return choices


def with_gmt_offset(timezones, now=None, use_pytz=None):
    """
    Given a list of timezones (either strings of timezone objects),
    return a list of choices with
        * values equal to what was passed in
        * display strings formated with GMT offsets and without
          underscores. For example: "GMT-05:00 America/New York"
        * sorted by their timezone offset
    """
    tz_backend = get_tz_backend(use_pytz)
    now = now or datetime.datetime.now(tz_backend.utc_tzobj)
    _choices = []
    for tz in timezones:
        tz_str = str(tz)
        now_tz = now.astimezone(tz_backend.to_tzobj(tz_str))
        delta = now_tz.replace(tzinfo=tz_backend.utc_tzobj) - now
        display = "GMT{sign}{gmt_diff} {timezone}".format(
            sign="+" if delta == abs(delta) else "-",
            gmt_diff=str(abs(delta)).zfill(8)[:-3],
            timezone=tz_str.replace("_", " "),
        )
        _choices.append((delta, tz, display))
    _choices.sort(key=lambda x: x[0])
    choices = [(one, two) for zero, one, two in _choices]
    return choices
