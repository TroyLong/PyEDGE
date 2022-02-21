# PyEDGE TODO List

## Module Goals
### Data Types
- [ ] Use pytest platform to find accuracy of connections

### Analysis
- [ ] Run speed test on the deepcopy versions of filters.
- [ ] Currently neighborhood analysis has to be run a few times before removing noise in the data.
- [ ] Fix the intersection neighbor filter. This got worse after AppCore was created
- [x] Leverage filters to use the remove neighbor functions

### Multi-Image Analysis
- [ ] Continue to develop useful functions
- [ ] Build in appropriate calling to single-state analysis
- [ ] Ensure data types and large state loading is stable
- [x] Built Gui connections to Multi-Image Analysis.

### GUI
- [ ] Fix the open menu so it does not throw an error if canceled.
- [ ] Introduce multi-file image open support.
- [ ] Integrate a multi-image analysis panel.
- [ ] Set values of the gui to be rescalable. Not important now, but will help small screen users.

- - -

## Framework Goals
### Project Layout
- [ ] splitting AppFrame and AppCore might have effected filters
- [x] split app gui into AppFrame and AppCore objects


### Testing
- [ ] Build interface to AppCore
- [ ] Test Immutability/copy/deepcopy for dataTypes, and the results of deleting from other objects.

- - -

## Paradigm Goals
### Object Oriented
- [ ] Abstractify and build interfaces as program becomes more complex
- [ ] Consider command objects
- [x] Seperating the responsibilties of the panels helped split of AppFrame and AppCore
- [x] Read Docs Python Tutorial

### Functional
- [ ] Continue to isolate "side effects"