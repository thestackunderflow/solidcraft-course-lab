# Lesson 5's pre-registered requests (PLAN-L5 rev 2 §3, written before any run). Sourced by l5run.sh with the run's
# name. A1: not asked to check; B1: one sentence put in front of A's message, which follows word for word.
# One message per run. If Claude asks a question instead of acting, the driver sends "Your choice." once (lab/l5drive.py).
A="In SolidCraft, the open design is a wall hook I want to 3D print. Send it to the slicer."
ASK="Before you send it, check that it's ready to print: one body, closed, the size in millimetres, and pick the flat face it should lie on."
case "$1" in
  A*) export M1="$A" ;;
  B*) export M1="$ASK $A" ;;
  *) echo "unknown run $1 (A1, B1)" >&2; return 2 ;;
esac
