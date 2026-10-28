from PIL import Image
from pathlib import Path
import sys

# 1. Ask for the path where the PNG files are located
input_path_str = input("Enter the path to the folder containing PNG files: ").strip()
# Remove quotes if the user pasted a path with quotes (common in Windows)
input_path_str = input_path_str.strip('\"\'')
png_folder = Path(input_path_str)

if not png_folder.exists() or not png_folder.is_dir():
    print("Error: The specified folder does not exist.")
    sys.exit()

# 2. Ask if the GIF should be saved in the same folder
while True:
    save_same = input("Do you want to save the generated GIF to the same folder? (Yes/No): ").strip().lower()
    if save_same in ['yes', 'y', 'no', 'n']:
        break
    print("Please answer with 'Yes' or 'No'.")

# 3. Determine the output directory based on the answer
if save_same in ['yes', 'y']:
    output_dir = png_folder
else:
    output_dir_str = input("Enter the path where you want to save the GIF: ").strip()
    output_dir_str = output_dir_str.strip('\"\'')
    output_dir = Path(output_dir_str)
    
    # Create the output directory if it doesn't exist
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

# 4. Ask for the name of the GIF
gif_name = input("What name should I give to the GIF? (e.g., my_animation): ").strip()
if not gif_name.lower().endswith(".gif"):
    gif_name += ".gif"

output_path = output_dir / gif_name

# 5. Ask for the frame duration in seconds
while True:
    try:
        duration_sec = float(input("Enter the frame duration in seconds (e.g., 0.5, 2): ").strip())
        if duration_sec <= 0:
            print("Please enter a number greater than 0.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a valid number for seconds.")

# Convert seconds to milliseconds for Pillow
duration_ms = int(duration_sec * 1000)

# Safely grab and sort only the PNG files that have integer names (e.g., 1.png, 2.png)
files = []
for f in png_folder.glob("*.png"):
    if f.stem.isdigit():
        files.append(f)

# Sort them numerically
files.sort(key=lambda x: int(x.stem))

if not files:
    print(f"No numeric PNG files found in: {png_folder}")
else:
    print(f"Found {len(files)} frames. Generating GIF...")
    
    # Load images
    frames = [Image.open(f).convert("RGBA") for f in files]

    # Save as animated GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms, # Dynamic duration based on input
        loop=0,               # Infinite loop
        format="GIF"
    )
    print(f"Success! Saved '{gif_name}' to {output_dir}")