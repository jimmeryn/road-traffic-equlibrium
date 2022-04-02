# Road Traffic Equlibrium

To save the packages installed in the project run:

```
pip freeze > requirements.txt
```

To restore packages run:

```
pip install -r requirements.txt
```

Running env:

```
.\.venv\Scripts\activate
```

## How to read data files:

- `<city-name>_net.tntp` - Network
- `<city-name>_trips.tntp` - Demand
- `<city-name>_node.tntp` - Node Coordinates
- `<city-name>_flow.tntp` - Best known flow solution

For more info go to [Transportation Networks Repository](https://github.com/bstabler/TransportationNetworks).

## TODO:

### Algorithms:

- [ ] Dial - Algorithm B - 2006
- [ ] Bar-Gera - OBA Algorithm - 2002
- [ ] Bar-Gera - TAPAS Algorithm - 2010

### Tests:

- [ ] 2x2 Graph
- [ ] 3x3 Graph
- [ ] SiouxFalls
- [ ] Another city from Transportation Networks Repository (Chicago-Sketch or Anahaim)
- [ ] Wroclaw (ITS)
