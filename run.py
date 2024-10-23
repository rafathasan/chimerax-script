import os
import sys
import re

def extract_and_calculate(text):
    # Regex patterns to match the coordinate groups
    pattern = r'\(([-+]?\d*\.\d+),\s*([-+]?\d*\.\d+),\s*([-+]?\d*\.\d+)\)'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    
    # Use a set to store unique coordinates
    unique_matches = []
    seen = set()

    for match in matches:
        coords = tuple(map(float, match))
        if coords not in seen:
            seen.add(coords)
            unique_matches.append(coords)

    if len(unique_matches) < 3:
        raise ValueError("Not enough unique coordinate groups found in the text.")

    # Parse the coordinates into floats
    center_mass_index = unique_matches[0]    # (117.07, 120.32, 125.36)
    scene_coordinates = unique_matches[1]     # (97.17, 99.87, 104.05)
    atoms_center_mass = unique_matches[2]     # (0.42, 7.08, -8.36)

    # Calculate the result of subtracting the third from the second
    result = tuple(scene_coordinates[i] - atoms_center_mass[i] for i in range(3))
    
    return center_mass_index, scene_coordinates, atoms_center_mass, result
    

def process(pdb_file, map_file, fit_pdb_file):
    import subprocess

    # Define the command as a list of arguments
    command = ['/usr/bin/chimerax', '--nogui', '--exit', '--script',f"/app/process.py {pdb_file} {map_file}"]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Write the output to the log file using tee
    # with open(log_file, 'w') as log:
    #     log.write(result.stdout)
        # log.write(result.stderr)

    # Print the output and errors
    # print("Output:")
    # print(result.stdout)
    # print("Errors:")
    # print(result.stderr)

    
    center_mass_index, scene_coordinates, atoms_center_mass, xyz = extract_and_calculate(result.stdout)
    x,y,z = scene_coordinates
    print(x,y,z)

    # Define the command as a list of arguments
    command = ['/usr/bin/chimerax', '--nogui', '--exit', '--script',f"/app/fit.py {pdb_file} {map_file} {fit_pdb_file} {x} {y} {z}"]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)


def list_files_in_subdirs(data_dir):
    # Loop through each subdirectory
    for root, dirs, files in os.walk(data_dir):
        pdb_file = None
        map_file = None

        # Check for .pdb and .map files in the current directory
        for file in files:
            if ("_fit." not in file) and file.endswith('.pdb'):
                pdb_file = os.path.join(root, file)
            elif file.endswith('.map'):
                map_file = os.path.join(root, file)

        # Print the files if both are found
        if pdb_file and map_file:
            print(f"Directory: {root}")
            print(f"  PDB: {pdb_file}")
            print(f"  MAP: {map_file}")
            try:
                process(pdb_file, map_file, pdb_file.replace('.', '_fit.'))
            except:
                print(f"{root} got an error")
            print()  # Blank line for better readability

data_dir = '/data'  # Replace with your data directory path
list_files_in_subdirs(data_dir)