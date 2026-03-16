#!/bin/sh

set -eu
if [ -f /etc/default/rotebeete ]; then
  set -a; . /etc/default/rotebeete; set +a
fi

if [ "${1:-}" = "runserver" ] || [ "${1:-}" = "uvicorn" ]; then
  django-admin migrate --no-input
  django-admin collectstatic --no-input
fi


_is_true() {
  echo "$1" | grep --quiet --ignore-case --extended-regexp '^(1|yes|on|true)$'
}

if [ "${1:-}" = "uvicorn" ]; then
  listen=${2:-0.0.0.0:8000}
  host=$(echo "$listen" | cut -d: -f1)
  port=$(echo "$listen" | cut -d: -f2)
  args=
  if _is_true "${ROTEBEETE_DEBUG:-0}"; then
    args="--reload --reload-dir /usr/local/share/rotebeete/"
  fi
  # shellcheck disable=SC2086
  exec uvicorn rotebeete.asgi:application $args \
    --lifespan off \
    --host "$host" \
    --port "$port"
else
  exec django-admin "$@"
fi
