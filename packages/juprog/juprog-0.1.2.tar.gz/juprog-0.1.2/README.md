juprog
======
Circle progress for Jupyter notebook

Basic Example
=============

```python

from time import sleep
from juprog import CircleProgress

for x in CircleProgress(sequence):
    # fake long process
    sleep(0.2)
```

![juprog](juprog.gif)

Install
=======

Release
-------
```bash
    pip install https://github.com/hainm/juprog/archive/v0.1.tar.gz
```

Development version
-------------------

```bash
    pip install git+https://github.com/hainm/juprog
```

Acknowledgement
===============
Use [progress-circle](https://github.com/iammary/progress-circle) for displaying progress. 
