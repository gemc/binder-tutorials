# binder-tutorials
GEMC Jupyter Notebooks Tutorials on Binder

# Produce new examples:

Edit `examples.yaml` then run:


```shell
 python setup_examples.py examples.yaml   
 ```

# Build and run:

```shell
docker build -t gemc-binder .
docker run --rm -p 8888:8888  gemc-binder
```


