from datetime import datetime, timezone


def parse_twitter_date(date_str):
    return datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y").replace(tzinfo=timezone.utc)

def format_date(date_str):
    return parse_twitter_date(date_str).strftime("%A, %B %d, %Y at %I:%M %p %Z")

def minutes_passed(date_str):
    # Convert the string to a datetime object
    past_time = str_to_date(date_str)

    # Get the current time
    now = datetime.now(timezone.utc)

    # Calculate the difference
    time_difference = now.replace(tzinfo=timezone.utc) - past_time.replace(tzinfo=timezone.utc)

    # Get the total minutes passed
    return time_difference.total_seconds() / 60

def date_to_str(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

def str_to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)