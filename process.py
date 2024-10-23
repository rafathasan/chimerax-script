import sys
from chimerax.core.commands import run

pdb_file = sys.argv[1]
map_file = sys.argv[2]

run(session, f"open {map_file}")
run(session, f"open {pdb_file}")

print("----- Measure center for pdb")
run(session, "measure center #1")

print("----- Measure center for density map")
run(session, "measure center #2")