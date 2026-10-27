# SolidCraft + Claude Course lab: the desktop app with its window on a virtual display (Xvfb, software Vulkan),
# a recorder (ffmpeg), a fake mouse/keyboard (xdotool) and Python for the checker. Pinned on the lab's start day
# (27 Oct 2026): 0.24.1, the stable release on GitHub that day; 0.23.1 kept beside it for the update check (Q11).
# Both Linux x86_64 tarballs are checked against their release's SHA256SUMS.txt.
FROM ubuntu:24.04
ARG SC_VER=0.24.1
ARG SC_OLD=0.23.1
ARG GH=https://github.com/tangency-labs/solidcraft/releases/download
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
      mesa-vulkan-drivers libvulkan1 libgl1 libegl1 \
      xvfb xauth x11-utils xdotool ffmpeg imagemagick \
      libx11-6 libx11-xcb1 libxcursor1 libxrandr2 libxi6 libxkbcommon0 libxkbcommon-x11-0 libxcb1 \
      libwayland-client0 libdbus-1-3 libfontconfig1 fonts-dejavu-core \
      python3 python3-pytest python3-numpy \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /tmp/dl
RUN set -e; for v in $SC_VER $SC_OLD; do \
      a=solidcraft-$v-linux-x86_64.tar.gz; \
      curl -fsSLO "$GH/v$v/$a"; curl -fsSL -o SUMS-$v.txt "$GH/v$v/SHA256SUMS.txt"; \
      grep " $a\$" SUMS-$v.txt > check-$v.txt; test "$(wc -l < check-$v.txt)" = 1; sha256sum -c check-$v.txt; \
      mkdir -p /opt/solidcraft-$v; tar -xzf "$a" -C /opt/solidcraft-$v --strip-components=1; \
      cp SUMS-$v.txt check-$v.txt /opt/solidcraft-$v/; rm "$a"; \
    done; ln -s /opt/solidcraft-$SC_VER /opt/solidcraft; cd /; rm -rf /tmp/dl
ENV PATH=/opt/solidcraft/bin:$PATH
WORKDIR /work
