# fx5 (4 Nov 2026): lesson 5's image (SolidCraft 0.28.0, PrusaSlicer 2.9.2 Debian package, Xvfb, Mesa) plus the
# libraries the OrcaSlicer and Bambu Studio Linux AppImages load from the system (GTK 3, WebKitGTK 4.1, GStreamer),
# a session bus, and `script`. The AppImages themselves are NOT baked in: they are mounted from out/scratch/fx5-apps
# (official GitHub release files, names in out/fx5/G/pins.txt) and run after --appimage-extract (no FUSE in Docker).
#   docker build -t sc5-fx5:0.28.0 -f docker/fx5.Dockerfile docker
FROM sc5-l5:0.28.0
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libgtk-3-0t64 libwebkit2gtk-4.1-0 libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 \
      gstreamer1.0-plugins-base gstreamer1.0-plugins-good libsecret-1-0 libglu1-mesa libosmesa6 \
      dbus dbus-x11 bsdutils file squashfs-tools \
 && rm -rf /var/lib/apt/lists/*
ENV LIBGL_ALWAYS_SOFTWARE=1
