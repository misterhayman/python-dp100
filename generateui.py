import os
import subprocess

# Define the folders and their corresponding UI generators
UI_FOLDERS_AND_GENERATORS = {
    "./DP100GUI": "pyuic5",
}


def convert_ui_files(folder, generator):
    # Check if the folder exists
    if not os.path.isdir(folder):
        print(f"Error: The folder {folder} does not exist.")
        return

    # List all .ui files in the folder
    files = [f for f in os.listdir(folder) if f.endswith(".ui")]
    if not files:
        print(f"No .ui files found in {folder}.")
        return

    # Process each .ui file
    for file in files:
        full_path = os.path.join(folder, file)
        output_filename = f"ui_{os.path.splitext(file)[0]}.py"
        output_path = os.path.join(folder, output_filename)

        # Construct the command to run
        command = [generator, full_path, "-o", output_path]

        # Execute the command
        try:
            subprocess.run(command, check=True)
            print(f"Success: Converted {file} to {output_filename} using {generator}")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to convert {file} using {generator}")
            input("Press Enter to continue...")


# Loop through each folder and use the designated UI generator
for folder, generator in UI_FOLDERS_AND_GENERATORS.items():
    print(f"Processing folder: {folder} with generator {generator}")
    convert_ui_files(folder, generator)
