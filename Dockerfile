FROM kubeflownotebookswg/codeserver-python:v1.9.2

COPY --chown=jovyan:jovyan bashrc /home/jovyan/.bashrc
COPY --chown=jovyan:jovyan pixi_config.toml /home/jovyan/.pixi/config.toml

RUN touch ~/.secrets && \
    curl -fsSL https://pixi.sh/install.sh | sh

COPY --chown=jovyan:jovyan profile.yaml /home/jovyan/.config/snakemake/default/config.yaml
COPY --chown=jovyan:jovyan --chmod=+x setup-wizard.py /home/jovyan/.local/bin/setup-wizard
ENV SNAKEMAKE_PROFILE=default

RUN source ~/.bashrc && \
    pixi global install snakemake --with snakemake-executor-plugin-kubernetes --with snakemake-storage-plugin-s3 && \
    pixi global install python --with inquirerpy --with pyyaml

# TODO spawn wizard automatically when starting a terminal?