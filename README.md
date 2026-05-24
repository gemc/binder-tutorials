# binder-tutorials
GEMC Jupyter Notebooks Tutorials on Binder

# Build and run:

```shell
docker pull ghcr.io/gemc/src:dev-ubuntu-24.04
docker build -t gemc-binder .
docker run --rm -p 8888:8888  gemc-binder
```

