# A container image for using Snakemake in kubeflow vscode sessions

The image assumes that your kubeflow instance grants you access to a kubernetes namespace and an S3 storage.

When starting a kubeflow vscode session with this image, open a terminal in vscode, and first run

```bash
setup-wizard
```

in order to setup the required S3 credentials, the S3 prefix (e.g. bucket) for storing data, and the kubernetes namespace.
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