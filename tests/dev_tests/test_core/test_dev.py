import unittest

from tests.dev_tests.variables import PORT

from ctrl_laser.core import Arduino


class TestArduino(unittest.TestCase):

    dev: Arduino

    @classmethod
    def setUpClass(cls) -> None:
        cls.dev = Arduino(PORT)

    def set_to_default(self) -> None:
        self.dev.write_regime(0)
        self.dev.write_pulse_width(1)
        self.dev.write_pulse_period(1000)

    def test_read(self) -> None:
        self.set_to_default()
        for method, result in (
            (self.dev.read_firmware_version, [0, 0, 0, 1]),
            (self.dev.read_update_date, [2022, 11, 4]),
            (self.dev.read_timer_frequency, 50000),
            (self.dev.read_regime, 0),
            (self.dev.read_pulse_period, 1000),
            (self.dev.read_pulse_width, 1),
        ):
            with self.subTest(method=method.__name__):
                self.assertEqual(result, method())

    def test_write(self) -> None:
        for write_method, value, read_method in (
                (self.dev.write_regime, 2, self.dev.read_regime),
                (self.dev.write_pulse_period, 500, self.dev.read_pulse_period),
                (self.dev.write_pulse_width, 100, self.dev.read_pulse_width),
        ):
            with self.subTest(method=write_method.__name__):
                self.assertEqual(value, write_method(value))
                self.assertEqual(value, read_method())

    def test_validate_pulse_width(self) -> None:
        self.dev.write_pulse_period(200)

        for width in (198, 199, 200, 201, 500):
            self.assertEqual(198, self.dev.write_pulse_width(width))

        self.dev.write_pulse_period(100)
        self.assertEqual(98, self.dev.read_pulse_width())

    def test_validate_pulse_period(self) -> None:
        self.assertEqual(2, self.dev.write_pulse_period(1))
        self.assertEqual(0, self.dev.read_pulse_width())
