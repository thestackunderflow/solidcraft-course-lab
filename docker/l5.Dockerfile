# Lesson 5 (31 Oct 2026): SolidCraft 0.28.0 and a pinned slicer on the same virtual display, so "Send to Slicer"
# finds the slicer and the hand-off is filmed. Debian 13 (trixie), because its PrusaSlicer package is 2.9.2
# (Ubuntu 24.04 has 2.7.2, and PrusaSlicer's own Linux builds are Flathub only). SolidCraft is copied from the lesson's
# app image (sc5-app:0.28.0, built from app.Dockerfile with SC_VER=0.28.0 SC_OLD=0.27.1; tarball checked against
# SHA256SUMS.txt there). Claude Code is pinned as in lessons 3, 4 and 7.
#   docker build -t sc5-app:0.28.0 --build-arg SC_VER=0.28.0 --build-arg SC_OLD=0.27.1 -f docker/app.Dockerfile docker
#   docker build -t sc5-l5:0.28.0 -f docker/l5.Dockerfile docker
ARG APP=sc5-app:0.28.0
FROM ${APP} AS app
FROM debian:trixie
ARG PRUSA=2.9.2+dfsg-1
ARG CLAUDE_VER=2.1.311
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
      mesa-vulkan-drivers libvulkan1 libgl1 libegl1 libgl1-mesa-dri \
      xvfb xauth x11-utils xdotool ffmpeg imagemagick xterm wmctrl tmux dmz-cursor-theme openbox \
      libx11-6 libx11-xcb1 libxcursor1 libxrandr2 libxi6 libxkbcommon0 libxkbcommon-x11-0 libxcb1 \
      libwayland-client0 libdbus-1-3 libfontconfig1 fonts-dejavu-core \
      python3 python3-pytest python3-numpy \
      prusa-slicer=${PRUSA} \
 && rm -rf /var/lib/apt/lists/* \
 && prusa-slicer --help | head -1
# PrusaSlicer refuses to start its window in English without a generated en_US locale
RUN apt-get update && apt-get install -y --no-install-recommends locales \
 && sed -i 's/^# *en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen && locale-gen && rm -rf /var/lib/apt/lists/*
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
COPY --from=app /opt/solidcraft-0.28.0 /opt/solidcraft-0.28.0
RUN ln -s /opt/solidcraft-0.28.0 /opt/solidcraft
ENV PATH=/opt/solidcraft/bin:$PATH
RUN curl -fsSL https://claude.ai/install.sh | bash -s $CLAUDE_VER \
 && ln -sf /root/.local/bin/claude /usr/local/bin/claude && claude --version
ENV XCURSOR_THEME=DMZ-White XCURSOR_SIZE=72
WORKDIR /work
