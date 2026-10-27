# Shared helpers for the lab scripts (sourced inside the sc1-app image). A fresh container = a fresh home folder.
export XDG_RUNTIME_DIR=/tmp/xdg; mkdir -p -m 700 "$XDG_RUNTIME_DIR"
unset SOLIDCRAFT_CONTROL_PORT SOLIDCRAFT_CONTROL_TOKEN
W=1600; H=1000

start_display() {
  Xvfb :99 -screen 0 ${W}x${H}x24 -nolisten tcp >/dev/null 2>&1 &
  export DISPLAY=:99; sleep 2
}

record() {        # record OUT.mp4: films the whole display until stop_record
  ffmpeg -loglevel error -y -f x11grab -framerate 10 -video_size ${W}x${H} -i :99 \
    -c:v libx264 -preset veryfast -pix_fmt yuv420p "$1" &
  REC=$!; sleep 1
}

stop_record() { [ -n "${REC:-}" ] && kill -INT "$REC" && wait "$REC" 2>/dev/null; REC=; }

shot() {          # shot NAME.png: the display as it is now
  import -window root "$1" 2>/dev/null
}

stamp() { date -u +%Y-%m-%dT%H:%M:%S.%3NZ; }

event() {         # event FILE what...: one timeline line (UTC), so footage can be matched to logs
  printf '{"t": "%s", "event": "%s"}\n' "$(stamp)" "$2" >> "$1"
}

client_files() {  # the Claude apps' files SolidCraft may write, with hashes
  for f in "$HOME/.config/Claude/claude_desktop_config.json" "$HOME/.claude.json"; do
    if [ -f "$f" ]; then echo "$(sha256sum "$f" | cut -c1-64)  ${f/#$HOME/~}"; else echo "(none)  ${f/#$HOME/~}"; fi
  done
  ls -la "$HOME/.config/Claude/" 2>/dev/null | sed "s#$HOME#~#g"
}

start_app() {     # start_app LOG [solidcraft binary]: no --control, no SOLIDCRAFT_CONTROL_PORT
  "${2:-solidcraft}" > "$1" 2>&1 &
  APP=$!
}

quit_app() {      # close the window the way a person does (Ctrl+Q), then make sure it is gone
  xdotool search --name SolidCraft windowactivate --sync key --clearmodifiers ctrl+q 2>/dev/null
  for i in $(seq 1 20); do kill -0 "$APP" 2>/dev/null || break; sleep 0.5; done
  kill -0 "$APP" 2>/dev/null && { echo "app still running after Ctrl+Q: TERM" >&2; kill "$APP"; sleep 2; }
  APP=
}
