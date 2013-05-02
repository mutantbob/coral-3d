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
 
    # Link new object to the given scene and select it
    scene.objects.link(ob_new)
    ob_new.select = True
 
    return ob_new

o2 = duplicateObject(bpy.context.scene, "bacon", bpy.context.object)

o2.location.x = -random.random()*10
o2.location.y = random.random()*10
o2.hide_render = 1
o2.keyframe_insert(data_path="hide_render", frame=1)
o2.hide_render = 0
o2.keyframe_insert(data_path="hide_render", frame=random.randint(5,50))

