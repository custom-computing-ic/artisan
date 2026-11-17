# Tutorial-based tests

On Linux, create and activate the development environment as described in the
repository README, then install pytest and run:

```bash
python -m pip install pytest
python -m pytest tests
```

The tests copy tutorial projects into temporary directories. Parsing requires
the configured Artisan environment, including libclang and compiler flags;
cloning also uses `clang-format`. Integration tests use `make` and `g++` and
skip their respective checks if those commands are unavailable.
