import sys
from chimerax.core.commands import run

pdb_file = sys.argv[1]
map_file = sys.argv[2]
fit_pdb_file = sys.argv[3]
x = sys.argv[4]
y = sys.argv[5]
z = sys.argv[6]

run(session, f"open {map_file}")
run(session, f"open {pdb_file}")


print("----- Measure center for pdb")
run(session, f"move {x}, {y}, {z} model #2")
run(session, "fitmap #2 in_map #1")
run(session, f"save {fit_pdb_file} model #2")