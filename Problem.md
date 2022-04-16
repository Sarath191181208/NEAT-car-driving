## Finding an optimal course and speed in car racing.

Statement:

- All of the modren autonomous driving algorithms try to generalize the self driving car algorithm. This is completely fine when speed and road relavance are out of the picture. This is hardly the case in racing. Tracks rarely change & Speed is of utmost importance.

- We need to generate an algorithm that reliably tries to pass through the checkpoints and laps around the track in a well grounded manner.

Similar Papers:

- https://ieeexplore.ieee.org/abstract/document/9488179
- https://arxiv.org/abs/2112.06435
- https://arxiv.org/abs/2111.15343

Relavant:

- https://ieeexplore.ieee.org/abstract/document/9562079
- https://arxiv.org/abs/2103.04909

**Algorithm:** The algorithm consists of two parts on

1. The scanning phase -> using A\* algorithm to apply the fitness points.

2. The training phase -> using the NEAT algorithm to find the most optimal route the heuristic is going to be defined by our scanning phase.

How is this differnet :

- Most of the self drivinng car algoritms generalize too much this inturn gives almost to no significance to speed of the car. We are tyring to address this issue.

Drawbacks:

1. **Time:**
   The algorithms takes a while to train this can be further imporved by having a referece motion tracing which is a firm task on it's own. But some papers are gonna adress this issue. We can also train in a more simpler track and use it to reduce time.
2. **Possibility of sub optimal path**
   As we are not searching through the whole search space our algorithm can be stuck in a sub-optimal path thus it's children linger in the same way.This can e addressed using an optimal latent space.

```python3
[NEAT]
fitness_criterion     = max
fitness_threshold     = 100000000
pop_size              = 200
reset_on_extinction   = True

[DefaultGenome]
# node activation options
activation_default      = tanh
activation_mutate_rate  = 0.01
activation_options      = tanh

# node aggregation options
aggregation_default     = sum
aggregation_mutate_rate = 0.01
aggregation_options     = sum

# node bias options
bias_init_mean          = 0.0
bias_init_stdev         = 1.0
bias_max_value          = 30.0
bias_min_value          = -30.0
bias_mutate_power       = 0.5
bias_mutate_rate        = 0.7
bias_replace_rate       = 0.1

# genome compatibility options
compatibility_disjoint_coefficient = 1.0
compatibility_weight_coefficient   = 0.5

# connection add/remove rates
conn_add_prob           = 0.5
conn_delete_prob        = 0.5

# connection enable options
enabled_default         = True
enabled_mutate_rate     = 0.01

feed_forward            = True
initial_connection      = full

# node add/remove rates
node_add_prob           = 0.2
node_delete_prob        = 0.2

# network parameters
num_hidden              = 0
num_inputs              = 5
num_outputs             = 4

# node response options
response_init_mean      = 1.0
response_init_stdev     = 0.0
response_max_value      = 30.0
response_min_value      = -30.0
response_mutate_power   = 0.0
response_mutate_rate    = 0.0
response_replace_rate   = 0.0

# connection weight options
weight_init_mean        = 0.0
weight_init_stdev       = 1.0
weight_max_value        = 30
weight_min_value        = -30
weight_mutate_power     = 0.5
weight_mutate_rate      = 0.8
weight_replace_rate     = 0.1

[DefaultSpeciesSet]
compatibility_threshold = 2.0

[DefaultStagnation]
species_fitness_func = max
max_stagnation       = 20
species_elitism      = 2

[DefaultReproduction]
elitism            = 3
survival_threshold = 0.2

```
