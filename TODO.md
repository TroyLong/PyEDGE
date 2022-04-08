# PyEDGE TODO List

## Major House-Keeping Goals
- [x] Rewrite data structures to be slots objects
- [x] Rewrite filters to work with new data structures
- [x] Make sibling classes fit a standard format
- [x] Rewrote entire codebase to better follow PEP 8 standards

## Module Goals
### Data Types
- [ ] Use pytest platform to find accuracy of connections

### Analysis

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
- [ ] Protect against bad data loading to states

### Testing
- [ ] Build interface to AppCore

- - -

## Paradigm Goals
### Object Oriented
- [ ] Abstractify and build interfaces as program becomes more complex
- [ ] Consider command objects

### Functional
- [ ] Continue to isolate "side effects"