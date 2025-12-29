# -*- coding: utf-8 -*-
"""
@Project: Project Elaine
@File: download_dataset.py
@Author: DanKe
@Description:
    This script utilizes the ModelScope CLI to automate the downloading of
    customized identity datasets. The dataset serves as the raw corpus for
    subsequent fine-tuning and is saved in the 'Yuki_identity_sft' directory.
"""

import os
import subprocess


def download_dataset():
    """
    Downloads the dataset via subprocess by calling the modelscope-cli.
    Configuration:
    - dataset: The unique ID of the dataset on ModelScope (DanKe123abc/Yuki_identity_sft).
    - local_dir: The local directory for storage, mapped to 'Yuki_identity_sft' in the root.
    """
    # Address OpenMP runtime conflicts on Windows environments
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

    # Get the absolute path of the current working directory
    current_dir = os.getcwd()
    # Define the target storage directory
    target_dir = os.path.join(current_dir, 'Yuki_identity_sft')

    # Ensure the target directory exists; create it if it doesn't
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Creating directory: {target_dir}")

    print(f"Starting ModelScope download task...")
    print(f"Target Dataset: DanKe123abc/Yuki_identity_sft")
    print(f"Destination: {target_dir}")

    try:
        # Invoke the system-installed modelscope command line tool
        # --local_dir ensures the dataset is downloaded to the specific folder
        result = subprocess.run(
            ['modelscope', 'download', '--dataset', 'DanKe123abc/Yuki_identity_sft', '--local_dir', target_dir],
            capture_output=True,
            text=True,
            encoding='utf-8'  # Explicitly set encoding to prevent garbled output on Windows consoles
        )

        # Output the standard execution results
        if result.stdout:
            print(f"\n[ModelScope Output]:\n{result.stdout}")

        # Capture potential errors or warnings
        if result.stderr:
            print(f"⚠️  Warning/Error info:\n{result.stderr}")

        if result.returncode == 0:
            print(f"✅ Dataset downloaded successfully! Exit code: {result.returncode}")
        else:
            print(f"❌ Download might not have completed successfully. Exit code: {result.returncode}")

    except FileNotFoundError:
        print("❌ Error: 'modelscope' command not found. Please run 'pip install modelscope' first.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    print("=" * 40)
    print("Project Elaine - Data Preparation Phase")
    print("=" * 40)
    download_dataset()