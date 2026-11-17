# Building and publishing the Conda package

On Linux, create and activate the build environment from the repository root:

```bash
conda env create -f conda/environment.yml
conda activate conda-build
```

Authenticate with Anaconda (`anaconda login`), then build and upload the package:

```bash
bash conda/publish-conda-builds.sh
```

The script builds and publishes for the Python versions listed in it. It purges
the Conda build cache before and after publishing. The upload uses the currently
authenticated Anaconda account.

The package recipe is in `conda/recipe/`. To build or publish one Python
version at a time, run these commands from the repository root:

```bash
bash conda/conda.env.build 3.12
bash conda/conda.env.publish 3.12
```
