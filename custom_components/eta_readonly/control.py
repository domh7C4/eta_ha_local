# SPDX-License-Identifier: GPL-3.0-only
"""Validate and encode supported ETA writes; no Home Assistant dependencies."""
from decimal import Decimal, InvalidOperation
import re


def check_uri(uri):
    if not isinstance(uri, str) or not re.fullmatch(r"[0-9]+(?:/[0-9]+){4}", uri):
        raise ValueError("Ungültige ETA-Adresse")
    return uri


def decimal_value(value):
    text = str(value).strip().replace(",", ".")
    if len(text) > 64:
        raise ValueError("Wert zu lang")
    try:
        result = Decimal(text)
    except InvalidOperation as err:
        raise ValueError("Numerischen Wert oder gültige Auswahl angeben") from err
    if not result.is_finite() or abs(result) > Decimal("1e18"):
        raise ValueError("Ungültiger numerischer Wert")
    return result


def write_payload(info, value, *, raw=False, begin=None, end=None):
    """Use enum labels or display units by default; raw CAN integers explicitly."""
    if not info.get("writable"):
        raise ValueError("Die ETA-API meldet diesen Datenpunkt als nicht schreibbar")
    choices = info.get("choices", [])
    if choices and not raw:
        matches = [item for item in choices if item["label"] == str(value)]
        if len(matches) != 1:
            raise ValueError("Wert muss einer eindeutigen, vom Gerät gemeldeten Auswahl entsprechen")
        number = decimal_value(matches[0]["raw"])
    else:
        number = decimal_value(value)
        if not raw:
            if info.get("type") == "TEXT":
                raise ValueError("Textwert ohne Auswahlliste benötigt einen expliziten Rohwert")
            scale = decimal_value(info.get("scale_factor", "1"))
            if scale <= 0:
                raise ValueError("Ungültige Skalierung")
            number *= scale
    if number != number.to_integral_value():
        raise ValueError("Wert passt nicht zur Rohwertauflösung des Geräts; keine automatische Rundung")
    if abs(number) > Decimal("1e18"):
        raise ValueError("Rohwert außerhalb des unterstützten Zahlenbereichs")
    if choices and all(number != decimal_value(item["raw"]) for item in choices):
        raise ValueError("Rohwert gehört nicht zu den vom Gerät erlaubten Werten")
    payload = {"value": str(int(number))}
    if (begin is None) != (end is None):
        raise ValueError("Zeitfenster benötigt begin und end gemeinsam")
    if begin is not None:
        if (type(begin) is not int or type(end) is not int
                or not 0 <= begin <= end <= 96):
            raise ValueError("Zeitfenster: ganze Viertelstunden 0 bis 96, begin <= end")
        payload.update(begin=str(begin), end=str(end))
    return payload
