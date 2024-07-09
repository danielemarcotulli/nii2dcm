"""
nii2dcm entrypoint code and command line interface (CLI)
"""

import sys
import argparse
from pathlib import Path
from nii2dcm.run import run_nii2dcm
from nii2dcm._version import __version__


def cli(args=None):
    """
    Run nii2dcm via command line
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="nii2dcm",
        description="nii2dcm - NIfTI file to DICOM conversion"
    )
    parser.add_argument("input_file", type=str, help="[.nii/.nii.gz] input NIfTI file")
    parser.add_argument("output_dir", type=str, help="[directory] output DICOM path")
    parser.add_argument(
        "-d", "--dicom_type",
        type=str,
        help="[string] type of DICOM. Available types: MR, SVR."
    )
    parser.add_argument('--study-date', type=str, help='Study Date')
    parser.add_argument('--study-id', type=str, help='StudyID')
    parser.add_argument("-r", "--ref_dicom", type=str, help="[.dcm] Reference DICOM file for Attribute transfer")
    parser.add_argument("-v", "--version", action="version", version=__version__)

    args = parser.parse_args()

    # Collect new metadata
    new_metadata = {
        'StudyDate': args.study_date,
        'StudyID': args.study_id
    }

    # Remove None values from metadata
    new_metadata = {k: v for k, v in new_metadata.items() if v is not None}

    # Load the NIfTI file
    nii_img = nib.load(args.nifti_file)
    img_data = nii_img.get_fdata()

    # Initialize DICOM object with new metadata
    dicom_mri = DicomMRI(new_metadata=new_metadata)

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Iterate over each slice and write it as a DICOM file
    for slice_index in range(img_data.shape[2]):
        write_slice(dicom_mri, img_data, slice_index, args.output_dir, new_metadata)

if __name__ == '__main__':
    main()

    args = parser.parse_args()

    input_file = Path(args.input_file)  # TODO: add check that file is .nii/.nii.gz
    output_dir = Path(args.output_dir)  # TODO: add check that this is directory

    if not input_file.exists():
        print(f"Input file '{input_file}' not found")
        raise SystemExit(1)

    if not output_dir.exists():
        print(f"Output directory '{output_dir}' does not exist")
        raise SystemExit(1)

    # Coding of optional file checks below is quite verbose
    if args.dicom_type is not None:
        dicom_type = args.dicom_type  # TODO: add check that supplied dicom_type is permitted
    elif args.dicom_type is None:
        dicom_type = None

    if args.ref_dicom is not None:
        ref_dicom_file = Path(args.ref_dicom)   # TODO: add check that file is DICOM
    elif args.ref_dicom is None:
        ref_dicom_file = None

    # execute nii2dcm
    run_nii2dcm(
        input_file,
        output_dir,
        dicom_type,
        ref_dicom_file
    )


if __name__ == "__main__":
    sys.exit(cli())
