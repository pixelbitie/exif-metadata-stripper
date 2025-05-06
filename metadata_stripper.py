import os
import piexif
from PIL import Image

# Privacy-sensitive tags to remove (in piexif format)
SENSITIVE_TAGS = {
    "0th": [piexif.ImageIFD.Make, piexif.ImageIFD.Model, piexif.ImageIFD.Software, piexif.ImageIFD.Artist],
    "Exif": [piexif.ExifIFD.DateTimeOriginal, piexif.ExifIFD.LensMake, piexif.ExifIFD.LensModel],
    "GPS": "all",
    "1st": [],  # Typically thumbnail data — optional
}

def strip_exif_jpeg(image_path, keep_safe=True):
    try:
        # Open the image with Pillow (PIL)
        img = Image.open(image_path)

        # Load the EXIF data
        exif_dict = piexif.load(img.info['exif']) if 'exif' in img.info else {}

        if keep_safe:
            # Selectively remove only sensitive tags
            for ifd in SENSITIVE_TAGS:
                if SENSITIVE_TAGS[ifd] == "all":
                    exif_dict[ifd] = {}
                else:
                    for tag in SENSITIVE_TAGS[ifd]:
                        exif_dict[ifd].pop(tag, None)

            new_exif = piexif.dump(exif_dict)
        else:
            # Remove all metadata
            new_exif = piexif.dump({})  # Empty EXIF

        # Save the image back with the new EXIF data
        img.save(image_path, "JPEG", exif=new_exif)

        print(f"Metadata successfully removed from {image_path}")

    except Exception as e:
        print(f"Failed to process {image_path}: {e}")

def process_folder(folder_path, keep_safe):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            strip_exif_jpeg(full_path, keep_safe)

def main():
    print("This program strips privacy-sensitive metadata from .jpg or .jpeg files.")
    choice = input("Strip metadata from a (1) single image or (2) a folder? Enter 1 or 2: ").strip()
    
    if choice not in {'1', '2'}:
        print("Invalid input. Please enter 1 or 2.")
        return
    
    keep_safe = input("Strip only privacy-sensitive data? (y/n): ").strip().lower() == 'y'
    
    # individual photo strip
    if choice == '1':
        file_path = input("Enter path to JPEG file: ").strip()
        if os.path.isfile(file_path) and file_path.lower().endswith(('.jpg', '.jpeg')):
            strip_exif_jpeg(file_path, keep_safe)
        else:
            print("Invalid file. Please provide a valid .jpg or .jpeg file.")
    
    # folder data strip (will skip all non-.jpg or .jpeg files)
    elif choice == '2':
        folder_path = input("Enter folder path: ").strip()
        if os.path.isdir(folder_path):
            process_folder(folder_path, keep_safe)
        else:
            print("Invalid folder path.")

if __name__ == "__main__":
    main()
