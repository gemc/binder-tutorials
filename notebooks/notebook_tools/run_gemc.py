from pathlib import Path
from IPython.display import Image, display


def run_gemc_display(result, image_name=None):
    """Print GEMC subprocess output and display the screenshot if present.

    GEMC writes its offscreen screenshot as ``gemc_run_<runno>.png``, where the
    run number comes from the YAML ``runno`` field. When ``image_name`` is not
    given, the most recently written ``gemc_run_*.png`` is displayed.
    """
    if result.returncode != 0:
        print("GEMC failed:")
        print(result.stderr)
        print("If this was an intermittent startup or display failure, re-run this cell.")
    else:
        print(result.stdout)

    if image_name is not None:
        image_file = Path(image_name)
    else:
        screenshots = sorted(Path.cwd().glob("gemc_run_*.png"), key=lambda p: p.stat().st_mtime)
        image_file = screenshots[-1] if screenshots else Path("gemc_run_0.png")

    if image_file.exists():
        display(Image(filename=str(image_file)))
    else:
        print(f"No GEMC image found: {image_file}")
