# The site check (Q1): a real browser with JavaScript (headless Chromium from Debian) and curl, nothing else.
FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl chromium fonts-dejavu-core python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
