# GEMC Binder tutorials

Interactive Jupyter tutorials for building detector geometry, running GEMC, and analyzing simulation output.
Run each notebook from top to bottom; the optional final cells let you edit the copied example files and repeat
the workflow.

# Tutorials

## Basic

- [Quickstart](notebooks/basic/quickstart.ipynb)
- [B2](notebooks/basic/b2.ipynb)
- [Materials](notebooks/basic/materials.ipynb)
- [Scintillator barrel](notebooks/basic/scintillator_barrel.ipynb)
- [CAD organs](notebooks/basic/cad.ipynb)
- [Boolean solids](notebooks/basic/boolean_solids.ipynb)
- [B1](notebooks/basic/b1.ipynb)
- [Simple flux](notebooks/basic/simple_flux.ipynb)

## Optical

- [Cherenkov](notebooks/optical/cherenkov.ipynb)
- [Mirrors](notebooks/optical/mirrors.ipynb)
- [Parabolic mirror](notebooks/optical/parabolic_mirror.ipynb)

## Build and run locally

```shell
docker pull ghcr.io/gemc/src:dev-ubuntu-26.04
docker build -t gemc-binder .
docker run --rm -p 8888:8888 gemc-binder
```

Open the JupyterLab URL printed by the container, then choose a notebook under `notebooks/`.
