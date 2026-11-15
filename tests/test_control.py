# SPDX-License-Identifier: GPL-3.0-only
import importlib.util
from pathlib import Path
import unittest
from test_parser import m, wrap

path = Path(__file__).resolve().parents[1] / "custom_components/eta_readonly/control.py"
spec = importlib.util.spec_from_file_location("eta_control", path)
control = importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)

TEXT = {"writable": True, "type": "TEXT", "scale_factor": "1", "choices": [
    {"label": "Aus", "raw": "1802"}, {"label": "Ein", "raw": "1803"}]}
NUMBER = {"writable": True, "type": "NUMBER", "scale_factor": "10", "choices": []}


class ControlTests(unittest.TestCase):
    def test_metadata(self):
        info = m.varinfo(wrap('<varInfo><variable uri="40/10021/0/0/12080" isWritable="1" scaleFactor="1">'
                             '<type>TEXT</type><validValues><value strValue="Aus">1802</value>'
                             '<value strValue="Ein">1803</value></validValues></variable></varInfo>'))
        self.assertTrue(info["writable"])
        self.assertEqual(info["choices"], TEXT["choices"])

    def test_readonly_or_missing_permission(self):
        for info in ({**NUMBER, "writable": False}, {}):
            with self.assertRaises(ValueError):
                control.write_payload(info, 40)

    def test_enum_and_raw_enum(self):
        self.assertEqual(control.write_payload(TEXT, "Ein"), {"value": "1803"})
        self.assertEqual(control.write_payload(TEXT, "1802", raw=True), {"value": "1802"})
        with self.assertRaises(ValueError):
            control.write_payload(TEXT, "An")
        with self.assertRaises(ValueError):
            control.write_payload(TEXT, "9999", raw=True)

    def test_numeric_scale_and_raw(self):
        self.assertEqual(control.write_payload(NUMBER, "40,5"), {"value": "405"})
        self.assertEqual(control.write_payload(NUMBER, "405", raw=True), {"value": "405"})
        self.assertEqual(control.write_payload(NUMBER, "-2.5"), {"value": "-25"})

    def test_invalid_numbers_and_resolution(self):
        for value in ("NaN", "Infinity", "1e99999", "40.555", "not a number"):
            with self.assertRaises(ValueError):
                control.write_payload(NUMBER, value)

    def test_time_slot(self):
        self.assertEqual(control.write_payload(NUMBER, 40, begin=0, end=48),
                         {"value": "400", "begin": "0", "end": "48"})
        for args in ({"begin": 1}, {"end": 1}, {"begin": -1, "end": 5},
                     {"begin": 49, "end": 48}, {"begin": 0, "end": 97},
                     {"begin": 0.5, "end": 10}):
            with self.assertRaises(ValueError):
                control.write_payload(NUMBER, 40, **args)

    def test_uri_and_metadata_validation(self):
        self.assertEqual(control.check_uri("112/10021/0/0/12080"), "112/10021/0/0/12080")
        for uri in ("../user/api", "112/1/0/0/1?x=2", "/112/1/0/0/1", "1/2/3"):
            with self.assertRaises(ValueError):
                control.check_uri(uri)
        for body in ('<success/>', '<varInfo><variable scaleFactor="0"/></varInfo>',
                     '<varInfo><variable scaleFactor="bad"/></varInfo>',
                     '<varInfo><variable><validValues><value>bad</value></validValues></variable></varInfo>'):
            with self.assertRaises(ValueError):
                m.varinfo(wrap(body))
