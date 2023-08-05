from __future__ import unicode_literals
from __future__ import print_function

import unittest

from mock import patch
from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.policies.appsensor import SqliSensor

class SqliSensorTest(unittest.TestCase):

    def create_default_sensor_test(self):
        sensor = SqliSensor()
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.exclude_headers, False)
        self.assertEqual(sensor.exclude_forms, False)
        self.assertEqual(sensor.exclude_cookies, False)
        self.assertEqual(sensor.dp, "sqli")
        self.assertEqual(sensor.libinjection, False)
        self.assertEqual(sensor.active_pattern_ids, {})
        self.assertEqual(sensor.exclusions, {})
