import datetime
import requests
import pytz


def get_timezone(ip_: str) -> str | None:
    response: dict = requests.get(
        f'https://ipapi.co/{ip_}/json/'
    ).json()

    return response.get('timezone')


def _convert_string_to_timezone(timezone_: str) -> pytz.timezone:
    return pytz.timezone(timezone_)


def get_formatted_time(timezone_: str | None) -> str:
    if timezone_ is None:
        return datetime.datetime.now().strftime("%d:%m:%Y %H:%M:%S")

    timezone_object: pytz.timezone = _convert_string_to_timezone(timezone_)

    return datetime.datetime.now(timezone_object).strftime("%d:%m:%Y %H:%M:%S")


if __name__ == '__main__':
    timezone: str = get_timezone('212.182.18.231')
    time = get_formatted_time(timezone)

    print(time)
