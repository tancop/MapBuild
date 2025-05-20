import bpy
import os

bl_info = {
    "name": "MapBuild",
    "category": "Export",
    "author": "Trap Money Games",
    "description": "Export a game map to Godot",
    "blender": (4, 4, 0),
    "version": (1, 0)
}

class MapExportOperator(bpy.types.Operator):
    bl_idname = "export_scene.gltf_map"
    bl_label = "Export Map as glTF"

    def replace_with_empty(self):
        dollar_objects = [obj for obj in bpy.data.objects if obj.name.startswith("$")]

        for obj in dollar_objects:
            bpy.ops.object.add(type='EMPTY', location=obj.location)
            target = bpy.context.object

            real_name = obj.name
            obj.name = "_" + obj.name

            target.name = real_name
            target.matrix_world = obj.matrix_world

            for coll in target.users_collection:
                coll.objects.unlink(target)

            for coll in obj.users_collection:
                coll.objects.link(target)


            # Hide the original
            obj.hide_set(True)
            obj.hide_render = True

            print(f"Created empty from {obj.name}")

    def replace_back(self):
        empty_objects = [obj for obj in bpy.data.objects if obj.name.startswith("$")]
        moved_objects = [obj for obj in bpy.data.objects if obj.name.startswith("_$")]

        for obj in empty_objects:
            bpy.data.objects.remove(obj, do_unlink=True)

        for obj in moved_objects:
            obj.hide_set(False)
            obj.hide_render = False
            obj.name = obj.name[1:]

    def execute(self, context):
        blend_path = bpy.data.filepath
        if not blend_path:
            raise Exception("Please save your .blend file first")

        self.replace_with_empty()

        # Create the glb path by replacing extension
        glb_path = os.path.splitext(blend_path)[0] + ".glb"

        bpy.ops.export_scene.gltf(filepath=glb_path, export_materials='PLACEHOLDER',
            use_visible=True, export_apply=True)

        self.replace_back()
        return {'FINISHED'}

addon_keymaps = []

def register():
    bpy.utils.register_class(MapExportOperator)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new(MapExportOperator.bl_idname, 'E', 'PRESS', ctrl=True, shift=True)
    addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_class(MapExportOperator)

    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
