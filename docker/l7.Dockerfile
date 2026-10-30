# Lesson 7 layer (29 Oct 2026): the same terminal + Claude Code layer as lesson 3, on the lesson 7 pin (sc7-app:0.27.0,
# built from app.Dockerfile with SC_VER=0.27.0 SC_OLD=0.26.1; 0.26.1 kept for the wrong-version case).
#   docker build -t sc7-app:0.27.0 --build-arg SC_VER=0.27.0 --build-arg SC_OLD=0.26.1 -f docker/app.Dockerfile docker
#   docker build -t sc7-l7:0.27.0 -f docker/l7.Dockerfile docker
# Lesson 2 layer (27 Oct 2026): the pinned SolidCraft image (sc2-app:0.25.0, built from app.Dockerfile with
# SC_VER=0.25.0 SC_OLD=0.24.1) plus a terminal window (xterm) and Claude Code, so the Claude run is filmed in a real
# terminal on the same virtual display as SolidCraft's window (tmux inside the xterm lets the script read the
# screen text, to answer the real approval prompts; a large cursor theme so the pointer reads on a phone). Nothing on
# the host changes.
#   docker build -t sc2-app:0.25.0 --build-arg SC_VER=0.25.0 --build-arg SC_OLD=0.24.1 -f docker/app.Dockerfile docker
#   docker build -t sc2-l2:0.25.0 -f docker/l2.Dockerfile docker
ARG BASE=sc7-app:0.27.0
FROM ${BASE}
ARG CLAUDE_VER=2.1.311
RUN apt-get update \
 && apt-get install -y --no-install-recommends xterm wmctrl tmux dmz-cursor-theme \
 && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://claude.ai/install.sh | bash -s $CLAUDE_VER \
 && ln -sf /root/.local/bin/claude /usr/local/bin/claude && claude --version
ENV XCURSOR_THEME=DMZ-White XCURSOR_SIZE=72
WORKDIR /work
