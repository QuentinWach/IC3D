########## CONFIGURATION (EDIT THIS PART) #####################################
# zmin and zmax are the minimum and maximum heights of the layer given in microns

# Layer stack for more visible layers and geometry.
layerstack = {   
    (41,0): {'name':'topelect', 'zmin':100, 'zmax':300, 'color':[0.5, 0.5, 0.5, 1.0]},
    (28,0): {'name':'labels', 'zmin':200, 'zmax':300, 'color':[0.5, 0.5, 0.5, 1.0]},
    (150,0): {'name':'stress_relief', 'zmin':200, 'zmax':250, 'color':[0.5, 0.5, 0.5, 1.0]},
    (15,0): {'name':'edging_paths', 'zmin':150, 'zmax':200, 'color':[0.5, 0.5, 0.5, 1.0]},
    (10,0): {'name':'waveguides', 'zmin':100, 'zmax':200, 'color':[0.5, 0.5, 0.5, 1.0]},
    (12,0): {'name':'large_waveguides', 'zmin':100, 'zmax':200, 'color':[0.5, 0.5, 0.5, 1.0]},
    (21,0): {'name':'subelect', 'zmin':0, 'zmax':100, 'color':[0.5, 0.5, 0.5, 1.0]},
    (7,0): {'name':'chip_border', 'zmin':0, 'zmax':100, 'color':[0.5, 0.5, 0.5, 1.0]},
}
toy_materials = {
}