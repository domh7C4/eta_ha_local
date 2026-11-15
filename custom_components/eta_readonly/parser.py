# SPDX-License-Identifier: GPL-3.0-only
"""Parse ETA REST v1 XML without depending on Home Assistant."""
from decimal import Decimal, InvalidOperation
import re
from xml.etree import ElementTree as ET

NS = "{http://www.eta.co.at/rest/v1}"

def xml_root(data):
    if "<!DOCTYPE" in data.upper() or "<!ENTITY" in data.upper():
        raise ValueError("DTD/entities are not supported")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as err:
        raise ValueError("Malformed ETA XML") from err
    if root.tag != NS + "eta":
        raise ValueError("Not an ETA REST XML response")
    return root

def menu(data):
    root = xml_root(data)
    node = root.find(NS + "menu")
    if node is None:
        raise ValueError("Missing menu")
    result = {}
    def walk(element, names):
        for child in element:
            path = names + [child.get("name", "?")]
            uri = child.get("uri", "").strip("/")
            if re.fullmatch(r"[0-9]+(?:/[0-9]+){4}", uri):
                result[uri] = " > ".join(path)
            walk(child, path)
    walk(node, [])
    return result

def value(data):
    node = xml_root(data).find(NS + "value")
    if node is None:
        raise ValueError("Missing value")
    raw = (node.text or "").strip()
    formatted = node.get("strValue", raw)
    unit = node.get("unit", "").strip()
    offset = int(node.get("advTextOffset", "0"))
    # Text states must retain their label, not the internal numeric enum.
    numeric = None
    try:
        scale = Decimal(node.get("scaleFactor", "1"))
        if not scale.is_finite() or scale == 0:
            raise ValueError("Invalid scale factor")
        number = Decimal(raw) / scale
        display = Decimal(formatted.replace(",", "."))
        if offset == 0 and number.is_finite() and display.is_finite():
            numeric = float(number)
    except InvalidOperation:
        pass
    return {"state": numeric if numeric is not None else formatted[:255],
            "unit": unit if numeric is not None else None,
            "raw": raw, "formatted": formatted, "scale_factor": node.get("scaleFactor", "1"),
            "text_offset": offset}
