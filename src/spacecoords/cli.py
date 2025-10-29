import argparse


def main():
    import spacecoords as sc

    parser = argparse.ArgumentParser(description="Download files")
    parser.add_argument("de_kernel")
    parser.add_argument("output")
    args = parser.parse_args()

    sc.download.naif_kernel(
        kernel_path=sc.download.KERNEL_PATHS["planetary"] + args.de_kernel,
        output_file=args.output,
        progress=True,
    )
