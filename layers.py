########## CONFIGURATION (EDIT THIS PART) #####################################
# zmin and zmax are the minimum and maximum heights of the layer given in microns

# Layer stack for more visible layers and geometry.
"""
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
"""
toy_materials = {
}

layerstack = {   
    (64,20): {'name':'L1', 'zmin':2700, 'zmax':2800, 'color':[0.5, 0.5, 0.5, 1.0]},
    (64,59): {'name':'L2', 'zmin':2600, 'zmax':2700, 'color':[0.5, 0.5, 0.5, 1.0]},
    (65,20): {'name':'L1', 'zmin':2500, 'zmax':2600, 'color':[0.5, 0.5, 0.5, 1.0]},
    (65,44): {'name':'L1', 'zmin':2400, 'zmax':2500, 'color':[0.5, 0.5, 0.5, 1.0]},
    (66,20): {'name':'L1', 'zmin':2300, 'zmax':2400, 'color':[0.5, 0.5, 0.5, 1.0]},
    (66,44): {'name':'L1', 'zmin':2200, 'zmax':2300, 'color':[0.5, 0.5, 0.5, 1.0]},
    (68,16): {'name':'L1', 'zmin':2100, 'zmax':2200, 'color':[0.5, 0.5, 0.5, 1.0]},
    (68,20): {'name':'L1', 'zmin':1900, 'zmax':2000, 'color':[0.5, 0.5, 0.5, 1.0]},
    (69,20): {'name':'L1', 'zmin':1800, 'zmax':1900, 'color':[0.5, 0.5, 0.5, 1.0]},
    (69,44): {'name':'L1', 'zmin':1700, 'zmax':1800, 'color':[0.5, 0.5, 0.5, 1.0]},
    (70,20): {'name':'L1', 'zmin':1600, 'zmax':1700, 'color':[0.5, 0.5, 0.5, 1.0]},
    (70,44): {'name':'L1', 'zmin':1500, 'zmax':1600, 'color':[0.5, 0.5, 0.5, 1.0]},
    (71,5): {'name':'L1', 'zmin':1400, 'zmax':1500, 'color':[0.5, 0.5, 0.5, 1.0]},
    (71,16): {'name':'L1', 'zmin':1300, 'zmax':1400, 'color':[0.5, 0.5, 0.5, 1.0]},
    (71,20): {'name':'L1', 'zmin':1200, 'zmax':1300, 'color':[0.5, 0.5, 0.5, 1.0]},
    (71,44): {'name':'L1', 'zmin':1100, 'zmax':1200, 'color':[0.5, 0.5, 0.5, 1.0]},
    (71,44): {'name':'L1', 'zmin':1000, 'zmax':1100, 'color':[0.5, 0.5, 0.5, 1.0]},
    (72,5): {'name':'L1', 'zmin':900, 'zmax':1000, 'color':[0.5, 0.5, 0.5, 1.0]},
    (72,16): {'name':'L1', 'zmin':800, 'zmax':900, 'color':[0.5, 0.5, 0.5, 1.0]},
    (72,20): {'name':'L1', 'zmin':700, 'zmax':800, 'color':[0.5, 0.5, 0.5, 1.0]},
    (78,44): {'name':'L1', 'zmin':600, 'zmax':700, 'color':[0.5, 0.5, 0.5, 1.0]},
    (81,4): {'name':'L1', 'zmin':600, 'zmax':600, 'color':[0.5, 0.5, 0.5, 1.0]},
    (81,23): {'name':'L1', 'zmin':400, 'zmax':500, 'color':[0.5, 0.5, 0.5, 1.0]},
    (93,44): {'name':'L1', 'zmin':300, 'zmax':400, 'color':[0.5, 0.5, 0.5, 1.0]},
    (94,20): {'name':'L1', 'zmin':200, 'zmax':300, 'color':[0.5, 0.5, 0.5, 1.0]},
    (95,20): {'name':'L1', 'zmin':100, 'zmax':200, 'color':[0.5, 0.5, 0.5, 1.0]},
    (122,16): {'name':'L1', 'zmin':0, 'zmax':100, 'color':[0.5, 0.5, 0.5, 1.0]}
}