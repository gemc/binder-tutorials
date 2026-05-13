FROM ghcr.io/gemc/src:dev-ubuntu-24.04

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --break-system-packages \
      'jupyterlab>=3' \
      ipywidgets \
      'pyvista[all,trame]' \
      jupyter-server-proxy \
      pandas \
      trame_jupyter_extension


ENV PYVISTA_OFF_SCREEN=true
ENV PYVISTA_TRAME_JUPYTER_MODE=extension

USER ubuntu
WORKDIR /home/ubuntu

COPY --chown=ubuntu:ubuntu notebooks/      /home/ubuntu/notebooks/


CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser"]