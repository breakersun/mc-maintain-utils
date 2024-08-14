import os
import zipfile
import shutil
import sys

def process_mcaddon(mcaddon_path):
    # Extract the base name of the .mcaddon file (without extension)
    base_name = os.path.splitext(os.path.basename(mcaddon_path))[0]

    # Create a temporary directory for extraction
    temp_dir = f"temp_{base_name}"
    os.makedirs(temp_dir, exist_ok=True)

    # Create output directory
    output_dir = base_name
    os.makedirs(output_dir, exist_ok=True)

    # Decompress the .mcaddon file
    with zipfile.ZipFile(mcaddon_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Find the 'b' and 'r' folders
    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        if os.path.isdir(item_path):
            if item.startswith('b'):
                create_mcpack(item_path, os.path.join(output_dir, f"b_{base_name}.mcpack"))
            elif item.startswith('r'):
                create_mcpack(item_path, os.path.join(output_dir, f"r_{base_name}.mcpack"))

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

    print(f"Processed files for '{mcaddon_path}' are in the '{output_dir}' folder.")

def create_mcpack(folder_path, output_file):
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(f"Created {output_file}")

def main():
    # Check if command-line arguments are provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_mcaddon_file1> [<path_to_mcaddon_file2> ...]")
        sys.exit(1)

    # Process each .mcaddon file
    for mcaddon_file in sys.argv[1:]:
        if os.path.exists(mcaddon_file) and mcaddon_file.lower().endswith('.mcaddon'):
            print(f"\nProcessing: {mcaddon_file}")
            process_mcaddon(mcaddon_file)
        else:
            print(f"\nInvalid file path or not an .mcaddon file: {mcaddon_file}")
            print("Skipping this file and continuing with the next one (if any).")

if __name__ == "__main__":
    main()
