#   Ullman's Subgraph Isomorphism Test

This repository contains the implementation of the Ullman algorithm to test whether one graph is a subgraph of another.

## Installation

#### Prerequisites
- Python >= 3.10

#### Install
```bash
# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install the Python package
python3 -m pip install -e .
```

### Initialization of the Future Match Table
$$
F(u, v) =
\begin{cases}
1, & \text{if } \deg(u) \leq \deg(v) \\
0, & \text{otherwise}
\end{cases}
$$

### Edge Structure Constraint Check

To check the edge structure constraint:

$$
\text{if} \quad A_1[u, w] \neq A_2[v, w']: \quad F(w, w') = 0
$$