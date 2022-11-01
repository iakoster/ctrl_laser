import pandas as pd

from pyinstr_iakoster.core import Code
from pyinstr_iakoster.communication import (
    PackageFormat,
    MessageFormat,
    RegisterMap,
    FieldSetter,
)


PF = PackageFormat(
    RegisterMap(
        pd.DataFrame(
            columns=RegisterMap.EXPECTED_COLUMNS,
            data=[
                [None, "firmware_ver", "std", 0x03, "ro", 4, None, ""],
                [None, "update_date", "std", 0x04, "ro", 4, None, ""],
                [None, "frequency", "std", 0x05, "ro", 4, None, ""],
                [None, "regime", "std", 0x10, "rw", 1, "B", ""],
                [None, "pulse_period", "std", 0x11, "rw", 4, None, ""],
                [None, "pulse_width", "std", 0x12, "rw", 4, None, ""]
            ]
        )
    ),
    std=MessageFormat(
        response=FieldSetter.response(
            fmt="B", codes={0: Code.OK}, default=Code.ERROR
        ),
        address=FieldSetter.address(fmt="B"),
        operation=FieldSetter.operation(fmt="B", desc_dict={"r": 0, "w": 1}),
        data_length=FieldSetter.data_length(fmt="B"),
        data=FieldSetter.data(expected=-1, fmt=">I"),
    )
)
