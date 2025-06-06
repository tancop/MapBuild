@tool
extends Node3D

@export_tool_button("Import") var btn: Callable = import_map

func replace_node(template: Node, new_node: Node, new_name: String) -> void:
	await get_tree().process_frame
	if new_node is Node3D:
		var node_3d := new_node as Node3D
		node_3d.global_transform = template.global_transform
	var parent := template.get_parent()
	if parent.has_node(new_name):
		parent.get_node(new_name).free()
	parent.add_child(new_node)
	new_node.name = new_name
	new_node.owner = self.owner
	template.hide()

func handle_node(node: Node) -> void:
	if node.name.begins_with("$"):
		var real_name := node.name.trim_prefix("$")
		var scene_name := real_name
		var right := real_name.right(4)
		if right[0] == "_":
			var tag := right.right(3)
			if tag.is_valid_int():
				# remove blender ".001"
				scene_name = real_name.left(-4)

		print("Spawning entity: ", real_name)
		var scene: PackedScene
		if FileAccess.file_exists("res://scenes/%s.tscn" % scene_name):
			# text
			scene = load("res://scenes/%s.tscn" % scene_name)
		elif FileAccess.file_exists("res://scenes/%s.scn" % scene_name):
			# binary
			scene = load("res://scenes/%s.scn" % scene_name)
		else:
			printerr("Scene with name \"%s\" doesn't exist in res://scenes" % scene_name)

		var new_node := scene.instantiate()
		replace_node(node, new_node, real_name)
		return

	for child in node.get_children():
		handle_node(child)

func import_map() -> void:
	print("Importing level")
	for child in get_children():
		handle_node(child)
