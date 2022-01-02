# PyEDGE TODO List

### Analysis Goals by Priority
- [ ] Currently neighborhood analysis has to be run a few times before removing noise in the data.
- [ ] Fix the intersection neighbor filter.

### GUI Goals by Cells only store one neighbor list. Priority
- [ ] Fix the open menu so it does not throw an error if canceled.
- [ ] Introduce multi-file image open support.
- [ ] Set values of the gui to be rescalable. Not important now, but will help small screen users.

### Github and Code Analysis Goals by Priority
- [ ] Just looked at the number of comments. Doesn't match even remotely. All past data is no bueno
- [ ] Have the most up to date code analysis replace the current one on the readme.
- [ ] Learn new metrics that might be interesting to analyize.

### Resently Completed Goals
- [x] Split code into multiple packages for source code clarity.
- [x] Found consistant way to import modules
- [x] Fixed the neighbor analysis so it removes neighbors when analysis is rerun. Histogram finally works.
- [x] Leveraged tuples throughout code, and introduced functional programming techniques.
