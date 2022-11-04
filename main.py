import logging.config

from pyinstr_iakoster.log import get_logging_dict_config

from ctrl_laser.core import Arduino
from ctrl_laser.core import UART

logging.config.dictConfig(get_logging_dict_config(
    info_rotating_file_handler=False,
    error_file_handler=False,
))
logger = logging.getLogger(__name__)

print(UART.get_available_com_ports())

ard = Arduino("COM7")
print(ard.read_pulse_width())
print(ard.write_pulse_width(999))
print(ard.read_pulse_width())
