from pathlib import Path
from IPython.display import Image, display


def run_gemc_display(result, image_name="gemc_run_0.png"):
    """Print GEMC subprocess output and display the screenshot if present."""
    if result.returncode != 0:
        print("GEMC failed:")
        print(result.stderr)
        print("If this was an intermittent startup or display failure, re-run this cell.")
    else:
        print(result.stdout)

    image_file = Path(image_name)
    if image_file.exists():
        display(Image(filename=str(image_file)))
    else:
        print(f"No GEMC image found: {image_file}")
