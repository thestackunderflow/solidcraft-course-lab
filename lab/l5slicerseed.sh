# Lesson 5: seed PrusaSlicer's settings before the first start (sourced inside sc5-l5:0.28.0): the wizard-made
# slicer/gui/PrusaSlicer.ini, the bundled Prusa profile (config_version 2.2.7) and its index, the bundled archive list.
seed_slicer() {
  local d="$HOME/.config/PrusaSlicer" p=/usr/share/PrusaSlicer/profiles
  mkdir -p "$d/vendor"
  cp /work/slicer/gui/PrusaSlicer.ini "$d/PrusaSlicer.ini"
  cp "$p/PrusaResearch.ini" "$p/PrusaResearch.idx" "$d/vendor/"
  cp "$p/ArchiveRepositoryManifest.json" "$d/" 2>/dev/null
  export GDK_SCALE=${GDK_SCALE:-2}
}
quit_slicer() { pkill -x slic3r_main; for i in $(seq 1 20); do pgrep -x slic3r_main >/dev/null || break; sleep 0.5; done; }
