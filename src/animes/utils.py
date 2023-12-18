from dateutil import parser


def convert_date(date_string):
    if not date_string:
        return None
    try:
        return parser.parse(date_string)
    except ValueError:
        return None
