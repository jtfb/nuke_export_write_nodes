import nuke

def find_connected_read(node):
    """
    Recursively find the first connected Read node upstream.
    Returns the Read node if found, or None if no Read node is connected.
    """
    for input_node in nuke.dependencies(node):
        if input_node.Class() == 'Read':
            return input_node
        else:
            # Recursively search upstream
            upstream_read = find_connected_read(input_node)
            if upstream_read:
                return upstream_read
    return None

def render_enabled_write_nodes():
    """
    Finds all enabled Write nodes, determines the frame range from a connected Read node,
    and renders each Write node accordingly.
    """
    # Get all enabled Write nodes
    write_nodes = [node for node in nuke.allNodes('Write') if not node['disable'].value()]

    if not write_nodes:
        nuke.message("No enabled Write nodes found in the script.")
        return

    for write_node in write_nodes:
        # Get the connected Read node
        connected_read = find_connected_read(write_node)

        if connected_read:
            # Use the frame range from the connected Read node
            first_frame = 1000
            last_frame = int(connected_read['last'].value())
        else:
            # Use the Nuke script frame range if no Read node is found
            first_frame = 1000
            last_frame = int(nuke.root()['last_frame'].value())

        # Render the Write node using the determined frame range
        print(f"Rendering node: {write_node.name()} from frame {first_frame} to {last_frame}")
        nuke.execute(write_node, first_frame, last_frame)

    print("All enabled Write nodes have been rendered.")

# Call the function to render all enabled Write nodes
render_enabled_write_nodes()
