import bpy
import os
import pyperclip
import tempfile

# Create a temporary directory
temp_dir = tempfile.mkdtemp()

# Get the PNG data from the clipboard
png_data = pyperclip.paste()

# Save the PNG data to a temporary file
png_file = os.path.join(temp_dir, "input.png")
with open(png_file, "wb") as f:
    f.write(png_data.encode())

# Load the PNG image as a texture
image = bpy.data.images.load(png_file)
texture = bpy.data.textures.new('ImageTexture', type='IMAGE')
texture.image = image

# Create a new scene
scene = bpy.context.scene

# Delete the default cube
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Get the dimensions of the PNG image
width, height = image.size

# Create a new plane with the dimensions of the PNG image
bpy.ops.mesh.primitive_plane_add(size=1, calc_uvs=True)
plane = bpy.context.active_object
plane.scale = (width / 100, height / 100, 1)  # Scale the plane to match the image dimensions
plane.data.materials.append(bpy.data.materials.new(name="ImageMaterial"))
plane.data.materials["ImageMaterial"].use_nodes = True
plane.data.materials["ImageMaterial"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 1, 1)  # Set the base color to white

# Set the texture
texture_node = plane.data.materials["ImageMaterial"].node_tree.nodes.new("ShaderNodeTexImage")
texture_node.image = image
plane.data.materials["ImageMaterial"].node_tree.links.new(
    texture_node.outputs["Color"], plane.data.materials["ImageMaterial"].node_tree.nodes["Principled BSDF"].inputs["Base Color"]
)

# Enable transparency
plane.data.materials["ImageMaterial"].blend_method = 'BLEND'

# Save the USDZ file
usdz_file = os.path.join(temp_dir, "output.usdz")
bpy.ops.wm.usd_export(filepath=usdz_file, export_materials=True)

# Copy the USDZ file path to the clipboard
pyperclip.copy(usdz_file)

print(f"USDZ file created: {usdz_file}")