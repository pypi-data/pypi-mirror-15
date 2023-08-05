import os
import unittest

from simple_monitor_alert.monitor import Monitor
from simple_monitor_alert.lines import Observable, RawItemLine

DIR_PATH = os.path.dirname(os.path.abspath(__file__))


class TestMonitor(unittest.TestCase):

    def test_ok_execute(self):
        monitor = Monitor(os.path.join(DIR_PATH, 'assets', 'ok-monitor.py'))
        monitor.execute()
        item = Observable('test')
        item.add_line(RawItemLine('test.expected=1', self))
        item.add_line(RawItemLine('test.value=1', self))
        self.assertIn((item.name, None), monitor.items.keys())
        self.assertEqual(item, monitor.items[(item.name, None)])

    def test_get_header(self):
        monitor = Monitor(os.path.join(DIR_PATH, 'assets', 'run-every.py'))
        monitor.execute()


if __name__ == '__main__':
    unittest.main()
