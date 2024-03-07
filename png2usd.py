import sys
from PIL import Image
from pxr import Usd, UsdGeom, Sdf

def create_usda_and_convert_to_usdz(png_path):
    # Load the image to get its dimensions
    with Image.open(png_path) as img:
        width, height = img.size

    # Calculate the plane dimensions based on the image dimensions
    plane_width = width / max(width, height)
    plane_height = height / max(width, height)

    # Define the output paths
    usda_path = png_path.rsplit('.', 1)[0] + '.usda'
    usdz_path = png_path.rsplit('.', 1)[0] + '.usdz'

    # Create a new stage
    stage = Usd.Stage.CreateNew(usda_path)

    # Define the Mesh
    mesh = UsdGeom.Mesh.Define(stage, '/Plane')
    mesh.CreatePointsAttr([(-plane_width / 2, 0, 0), (plane_width / 2, 0, 0), (plane_width / 2, plane_height, 0), (-plane_width / 2, plane_height, 0)])
    mesh.CreateFaceVertexCountsAttr([4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    mesh.CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.varying).Set([(0, 0), (1, 0), (1, 1), (0, 1)])

    # Create Material and Shader
    material = UsdGeom.Material.Define(stage, '/PlaneMaterial')
    shader = Usd.Shader.Define(stage, '/PlaneMaterial/Shader')
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseTexture", Sdf.ValueTypeNames.Asset).Set(png_path)
    UsdShade.MaterialBindingAPI(mesh.GetPrim()).Bind(material)

    # Save the stage
    stage.GetRootLayer().Save()

    print(f"Saved .usda file at {usda_path}")

    # Convert .usda to .usdz using usd-core
    stage.Export(usdz_path)
    print(f"Converted .usda to .usdz at {usdz_path}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_png>")
    else:
        create_usda_and_convert_to_usdz(sys.argv[1])
