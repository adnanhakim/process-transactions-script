import logging
from decimal import Decimal
from typing import Self

from tabulate import tabulate

from enums.AssetType import AssetType
from enums.TransactionType import TransactionType
from models.Transaction import Transaction
from models.TransactionRow import TransactionRow
from utils.dates import to_datetime
from utils.files import read_excel_to_list, write_list_to_excel


class TransactionService:
    """Class to process transactions with implementation"""

    _first_row: int
    _name_col: int
    _date_col: int
    _qty_col: int
    _price_col: int
    _date_format: str
    _input_filename: str
    _output_filename: str
    _asset_type: AssetType

    def __init__(
        self: Self,
        first_row: int,
        name_col: int,
        date_col: int,
        qty_col: int,
        price_col: int,
        date_format: str,
        input_filename: str,
        output_filename: str,
        asset_type: AssetType,
    ) -> None:
        self._first_row = first_row
        self._name_col = name_col
        self._date_col = date_col
        self._qty_col = qty_col
        self._price_col = price_col
        self._date_format = date_format
        self._input_filename = input_filename
        self._output_filename = output_filename
        self._asset_type = asset_type

    def execute(self: Self):
        txn_rows: list = self._read_file()

        txn_row_map: dict[str : list[TransactionRow]] = self._create_txn_row_map(
            txn_rows
        )

        # Create transactions
        final_txns: list[Transaction] = []
        for name, txn_rows in txn_row_map.items():
            # Segregate into buy/sell transactions
            buy_txns: list[TransactionRow] = self._get_buy_txns(txn_rows)
            sell_txns: list[TransactionRow] = self._get_sell_txns(txn_rows)

            final_txns.extend(self._process_transactions(name, buy_txns, sell_txns))

        # Sort transactions based on date
        sorted_txns: list[Transaction] = sorted(
            final_txns, key=lambda x: (x.buy_date, x.name)
        )

        # Create a list and print it
        tuple_list: list[tuple] = self._create_list(sorted_txns)

        # Get sheet name
        sheet_name: str = self._get_sheet_name()

        # Save to excel
        write_list_to_excel(tuple_list, self._output_filename, sheet_name)

    def _read_file(self: Self):
        return read_excel_to_list(self._input_filename)

    def _create_txn_row_map(
        self: Self, txn_rows: list[TransactionRow]
    ) -> dict[str : list[TransactionRow]]:
        txn_row_map: dict[str : list[TransactionRow]] = {}

        for txn in txn_rows[self._first_row :]:
            if txn[self._qty_col] is None or txn[self._qty_col] == 0:
                continue

            name: str = txn[self._name_col].strip()

            txn_row = TransactionRow(
                qty=Decimal(str(txn[self._qty_col])),
                date=to_datetime(txn[self._date_col], self._date_format),
                price=Decimal(str(txn[self._price_col])),
            )

            if name in txn_row_map:
                txn_row_map[name].append(txn_row)
            else:
                txn_row_map[name] = [txn_row]

        return txn_row_map

    def _process_transactions(
        self: Self,
        name: str,
        buy_txns: list[TransactionRow],
        sell_txns: list[TransactionRow],
    ):
        logging.info("Processing transactions for %s", name)

        final_txns: list[Transaction] = []

        # Adding all buy transactions
        for buy_txn in buy_txns:
            final_txns.append(
                Transaction(
                    name=name,
                    buy_sell=TransactionType.BUY,
                    qty=buy_txn.qty,
                    buy_date=buy_txn.date,
                    buy_price=buy_txn.price,
                )
            )

        # Booking sell transactions
        self._book_transactions(sell_txns, final_txns)

        # Print summary
        self._print_summary(final_txns)

        return final_txns

    def _get_buy_txns(
        self: Self, transaction_rows: list[TransactionRow]
    ) -> list[TransactionRow]:
        buy_txns: list[TransactionRow] = []

        for txn_row in transaction_rows:
            if txn_row.qty > 0:
                buy_txns.append(txn_row)

        logging.debug("Found %s buy transactions", len(buy_txns))

        return buy_txns

    def _get_sell_txns(
        self: Self, transaction_rows: list[TransactionRow]
    ) -> list[TransactionRow]:
        sell_txns: list[TransactionRow] = []

        for txn_row in transaction_rows:
            if txn_row.qty < 0:
                sell_txns.append(txn_row)

        logging.debug("Found %s sell transactions", len(sell_txns))

        return sell_txns

    def _book_transactions(
        self: Self, sell_txns: list[TransactionRow], final_txns: list[Transaction]
    ):
        for sell_txn in sell_txns:
            qty_to_sell: Decimal = abs(sell_txn.qty)

            for index, txn in enumerate(final_txns):
                # Ignore already sold transactions
                if txn.buy_sell is TransactionType.SELL:
                    continue

                # Sufficient quantity to sell -> sell the whole transaction
                if qty_to_sell >= txn.qty:
                    txn.buy_sell = TransactionType.SELL
                    txn.sell_date = sell_txn.date
                    txn.sell_price = sell_txn.price

                    # Reduce quantity left to sell
                    qty_to_sell -= txn.qty

                    # If quantity is zero, end the loop
                    if qty_to_sell == 0:
                        break

                # Insufficient quantity to sell -> split the transaction into 2
                elif qty_to_sell < txn.qty:
                    total_qty: Decimal = txn.qty

                    # Fully sell the existing transaction and reduce the quantity
                    txn.buy_sell = TransactionType.SELL
                    txn.qty = qty_to_sell
                    txn.sell_date = sell_txn.date
                    txn.sell_price = sell_txn.price

                    # Create a buy transaction with the unsold quantity
                    final_txns.insert(
                        index + 1,
                        Transaction(
                            name=txn.name,
                            buy_sell=TransactionType.BUY,
                            qty=total_qty - qty_to_sell,
                            buy_date=txn.buy_date,
                            buy_price=txn.buy_price,
                        ),
                    )

                    # No more quantity left to sell, end the loop
                    break

    def _print_summary(self: Self, transactions: list[Transaction]):
        buy_qty = 0
        sell_qty = 0

        for txn in transactions:
            if txn.buy_sell == TransactionType.BUY:
                buy_qty += txn.qty
            else:
                sell_qty += txn.qty

        logging.debug("Total txn count: %s", len(transactions))
        logging.debug("Total qty held: %s", buy_qty)
        logging.debug("Total qty booked: %s", sell_qty)

    def _create_list(self: Self, transactions: list[Transaction]):
        logging.info("Final count of all transactions: %s", len(transactions))

        tuple_list: list[tuple] = []
        tuple_list.append(
            [
                "Fund Name",
                "Buy/Sell",
                "Units",
                "Buy Date",
                "Buy Price",
                "Sell Date",
                "Sell Price",
            ]
        )
        for txn in transactions:
            tuple_list.append(txn.to_tuple())

        print(tabulate(tuple_list[1:], headers=tuple_list[0]))

        return tuple_list

    def _get_sheet_name(self: Self):
        if self._asset_type is AssetType.MUTUAL_FUND:
            return "MF Data"
        elif self._asset_type is AssetType.STOCK:
            return "Stock Data"
        else:
            return "Sheet1"
