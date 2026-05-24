#!/usr/bin/env python3

"""
setup_examples.py

Read a YAML file describing GEMC examples and generate one Jupyter notebook
per example.

Example:
    python setup_examples.py examples.yaml

By default this writes:
    notebooks/basic/b1.ipynb
    notebooks/basic/b2.ipynb
    notebooks/basic/simple_flux.ipynb
    notebooks/optical/cherenkov.ipynb
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

GEMC_EXAMPLES_ROOT = Path("/opt/projects/gemc/src/examples")

def binder_markdown(section_name: str, entry: dict[str, Any]) -> str:
	example_name = entry["name"]
	header = str(entry.get("header", "")).strip()
	documentation_slug = entry.get("documentation", example_name)
	documentation_url = f"https://gemc.github.io/home/examples/{section_name}/{documentation_slug}"

	return f"""# GEMC in Binder
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>
Welcome! This notebook runs GEMC directly in your browser.           
How to use:                                                          

1. Click any grey code cell to select it                             
2. Press `Shift + Enter` to run it (or click ▶ in the toolbar)       
3. Run cells in order, top to bottom                                 
4. Wait for `In [*]` to become `In [1]` before running the next cell 

<br/>

## Example: {example_name} → [documentation]({documentation_url}).

<hr style="height:2px;border:0;background:#4a90e2;">

<br/>

{header}

<br/>
"""


def comment_box(lines: list[str]) -> str:
	width = max(len(line) for line in lines)

	top = "# ┌" + "─" * width + "┐"
	body = "\n".join("# │" + line.ljust(width) + "│" for line in lines)
	bot = "# └" + "─" * width + "┘"

	return f"{top}\n{body}\n{bot}"


def environment_setup_cell(section_name: str, entry: dict[str, Any]) -> str:
	example_name = entry["name"]
	source_name = entry.get("source", example_name)
	example_path = f"examples/{section_name}/{source_name}"

	header = comment_box(
		[
			"  Cell 1 · Environment Setup (Shift+Enter to run)  ",
			"  import PyVista and editor          ",
			f"  Copy {section_name}/{source_name} example to local directory  ",
		]
	)

	return f"""{header}

import subprocess, warnings, sys, vtk
import pyvista as pv
vtk.vtkObject.GlobalWarningDisplayOff()  # suppress warnings

from pygemc.api.run_geometry import run_geometry
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent))
from notebook_tools import edit, setup_example
setup_example("{example_path}")

"""


def edit_file_cell(filename: str, cell_number: int) -> str:
	header = comment_box(
		[
			f"  Optional: Cell {cell_number} · Edit {filename} (Shift+Enter to run)  ",
		]
	)

	return f"""{header}

edit("{filename}")
"""

def edit_yaml_cell(yaml_file: str, cell_number: int) -> str:
	header = comment_box(
		[
			f"  Optional: Cell {cell_number} · Edit {yaml_file} (Shift+Enter to run)  ",
			"  ",
			"  Edit the YAML file to change generator, variation, output, etc. ",
		]
	)

	return f"""{header}

edit("{yaml_file}")
"""

def yaml_filename_for_entry(
		entry: dict[str, Any],
		source_dir: Path,
		example_name: str,
) -> str:
	configured = entry.get("yaml") or entry.get("yaml_file")
	if configured:
		return str(configured)

	default_yaml = source_dir / f"{example_name}.yaml"
	if default_yaml.exists():
		return default_yaml.name

	yaml_files = sorted(
		p for p in source_dir.iterdir()
		if p.is_file() and p.suffix in {".yaml", ".yml"}
	) if source_dir.exists() and source_dir.is_dir() else []

	if len(yaml_files) == 1:
		return yaml_files[0].name

	return f"{example_name}.yaml"


def build_geometry_cell(example_name: str, geometry_script: str, cell_number: int) -> str:
	header = comment_box(
		[
			f"  Cell {cell_number} · Build {example_name} detector (Shift+Enter to run)  ",
			"  ",
			"  The geometry is rendered by PyVista in Jupyter. ",
			"  Use the mouse to zoom/rotate/shift the view. "

		]
	)

	return f"""{header}

run_geometry("{geometry_script}")
"""


def gemc_run_cell(
		entry: dict[str, Any],
		section_name: str,
		example_name: str,
		source_dir: Path,
		cell_number: int,
) -> str:
	nevents_value = entry.get("nevents", 1000)
	nevents_label = f"{int(nevents_value):,}" if isinstance(nevents_value, int) else str(nevents_value)

	yaml_file = yaml_filename_for_entry(entry, source_dir, example_name)

	camera_value = entry.get("g4camera", "[{phi: -10*deg, theta: 250*deg}]")
	light_value = entry.get("g4light", "[{phi: 160*deg, theta: 120*deg}]")
	driver_arg = "-g4view=[{driver: TOOLSSG_OFFSCREEN}]"
	camera_arg = f"-g4camera={camera_value}"
	light_arg = f"-g4light={light_value}"

	header = comment_box(
		[
			f"  Cell {cell_number} · Run {nevents_label} events in GEMC (Shift+Enter to run)  ",
			"                                                           ",
			f"  - Load {example_name} gsystem                              ",
			"  - Write CSV, ROOT outputs                                 ",
			"  - Display generated screenshot if present                 ",
		]
	)

	return f"""{header}

from pathlib import Path
from IPython.display import Image, display

yaml={yaml_file!r}
driver={driver_arg!r}
camera={camera_arg!r}
light={light_arg!r}
nevents="-n={nevents_value}"
nthreads="-nthreads=1"

result = subprocess.run(["gemc", yaml, driver, camera, light, nevents, nthreads], capture_output=True, text=True)
if result.returncode != 0:
    print("GEMC failed:")
    print(result.stderr)
else:
    print(result.stdout)

image_file = Path("gemc_run_0.png")
if image_file.exists():
    display(Image(filename=str(image_file)))
else:
    print(f"No GEMC image found: {{image_file}}")
    
    
result = subprocess.run(
	["ls", "-l"],
	capture_output=True,
	text=True,
)

print(result.stdout)
"""


def markdown_cell(source: str) -> dict[str, Any]:
	return {
		"cell_type": "markdown",
		"metadata": {},
		"source": source,
	}


def code_cell(source: str) -> dict[str, Any]:
	return {
		"cell_type": "code",
		"execution_count": None,
		"metadata": {},
		"outputs": [],
		"source": source,
	}


def make_notebook(cells: list[dict[str, Any]]) -> dict[str, Any]:
	return {
		"cells": cells,
		"metadata": {
			"kernelspec": {
				"display_name": "Python 3",
				"language": "python",
				"name": "python3",
			},
			"language_info": {
				"name": "python",
				"pygments_lexer": "ipython3",
			},
		},
		"nbformat": 4,
		"nbformat_minor": 5,
	}


def find_python_files(source_dir: Path) -> list[Path]:
	if not source_dir.exists():
		print(f"WARNING: source directory does not exist: {source_dir}")
		return []

	if not source_dir.is_dir():
		print(f"WARNING: source path is not a directory: {source_dir}")
		return []

	return sorted(
		p for p in source_dir.iterdir()
		if p.is_file() and p.suffix == ".py"
	)


def write_notebook(
		output_path: Path,
		section_name: str,
		entry: dict[str, Any],
		gemc_examples_root: Path,
		overwrite: bool,
) -> None:
	example_name = entry["name"]
	source_name = entry.get("source", example_name)
	geometry_script = entry.get("script", f"{source_name}.py")

	if output_path.exists() and not overwrite:
		print(f"Skipping existing notebook: {output_path}")
		return

	source_dir = gemc_examples_root / section_name / source_name
	python_files = find_python_files(source_dir)

	cells: list[dict[str, Any]] = [
		markdown_cell(binder_markdown(section_name, entry)),
		code_cell(environment_setup_cell(section_name, entry)),
	]

	for index, python_file in enumerate(python_files, start=2):
		cells.append(code_cell(edit_file_cell(python_file.name, index)))

	build_cell_number = len(cells)
	cells.append(
		code_cell(
			build_geometry_cell(
				example_name=example_name,
				geometry_script=geometry_script,
				cell_number=build_cell_number,
			)
		)
	)

	run_cell_number = len(cells)
	cells.append(
		code_cell(
			gemc_run_cell(
				entry=entry,
				section_name=section_name,
				example_name=example_name,
				source_dir=source_dir,
				cell_number=run_cell_number,
			)
		)
	)

	yaml_edit_cell_number = len(cells)
	yaml_file = yaml_filename_for_entry(entry, source_dir, example_name)
	cells.append(
		code_cell(
			edit_yaml_cell(
				yaml_file=yaml_file,
				cell_number=yaml_edit_cell_number,
			)
		)
	)

	notebook = make_notebook(cells)

	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(
		json.dumps(notebook, indent=2, ensure_ascii=False),
		encoding="utf-8",
	)

	print(f"Wrote {output_path}")


def load_yaml(path: Path) -> dict[str, Any]:
	with path.open("r", encoding="utf-8") as f:
		data = yaml.safe_load(f)

	if not isinstance(data, dict):
		raise ValueError("YAML top level must be a mapping, e.g. basic:, optical:")

	return data


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Generate GEMC Binder Jupyter notebooks from a YAML file."
	)
	parser.add_argument(
		"yaml_file",
		type=Path,
		help="Input YAML file describing GEMC examples.",
	)
	parser.add_argument(
		"--output-dir",
		type=Path,
		default=Path("notebooks"),
		help="Base output directory. Default: notebooks.",
	)
	parser.add_argument(
		"--gemc-examples-root",
		type=Path,
		default=GEMC_EXAMPLES_ROOT,
		help=f"GEMC examples source root. Default: {GEMC_EXAMPLES_ROOT}",
	)
	parser.add_argument(
		"--no-overwrite",
		action="store_true",
		help="Do not overwrite notebooks that already exist.",
	)

	args = parser.parse_args()

	data = load_yaml(args.yaml_file)
	overwrite = not args.no_overwrite

	for section_name, entries in data.items():
		if not isinstance(entries, list):
			raise ValueError(f"YAML section '{section_name}' must contain a list.")

		for entry in entries:
			if not isinstance(entry, dict):
				raise ValueError(f"Entry in section '{section_name}' is not a mapping.")

			example_name = entry.get("name")
			if not example_name:
				raise ValueError(f"Entry in section '{section_name}' is missing 'name'.")

			notebook_name = entry.get("notebook", example_name)
			output_path = args.output_dir / section_name / f"{notebook_name}.ipynb"

			write_notebook(
				output_path=output_path,
				section_name=section_name,
				entry=entry,
				gemc_examples_root=args.gemc_examples_root,
				overwrite=overwrite,
			)


if __name__ == "__main__":
	main()
