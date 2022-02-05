# PyEDGE TODO List

## Module Goals
### Data Types
- [ ] Test connection between cells and neighbors in a pytest setting. I am not sure if they are working as expected
- [x] Design a controlled connection between cells and neighbors

### Analysis
- [ ] Leverage filters to use the remove neighbor functions
- [ ] Run speed test on the old, new, and deepcopy versions of filters.
- [ ] Currently neighborhood analysis has to be run a few times before removing noise in the data.
- [ ] Fix the intersection neighbor filter.
- [x] Fixed the neighbor analysis so it removes neighbors when analysis is rerun. Histogram finally works.

### Multi-Image Analysis
- [ ] Continue to develop useful functions
- [ ] Build in appropriate calling to single-state analysis
- [ ] Ensure data types and large state loading is stable

### GUI
- [ ] Fix the open menu so it does not throw an error if canceled.
- [ ] Introduce multi-file image open support.
- [ ] Integrate a multi-image analysis panel.
- [ ] Set values of the gui to be rescalable. Not important now, but will help small screen users.

- - -

## Framework Goals
### Project Layout
- [x] Split code into multiple packages for source code clarity.
- [x] Found consistant way to import modules
- [x] Leveraged tuples throughout code, and introduced functional programming techniques.

### Testing
- [ ] Develop a testing platform using pytest

- - -

## Paradigm Goals
### Object Oriented
- [ ] Read on Python specific OOP
- [ ] Abstractify and build interfaces as program becomes more complex
### Functional
- [ ] Continue to isolate "side effects"