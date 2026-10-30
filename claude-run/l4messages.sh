# Lesson 4's pre-registered requests (PLAN-L4 rev 2 §3, written before any run). Sourced by l4run.sh with the run's
# name. A1, A2: not asked for names; B1, B2: one sentence put in front of A's message, which follows word for word.
# The second message is the same for every run. If Claude asks a question instead of acting on message 1, the driver
# sends the fixed answer "Your choice." once (lab/l4drive.py).
A="In SolidCraft, the open design is a wall hook. Add two 4.5 mm screw holes through its back plate, one above the other, 15 mm and 45 mm below the top edge, centred across the plate's width. Then round the back plate's two long top edges, front and back, with a 2 mm fillet."
ASK="Use named sizes (parameters): add hole_d 4.5, and write the hole diameter and the hole positions from the named sizes."
case "$1" in
  A*) export M1="$A" ;;
  B*) export M1="$ASK $A" ;;
  *) echo "unknown run $1 (A1, A2, B1, B2)" >&2; return 2 ;;
esac
export M2="Make the hook 30 wide instead of 20."
