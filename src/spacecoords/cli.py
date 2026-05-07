import argparse
import spacecoords as sc


def build_naif_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("naif_kernel", help="Download NAIF Kernels")
    parser.add_argument(
        "kernel_type",
        choices=list(sc.download.KERNEL_PATHS.keys()),
        help="Type of kernel (determines location on server)",
    )
    parser.add_argument("kernel_name", help="Kernel filename")
    parser.add_argument("output_file", help="Path to output file")


def build_mpcorb(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("mpcorb_database", help="Download MPCORB database")
    parser.add_argument("output_file", help="Path to output file")


def main() -> None:

    parser = argparse.ArgumentParser(description="Download files")
    subparsers = parser.add_subparsers(
        help="Available download interfaces", dest="command"
    )

    build_naif_parser(subparsers)
    build_mpcorb(subparsers)

    args = parser.parse_args()

    if args.command == "naif_kernel":
        sc.download.naif_kernel_main(args)
    elif args.command == "mpcorb_database":
        sc.download.mpcorb_main(args)
