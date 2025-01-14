# Vehicle-Routing-Optimization & Shortest Path Finder
This project processes OpenStreetMap (OSM) data to analyze road networks and visualize the shortest path between nodes using Dijkstra’s algorithm. The system parses OSM data, generates node connectivity matrices, and creates interactive maps using Folium. It allows users to select source and destination nodes and view the computed shortest path on an interactive map.

Features
OSM Data Parsing: Extracts node coordinates, ways (roads), and their relationships.
Connectivity Matrix: Builds a matrix representing node connectivity based on road types (e.g., highways, residential roads).
Shortest Path Calculation: Uses Dijkstra’s algorithm to find the shortest path between any two nodes.
Interactive Map Generation: Visualizes:
All nodes in the network.
Nodes connected to a selected source node.
The shortest path between source and destination.


How It Works
Data Parsing: The script reads the OSM file, parsing essential data (nodes, ways, and road tags).
Connectivity Matrix: The road network is converted into a connectivity matrix, where roads between nodes are represented as edges.
Dijkstra's Algorithm: Calculates the shortest path between the selected source and destination nodes.
Map Visualization: Interactive maps are generated using Folium to display nodes and paths.



Usage Requirements
Python 3.x
Install dependencies:
bash
```pip install -r requirements.txt```


Interacting with the Maps:

First Map: Displays all nodes in the network.
Source Node: Input a node ID to see nearby connected nodes.
Destination Node: Select a destination, and the shortest path is displayed on the map.
Example Output:
All Node Map: Displays all nodes.
Closest Nodes Map: Shows nodes nearest to the source.
Path Map: Displays the shortest route between source and destination nodes.


Algorithm :
The project uses Dijkstra’s algorithm to find the shortest path between two nodes by iteratively visiting the nearest unvisited node and updating its distance from the source. The algorithm terminates when the destination node is reached.

Visualization :
Interactive HTML maps generated with Folium:

Nodes are shown as green markers.
Source Node is highlighted in blue.
Destination Node is shown in red.
Shortest Path is drawn as a blue line between the source and destination.



# License
This project is open-source under the MIT License.


