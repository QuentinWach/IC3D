# IC3D

<img align="right" width="40%" margin="15px" src="docs/xyz2.png"> 

<div style="text-align: center;">
<b>Convert your .gds to .gltf files to create photo-real animations of your photonic/electronic integrated circuits.</b>
</div>
<br>

+ ✍🏻 Define your process for each layer easily (i.e. materials, layer heights).
+ 📐 Converts the `.gds` to the common `.gltf` file format for 3D objects including BDSF material based on the defined process.
+ 🎨 Import the `.gltf` file into [Blender](https://www.blender.org/) (or any other 3D software of your choice) to create a 3D render.


This code is based on [https://github.com/mbalestrini/GDS2glTF](https://github.com/mbalestrini/GDS2glTF) which in turn is based on [https://github.com/dteal/gdsiistl](https://github.com/dteal/gdsiistl).
The main changes here ensure that complex nested cells, flips, and rotations are done correctly so that complex integrated photonics designs can be rendered in 3D.

---
### 🚀 Get Started

>[!NOTE]
Feel free to reach out to me on [X (formerly Twitter) @QuentinWach](https://x.com/QuentinWach) if you need help to set this up and get started. I'd love to help and get some feedback. 😃

**1. Install**. [Clone the repository](). Then navigate to the directory in your terminal and activate whatever environment you want to use, then:
```
pip install -r requirements.txt
```
This installs all the required libraries. Or it should. When using [Anaconda]() you may encounter the error _"ERROR: Failed building wheel for gdspy"_.
You can resolve this issue by opening the Anaconda shell directly, activating the chosen environment, and running:
```
conda install gdspy
```
The run the requirements install command again just to make sure all the requirements are fulfilled.

**2. Create 3D File.** Open `layers.py`. This file defines what each layer represents and what layers you want to export to a 3D file. An example is given which should make it clear how to use it. Once done with that, you can go ahead and test the conversion by running
```
python main.py test.gds
```
which converts the `test.gds` file into a `.gds.gltf` file.
You can then import it into any 3D rendering software or game engine of your choice.

**3. Render with Blender.** 
[Blender](https://www.blender.org/) is a free and open-source option to create visualizations of the chip's 3D file. Open Blender and import the `.gltf` file directly which will display it with the proper materials and geometry as defined by your layer/process file.

I recommend watching this [Product Design and Rendering Blender Tutorial](https://www.youtube.com/watch?v=up_UGQIDOFg).
