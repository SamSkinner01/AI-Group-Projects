#include <iostream>
#include <vector> 

using namespace std;

// Goal State for 8-Puzzle
const vector<vector<int> > goal_state = {
        {0,1,2},
        {3,4,5},
        {6,7,8}
};

// Will return the row and column value for the goal state
const vector<vector<int> > row_col_for_goal = {
        {0,1},  // 1
        {0,2},  // 2
        {1,0},  // 3
        {1,1},  // 4
        {1,2},  // 5
        {2,0},  // 6
        {2,1},  // 7
        {2,2}   // 8
};


// Node struct
struct Node {
    vector<vector<int> > state;
    Node* Parent;
    int path_cost;
    string action;
};

void print_state(vector<vector<int> > state){
    // Function to print the state of the 8-Puzzle
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            cout << state[i][j] << " ";
        }
        cout << endl;
    }
}

bool is_goal(vector<vector<int> > state){
    // Checks if the state is the goal state
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            if(state[i][j] != goal_state[i][j]){
                return false;
            }
        }
    }
    return true;
}

int mahattan_distance_heuristic(vector<vector<int> > state){
    int distance = 0;
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            int value = state[i][j];
            if(value != 0){
                // Get the goal row and column from global variable
                int goal_row = row_col_for_goal[value-1][0]; // gets index for value - 1 (so like value 1 is index 0 in const array)
                int goal_col = row_col_for_goal[value-1][1]; // and gets the row ([0]) and col ([1])

                // Calculte x and y distance 
                // and add to the total distance
                distance += abs(goal_row - i) + abs(goal_col - j);
            }
        }
    }
    return distance;
}

int evaluation_function(vector<vector<int> > state, int path_cost){
    // defines the evaluation function f(n) = g(n) + h(n)
    return path_cost + mahattan_distance_heuristic(state);
}

int find_index_of_empty(vector<vector<int> > state, int* row, int* col){
    // Finds the empty space in the state
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            if(state[i][j] == 0){
                *row = i;
                *col = j;
            }
        }
    }
    return -1, -1;
}

vector<vector<int> > move(vector<vector<int> > state, string choice){
    // Make a copy of the state and initialize an empty state for if the move is not valid
    vector<vector<int> > new_state = state;
    vector<vector<int> > empty = {{0,0,0},{0,0,0},{0,0,0}};
    
    // Find the index of the empty space
    int row, col;
    find_index_of_empty(state, &row, &col);

    // Make the move
    if(choice == "up"){
        // Check if the move is legal
        if(row == 0){
            return empty;
        }
        else{
            int temp = new_state[row][col];
            new_state[row][col] = new_state[row-1][col];
            new_state[row-1][col] = temp;
            return new_state;
        }
    }
    else if(choice == "down"){
        // Check if the move is legal
        if(row == 2){
            return empty;
        }
        else{
            int temp = new_state[row][col];
            new_state[row][col] = new_state[row+1][col];
            new_state[row+1][col] = temp;
            return new_state;
        }
    }
    else if(choice == "left"){
        // Check if the move is legal
        if(col == 0){
            return empty;
        }
        else{
            int temp = new_state[row][col];
            new_state[row][col] = new_state[row][col-1];
            new_state[row][col-1] = temp;
            return new_state;
        }
    }
    else if(choice == "right"){
        // Check if the move is legal
        if(col == 2){
            return empty;
        }
        else{
            int temp = new_state[row][col];
            new_state[row][col] = new_state[row][col+1];
            new_state[row][col+1] = temp;
            return new_state;
        }
    }
    else{
        return empty;
    }
}

vector<Node> expand(vector<vector<int> > state, Node* node){
    // Initialize a vector of children
    vector<Node> children;
    // All possible moves
    vector<string> choices = {"up", "down", "left", "right"};
    
    // For all possible moves
    for(int i = 0; i < 4; i++){
        // Return the state for making a move
        vector<vector<int> > new_state = move(state, choices[i]);
        
        // If the move is a valid move, add it to the vector of children
        if(new_state != vector<vector<int> >{{0,0,0},{0,0,0},{0,0,0}}){
            Node child;
            child.state = new_state;
            child.action = choices[i];
            child.path_cost = node->path_cost + 1;
            child.Parent = node;
            children.push_back(child);
        }
    }
    return children;
}

Node* create_initial_node(vector<vector<int> > state){
    // Creates the inital node with the given initial state
    Node* initial_node = new Node;
    initial_node->state = state;
    initial_node->Parent = NULL;
    initial_node->path_cost = 0;
    initial_node->action = "None";
    return initial_node;
}

Node* pop_from_frontier(vector<Node>& frontier){
    // Initialize the lowest index and value
    int lowest_index = 0;
    int lowest_value = evaluation_function(frontier[0].state, frontier[0].path_cost);
    
    // Check all other nodes in the frontier
    // If one has a lower evaluation function, set it as the lowest
    for(int i = 1; i < frontier.size(); i++){
        int value = evaluation_function(frontier[i].state, frontier[i].path_cost);
        if(value < lowest_value){
            lowest_value = value;
            lowest_index = i;
        }
    }

    // Create node to pop and remove the lowest node from the frontier
    Node* node = new Node;
    *node = frontier[lowest_index];
    frontier.erase(frontier.begin() + lowest_index);
    return node;
}


Node* a_star(Node* initial_node){
    // Initialize the frontier and add the initial node to it
    vector<Node> frontier;
    frontier.push_back(*initial_node);

    // Initialize Reached
    vector<Node> reached;

    // While the frontier is not empty
    while(frontier.size() != 0){
        // Pop the node with the lowest evaluation function
        Node* node = new Node;
        node = pop_from_frontier(frontier);

        // Check if it is the goal state
        if(is_goal(node->state)){
            return node;
        }

        // If not the goal state
        // Expand the node into it's children
        vector<Node> children = expand(node->state, node);

        // For all the children
        for(int i = 0; i < children.size(); i++){
            // Get state of the child
            vector<vector<int> > s = children[i].state;

            // Assume not in reached
            bool in_reached = false;
            
            // Check if in reached
            for(int j = 0; j < reached.size(); j++){
                if(s == reached[j].state){
                    in_reached = true;
                }
            }

            // If not in reached, or is a better path add to frontier and reached
            if(!in_reached || children[i].path_cost < reached[i].path_cost){
                frontier.push_back(children[i]);
                reached.push_back(children[i]);
            }
        }
    }

    // If no solution is found at all
    return NULL;

}

void print_path(Node* node){
    Node *temp = node; 
    vector<Node> path;
    while(temp != NULL){
        path.push_back(*temp);
        temp = temp->Parent;
    }
    for(int i = path.size()-1; i >= 0; i--){
        cout << "Action: " << path[i].action << endl;
        print_state(path[i].state);
        cout << endl;
    }
}

int main(){
    // List of initial states to test
    vector<vector<vector<int>> > list_of_initial_goal_states{{
        // 0
        {
            {1, 2, 3},
            {4, 5, 6},
            {0, 7, 8}
        },

        // 1
        {   
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 0}
        },

        // 2
        {
            {5, 6, 7},
            {4, 0, 8},
            {3, 2, 1}
        },
        // 3
        {
            {1, 0, 2},
            {3, 4, 5},
            {6, 7, 8}
        },

        // 4
        {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 0}
        },

        // 5
        {
            {3, 1, 2},
            {4, 0, 5},
            {6, 7, 8}
        },

        // 6
        {
            {1, 8, 3},
            {6, 2, 5},
            {7, 4, 0}
        }
    }};

    // Create the initial node and print
    Node *initial_node = create_initial_node(list_of_initial_goal_states[6]);
    print_state(initial_node->state);

    // Get the goal node and print the path it took if it exists.
    Node *goal_node = a_star(initial_node);

    if (goal_node == NULL){
        cout << "No solution found" << endl;
        return 0;
    }
    print_path(goal_node);

    // Print the path cost
    cout << "Path Cost: " << goal_node->path_cost << endl;

}