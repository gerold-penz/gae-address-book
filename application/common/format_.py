#!/usr/bin/env/python
# coding: utf-8
"""
Formathelper
"""

import string
import datetime
import pytz
import decimal


ALLLOWED_ASCII_CHARS = string.digits + string.ascii_letters + "-_ "


def string_to_date(date_string):
    """
    Versucht den übergebenen Text in ein datetime.date-Objekt umzuwandeln

    Falls versehentlich ein datetime.date-Objekt übergeben wird, wird auf die
    Umwandlung verzichtet.
    """

    if not date_string:
        return None

    if date_string.endswith("\\"):
        date_string = date_string[:-1]

    # Wenn date_string länger als yyyy-mm-dd ist
    if len(date_string) > 10:
        date_string = date_string[0:10]

    if isinstance(date_string, datetime.date):
        date_object = date_string
    else:
        if "-" in date_string:
            year, month, day = [
                int(item, 10) for item in date_string.split("-", 3)
            ]
        else:
            day, month, year = [
                int(item, 10) for item in date_string.split(".", 3)
            ]
        date_object = datetime.date(year, month, day)

    return date_object


def string_to_datetime(datetime_string):
    """
    Versucht den übergebenen Text in ein datetime.datetime-Objekt umzuwandeln

    Falls versehentlich ein datetime.datetime-Objekt übergeben wird, wird auf die
    Umwandlung verzichtet.
    """

    if not datetime_string:
        return None

    if isinstance(datetime_string, datetime.datetime):
        return datetime_string
    else:
        if len(datetime_string) == 10:
            # Wenn kein Datum angegeben ist
            datetime_string += " 00:00:00"
        elif "T" in datetime_string:
            # Wenn ISO-String mit 'T'-Connector übergeben wird
            datetime_string = datetime_string.replace("T", " ")

    return datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")


def date_to_iso(date_obj, empty_string_if_none = False):
    """
    Formatiert das übergebene Datum im ISO-Format
    """

    try:
        return date_obj.strftime("%Y-%m-%d")
    except AttributeError:
        if empty_string_if_none:
            return ""
        else:
            return None


def datetime_to_iso(
    datetime_obj,
    empty_string_if_none = False,
    with_timezone = False
):
    """
    Formatiert den übergebene Timestamp im ISO-Format
    """

    try:
        if (
            with_timezone and
            datetime_obj.tzinfo and
            hasattr(datetime_obj.tzinfo, "utcoffset")
        ):
            offset_hours = (
                datetime_obj.tzinfo.utcoffset(datetime_obj).seconds / 60 / 60
            )
            offset_str = "+" if offset_hours >= 0 else "-"
            offset_str += str(offset_hours).rjust(2, "0")
            offset_str += ":00"
        else:
            offset_str = ""
        return datetime_obj.strftime("%Y-%m-%dT%H:%M:%S") + offset_str
    except AttributeError:
        if empty_string_if_none:
            return ""
        else:
            return None


def safe_unicode(value):
    """
    Versucht den übergebenen Wert als Unicode-String zurück zu geben, auch wenn
    dabei Informationen verloren gehen.
    """

    if isinstance(value, unicode):
        return value

    try:
        return unicode(value)
    except UnicodeDecodeError:
        try:
            return unicode(value, "utf-8")
        except UnicodeDecodeError:
            return unicode(value, "iso-8859-15", "ignore")
        except StandardError, err:
            return unicode(repr(value))
    except StandardError, err:
        return unicode(repr(value))


def safe_ascii(text):
    """
    Gibt einen von Sonderzeichen bereinigten Unicode-String zurück.
    """

    text = safe_unicode(text)

    # Umlaute umschreiben
    for searchchar, replacechar in (
        (u"ö", u"oe"),
        (u"Ö", u"Oe"),
        (u"ä", u"ae"),
        (u"Ä", u"Ae"),
        (u"ü", u"ue"),
        (u"Ü", u"Ue"),
        (u"ß", u"ss"),
    ):
        text = text.replace(searchchar, replacechar)

    # Sonderzeichen entfernen
    text_tmp = ""
    for char in text:
        if char in ALLLOWED_ASCII_CHARS:
            text_tmp += char
    text = text_tmp

    # Fertig
    return text


def safe_errormessage(value):
    """
    Gibt den übergebenen Text garantiert Sonderzeichen-bereinigt und
    Unicode zurück.
    """

    return safe_unicode(value)


    # ascii_string = safe_ascii(value)
    #
    # # String wird hier von allen Sonderzeichen bereinigt
    # ascii_string = ascii_string.decode("ascii", "replace")
    # ascii_string = ascii_string.encode("ascii", "replace")
    #
    # # Fertig
    # return unicode(ascii_string)


def string_to_boolean(text):
    """
    Wandelt typische True-/False-Textausdrücke in die Python-typischen
    `True`, `False` oder `None` um.

    - "" --> None
    - " " --> None
    - "none" --> None
    - "null" --> None
    - "true|yes|y|t|1|si" --> True
    - "false|no|n|f|0" --> False
    """

    if text is None:
        return None
    if text is True:
        return True
    if text is False:
        return False

    text = unicode(text).strip().lower()
    if text in ("true", "yes", "y", "t", "1", "si"):
        return True
    elif text in ("false", "no", "n", "f", "0"):
        return False
    elif text in ("", "none", "null"):
        return None
    else:
        raise ValueError("Boolean string expression expected!")


def string_to_integer(text):
    """
    Wandelt einen Text in einen Integer um. Wird keine gültige Zahl übergeben,
    wird None zurück geliefert

    - True --> 1
    - False --> 0
    - "" --> None
    - " " --> None
    - "none" --> None
    - "null" --> None
    - "123" --> 123
    """

    if isinstance(text, int):
        return text
    if text is None:
        return None
    if text is True:
        return 1
    if text is False:
        return 0

    text = unicode(text).strip().lower()
    if text in ("true", "yes", "y", "t", "1"):
        return 1
    elif text in ("false", "no", "n", "f", "0"):
        return 0
    elif text in ("", "none", "null"):
        return None
    else:
        try:
            return int(text)
        except (ValueError, TypeError):
            raise ValueError("Integer string expression expected!")


def string_to_float(text):
    """
    Wandelt einen Text in eine Fließkommazahl um. Wird keine gültige Zahl übergeben,
    wird None zurück geliefert

    - True --> 1.0
    - False --> 0.0
    - "" --> None
    - " " --> None
    - "none" --> None
    - "null" --> None
    - "123" --> 123.0
    - "123.1" --> 123.1
    """

    if isinstance(text, float):
        return text
    if isinstance(text, int):
        return float(text)
    if text is None:
        return None
    if text is True:
        return 1.0
    if text is False:
        return 0.0

    text = unicode(text).strip().lower()
    if text in ("true", "yes", "y", "t", "1"):
        return 1.0
    elif text in ("false", "no", "n", "f", "0"):
        return 0.0
    elif text in ("", "none", "null"):
        return None
    else:
        try:
            return float(text)
        except (ValueError, TypeError):
            raise ValueError("Float string expression expected!")


def string_to_string(text):
    """
    Prüft einen Text auf das Vorkommen von typischen NULL/None-Strings und gibt
    den gestripten Text zurück.

    - True --> "1"
    - False --> None
    - "" --> None
    - " " --> None
    - "none" --> None
    - "null" --> None
    """

    if text is None:
        return None
    if text is True:
        return "1"
    if text is False:
        return None

    text = unicode(text).strip()
    if not text:
        return None
    if text.lower() in ("none", "null"):
        return None
    else:
        return text


def datetime_utc_with_timezone(dt):
    """
    Fügt zum Datetime-Wert die UTC-Zeitzone hinzu
    """

    if dt is None:
        return

    return pytz.UTC.fromutc(dt)


def get_traceback_string():
    """
    Gibt den Traceback-String des letzten Fehlers zurück
    """

    from sys import exc_info as _exc_info
    exc = _exc_info()
    if exc == (None, None, None):
        return ""
    import traceback
    tb = "".join(traceback.format_exception(*exc))

    # Fertig
    return tb


def utf8_to_unicode(text):
    """
    Wandelt einen Text (egal ob UTF-8 oder bereits Unicode) nach Unicode um
    """

    if text is None:
        return None

    if isinstance(text, unicode):
        return text

    if isinstance(text, str):
        return text.decode("utf-8")

    return unicode(text)


def num(number, decimal_places = 2, group_sep = ".", decimal_sep = ","):
    """
    http://code.activestate.com/recipes/499351-format-number-function/
    """

    if number is None:
        return

    number = float(number)
    number = ('%.*f' % (max(0, decimal_places), number)).split('.')

    integer_part = number[0]
    if integer_part[0] == '-':
        sign = integer_part[0]
        integer_part = integer_part[1:]
    else:
        sign = ''

    if len(number) == 2:
        decimal_part = decimal_sep + number[1]
    else:
        decimal_part = ''

    integer_part = list(integer_part)
    c = len(integer_part)

    while c > 3:
        c -= 3
        integer_part.insert(c, group_sep)

    return sign + ''.join(integer_part) + decimal_part


def num_int(number):
    """
    Gibt eine formatierte Zahl ohne Kommastellen zurück

    http://code.activestate.com/recipes/499351-format-number-function/

    :return: String
    """

    number = string_to_integer(number)
    if number is None:
        return ""

    l = list(str(number))
    c = len(l)

    while c > 3:
        c -= 3
        l.insert(c, '.')

    return ''.join(l)


def num_minimal(num_value):
    """
    Gibt die übergebene Zahl als Text zurück. Ist die Zahl ein Integer,
    dann wird keine Kommastelle angezeigt. Ist die Zahl ein Float, dann werden
    so viele Kommastellen angezeigt, so viele nötig sind um den Wert zu
    repräsentieren.

    :return: Unicode-String
    """

    num_value = string_to_float(num_value)
    if num_value is None:
        return ""

    num_value = decimal.Decimal("%s" % num_value)
    if num_value._isinteger():
        formatstr = u"%i"
    else:
        formatstr = u"%s"
    return (formatstr % num_value).replace(u".", u",")


def email_address(email):
    """
    Gibt eine von Sonderzeichen bereinigte E-Mail-Adresse zurück.
    """

    email = string_to_string(email)

    ALLLOWED_CHARS = \
        string.digits + \
        string.ascii_lowercase + \
        "!#$%&'*+-/=?^_`{|}~.@"

    if not email or not email.strip():
        return None

    # Klein schreiben, Zeilenumbrüche und Beistriche entfernen
    email = email.strip().lower()
    if "\r" in email:
        email = email[:email.index("\r")]
    if "\n" in email:
        email = email[:email.index("\n")]
    if "," in email:
        email = email[:email.index(",")]

    # Umlaute umschreiben
    for searchchar, replacechar in (
        (u"ö", u"oe"),
        (u"ä", u"ae"),
        (u"ü", u"ue"),
        (u"ß", u"ss"),
    ):
        email = email.replace(searchchar, replacechar)

    # Sonderzeichen entfernen
    email_tmp = ""
    for char in email:
        if char in ALLLOWED_CHARS:
            email_tmp += char
    email = email_tmp

    # Fertig
    return email
