# Lesson 3's pre-registered requests (PLAN-L3 rev 2 §3, written before any run). Sourced by l3run.sh with the run's
# name. A1, A2: not asked for names; B1, B2: one sentence put in front of A's message, which follows word for word.
# The second message is the same for every run.
A="In SolidCraft, sketch this outline on the XZ plane, standing up (Z from 0 to 60), starting at 0,0: right 25, up 10, left 5, down 5, left 15, up 55, left 5, then back to the start. Extrude it 20 mm."
ASK="Use named sizes (parameters) plate_height 60, width 20, thickness 5, hook_depth 25, lip_height 10, and write every length and the extrude distance from them."
case "$1" in
  A*) export M1="$A" ;;
  B*) export M1="$ASK $A" ;;
  *) echo "unknown run $1 (A1, A2, B1, B2)" >&2; return 2 ;;
esac
export M2="Make the hook 40 deep instead of 25."
