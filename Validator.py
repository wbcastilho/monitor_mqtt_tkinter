import re


class Validator:
    @staticmethod
    def validate_ip(value):
        match = re.match(
            r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)"
            r"{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",
            value)

        return bool(match)
