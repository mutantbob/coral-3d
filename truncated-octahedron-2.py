import bpy
import bmesh

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
          (1,-2,0), (0,-2,1), (-1,-2,0), (0,-2,-1), #y-
          
)
faces=[ (0,1,2,3), (4,7,6,5), 
        (8,9,10,11), (12,15,14,13),
        (16,19,18,17), (20,21,22,23),
 ]
f2 = ((16,17,1,0,9,8),
        (8,11,4,5,19, 16),
        (11,10, 20,23,7,4),
        (0,3,21,20,10,9),
        (3,2, 13,14, 22,21),
        (23,22, 14,15, 6,7),
        (2,1, 17,18, 12,13),
        (18,19, 5,6, 15, 12)
        )
        
for f in f2:
    i0 = len(verts)
    v0 =verts[f[0]]
    v3 = verts[f[3]]
    v7 = ((v0[0]+v3[0])/2 ,
    (v0[1]+v3[1])/2 ,
    (v0[2]+v3[2])/2 )
    
    verts = verts + (v7,)
    newF = [ (i0, f[j], f[(j+1)%6]) for j in range(len(f)) ]
    faces .extend(newF)
        
print (len(verts))
for v in verts:
    print(v)

print (len(faces))
for f in faces:
    print(f)


to = createMeshFromData('truncOct', (0,0,0), verts, faces)



to.data.materials.append(bpy.data.materials['stork'])

def truncOctUV(to):
    to.data.uv_textures.new("hippo")
    
    bm = bmesh.new()
    bm.from_mesh(to.data)

    uv_layer = bm.loops.layers.uv[0]

    for fi in range(6, len(bm.faces)):
        print(bm.faces[fi])
        bm.faces[fi].loops[0][uv_layer].uv = (0.5,0.5)

    bm.to_mesh(to.data)
    
def truncOctUV2(to):
    to.data.uv_textures.new("hippo")
    return

truncOctUV(to)