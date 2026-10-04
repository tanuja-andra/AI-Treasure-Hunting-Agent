AI Treasure Hunting Agent

Project Description

AI Treasure Hunting Agent is an intelligent grid-based search system that finds a hidden treasure using Artificial Intelligence search algorithms.

The agent operates in a 10 × 10 grid containing a starting position, a treasure, and obstacles. It uses search algorithms to find a path from the starting point to the treasure while avoiding obstacles.

The project supports both Known and Unknown environments.

Objectives

- Find the treasure efficiently in a grid environment.
- Implement and compare different AI search algorithms.
- Compare the performance of Best First Search and A* Search.
- Demonstrate the difference between searching in Known and Unknown environments.
- Visualize the search process and final path using a Streamlit web application.

Algorithms Used

1. Best First Search

Best First Search selects the next cell based on its heuristic value.

The heuristic used in this project is Manhattan Distance:

h(n) = |current_row - goal_row| + |current_column - goal_column|

2. A* Search

A* combines the actual cost of reaching a cell with the estimated cost to the treasure.

f(n) = g(n) + h(n)

Where:

- g(n) = cost from the starting position to the current cell
- h(n) = Manhattan distance from the current cell to the treasure

Environment Types

1. Known Environment

In the Known environment, the agent can see the complete grid and knows where all obstacles are located before starting the search.

2. Unknown Environment

In the Unknown environment, the agent does not initially know where the obstacles are.

The agent discovers cells while moving through the environment and updates its knowledge before replanning its path.

Grid

The project uses a 10 × 10 grid.

Starting Position: (0, 0)

Treasure Position: (9, 9)

The user can generate obstacles and run the selected search algorithm.

Technologies Used

- Python
- Streamlit
- Pandas
- Heap Queue (heapq)
- Artificial Intelligence Search Algorithms

Features

- 10 × 10 interactive grid
- Random obstacle generation
- Best First Search
- A* Search
- Known environment
- Unknown environment
- Treasure and obstacle visualization
- Final path visualization
- Cells explored calculation
- Path length calculation
- Execution time calculation
- Comparison of Best First Search and A*

Performance Comparison

The application compares the algorithms based on the following metrics:

| Metric | Description |
|--------|-------------|
| Cells Explored | Number of cells explored or discovered |
| Path Length | Number of moves from the start to the treasure |
| Execution Time | Time taken by the algorithm to complete the search |

How to Run the Project

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/AI-Treasure-Hunting-Agent.git

2. Open the Project Folder

cd AI-Treasure-Hunting-Agent

3. Install the Required Packages

pip install -r requirements.txt

4. Run the Streamlit Application

streamlit run app.py

The application will open in your web browser.

Requirements

The project requires the following Python packages:

- streamlit
- pandas

These dependencies are listed in the requirements.txt file.

How to Use

1. Open the application.
2. Select the required environment:
   - Known
   - Unknown
3. Select a search algorithm:
   - Best First Search
   - A* Search
4. Generate obstacles.
5. Click Run Search.
6. View the discovered cells and final path.
7. Run both algorithms on the same grid.
8. Click Compare Results to compare their performance.

If no obstacles are present, the application asks the user to generate obstacles before running the search.

Project Type

College Project Based Learning (PBL) Project

Project Title: AI Treasure Hunting Agent

Objective: To demonstrate and compare AI search algorithms for finding a treasure in a grid-based environment with obstacles.