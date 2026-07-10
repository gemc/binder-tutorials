# binder-tutorials
GEMC Jupyter Notebooks Tutorials on Binder

# Tutorials

## Basic

- [Quickstart](notebooks/basic/quickstart.ipynb)
- [B2](notebooks/basic/b2.ipynb)
- [Materials](notebooks/basic/materials.ipynb)
- [Scintillator barrel](notebooks/basic/scintillator_barrel.ipynb)
- [CAD organs](notebooks/basic/cad.ipynb)
- [B1](notebooks/basic/b1.ipynb) - deprecated; kept for reference.
- [Simple flux](notebooks/basic/simple_flux.ipynb) - deprecated; kept for reference.

## Optical

- [Cherenkov](notebooks/optical/cherenkov.ipynb)
- [Mirrors](notebooks/optical/mirrors.ipynb)
- [Parabolic mirror](notebooks/optical/parabolic_mirror.ipynb)

# Build and run:

```shell
docker pull ghcr.io/gemc/src:dev-ubuntu-26.04
docker build -t gemc-binder .
docker run --rm -p 8888:8888  gemc-binder
```
