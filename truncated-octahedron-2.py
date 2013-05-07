import bpy
import random

# The following function is adapted from
# Nick Keeline "Cloud Generator" addNewObject
# from object_cloud_gen.py (an addon that comes with the Blender 2.6 package)
#
def duplicateObject(scene, name, copyobj):
 
    # Create new mesh
    mesh = bpy.data.meshes.new(name)
 
    # Create new object associated with the mesh
    ob_new = bpy.data.objects.new(name, mesh)
 
    # Copy data block from the old object into the new object
    ob_new.data = copyobj.data.copy()
    ob_new.scale = copyobj.scale
    ob_new.location = copyobj.location
 
    while 0<len(ob_new.data.materials.items()):
        ob_new.data.materials.pop(0,1)
        
    # Link new object to the given scene and select it
    scene.objects.link(ob_new)
    ob_new.select = True
 
    return ob_new

def popUpMaterial( c, t0, t1, t2, t3):
    rval = bpy.data.materials.new('fadeIn')
    rval.use_transparency=1
    rval.diffuse_color=(1,1,1)
    rval.alpha=0
    rval.emit=1
    rval.diffuse_intensity=0
    rval.keyframe_insert(data_path='alpha', frame=t0)
    rval.alpha=1
    rval.keyframe_insert(data_path='alpha', frame=t1)
    rval.keyframe_insert(data_path='diffuse_color', frame=t1)
    rval.keyframe_insert(data_path='diffuse_intensity', frame=t1)
    rval.keyframe_insert(data_path='emit', frame=t1)
    rval.diffuse_color=c
    rval.emit=0.2
    rval.diffuse_intensity=0.7
    rval.keyframe_insert(data_path='diffuse_color', frame=t2)
    rval.keyframe_insert(data_path='diffuse_intensity', frame=t2)
    rval.keyframe_insert(data_path='emit', frame=t2)
    
    for curve in rval.animation_data.action.fcurves.items():
        print (curve[1].data_path )
        if 'diffuse_color'==curve[1].data_path:
            curve[1].keyframe_points.items()[1][1].interpolation = 'LINEAR'

    
    rval.diffuse_color=(0.5,0.5,0.5)
    rval.keyframe_insert(data_path='diffuse_color', frame=t3)

    return rval


def materialNodeMix(mat, solid, flash, texture):
    
    mat.use_nodes = 1
    
    for node in mat.node_tree.nodes.values() :
        mat.node_tree.nodes.remove(node)
    
    l= mat.node_tree.links
    
    nm1 = mat.node_tree.nodes.new('MATERIAL')
    nm1.location = (0,200)
    nm1.material = solid
    
    nm2 = mat.node_tree.nodes.new('MATERIAL')
    nm2.location = (300,0)
    nm2.material = flash
    
    nx1 = mat.node_tree.nodes.new('MIX_RGB')
    nx1.location = (300,200)
    
    nm3 = mat.node_tree.nodes.new('TEXTURE')
    nm3.location = (100,0)
    nm3.texture = texture
    
    ng = mat.node_tree.nodes.new("GEOMETRY")
    ng.location = (-150,0)
    
    l.new(ng.outputs['UV'], nm3.inputs['Vector'])
    
    l.new(nm1.outputs['Color'], nx1.inputs['Color1'])
    l.new(nm3.outputs['Color'], nx1.inputs['Color2'])
    l.new(nm3.outputs['Value'], nx1.inputs['Fac'])
    
    nx2 = mat.node_tree.nodes.new('MATH')
    nx2.operation = 'MAXIMUM'
    nx2.location = (450,400)
    
    l.new(nm1.outputs['Alpha'], nx2.inputs[0])
    l.new(nm2.outputs['Alpha'], nx2.inputs[1])
    
    nx4 = mat.node_tree.nodes.new('MIX_RGB')
    nx4.location = (450,200)
    
    l.new(nm1.outputs['Alpha'], nx4.inputs['Fac'])
    l.new(nx1.outputs[0], nx4.inputs['Color2'])
    l.new(nm2.outputs['Color'], nx4.inputs['Color1'])
    
    nx3 = mat.node_tree.nodes.new('MIX_RGB')
    nx3.location = (600,100)
    
    l.new(nx4.outputs[0], nx3.inputs['Color1'])
    l.new(nm2.outputs['Color'], nx3.inputs['Color2'])
    l.new(nm2.outputs['Alpha'], nx3.inputs['Fac'])
    
    no = mat.node_tree.nodes.new('OUTPUT')
    no.location = (750,200)
    
    l.new(nx3.outputs['Color'], no.inputs['Color'] )
    l.new(nx2.outputs[0], no.inputs['Alpha'])
    
def findCurve(animation_data, data_path):
    for c in animation_data.action.fcurves.values():
        if c.data_path == data_path:
            return c
        
def fadeToGrey(c, c2, t0, t1, t2):
    mat = bpy.data.materials.new('fadeToGrey')
    
    mat.use_transparency=1
    mat.diffuse_color=c
    mat.alpha=0
    mat.emit=0.2
    
    mat.keyframe_insert(data_path='alpha', frame =1)
    
    mat.alpha=1
    mat.keyframe_insert(data_path='alpha', frame=t0)
    
    mat.keyframe_insert(data_path='diffuse_color', frame=t1)
    
    mat.diffuse_color=c2
    mat.keyframe_insert(data_path='diffuse_color', frame=t2)
    
    fc = findCurve(mat.animation_data, 'alpha')
    kp = fc.keyframe_points.values()
    kp[0].interpolation = 'CONSTANT'
    kp[1].interpolation = 'LINEAR'
#    fc.keyframe_points.remove(kp[2])
    
    
    return mat
    
def flashIn(t0, t1, t2):
    rval = bpy.data.materials.new('flashIn')

    rval.use_transparency=1
    rval.diffuse_color=(1,1,1)
    rval.alpha=0
    rval.emit=1
    rval.diffuse_intensity=0

    rval.keyframe_insert(data_path='alpha', frame=t0)

    rval.alpha=1
    rval.keyframe_insert(data_path='alpha', frame=t1)

    rval.alpha=0
    rval.keyframe_insert(data_path='alpha', frame=t2)
    
    kp = findCurve(rval.animation_data, 'alpha').keyframe_points.values()
    kp[0].interpolation='LINEAR'
    kp[1].interpolation= 'LINEAR'
    
    return rval


def knotworkMaterial(c, t0, t1, t2, t3):
    mat = bpy.data.materials.new("popIn")
    
    materialNodeMix(mat, fadeToGrey( (0,0.8,0), (0.5,0.5,0.5), t1, t2, t3),
    flashIn(t0, t1, t1+10),
    bpy.data.textures['knot 2'] )
    
    #mat.use_face_texture = 1
    #mat.use_face_texture_alpha=1
    mat.use_transparency = 1
    
    return mat

def knotworkMaterial2(c, t0, t1, t2, t3):
    mat = bpy.data.materials.new("popIn")
    
    materialNodeMix(mat, fadeToGrey( c, (0.5,0.5,0.5), t1, t2, t3),
    flashIn(t0, t1, t1+10),
    bpy.data.textures['knot 3'] )
    
    #mat.use_face_texture = 1
    #mat.use_face_texture_alpha=1
    mat.use_transparency = 1
    
    return mat


def putInGroup(o, gn):
    if gn in bpy.data.groups:
        group = bpy.data.groups[gn]
    else:
        group = bpy.data.groups.new(gn)

    group.objects.link(o)

def addLump(x,y,z, t):
    o2 = duplicateObject(bpy.context.scene, "lump", bpy.context.object)
    o2.location = (x,y,z)
    o2.hide_render=1
    o2.hide = 1
    fr = t*10
    o2.keyframe_insert(data_path="hide_render", frame=1)
    o2.keyframe_insert(data_path="hide", frame=1)
    o2.hide_render = 0
    o2.hide = 0
    o2.keyframe_insert(data_path="hide_render", frame=fr)
    o2.keyframe_insert(data_path="hide", frame=fr)
#    m1 = popUpMaterial( (0,0.8,0) , fr, fr+7, fr+20, fr+600)
    m1 = knotworkMaterial( (0,0.8,0) , fr, fr+7, fr+20, fr+600)
    m3 = knotworkMaterial2((0,0,1) , fr, fr+7, fr+20, fr+600)
    o2.data.materials.append(m1)
    o2.data.materials.append(m3)
    
    for fi in range(6, len(o2.data.polygons)):
        o2.data.polygons[fi].material_index=1
    
    o2.data.uv_textures.new("hippo")
    putInGroup(o2, "lumps")

addLump(0.0, 0.0, 0.0,  1)
