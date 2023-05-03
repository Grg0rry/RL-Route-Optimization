import os
import xml.etree.ElementTree as ET


def network_file_config(network_folder, node_file = 'nodes.nod.xml', edge_file = 'edges.edg.xml', network_output_file = 'network.net.xml'):
    # Change directory to store files
    os.chdir(network_folder)

    def nodes_setup():
        # Create XML document for nodes
        try:
            print(f"**Setting Up Node file --> {node_file} ...**")
            root = ET.Element("nodes")
            node1 = ET.SubElement(root, "node", {"id": "A", "x": "0", "y": "0"})
            node2 = ET.SubElement(root, "node", {"id": "B", "x": "100", "y": "100"})
            node3 = ET.SubElement(root, "node", {"id": "C", "x": "100", "y": "0"})
            node4 = ET.SubElement(root, "node", {"id": "D", "x": "100", "y": "-100"})
            node5 = ET.SubElement(root, "node", {"id": "E", "x": "200", "y": "100"})
            node6 = ET.SubElement(root, "node", {"id": "F", "x": "200", "y": "0"})
            node7 = ET.SubElement(root, "node", {"id": "G", "x": "200", "y": "-100"})
            node8 = ET.SubElement(root, "node", {"id": "H", "x": "300", "y": "100"})
            node9 = ET.SubElement(root, "node", {"id": "I", "x": "300", "y": "0"})
            node10 = ET.SubElement(root, "node", {"id": "J", "x": "300", "y": "-100"})
            node11 = ET.SubElement(root, "node", {"id": "K", "x": "400", "y": "100"})
            node12 = ET.SubElement(root, "node", {"id": "L", "x": "400", "y": "0"})
            node13 = ET.SubElement(root, "node", {"id": "M", "x": "400", "y": "-100"})
            node14 = ET.SubElement(root, "node", {"id": "N", "x": "500", "y": "0"})
            tree = ET.ElementTree(root)
            tree.write(node_file)
            print("**Setup Completed!**")
            print("**Successfully Setup Node file**\n")
        except Exception as e:
            print(f"**Error in setting up Node file: {e}**")
            sys.exit(1)
        
    
    def edges_setup():
        # Create XML document for edges
        try:
            print(f"**Setting Up Edge file --> {edge_file} ...**")
            root = ET.Element("edges")
            edge1 = ET.SubElement(root, "edge", {"id": "gneE0", "from": "A", "to": "C", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge2 = ET.SubElement(root, "edge", {"id": "-gneE0", "from": "C", "to": "A", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge3 = ET.SubElement(root, "edge", {"id": "gneE1", "from": "C", "to": "F", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge4 = ET.SubElement(root, "edge", {"id": "-gneE1", "from": "F", "to": "C", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge5 = ET.SubElement(root, "edge", {"id": "gneE2", "from": "F", "to": "I", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge6 = ET.SubElement(root, "edge", {"id": "-gneE2", "from": "I", "to": "F", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge7 = ET.SubElement(root, "edge", {"id": "gneE3", "from": "I", "to": "L", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge8 = ET.SubElement(root, "edge", {"id": "-gneE3", "from": "L", "to": "I", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge9 = ET.SubElement(root, "edge", {"id": "gneE4", "from": "L", "to": "N", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge10 = ET.SubElement(root, "edge", {"id": "-gneE4", "from": "N", "to": "L", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge11 = ET.SubElement(root, "edge", {"id": "gneE5", "from": "B", "to": "C", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge12 = ET.SubElement(root, "edge", {"id": "-gneE5", "from": "C", "to": "B", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge13 = ET.SubElement(root, "edge", {"id": "gneE6", "from": "B", "to": "E", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge14 = ET.SubElement(root, "edge", {"id": "-gneE6", "from": "E", "to": "B", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge15 = ET.SubElement(root, "edge", {"id": "gneE7", "from": "E", "to": "H", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge16 = ET.SubElement(root, "edge", {"id": "-gneE7", "from": "H", "to": "E", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge17 = ET.SubElement(root, "edge", {"id": "gneE8", "from": "H", "to": "K", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge18 = ET.SubElement(root, "edge", {"id": "-gneE8", "from": "K", "to": "H", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge19 = ET.SubElement(root, "edge", {"id": "gneE9", "from": "K", "to": "L", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge20 = ET.SubElement(root, "edge", {"id": "-gneE9", "from": "L", "to": "K", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge21 = ET.SubElement(root, "edge", {"id": "gneE10", "from": "C", "to": "D", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge22 = ET.SubElement(root, "edge", {"id": "-gneE10", "from": "D", "to": "C", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge23 = ET.SubElement(root, "edge", {"id": "gneE11", "from": "D", "to": "G", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge24 = ET.SubElement(root, "edge", {"id": "-gneE11", "from": "G", "to": "D", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge25 = ET.SubElement(root, "edge", {"id": "gneE12", "from": "G", "to": "J", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge26 = ET.SubElement(root, "edge", {"id": "-gneE12", "from": "J", "to": "G", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge27 = ET.SubElement(root, "edge", {"id": "gneE13", "from": "J", "to": "M", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge28 = ET.SubElement(root, "edge", {"id": "-gneE13", "from": "M", "to": "J", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge29 = ET.SubElement(root, "edge", {"id": "gneE14", "from": "L", "to": "M", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge30 = ET.SubElement(root, "edge", {"id": "-gneE14", "from": "M", "to": "L", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge31 = ET.SubElement(root, "edge", {"id": "gneE15", "from": "E", "to": "F", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge32 = ET.SubElement(root, "edge", {"id": "-gneE15", "from": "F", "to": "E", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge33 = ET.SubElement(root, "edge", {"id": "gneE16", "from": "F", "to": "G", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge34 = ET.SubElement(root, "edge", {"id": "-gneE16", "from": "G", "to": "F", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge35 = ET.SubElement(root, "edge", {"id": "gneE17", "from": "H", "to": "I", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge36 = ET.SubElement(root, "edge", {"id": "-gneE17", "from": "I", "to": "H", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge37 = ET.SubElement(root, "edge", {"id": "gneE18", "from": "I", "to": "J", "priority": "1", "numLanes": "1", "speed": "13.89"})
            edge38 = ET.SubElement(root, "edge", {"id": "-gneE18", "from": "J", "to": "I", "priority": "1", "numLanes": "1", "speed": "13.89"})
            tree = ET.ElementTree(root)
            tree.write(edge_file)
            print("**Setup Completed!**")
            print("**Successfully Setup Edge file**\n")
        except Exception as e:
            print(f"**Error in setting up Edge file: {e}**")
            sys.exit(1)


    def network_SUMO_setup():
        # Convert Network XML to SUMO format
        try:
            print(f"**Converting Network file to SUMO format --> {network_output_file} ...**")
            os.system(f'netconvert --node-files={node_file} --edge-files={edge_file} --output-file={network_output_file}')        
            print("**Convert Completed!**")
            print("**Successfully Convert Network to SUMO**\n")
        except Exception as e:
            print(f"**Error in converting Network file to SUMO format: {e}**")
            sys.exit(1)
            

    # Call the setup functions
    nodes_setup()
    edges_setup()
    network_SUMO_setup()

    # Change back to parent dir (cd ..)
    os.chdir(os.pardir)

    # Return file name of network file
    return network_output_file