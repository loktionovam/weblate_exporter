FROM python:3-alpine AS base

# Manual upgrade vulnerable packages
# https://github.com/docker-library/python/issues/680
RUN apk upgrade expat expat-dev libcrypto1.1 libssl1.1

FROM base as builder

COPY . /setup
RUN cd /setup \
    && apk update \
    && apk add gcc libc-dev \
    && python setup.py install \
    && find /usr/local/lib -name "*.pyc" -delete

FROM base AS weblate_exporter
ARG VERSION=dev
RUN adduser -H -S -D -u 1000 weblate_exporter
USER weblate_exporter

COPY --from=builder /usr/local/bin /usr/local/bin/
COPY --from=builder /usr/local/lib /usr/local/lib/

LABEL maintainer=loktionovam@gmail.com
LABEL version=${VERSION}
ENV DEBUG=0 \
    WEBLATE_API_URL=http://weblate:8080/api/ \
    WEBLATE_API_KEY= \
    WEBLATE_EXPORTER_BIND_PORT=9867

ENTRYPOINT [ "python", "-m", "weblate_exporter" ]

FROM weblate_exporter AS vulnscan
COPY --from=aquasec/trivy:latest /usr/local/bin/trivy /usr/local/bin/trivy
USER root
RUN trivy rootfs --exit-code 1 --no-progress --skip-files /usr/local/bin/trivy /

FROM weblate_exporter as main
