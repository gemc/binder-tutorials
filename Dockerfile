FROM ghcr.io/gemc/src:dev-ubuntu-24.04

USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3-pip \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --break-system-packages \
      jupyterlab==4.* \
      numpy matplotlib pandas ipywidgets

USER ubuntu
WORKDIR /home/ubuntu

COPY --chown=ubuntu:ubuntu notebooks/ /home/ubuntu/notebooks/

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser"]