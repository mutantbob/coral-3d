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

def popUpMaterial( c, t0, t1, t2):
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
    rval.emit=0
    rval.diffuse_intensity=0.8
    rval.keyframe_insert(data_path='diffuse_color', frame=t2)
    rval.keyframe_insert(data_path='diffuse_intensity', frame=t2)
    rval.keyframe_insert(data_path='emit', frame=t2)
    return rval



def fillLayer(x0,y0,z0, xCount,yCount, t0,dt):

    times=[]
    for t in range(0,xCount*yCount):
        times.append(t0+dt*t)

    for u in range(0,xCount):
        for v in range(0,yCount):
            o2 = duplicateObject(bpy.context.scene, "bacon", bpy.context.object)

            o2.location = ( x0+u*4, y0+v*4, z0)
            o2.hide_render = 1
            fr = times.pop(random.randint(0, len(times)-1))
            o2.keyframe_insert(data_path="hide_render", frame=1)
            o2.hide_render = 0
            o2.keyframe_insert(data_path="hide_render", frame=fr)
            m1 = popUpMaterial( (0,0.8,0) , fr, fr+5, fr+10)
            o2.data.materials.append(m1)


def addLump(x,y,z, t):
    o2 = duplicateObject(bpy.context.scene, "bacon", bpy.context.object)
    o2.location = (x,y,z)
    o2.hide_render=1
    fr = t*10
    o2.keyframe_insert(data_path="hide_render", frame=1)
    o2.hide_render = 0
    o2.keyframe_insert(data_path="hide_render", frame=fr)
    m1 = popUpMaterial( (0,0.8,0) , fr, fr+7, fr+20)
    o2.data.materials.append(m1)

#fillLayer(-20,0,0, 5,4, 5,3)
