FROM ghcr.io/gemc/src:dev-ubuntu-24.04

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --break-system-packages \
      'jupyterlab>=3' \
      ipywidgets \
      'pyvista[all,trame]' \
      numpy matplotlib pandas \
      jupyter-server-proxy \
      trame_jupyter_extension


ENV PYVISTA_OFF_SCREEN=true
ENV PYVISTA_TRAME_JUPYTER_MODE=extension

USER ubuntu
WORKDIR /home/ubuntu

COPY --chown=ubuntu:ubuntu notebooks/ /home/ubuntu/notebooks/
COPY --chown=ubuntu:ubuntu gconfiguration.py /cvmfs/oasis.opensciencegrid.org/geant4/g4install/ubuntu24-gcc13-arm64/gemc/dev/api/
COPY --chown=ubuntu:ubuntu run_geometry.py   /cvmfs/oasis.opensciencegrid.org/geant4/g4install/ubuntu24-gcc13-arm64/gemc/dev/api/

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser"]