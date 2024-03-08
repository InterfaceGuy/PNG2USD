import bpy
import os

# Set the file paths
png_file = "test.png"
usdz_file = "test.usdz"

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
bpy.ops.wm.usd_export(filepath=usdz_file, export_materials=True)

print(f"USDZ file created: {usdz_file}")