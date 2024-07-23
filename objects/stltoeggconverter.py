import subprocess
import os


def convert_stl_to_egg( stl_file, egg_file ):
    # Step 1: Convert STL to OBJ
    obj_file = stl_file.replace( ".stl", ".obj" )
    subprocess.run( [ "assimp", "export", stl_file, obj_file, "--format", "obj" ] )

    # Step 2: Convert OBJ to EGG
    subprocess.run( [ "obj2egg", obj_file, "-o", egg_file ] )

    # Clean up intermediate OBJ file
    os.remove( obj_file )
