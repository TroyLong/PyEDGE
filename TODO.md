# PyEDGE TODO List


## Version One Goals
- [ ] Conduct super-state analysis of z
- [x] Conduct super-state analysis of time
- [x] Segment cells from image with openCV
- [x] Reduce and clean cell segment data
- [x] Construct GUI interface
- [x] Export data with Pandas

## Module Goals
### Data Types
- [ ] Use pytest platform to find accuracy of connections
- [ ] Make SingleState() a slots object
- [x] Make imageState Dictionary a SingleState() object

### Analysis
- [ ] Run speed test on the deepcopy versions of filters.
- [ ] Currently neighborhood analysis has to be run a few times before removing noise in the data.
- [ ] Fix the intersection neighbor filter. This got worse after AppCore was created

### Multi-Image Analysis
- [ ] Create z level roll-through
- [ ] Handle missing data states well
- [ ] Ensure data types and large state loading is stable
- [x] Use roll-through data to construct super-state
- [x] Build in appropriate calling to single-state analysis

### GUI
- [ ] Fix the open menu so it does not throw an error if canceled.
- [ ] Set values of the gui to be rescalable. Not important now, but will help small screen users.
- [x] Graphs are growing and shrinking. Find a way to lock this
- [x] Introduce multi-file image open support.
- [x] Integrate a multi-image analysis panel.


- - -

## Framework Goals
### Project Layout
- [ ] splitting AppFrame and AppCore might have effected filters
- [ ] Protect against bad data loading to states
- [x] I was initializing more objects than I wanted to. I removed the cause of duplicates


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