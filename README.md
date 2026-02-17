Course: AI 2002 – Artificial Intelligence (Spring 2026)  
Roll Numbers: 24F-0712, 24F-0808  

Project Overview  
AI-Pathfinder-Visualiser is a Python-based GUI application that visually demonstrates how different Artificial Intelligence search algorithms work on a 10×10 grid.

Users can:  
- Select a start node  
- Select a target node  
- Choose a search algorithm  
- Watch the algorithm explore the grid in real time  
- See the final shortest/valid path highlighted  

This project helps in understanding core AI search techniques through visualization.  

Features  
- 10×10 interactive grid  
- Strict clockwise 8-directional movement  
- Real-time animated visualization  
- Multiple AI search algorithms  
- Color-coded grid states  
- Clean cyber-style user interface  

Algorithms Implemented  
- Breadth-First Search (BFS): Explores level by level, guarantees shortest path in unweighted graphs  
- Depth-First Search (DFS): Explores deeply before backtracking, uses stack (LIFO)  
- Uniform Cost Search (UCS): Expands lowest-cost node first, diagonal movement cost = 1.4, straight movement cost = 1.0  
- Depth-Limited Search (DLS): DFS with a depth limit  
- Iterative Deepening DFS (IDDFS): Repeated DLS with increasing depth  
- Bidirectional Search: Searches simultaneously from start and target  

How to Use the Application  
- Run the program.  
- Click any grid cell to set the Start node.  
- Click another cell to set the Target node.  
- Select a search algorithm from the dropdown (or keyboard key).  
- Click RUN to start visualization.  
- Click RESET to clear the grid.
