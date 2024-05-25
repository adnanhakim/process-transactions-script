from argparse import Namespace
from typing import Self

from enums.AssetType import AssetType
from services.TransactionService import TransactionService
from utils.dates import get_timestamp


class KfintechService(TransactionService):

    _FIRST_ROW: int = 1
    _NAME_COL: int = 4
    _DATE_COL: int = 5
    _QTY_COL: int = 8
    _PRICE_COL: int = 9
    _DATE_FORMAT: str = "%d-%b-%Y"

    def __init__(self: Self, args: Namespace) -> None:
        output_filename: str | None = args.output_filename
        if output_filename is None:
            output_filename: str = "kfintech_output_" + get_timestamp() + ".xlsx"

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