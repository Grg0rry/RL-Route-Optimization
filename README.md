# RL-Route-Optimization

Route Optimization algorithm that is used to find the most optimal route to travel with the starting and ending point selected.

This study uses SUMO (more specifically the netedit file) to simulate the Road Network, with the agent as Reinforcement Learning models (SARSA and Q_Learning algorithm) to learn from the network environment and find the most optimal route.

## Project Scope

As there are multiple factors involved selecting the most optimal route, below are the factors that has been preset for this study:
- Traffic network is constant (no sudden abnormalities like accidents, weather changes, and natural disasters (floods, landslides, etc.))
- Speed is constant
- No traffic light

## Method of Evaluation

1. Comparision of the routes selected from the agent vs the baseline model (Dijkstra) 
2. Comparision on the cost function (distance travelled)
3. Comparision of the number of episodes taken to converge (SARSA vs Q_Learning)
4. Comparision on the time taken for the computation (selecting the optimal route)

## Method to Run

1. Download SUMO (https://sumo.dlr.de/docs/Downloads.php)
2. Clone this repository to your local machine.
3. Install the ncecessary packages
```
pip install -r requirements.txt
```
4. Update the main.py with your SUMO directory to set the environment variable
```
def sumo_configuration():
    os.environ["SUMO_HOME"] = "D:/app/SUMO/SUMO/" # -- change to own directory
    ...
```
5. Upload your netedit file and update the network_file variable
```
network_file = './network_files/fixed_network.net.xml'
```
**More on Netedit:** https://sumo.dlr.de/docs/Netedit/index.html 

6. Run the code
```
> python main.py
```
