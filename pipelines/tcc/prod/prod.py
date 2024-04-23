import os
import sys

prod_dir = os.path.dirname(__file__)
pipe_dir = os.path.dirname(prod_dir)
libs_dir = os.path.join(pipe_dir, "libs")

output_file = ""
libs_files = os.listdir(libs_dir)

for lib_file in libs_files:
    if lib_file.endswith(".groovy"):
        with open(os.path.join(libs_dir, lib_file), "r") as f:
            output_file += f.read()
            output_file += "\n"

with open(os.path.join(prod_dir, "header.groovy"), "r") as f:
    output_file += f.read()
output_file += "\n"

with open(os.path.join(prod_dir, "prod.groovy"), "r") as f:
    output_file += f.read()

with open(os.path.join(prod_dir, "output.groovy"), "w") as f:
    f.write(output_file)
