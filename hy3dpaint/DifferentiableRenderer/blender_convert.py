import bpy
import sys
import os

argv = sys.argv

if "--" not in argv:
    raise RuntimeError("Missing arguments")

argv = argv[argv.index("--")+1:]

input_obj = argv[0]
output_glb = argv[1]

# Reset Blender
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import OBJ
bpy.ops.wm.obj_import(filepath=input_obj)

# Select all meshes
for obj in bpy.context.scene.objects:
    obj.select_set(True)

# Export GLB
bpy.ops.export_scene.gltf(
    filepath=output_glb,
    export_format='GLB'
)

print("Finished:", output_glb)
