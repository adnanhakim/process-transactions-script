"""
services.camsservice
~~~~~~~~~~~~~~

This module contains a class to process CAMS transactions

"""

from argparse import Namespace
from typing import Self

from enums.AssetType import AssetType
from services.TransactionService import TransactionService
from utils.dates import get_timestamp


class CamsService(TransactionService):
    """Class to process Zerodha transactions"""

    _FIRST_ROW: int = 1
    _NAME_COL: int = 5
    _DATE_COL: int = 7
    _QTY_COL: int = 11
    _PRICE_COL: int = 12
    _DATE_FORMAT: str = "%d-%b-%Y"

    def __init__(self: Self, args: Namespace) -> None:
        output_filename: str | None = args.output_filename
        if output_filename is None:
            output_filename: str = "cams_output_" + get_timestamp() + ".xlsx"

        super().__init__(
            self._FIRST_ROW,
            self._NAME_COL,
            self._DATE_COL,
            self._QTY_COL,
            self._PRICE_COL,
            self._DATE_FORMAT,
            args.input_filename,
            output_filename,
            AssetType.MUTUAL_FUND,
        )
