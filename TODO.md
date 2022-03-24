# PyEDGE TODO List


## Version One Goals
- [ ] Conduct super-state analysis
- [x] Segment cells from image with openCV
- [x] Reduce and clean cell segment data
- [x] Construct GUI interface
- [x] Export data with Pandas

## Module Goals
### Data Types
- [ ] Use pytest platform to find accuracy of connections
- [ ] Make 3D datatype for states

### Analysis
- [ ] Run speed test on the deepcopy versions of filters.
- [ ] Currently neighborhood analysis has to be run a few times before removing noise in the data.
- [ ] Fix the intersection neighbor filter. This got worse after AppCore was created

### Multi-Image Analysis
- [ ] Create arbitary state roll-through
- [ ] Use roll-through data to construct super-state
- [ ] Build in appropriate calling to single-state analysis
- [ ] Ensure data types and large state loading is stable

### GUI
- [ ] Fix the open menu so it does not throw an error if canceled.
- [ ] Introduce multi-file image open support.
- [ ] Integrate a multi-image analysis panel.
- [ ] Set values of the gui to be rescalable. Not important now, but will help small screen users.
- [ ] Graphs are growing and shrinking. Find a way to lock this

- - -

## Framework Goals
### Project Layout
- [ ] splitting AppFrame and AppCore might have effected filters
- [ ] Split state mechanism from AppCore
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