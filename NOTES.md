# 🔨 To Do

+ [ ] Create an example `test.gds` file.
+ [ ] Animate it in Blender with the layers seperating and rotating.
+ [ ] Upload a .gif to the `README.md` as the header image.

## Conversion of .gds to .gltf
+ [X] Create and display a working .gltf file in Blender using GDS2glTF.
+ [X] Get the GDS2glTF code running.
+ [X] Display the .gltf file in blender.
+ [X] Debug the placing of the individual components! Currently, x and y seem to be correct, but not the angle a.
+ [X] Now the angle seems correct. But the placing is all at the origin. Fix this.
+ [X] Scale down the size! Right now it is so large, Blender is only showing items within a certain distance.
+ [X] Fix bug where flipped or flopped objects are not positioned correctly.
+ [-] Give the layers the correct height and depth in the z-direction. This can be done by modifying the `layers.py`.
+ [ ] Add optional argument to merge cells within layers to avoid crossing rendering artifacts!

## Add Blender Template Scenes
+ [ ] `finger.blend` contains a scene with a substrate on top a finger. Import your file and place it there. Simple lighting and animation has been preset so you can simply go ahead and render a short animation already.
+ [ ] `coin.blend` provides a simple scene with a white/grey background under studio lighting and a coin for reference.
+ [ ] `packaging.blend` provides a demo scene with a chip being packaged including bonding.

## Lifeview of .gltf in Browser
+ [ ] Install [tinytapeout_gds_viewer](https://github.com/QuentinWach/3D_gds_viewer?tab=readme-ov-file).

---
# The Basic Software Workflow
1. Install [GDS2glTF](https://github.com/QuentinWach/GDS2glTF). (Also compare to https://github.com/mbalestrini/gdsiistl.)
2. Install [tinytapeout_gds_viewer](https://github.com/QuentinWach/3D_gds_viewer?tab=readme-ov-file).
3. Convert your .gds file to a .gds.gltf file using GDS2gITF.
4. View the .gds.gltf file in the browser using the gds viewer.

---
## Ideas
+ Write a Python wrapper to convert and display any .gds in the browser with just a simple function and create a unified repository that is easy to use & understand.
+ Add grid view (showing only the edges/lines) for a more tron feel.
+ Export to Blender (.stl can be imported in Blender!) (See [this tutorial](https://www.zerotoasiccourse.com/post/3drendering/))
	+ Add materials and ray tracing (maybe just do this in blender).
+ Export the view in high res .png with or without background from the live view.
+ Give the layers materials directly in the `layers.py`. Use reference images.
+ Add a substrate layer.
+ Add boolean operations to mimic growth and edging.
+ Integrate a 3D renderer using C++ or Python to show and render the file without any third-party software.

## GDS3D
https://github.com/trilomix/GDS3D is a different 3D .gds viewer using C++ that seems quite advanced yet hasn't been updated in 4 years.

## GDS2glTF
This first version was built to create .glTF 3D files from SDK130 PDK .gds files. Alot of the work is based on the gdsiistl repo: https://github.com/dteal/gdsiistl which then continued in https://github.com/mbalestrini/GDS2glTF.

.glTF (GL Transmission Format) is used for 3D models in both web and native applications like Blender, Unity3D, Unreal Engine 4, or Godot. See [Blender's docs](https://docs.blender.org/manual/en/2.80/addons/io_scene_gltf2.html#) for more information.
