# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import importlib.util
import unittest
p = Path(__file__).resolve().parents[1] / 'custom_components' / 'eta_readonly'
spec = importlib.util.spec_from_file_location('eta_parser', p / 'parser.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
def wrap(body): return '<eta xmlns="http://www.eta.co.at/rest/v1">'+body+'</eta>'
class ParserTests(unittest.TestCase):
 def test_menu(self):
  self.assertEqual(m.menu(wrap('<menu><fub name="Kessel"><object name="Temperatur" uri="/112/10021/0/0/1"/></fub></menu>')),{'112/10021/0/0/1':'Kessel > Temperatur'})
 def test_scale(self):
  v=m.value(wrap('<value unit="°C" strValue="65,3" scaleFactor="10" advTextOffset="0">653</value>')); self.assertEqual(v['state'],65.3); self.assertEqual(v['unit'],'°C')
 def test_text(self):
  v=m.value(wrap('<value strValue="Off" scaleFactor="1" advTextOffset="1802">1802</value>')); self.assertEqual(v['state'],'Off'); self.assertIsNone(v['unit'])
 def test_numeric_text_enum(self):
  self.assertEqual(m.value(wrap('<value strValue="1" advTextOffset="1802">1803</value>'))['state'],'1')
 def test_negative(self):
  self.assertEqual(m.value(wrap('<value strValue="-2,5" scaleFactor="10">-25</value>'))['state'],-2.5)
 def test_bad_xml(self):
  for data in ('<eta>', '<html/>',wrap('<success/>'),'<!DOCTYPE eta>'+wrap('<value/>')):
   with self.assertRaises(ValueError): m.value(data)
 def test_zero_scale(self):
  with self.assertRaises(ValueError): m.value(wrap('<value scaleFactor="0">1</value>'))
