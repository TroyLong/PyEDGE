# PyEDGE TODO List

## Major House-Keeping Goals
- [x] Rewrite data structures to be slots objects
- [x] Rewrite filters to work with new data structures
- [ ] Make sibling classes fit a standard format

## Module Goals
### Data Types
- [ ] Use pytest platform to find accuracy of connections
- [x] Make State() a slots object

### Analysis
- [ ] Currently neighborhood analysis has to be run a few times before removing noise in the data
- [x] Fix the intersection neighbor filter. This got worse after AppCore was created

### Multi-Image Analysis
- [ ] Replace/Swap/Delete states
- [ ] Handle missing data states well
- [ ] Ensure data types and large state loading is stable

### GUI
- [ ] Fix the open menu so it does not throw an error if canceled.
- [ ] Set values of the gui to be rescalable. Not important now, but will help small screen users

- - -

## Framework Goals
### Project Layout
- [ ] splitting AppFrame and AppCore might have effected filters
- [ ] Protect against bad data loading to states

### Testing
- [ ] Build interface to AppCore
- [ ] Test Immutability/copy/deepcopy for dataTypes, and the results of deleting from other objects.

- - -

## Paradigm Goals
### Object Oriented
- [ ] Abstractify and build interfaces as program becomes more complex
- [ ] Consider command objects

### Functional
- [ ] Continue to isolate "side effects"