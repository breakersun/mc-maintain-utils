import os
import json
from zipfile import ZipFile
import sys  # Import sys module for command line arguments
import shutil

def get_pack_info(pack_file):
  """Decompresses a resource pack (.mcpack) file and retrieves information from manifest.json.

  Args:
    pack_file (str): Path to the .mcpack file.

  Returns:
    dict: A dictionary containing information from manifest.json and ".comment" data,
         or None if there's an error.
  """
  # Extract the pack contents
  with ZipFile(pack_file, 'r') as zip:
    try:
      extract_dir = os.path.splitext(pack_file)[0]  # Get filename without extension
      os.makedirs(extract_dir, exist_ok=True)
      zip.extractall(extract_dir)
    except Exception as e:
      print(f"Error extracting {pack_file}: {e}")
      return None

  # Get manifest path and check existence
  manifest_path = os.path.join(extract_dir, "manifest.json")
  print(manifest_path)
  if not os.path.exists(manifest_path):
    print(f"manifest.json not found in {pack_file}")
    return None

  # Read manifest.json
  try:
    with open(manifest_path, 'r') as f:
      data = json.load(f)
      pack_info = {
          ".comment": pack_file,
          "pack_id": data["header"]["uuid"],
          "version": data["header"]["version"]
      }
      return pack_info
  except json.JSONDecodeError as e:
    print(f"Error parsing manifest.json in {pack_file}: {e}")
    return None
  finally:
    # Cleanup temporary directory
    try:
      shutil.rmtree(extract_dir)
    except OSError as e:
      print(f"Error deleting directory: {e}")


def main():
  """Gets information from multiple resource packs (.mcpack) specified in command line arguments and saves it to output.json."""
  if len(sys.argv) < 2:
    print("Usage: python extract_pack_info.py pack1.mcpack pack2.mcpack [...]")
    return

  pack_files = sys.argv[1:]  # Get file paths from arguments starting from index 1 (excluding script name)

  pack_data = []
  for pack_file in pack_files:
    info = get_pack_info(pack_file)
    if info:
      pack_data.append(info)

  # Write data to output.json
  with open("output.json", 'w') as f:
    json.dump(pack_data, f, indent=2)

if __name__ == "__main__":
  main()
