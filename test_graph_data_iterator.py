import datetime
import unittest
from unittest.mock import MagicMock
from bson import ObjectId

class GraphData:
    def __init__(self, timestamp: datetime.datetime, value: float):
        self.timestamp = timestamp
        self.value = value

    def __repr__(self):
        return f"GraphData(date={self.date}, value={self.value})"

def dt(year=2026, month=1, day=1, hour=0, minute=0, second=0) -> datetime:
    return datetime.datetime(year, month, day, hour, minute, second)


class TestGraphDataIterator(unittest.TestCase):
    def setUp(self):
        self.graph_data_service = MagicMock()

        self.customer = "test-customer"
        self.installation = "test-installation"

        self.start = datetime.datetime(2026, 1, 1, 0, 0)
        self.end = datetime.datetime(2026, 1, 1, 1, 0)

        self.meter_1 = ObjectId()
        self.meter_2 = ObjectId()

        self.raw_data1 = [
            [self.start, 1.0],
            [self.start + datetime.timedelta(minutes=1), 2.0],
            [self.start + datetime.timedelta(minutes=2), 3.0],
        ]
        self.raw_data2 = [
            [self.start, 1.0],
            [self.start + datetime.timedelta(minutes=1), 2.0],
            [self.start + datetime.timedelta(minutes=2), 3.0],
        ]

    def build_iterator(self, trailing=False):
        from ikologikapi.dataiterator.GraphDataIterator import GraphDataIterator

        iterator = GraphDataIterator(
            customer=self.customer,
            installation=self.installation,
            start_date=self.start,
            end_date=self.end,
            api=self.graph_data_service
        )

        meters = [
            {"id": self.meter_1},
            {"id": self.meter_2},
        ]
        iterator.add_meters(meters)
        iterator.init()

        return iterator

    def _assert_and_print(self, label, iterator, trailing=False):
        current_date = iterator.current_date
        d1 = iterator.get_meter_data(self.meter_1, trailing)
        d2 = iterator.get_meter_data(self.meter_2, trailing)
        has_next = iterator.has_next()

        print(
            f"{label} | Current date: {current_date} "
            f"| Data 1: {d1} | Data 2: {d2} | Has next: {has_next}"
        )
        return current_date, d1, d2, has_next

    # ==================================================================
    # Test 1 — mirrors testIterator_NoShift
    # ==================================================================

    def test_iterator_no_shift(self):
        print("\nTest without date shift")

        # ✅ Mock matches self.api.graph.get_graph_data(...)
        self.graph_data_service.graph.get_graph_data.side_effect = (
            lambda customer, installation, meter_id, data_type, start, end, limit, b:
            self.raw_data1 if meter_id == self.meter_1 else self.raw_data2
        )

        iterator = self.build_iterator()

        self._assert_and_print("Step 0", iterator)

        iterator.next()
        self._assert_and_print("Step 1", iterator)

        iterator.next()
        self._assert_and_print("Step 2", iterator)

        iterator.next()
        _, _, _, has_next = self._assert_and_print("Step 3", iterator)

        self.assertFalse(has_next)
        print("Done")

        # ==================================================================
        # Test 2 — mirrors testIterator_DataShift
        # ==================================================================

    def test_iterator_data_shift(self):
        """meter2 timestamps are shifted +10 seconds relative to meter1."""
        print("\nTest with date shift")

        start = self.start

        self.raw_data1 = [
            [start, 1.0],
            [start + datetime.timedelta(minutes=1), 2.0],
            [start + datetime.timedelta(minutes=2), 3.0],
        ]
        self.raw_data2 = [
            [start + datetime.timedelta(seconds=10), 1.0],
            [start + datetime.timedelta(seconds=10, minutes=1), 2.0],
            [start + datetime.timedelta(seconds=10, minutes=2), 3.0],
        ]

        self.graph_data_service.graph.get_graph_data.side_effect = (
            lambda customer, installation, meter_id, data_type, start, end, limit, b:
            self.raw_data1 if meter_id == self.meter_1 else self.raw_data2
        )

        iterator = self.build_iterator()

        self._assert_and_print("Step 0", iterator)

        iterator.next()
        self._assert_and_print("Step 1", iterator)

        iterator.next()
        self._assert_and_print("Step 2", iterator)

        iterator.next()
        self._assert_and_print("Step 3", iterator)

        iterator.next()
        self._assert_and_print("Step 4", iterator)

        iterator.next()
        self._assert_and_print("Step 5", iterator)

        iterator.next()
        _, _, _, has_next = self._assert_and_print("Step 6", iterator)

        self.assertFalse(has_next)
        print("Done")

    # ==================================================================
    # Test 3 — mirrors testIterator_DataShift_Trailing
    # ==================================================================

    def test_iterator_data_shift_trailing(self):
        """
        Shifted meter2 + trailing=True flag.
        The 'trailing' flag means get_meter_data should carry forward the last
        known value when no new data point exists at the current timestamp.
        """
        print("\nTest with date shift and trailing data")

        start = self.start

        self.raw_data1 = [
            [start, 1.0],
            [start + datetime.timedelta(minutes=1), 2.0],
            [start + datetime.timedelta(minutes=2), 3.0],
        ]
        self.raw_data2 = [
            [start + datetime.timedelta(seconds=10), 1.0],
            [start + datetime.timedelta(seconds=10, minutes=1), 2.0],
            [start + datetime.timedelta(seconds=10, minutes=2), 3.0],
        ]

        self.graph_data_service.graph.get_graph_data.side_effect = (
            lambda customer, installation, meter_id, data_type, start, end, limit, b:
            self.raw_data1 if meter_id == self.meter_1 else self.raw_data2
        )

        iterator = self.build_iterator(trailing=True)

        self._assert_and_print("Step 0", iterator, trailing=True)

        iterator.next()
        self._assert_and_print("Step 1", iterator, trailing=True)

        iterator.next()
        self._assert_and_print("Step 2", iterator, trailing=True)

        iterator.next()
        self._assert_and_print("Step 3", iterator, trailing=True)

        iterator.next()
        self._assert_and_print("Step 4", iterator, trailing=True)

        iterator.next()
        self._assert_and_print("Step 5", iterator, trailing=True)

        iterator.next()
        _, _, _, has_next = self._assert_and_print("Step 6", iterator)

        self.assertFalse(has_next)
        print("Done")
    # ---------------------------------------------------------------------------

    if __name__ == "__main__":
        unittest.main(verbosity=2)
