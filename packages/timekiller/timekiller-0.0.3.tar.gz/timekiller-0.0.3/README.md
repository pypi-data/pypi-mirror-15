
[![pythonversions](https://img.shields.io/pypi/pyversions/timekiller.svg)](https://pypi.python.org/pypi/timekiller)
[![License](https://img.shields.io/pypi/l/timekiller.svg)](https://opensource.org/licenses/MIT)

# Timekiller
It lets call any function with a timeout!

## Install

```bash
pip install timekiller
```

Link pypi: https://pypi.python.org/pypi/timekiller

## Example

## Call function
```python
import timekiller
import time


def long_function(foo, bar):
    while True:
        time.sleep(10)
        print(foo, bar)

# call(func, max_time, *args, **kwargs)
timekiller.call(long_function, 5, "woo", bar="Uhmm")


@timekiller.timeout(5)
def long_function_with_decorator(foo, bar)
    while True:
        time.sleep(10)
        print(foo, bar)

long_function_with_decorator("woo", "Uhmm")
```

## Capture exception

```python
import timekiller
import time


@timeout(1)
def long_function():
    try:
        time.sleep(10)
    except timekiller.TimeoutException:
        print("capture exception")

long_function()
```
TODO:
 - It works in main thread and processes (not work in threads)
