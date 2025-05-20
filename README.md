# MapBuild

This exports all Blender objects with a name starting in `$` as empty represented by a Node3D.
The Godot side takes this and spawns nodes based on their name - `$Player` loads and spawns
`scenes/Player.tscn`.

1. Save your blend file in your game's map folder
2. Press Shift-Ctrl-E to export
3. Drag the .glb file into your main scene in Godot
4. Add `godot/ImportMap.gd` to the imported root node
5. Click on the big `Import` button!
