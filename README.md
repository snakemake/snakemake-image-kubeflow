# A container image for using Snakemake in kubeflow vscode sessions

## Prerequisites

The image assumes that your kubeflow instance grants you access to a kubernetes namespace and an S3 storage.

## Notebook setup

1. Start creation of a new **vscode** notebook.
2. Click "Custom Notebook", "Advanced Options", check "Custom image", and insert `ghcr.io/snakemake/snakemake-image-kubeflow:v1.0.17` as custom image.
3. Select at least 3 cores and 8GB RAM. These resources will only be needed for running the main Snakemake process. Your jobs will be send to kubernetes.
4. Delete the Workspace volume. There may be no workspace volumne in the notebook because that would overwrite the preinstalled snakemake and setup scripts.
5. Select or create a data volume (add new volume or create existing volume). This can be shared across many notebooks.
6. Launch the notebook.

## Intial steps

When starting a kubeflow vscode session with this image, open a terminal in vscode, and first run

```bash
setup-wizard
```

in order to setup the required S3 credentials, the S3 prefix (e.g. bucket) for storing data, and the kubernetes namespace.

## Usage

Afterwards, Snakemake is available as command `snakemake` in any terminal within the vscode session.
For running a given workflow (in a folder containing `workflow/Snakefile` or just `Snakefile`), run

```bash
snakemake -n
```

to perform a dry-run (without actual execution), and

```bash
snakemake -j 10
```

to execute the workflow with 10 parallel jobs.
That number should be ajusted according the the etiquette rules in your kubeflow cluster.

For inspecting the S3 storage, the container image provides ``s5cmd``, see

```bash
s5cmd --help
```

for usage instructions.

## Update running container

To update a running container to the latest versions of the contained tools (including Snakemake and its plugins), run

```bash
pixi global update
```
