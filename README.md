# Road Traffic Equlibrium

Implementation and testing for 3 algorithms used for the traffic assignment problem.

## Development:

### Requirements:

The project was developed with:

- Python 3.10.2
- Pip 21.2.4

### Install packages:

To restore packages run:

```
pip install -r requirements.txt
```

### Run project:

Running env:

```
.\.venv\Scripts\activate
```

Running MyPy;

```
mypy main.py
```

Profiler:
```
snakeviz .\tmp\tmp.prof
```

### Save installed packages:

To save the packages installed in the project run:

```
pip freeze > requirements.txt
```

## How to read data files:

Data files can be found at `src/data/<city-name>`.

- `<city-name>_net.tntp` - Network
- `<city-name>_trips.tntp` - Demand
- `<city-name>_node.tntp` - Node Coordinates
- `<city-name>_flow.tntp` - Best known flow solution

For more info go to [Transportation Networks Repository](https://github.com/bstabler/TransportationNetworks).
