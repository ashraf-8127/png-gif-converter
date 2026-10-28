# PNG to Animated GIF Converter

A friendly, interactive command-line utility for converting ordered sequences of PNG images into smooth, looping animated GIFs using Python and Pillow.

Designed specifically for Windows and cross-platform terminal use, it handles path formatting, quote stripping from drag-and-dropped folders, custom frame timing, and numerical sorting.

---

## Features

- **Interactive Prompts**: Guides you step-by-step through folder selection, output naming, and frame timing.
- **Drag-and-Drop Path Support**: Automatically strips surrounding single and double quotation marks when pasting paths from Windows File Explorer.
- **Flexible Output Locations**: Save the resulting GIF alongside the source images or specify an external directory (auto-creates directories if they do not exist).
- **Exact Frame Timing**: Configure frame duration in seconds or fractional seconds (e.g., `0.1` for 10 FPS, `0.5` for 2 FPS).
- **Proper Numerical Sorting**: Correctly sequences numbered files so frame `10.png` appears after `9.png` (preventing lexicographical sorting issues like `1.png`, `10.png`, `2.png`).
- **Infinite Looping**: Encoded with standard GIF loop tags (`loop=0`) for continuous playback.

---

## Prerequisites

- **Python 3.8+**
- **Pillow** (PIL fork)

Install Pillow via `pip`:

```bash
pip install pillow
```

---

## File Naming Convention

By default, the script scans for PNG files where the filename (without extension) is an integer:

```text
my_frames/
  ├── 1.png
  ├── 2.png
  ├── 3.png
  └── ...
```

Files with non-numeric names (e.g., `background.png`, `notes.txt`) are automatically filtered out.

---

## Usage

Run the script from your terminal:

```bash
python PNG_to_GIF.py
```

### Walkthrough of Interactive Prompts

1. **Source Folder**:
   ```text
   Enter the path to the folder containing PNG files: "M:\Ashraf\Repository\png"
   ```
   *(Pasting Windows paths with quotes is fully supported.)*

2. **Save Location**:
   ```text
   Do you want to save the generated GIF to the same folder? (Yes/No): Yes
   ```
   *(Enter `No` to specify a different folder path).*

3. **Output GIF Name**:
   ```text
   What name should I give to the GIF? (e.g., my_animation): output_animation
   ```
   *(The `.gif` extension will be added automatically if omitted).*

4. **Frame Duration**:
   ```text
   Enter the frame duration in seconds (e.g., 0.5, 2): 0.1
   ```

### Quick Duration Reference

| Frame Rate (FPS) | Duration per Frame (Seconds) | Duration (ms) | Typical Use Case |
| :--- | :--- | :--- | :--- |
| **30 FPS** | `0.033` | 33 ms | High frame-rate render |
| **20 FPS** | `0.05` | 50 ms | Smooth UI / animation |
| **10 FPS** | `0.1` | 100 ms | Standard web animation |
| **4 FPS** | `0.25` | 250 ms | Slideshow / walkthrough |
| **1 FPS** | `1.0` | 1000 ms | Slow step-by-step guide |

---

## Tips & Enhancements

### 1. Handling Transparent PNGs in GIFs
The GIF format supports only a 256-color palette and a single 1-bit transparency index. When saving raw `RGBA` images, semi-transparent pixels or anti-aliased borders may produce black outlines or color artifacts.

If you notice dark borders on transparent backgrounds, convert frames to RGB with a solid background color (e.g., white):

```python
# Optional: composite transparent PNGs over a solid background
rgb_frames = []
for f in files:
    img = Image.open(f).convert("RGBA")
    background = Image.new("RGBA", img.size, (255, 255, 255))
    combined = Image.alpha_composite(background, img)
    rgb_frames.append(combined.convert("RGB"))
```

### 2. Supporting Prefixed Filenames (e.g., `frame_1.png`)
If your source files include prefixes like `frame_1.png` or `render_002.png`, replace `f.stem.isdigit()` with regular expressions or `natsort`:

```python
import re

# Extracts numbers from filenames like frame_1.png, step-2.png
files = [f for f in png_folder.glob("*.png") if re.search(r"\d+", f.stem)]
files.sort(key=lambda x: int(re.search(r"\d+", x.stem).group()))
```

---

## License

Distributed under the MIT License. Free for personal and commercial use.
