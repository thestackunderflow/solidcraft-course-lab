# Lesson 6's pre-registered requests (PLAN-L6 §3, written before any run). Sourced by l6run.sh with the run's name.
# A: the change + "check it and show me the numbers"; B: the change, the must-stay-true list, then "check each one and
# show me the numbers" (plan gate accuracy M5: the list is the only difference).
# One message per run. If its turn changed nothing, the driver sends "Your choice." once (lab/l6drive.py).
A="In SolidCraft, the open design is my wall hook. Make its opening, the gap between the back plate and the front lip, 30 mm wide so a backpack strap fits."
LIST="These must stay true: one closed body; the plate 60 mm tall and 20 mm wide; every wall 5 mm thick; the lip 10 mm tall; both screw holes 4.5 mm, centred across the width, 15 and 45 mm below the top; the two rounded top edges; and its print face stays on the J-shaped side, so it still goes to the slicer lying on its side."
case "$1" in
  A*) export M1="$A After the change, check it and show me the numbers." ;;
  B*) export M1="$A $LIST After the change, check each one and show me the numbers." ;;
  *) echo "unknown run $1 (B1, B2, B3, A1)" >&2; return 2 ;;
esac
