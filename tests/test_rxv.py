# SPDX-FileCopyrightText: 2013 Joanna Tustanowska & Wojciech Bederski
#
# SPDX-License-Identifier: BSD-3-Clause

from io import open

import requests_mock
import testtools

import rxv

FAKE_IP = '10.0.0.0'
DESC_XML = 'http://%s/YamahaRemoteControl/desc.xml' % FAKE_IP


def sample_content(name):
    with open('tests/samples/%s' % name, encoding='utf-8') as f:
        return f.read()


class TestRXV(testtools.TestCase):

    @requests_mock.mock()
    def test_basic_object(self, m):
        m.get(DESC_XML, text=sample_content('rx-v675-desc.xml'))
        rec = rxv.RXV(FAKE_IP)
        self.assertEqual(
            rec.ctrl_url,
            'http://%s/YamahaRemoteControl/ctrl' % FAKE_IP)
        self.assertEqual(
            rec.unit_desc_url,
            'http://%s/YamahaRemoteControl/desc.xml' % FAKE_IP)


class TestDesc(testtools.TestCase):

    @requests_mock.mock()
    def test_discover_zones(self, m):
        m.get(DESC_XML, text=sample_content('rx-v675-desc.xml'))
        rec = rxv.RXV(FAKE_IP)
        zones = rec.zone_controllers()
        self.assertEqual(len(zones), 2, zones)
        self.assertEqual(zones[0].zone, "Main_Zone")
        self.assertEqual(zones[1].zone, "Zone_2")
