"""
This program converts a GDSII 2D layout file to a glTF 3D file.
Based on https://github.com/mbalestrini/GDS2glTF
and https://github.com/mbalestrini/gdsiistl.
But adapted and slighlty modified to work with more complex GDSII files
as common in integrated photonics.
"""
import sys
import numpy as np
import gdspy
import triangle
import pygltflib
from pygltflib import BufferFormat
from pygltflib.validator import validate, summary
from layers import *

# Get the input file name
if len(sys.argv) < 2:
    print("Error: need exactly one file as a command line argument.")
    sys.exit(0)
gdsii_file_path = sys.argv[1]

# Read the GDSII file
print('Reading GDSII file {}...'.format(gdsii_file_path))
gdsii = gdspy.GdsLibrary()
gdsii.read_gds(gdsii_file_path, units='import')

# Initialize glTF structure
gltf = pygltflib.GLTF2()
scene = pygltflib.Scene()
gltf.scenes.append(scene)
buffer = pygltflib.Buffer()
gltf.buffers.append(buffer)

# Create materials for each layer
for layer in layerstack:
    mainMaterial = pygltflib.Material()
    mainMaterial.doubleSided = False
    mainMaterial.name = layerstack[layer]['name']
    mainMaterial.pbrMetallicRoughness = {
        "baseColorFactor": layerstack[layer]['color'],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.5
    }
    gltf.materials.append(mainMaterial)

binaryBlob = bytes()

print('Extracting polygons...')

meshes_lib = {}

# Process each cell in the GDSII file
for cell in gdsii.cells.values():
    layers = {}

    print("\nProcessing cell:", cell.name)
    
    if cell.name == '$$$CONTEXT_INFO$$$':
        continue

    # Process paths in the cell
    print("\tpaths loop. total paths:", len(cell.paths))
    for path in cell.paths:
        lnum = (path.layers[0], path.datatypes[0])
        if lnum not in layerstack.keys():
            continue
        layers[lnum] = [] if lnum not in layers else layers[lnum]
        for poly in path.get_polygons():
            layers[lnum].append((poly, None, False))

    # Process polygons in the cell
    print("\tpolygons loop. total polygons:", len(cell.polygons))
    for polygon in cell.polygons:
        lnum = (polygon.layers[0], polygon.datatypes[0])
        if lnum not in layerstack.keys():
            continue
        layers[lnum] = [] if lnum not in layers else layers[lnum]
        for poly in polygon.polygons:
            layers[lnum].append((poly, None, False))

    # Triangulation
    print('\tTriangulating polygons...')
    num_triangles = {}

    for layer_number, polygons in layers.items():
        if layer_number not in layerstack.keys():
            continue

        num_triangles[layer_number] = 0

        for index, (polygon, _, _) in enumerate(polygons):
            # ... (triangulation code remains the same)

            num_polygon_points = len(polygon)

            # determine whether polygon points are CW or CCW
            area = 0
            for i, v1 in enumerate(polygon): # loop through vertices
                v2 = polygon[(i+1) % num_polygon_points]
                area += (v2[0]-v1[0])*(v2[1]+v1[1]) # integrate area

            clockwise = area > 0

            # GDSII implements holes in polygons by making the polygon edge
            # wrap into the hole and back out along the same line. However,
            # this confuses the triangulation library, which fills the holes
            # with extra triangles. Avoid this by moving each edge back a
            # very small amount so that no two edges of the same polygon overlap.
            delta = 0.00001 # inset each vertex by this much (smaller has broken one file)
            points_i = polygon # get list of points
            points_j = np.roll(points_i, -1, axis=0) # shift by 1
            points_k = np.roll(points_i, 1, axis=0) # shift by -1
            # calculate normals for each edge of each vertex (in parallel, for speed)
            normal_ij = np.stack((points_j[:, 1]-points_i[:, 1],
                                points_i[:, 0]-points_j[:, 0]), axis=1)
            normal_ik = np.stack((points_i[:, 1]-points_k[:, 1],
                                points_k[:, 0]-points_i[:, 0]), axis=1)
            length_ij = np.linalg.norm(normal_ij, axis=1)
            length_ik = np.linalg.norm(normal_ik, axis=1)
            normal_ij /= np.stack((length_ij, length_ij), axis=1)
            normal_ik /= np.stack((length_ik, length_ik), axis=1)
            if clockwise:
                normal_ij = -1*normal_ij
                normal_ik = -1*normal_ik
            # move each vertex inward along its two edge normals
            polygon = points_i - delta*normal_ij - delta*normal_ik

            # In an extreme case of the above, the polygon edge doubles back on
            # itself on the same line, resulting in a zero-width segment. I've
            # seen this happen, e.g., with a capital "N"-shaped hole, where
            # the hole split line cuts out the "N" shape but splits apart to
            # form the triangle cutout in one side of the shape. In any case,
            # simply moving the polygon edges isn't enough to deal with this;
            # we'll additionally mark points just outside of each edge, between
            # the original edge and the delta-shifted edge, as outside the polygon.
            # These parts will be removed from the triangulation, and this solves
            # just this case with no adverse affects elsewhere.
            hole_delta = 0.00001 # small fraction of delta
            holes = 0.5*(points_j+points_i) - hole_delta*delta*normal_ij
            # HOWEVER: sometimes this causes a segmentation fault in the triangle
            # library. I've observed this as a result of certain various polygons.
            # Frustratingly, the fault can be bypassed by *rotating the polygons*
            # by like 30 degrees (exact angle seems to depend on delta values) or
            # moving one specific edge outward a bit. I have absolutely no idea
            # what is wrong. In the interest of stability over full functionality,
            # this is disabled. TODO: figure out why this happens and fix it.
            use_holes = False

            # triangulate: compute triangles to fill polygon
            point_array = np.arange(num_polygon_points)
            edges = np.transpose(np.stack((point_array, np.roll(point_array, 1))))
            if use_holes:
                triangles = triangle.triangulate(dict(vertices=polygon,
                                                    segments=edges,
                                                    holes=holes), opts='p')
            else:
                triangles = triangle.triangulate(dict(vertices=polygon,
                                                    segments=edges), opts='p')

            if not 'triangles' in triangles.keys():
                triangles['triangles'] = []

            # each line segment will make two triangles (for a rectangle), and the polygon
            # triangulation will be copied on the top and bottom of the layer.
            num_triangles[layer_number] += num_polygon_points*2 + \
                                        len(triangles['triangles'])*2
            polygons[index] = (polygon, triangles, clockwise)


        # glTF Mesh creation
        zmin = layerstack[layer_number]['zmin']
        zmax = layerstack[layer_number]['zmax']
        layername = layerstack[layer_number]['name']
        node_name = cell.name + "_" + layername

        gltf_positions = []
        gltf_indices = []        
        indices_offset = 0

        for i, (_, poly_data, clockwise) in enumerate(polygons):
            p_positions_top = np.insert(poly_data['vertices'], 2, zmax, axis=1)
            p_positions_bottom = np.insert( poly_data['vertices'] , 2, zmin, axis=1)
            p_positions = np.concatenate( (p_positions_top, p_positions_bottom) )
            p_indices_top = poly_data['triangles']
            p_indices_bottom = np.flip ((p_indices_top+len(p_positions_top)), axis=1 )
            ind_list_top = np.arange(len(p_positions_top))
            ind_list_bottom = np.arange(len(p_positions_top)) + len(p_positions_top)
            if(clockwise):
                ind_list_top = np.flip(ind_list_top, axis=0)
                ind_list_bottom = np.flip(ind_list_bottom, axis=0)
            p_indices_right = np.stack( (ind_list_bottom, np.roll(ind_list_bottom, -1, axis=0) , np.roll(ind_list_top, -1, axis=0)), axis=1 )
            p_indices_left = np.stack( ( np.roll(ind_list_top, -1, axis=0), ind_list_top , ind_list_bottom ) , axis=1)
            p_indices = np.concatenate( (p_indices_top, p_indices_bottom, p_indices_right, p_indices_left) )
            if(len(gltf_positions)==0):
                gltf_positions = p_positions
            else:
                gltf_positions = np.append(gltf_positions , p_positions, axis=0)
            if(len(gltf_indices)==0):
                gltf_indices = p_indices
            else:    
                gltf_indices = np.append(gltf_indices, p_indices + indices_offset, axis=0)            
            indices_offset += len(p_positions)

        # Create buffer views and accessors for indices and positions
        indices_binary_blob = gltf_indices.astype(np.uint32).flatten().tobytes() #triangles.flatten().tobytes()
        positions_binary_blob = gltf_positions.astype(np.float32).tobytes() #points.tobytes()

        bufferView1 = pygltflib.BufferView()
        bufferView1.buffer = 0
        bufferView1.byteOffset = len(binaryBlob)
        bufferView1.byteLength = len(indices_binary_blob)
        bufferView1.target = pygltflib.ELEMENT_ARRAY_BUFFER
        gltf.bufferViews.append(bufferView1)

        accessor1 = pygltflib.Accessor()
        accessor1.bufferView = len(gltf.bufferViews)-1
        accessor1.byteOffset = 0
        accessor1.componentType = pygltflib.UNSIGNED_INT
        accessor1.type = pygltflib.SCALAR
        accessor1.count = gltf_indices.size
        accessor1.max = [int(gltf_indices.max())]
        accessor1.min = [int(gltf_indices.min())]
        gltf.accessors.append(accessor1)

        binaryBlob = binaryBlob + indices_binary_blob

        bufferView2 = pygltflib.BufferView()
        bufferView2.buffer = 0
        bufferView2.byteOffset = len(binaryBlob)
        bufferView2.byteLength = len(positions_binary_blob)
        bufferView2.target = pygltflib.ARRAY_BUFFER
        gltf.bufferViews.append(bufferView2)

        positions_count = len(gltf_positions)
        accessor2 = pygltflib.Accessor()
        accessor2.bufferView =  len(gltf.bufferViews)-1
        accessor2.byteOffset = 0
        accessor2.componentType = pygltflib.FLOAT
        accessor2.count = positions_count
        accessor2.type = pygltflib.VEC3
        accessor2.max = gltf_positions.max(axis=0).tolist()
        accessor2.min = gltf_positions.min(axis=0).tolist()
        gltf.accessors.append(accessor2)

        binaryBlob = binaryBlob + positions_binary_blob


        mesh = pygltflib.Mesh()
        mesh_primitive = pygltflib.Primitive()
        mesh_primitive.indices = len(gltf.accessors) - 2
        mesh_primitive.attributes.POSITION = len(gltf.accessors) - 1
        mesh_primitive.material = list(layerstack).index(layer_number)
        mesh.primitives.append(mesh_primitive)

        gltf.meshes.append(mesh)
        meshes_lib[node_name] = len(gltf.meshes) - 1

gltf.set_binary_blob(binaryBlob)
buffer.byteLength = len(binaryBlob)
gltf.convert_buffers(BufferFormat.DATAURI)


def create_transform_matrix(translation, rotation, scale, x_reflection):
    """
    TODO: Integrate this for individual cells as well. Has been ignored for now due to bugs.
    """
    matrix = np.eye(4)
    
    # Apply scale
    scale_matrix = np.diag([scale[0], scale[1], scale[2], 1])
    matrix = np.dot(matrix, scale_matrix)
    
    # Apply x-reflection if needed
    if x_reflection:
        reflection_matrix = np.diag([-1, 1, 1, 1])
        matrix = np.dot(matrix, reflection_matrix)
    
    # Apply rotation (assuming rotation is in degrees around Z-axis)
    if rotation is not None:
        angle_rad = np.radians(rotation)
        cos_theta, sin_theta = np.cos(angle_rad), np.sin(angle_rad)
        rotation_matrix = np.array([
            [cos_theta, -sin_theta, 0, 0],
            [sin_theta, cos_theta, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        matrix = np.dot(matrix, rotation_matrix)
    
    # Apply translation
    translation_matrix = np.array([
        [1, 0, 0, translation[0]],
        [0, 1, 0, translation[1]],
        [0, 0, 1, translation[2]],
        [0, 0, 0, 1]
    ])
    matrix = np.dot(matrix, translation_matrix)
    
    return matrix


# Function to add cell nodes to the scene graph
def add_cell_node(c, parent_node, prefix):
    for ref in c.references:
        instance_node = pygltflib.Node()
        instance_node.extras = {}
        instance_node.extras["type"] = ref.ref_cell.name

        if ref.properties.get(61) is None:
            instance_node.name = "???"
        else:
            instance_node.name = ref.properties[61]
            
        print(prefix, instance_node.name, "(", ref.ref_cell.name + ")")
        
        # Apply translation to position components correctly
        instance_node.translation = [ref.origin[0], ref.origin[1], 0]

        # Fix rotation issues
        if ref.rotation is not None:
            angle_rad = np.radians(ref.rotation)
            instance_node.rotation = [0, 0, np.sin(angle_rad/2), np.cos(angle_rad/2)]
        
        if ref.x_reflection:
            instance_node.scale = [1, -1, 1]  # Corrected scale for x-reflection

        for layer in layerstack.values():
            lib_name = ref.ref_cell.name + "_" + layer['name']
            if lib_name in meshes_lib:
                layer_node = pygltflib.Node()
                layer_node.name = lib_name
                layer_node.mesh = meshes_lib[lib_name]
                gltf.nodes.append(layer_node)
                instance_node.children.append(len(gltf.nodes) - 1)
        
        if len(ref.ref_cell.references) > 0:
            add_cell_node(ref.ref_cell, instance_node, prefix + "\t")

        gltf.nodes.append(instance_node)
        parent_node.children.append(len(gltf.nodes) - 1)

main_cell = gdsii.top_level()[0]
root_node = pygltflib.Node()
root_node.name = main_cell.name

# Apply scaling to the root node
scale_factor = 0.001  # Adjust this value as needed
#root_node.scale = [scale_factor, scale_factor, scale_factor]
root_transform = create_transform_matrix(
    translation=[0, 0, 0],
    rotation=None,
    scale=[scale_factor, scale_factor, scale_factor],
    x_reflection=False
)
root_node.matrix = root_transform.T.flatten().tolist()


gltf.nodes.append(root_node)

print("\nBuilding Scenegraph:")
print(root_node.name)

add_cell_node(main_cell, root_node, "\t")


for layer in layerstack.values():
    lib_name = main_cell.name + "_" + layer['name']
    if lib_name in meshes_lib:
        layer_node = pygltflib.Node()
        layer_node.name = lib_name
        layer_node.mesh = meshes_lib[lib_name]
        gltf.nodes.append(layer_node)
        root_node.children.append(len(gltf.nodes) - 1)

scene.nodes.append(0)
gltf.scene = 0

print("\nWriting glTF file:")
gltf.save(gdsii_file_path + ".gltf")

print('Done.')