FROM ghcr.io/astral-sh/uv:0.9.28 AS uv-bin


FROM python:3.13-slim-trixie AS base
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV APP_PATH=/usr/local/share/rotebeete
ENV ROTEBEETE_DATA_DIR=/var/lib/rotebeete
ENV ROTEBEETE_LOGGING_FILE_PATH=/var/lib/rotebeete/logging


FROM base AS deps
ARG UV_FLAGS=--no-default-groups
WORKDIR $APP_PATH
COPY --from=uv-bin /uv /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync $UV_FLAGS \
      --frozen \
      --no-editable \
      --no-cache \
      --compile-bytecode \
      --no-managed-python \
      --no-install-project


FROM base AS runtime-base
ARG build_version
ENV DEBIAN_FRONTEND=noninteractive
ENV APP_PATH=/usr/local/share/rotebeete
ENV APP_USER=_rotebeete
ENV ROTEBEETE_DATA_DIR=/var/lib/rotebeete
# upgrade system and remove unneeded packages
RUN apt update -y \
    && apt upgrade -y \
    && apt install -y --no-install-recommends \
      adduser  \
      locales \
      netcat-openbsd \
      fonts-liberation2 \
      pandoc \
    && apt autoremove -y --purge \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
# configure locales
RUN printf 'de_DE.UTF-8 UTF-8\nen_US.UTF-8 UTF-8\n' >/etc/locale.gen \
    && locale-gen \
    && update-locale LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8 LC_TIME=de_DE.UTF-8 LC_MESSAGES=en_US.UTF-8 \
ENV LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8 LC_TIME=de_DE.UTF-8 LC_MESSAGES=en_US.UTF-8
# configure runtime user
RUN adduser --system --group --firstuid 220 --firstgid 220 --home "$ROTEBEETE_DATA_DIR" "$APP_USER" \
    && chown -R _rotebeete: "$ROTEBEETE_DATA_DIR"
# remove vulnerable and no longer useful base system packages
RUN apt purge -y --allow-remove-essential \
      perl-base \
    && apt autoremove -y --purge
# bootstrap dependencies
WORKDIR $APP_PATH
COPY --from=deps "$APP_PATH/.venv" ./.venv
ENV PYTHONPATH=$APP_PATH
ENV PATH=$APP_PATH/.venv/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONUNBUFFERED=1
# cleanup bundled pip
RUN rm -rf /usr/local/lib/python3.13/ensurepip
RUN pip uninstall --yes pip
# set container runtime settings
ENV DJANGO_SETTINGS_MODULE=rotebeete.settings
ENV ROTEBEETE_VERSION=${build_version}

FROM runtime-base AS runtime
WORKDIR $ROTEBEETE_DATA_DIR
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/rotebeete"]
CMD ["uvicorn", "0.0.0.0:8000"]
HEALTHCHECK --start-period=20s CMD nc -z localhost 8000
COPY container/rotebeete.sh /usr/local/bin/rotebeete
COPY rotebeete $APP_PATH/rotebeete
COPY biddings $APP_PATH/biddings

FROM runtime AS dev
EXPOSE 28471
USER "$APP_USER"
