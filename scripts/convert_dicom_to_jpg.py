"""
Convert DICOM CT images to JPG format for web display
Applies proper windowing for lung imaging
"""
import pydicom
import numpy as np
from PIL import Image
import os
import glob

def apply_windowing(pixel_array, window_center, window_width):
    """Apply window/level adjustment to CT image"""
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2

    windowed = np.clip(pixel_array, img_min, img_max)
    windowed = ((windowed - img_min) / (img_max - img_min) * 255.0).astype(np.uint8)

    return windowed

def convert_dicom_to_jpg(dicom_path, output_path, window_center=-600, window_width=1500):
    """
    Convert DICOM to JPG with lung window settings

    Args:
        dicom_path: Path to DICOM file
        output_path: Path to save JPG
        window_center: HU center for windowing (default -600 for lung)
        window_width: HU width for windowing (default 1500 for lung)
    """
    try:
        # Read DICOM
        ds = pydicom.dcmread(dicom_path)

        # Get pixel array
        pixel_array = ds.pixel_array

        # Apply rescale slope/intercept to get Hounsfield Units
        if hasattr(ds, 'RescaleSlope') and hasattr(ds, 'RescaleIntercept'):
            pixel_array = pixel_array * ds.RescaleSlope + ds.RescaleIntercept

        # Apply windowing
        windowed_image = apply_windowing(pixel_array, window_center, window_width)

        # Convert to PIL Image
        img = Image.fromarray(windowed_image)

        # Save as JPG
        img.save(output_path, 'JPEG', quality=90)

        return True, f"Converted: {os.path.basename(dicom_path)}"

    except Exception as e:
        return False, f"Error with {dicom_path}: {str(e)}"

def main():
    """Extract representative CT slices from the downloaded DICOM series"""

    # Paths
    ct_series_dir = "example_files/dicom_data/1.3.6.1.4.1.14519.5.2.1.7014.4598.184537120112103188540038348452"
    output_dir = "backend/static/imaging"
    thumbnails_dir = os.path.join(output_dir, "thumbnails")
    full_dir = os.path.join(output_dir, "full")

    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(thumbnails_dir, exist_ok=True)
    os.makedirs(full_dir, exist_ok=True)

    # Get all DICOM files
    dicom_files = sorted(glob.glob(os.path.join(ct_series_dir, "*.dcm")))

    if not dicom_files:
        print(f"No DICOM files found in {ct_series_dir}")
        return

    total_slices = len(dicom_files)
    print(f"Found {total_slices} CT slices")

    # Extract representative slices (evenly distributed)
    # Get slices at 20%, 30%, 40%, 50%, 60%, 70%, 80% through the series
    percentages = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]
    selected_indices = [int(total_slices * p) for p in percentages]

    print(f"\nExtracting {len(selected_indices)} representative slices...")

    for i, idx in enumerate(selected_indices, 1):
        dicom_path = dicom_files[idx]

        # Output filenames
        output_name = f"lung_ct_{i:03d}.jpg"
        thumb_name = f"lung_ct_{i:03d}_thumb.jpg"

        full_path = os.path.join(full_dir, output_name)
        thumb_path = os.path.join(thumbnails_dir, thumb_name)

        # Convert full size
        success, msg = convert_dicom_to_jpg(dicom_path, full_path)
        if success:
            print(f"  [{i}/{len(selected_indices)}] {msg}")

            # Create thumbnail (resize to 300x300)
            img = Image.open(full_path)
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            img.save(thumb_path, 'JPEG', quality=85)
        else:
            print(f"  [{i}/{len(selected_indices)}] {msg}")

    print(f"\n✓ Conversion complete!")
    print(f"  Full images: {full_dir}")
    print(f"  Thumbnails: {thumbnails_dir}")
    print(f"\nGenerated {len(selected_indices)} CT images for dashboard display")

if __name__ == "__main__":
    main()