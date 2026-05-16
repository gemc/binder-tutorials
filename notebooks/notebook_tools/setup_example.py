import os
import shutil
import subprocess
from pathlib import Path

KEEP_EXTENSIONS = {".py", ".yaml", ".yml"}


def setup_example(example_path, keep_extensions=None, chdir=True):
	"""
	Copy selected files from a GEMC example directory into the notebook directory.

	Example:
		setup_example("examples/basic/b1")

	This will:
	  - use $SIM_HOME/gemc/dev/examples/basic/b1 as source
	  - create destination ./b1
	  - remove ./b1 if it already exists
	  - copy only files matching KEEP_EXTENSIONS
	  - optionally cd into ./b1
	  - run ls -l
	"""

	keep_extensions = keep_extensions or KEEP_EXTENSIONS

	gemc = Path(os.environ["SIM_HOME"]) / "gemc" / "dev"
	src = gemc / example_path

	if not src.exists():
		raise FileNotFoundError(f"Source directory does not exist: {src}")

	if not src.is_dir():
		raise NotADirectoryError(f"Source path is not a directory: {src}")

	dst_name = src.name

	# Avoid creating b1/b1 if the notebook cell is re-run after chdir into b1
	base_dir = Path.cwd()
	if base_dir.name == dst_name:
		base_dir = base_dir.parent

	dst = base_dir / dst_name

	if dst.exists():
		shutil.rmtree(dst)

	dst.mkdir(parents=True)

	for item in src.iterdir():
		if item.is_file() and item.suffix in keep_extensions:
			shutil.copy2(item, dst / item.name)

	if chdir:
		os.chdir(dst)

	# Remove stale GEMC saved configuration files
	for saved_config in Path.cwd().glob("gemc.saved_configuration*"):
		if saved_config.is_file():
			saved_config.unlink()

	result = subprocess.run(
		["ls", "-l"],
		cwd=Path.cwd() if chdir else dst,
		capture_output=True,
		text=True,
		check=True,
	)

	print(result.stdout)

	return dst
