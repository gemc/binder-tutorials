# binder-tutorials
GEMC Jupyter Notebooks Tutorials on Binder

# Test

```shell
docker build -t gemc-binder .
docker run --rm -p 8888:8888 -v $(pwd)/notebooks:/home/ubuntu/notebooks gemc-binder
  ```


