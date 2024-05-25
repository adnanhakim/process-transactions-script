"""
main
~~~~~~~~~~~~~~

This module contains the main python runner class.
Run python3 main.py --help for more information.

"""

import logging
from argparse import ArgumentParser, ArgumentTypeError, Namespace, _SubParsersAction

from services.CamsService import CamsService
from services.KfintechService import KfintechService
from utils import logger

parser = ArgumentParser(
    description="A Python script that processes transactions from different brokerages and repositories"
)

subparsers: _SubParsersAction = parser.add_subparsers(
    dest="command",
    help="type of command to be executed",
)

parser_process: ArgumentParser = subparsers.add_parser(
    "process", help="process buy and sell transactions"
)

parser_process.add_argument(
    "company",
    choices=["cams", "kfintech"],
    help="name of brokerage or repository",
)

parser_process.add_argument(
    "-i",
    "--input-filename",
    metavar="FILENAME",
    type=str,
    required=True,
    help="input file name of transactions sheet",
)

parser_process.add_argument(
    "-o",
    "--output-filename",
    metavar="FILENAME",
    type=str,
    help="output file name of transactions sheet",
)

parser_process.add_argument(
    "--verbose",
    dest="verbose",
    action="store_true",
    help="verbose mode for detailed logging",
)

args: Namespace = parser.parse_args()

# Setup logging
logger.setup_logging(args.verbose)

logging.debug(args)

command = args.command

if command == "process":
    if args.company == "cams":
        CamsService(args).execute()
    elif args.company == "kfintech":
        KfintechService(args).execute()
else:
    raise ArgumentTypeError(
        f"Unsupported command '{args.command}'. Run --help for more information."
    )
