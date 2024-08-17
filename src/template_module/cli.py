import argparse
import importlib
import pkgutil
from typing import Any, Dict

from . import PACKAGE_NAME


def load_subcommands() -> Dict[str, Any]:
    """Find and return subcommands names and cli parsers for each."""
    subcommands = {}
    package = importlib.import_module(".commands", package=PACKAGE_NAME)
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package.__name__}.{name}")
        if hasattr(module, "setup_parser"):
            parser = module.setup_parser()
            subcommands[name] = {"parser": parser, "module": module}
    return subcommands


def setup_main_parser(subcommands: Dict[str, Any]) -> argparse.ArgumentParser:
    """Set up the top level cli argument parser using the provided subcommands."""
    parser = argparse.ArgumentParser(description="Xpedition / KYN netlist tools")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")
    for name, subcommand in subcommands.items():
        subparsers.add_parser(name, parents=[subcommand["parser"]], add_help=False)
    return parser


def main():
    # Load subcommands from the commands folder
    subcommands = load_subcommands()

    # Set up the main parser with the loaded subcommands
    parser = setup_main_parser(subcommands)

    # Parse the arguments
    args = parser.parse_args()

    # Execute the corresponding function for the selected subcommand
    if args.command in subcommands:
        subcommands[args.command]["module"].do_something(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
