import bpy

def createMeshFromData(name, origin, verts, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True
 
    # Link object to scene and make active
    scn = bpy.context.scene
    scn.objects.link(ob)
    scn.objects.active = ob
    ob.select = True
 
    # Create mesh from given verts, faces.
    me.from_pydata(verts, [], faces)
    # Update mesh with new data
    me.update()    
    return ob
 
verts = ( (1,0, 2), (0,1, 2), (-1,0, 2), (0,-1, 2), # top
          (1,0,-2), (0,1,-2), (-1,0,-2), (0,-1,-2), # bottom
          ( 2,1,0), ( 2,0,1), ( 2,-1,0), ( 2,0,-1), #x+
          (-2,1,0), (-2,0,1), (-2,-1,0), (-2,0,-1), #x-
          (1, 2,0), (0, 2,1), (-1, 2,0), (0, 2,-1), #y+
          (1,-2,0), (0,-2,1), (-1,-2,0), (0,-2,-1) #y-
)
faces=( (0,1,2,3), (4,7,6,5), 
        (8,9,10,11), (12,15,14,13),
        (16,19,18,17), (20,21,22,23),
        (16,17,1,0,9,8),
        (8,11,4,5,19, 16),
        (11,10, 20,23,7,4),
        (0,3,21,20,10,9),
        (3,2, 13,14, 22,21),
        (23,22, 14,15, 6,7),
        (2,1, 17,18, 12,13),
        (18,19, 5,6, 15, 12),
 )

to = createMeshFromData('truncOct', (0,0,0), verts, faces)
