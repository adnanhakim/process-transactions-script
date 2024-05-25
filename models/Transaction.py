"""
models.transaction
~~~~~~~~~~~~~~

This module contains a Transaction model class.

"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, Self

from enums.TransactionType import TransactionType
from utils.dates import to_datestring


class Transaction:
    """A class representing a transaction model"""

    _name: str
    _buy_sell: TransactionType
    _qty: Decimal
    _buy_date: datetime
    _buy_price: Decimal
    _sell_date: datetime | None
    _sell_price: Decimal | None

    def __init__(
        self: Self,
        name: str,
        buy_sell: TransactionType,
        qty: Decimal,
        buy_date: datetime,
        buy_price: Decimal,
        sell_date: Optional[datetime] = None,
        sell_price: Optional[Decimal] = None,
    ) -> None:
        self._name = name
        self._buy_sell = buy_sell
        self._qty = qty
        self._buy_date = buy_date
        self._buy_price = buy_price
        self._sell_date = sell_date
        self._sell_price = sell_price

    @property
    def name(self: Self) -> str:
        return self._name

    @property
    def buy_sell(self: Self) -> TransactionType:
        return self._buy_sell

    @buy_sell.setter
    def buy_sell(self: Self, buy_sell: TransactionType) -> None:
        self._buy_sell = buy_sell

    @property
    def qty(self: Self) -> Decimal:
        return self._qty

    @qty.setter
    def qty(self: Self, qty: Decimal) -> Decimal:
        self._qty = qty

    @property
    def buy_date(self: Self) -> datetime:
        return self._buy_date

    @property
    def buy_price(self: Self) -> Decimal:
        return self._buy_price

    @property
    def sell_date(self: Self) -> datetime:
        return self._sell_date

    @sell_date.setter
    def sell_date(self: Self, sell_date: datetime) -> None:
        self._sell_date = sell_date

    @property
    def sell_price(self: Self) -> Decimal:
        return self._sell_price

    @sell_price.setter
    def sell_price(self: Self, sell_price: Decimal) -> None:
        self._sell_price = sell_price

    def to_tuple(self: Self) -> tuple[str]:
        """Convert the class to a list"""
        return (
            self._name,
            self._buy_sell.value,
            str(self._qty),
            to_datestring(self._buy_date),
            str(self._buy_price),
            to_datestring(self._sell_date) if self._sell_date is not None else "",
            str(self._sell_price) if self._sell_price is not None else "",
        )

    def __str__(self):
        attrs: str = ", ".join([f"{key}={value}" for key, value in vars(self).items()])
        return "{" + attrs + "}"
