# PyEDGE TODO List

### Analysis Goals by Priority
- [ ] Fix the neighbor analysis so it removes neighbors when analysis is rerun.
- [ ] Fix the intersection neighbor filter.

### GUI Goals by Priority
- [ ] (broken) Auto remember -- but not submit -- setting input when state is changed.
- [ ] Fix the open menu so it does not throw an error if canceled.
- [ ] Introduce multi-file image open support.
- [ ] Set values of the gui to be rescalable. Not important now, but will help small screen users.

### Github and Code Analysis Goals by Priority
- [ ] Have the most up to date code analysis replace the current one on the readme.
- [ ] Learn new metrics that might be interesting to analyize.

### Resently Completed Goals
- [x] Catch ValueErrors when strings are typed where floats belong in setting panels.
- [x] Document files, so they can more easily be traced to intent by users wishing to modify the code.
- [x] Lock setting input until image is loaded.
- [x] Re-connected neighbor analysis settings.
- [x] Auto clear image when blank state is set.
- [x] Implement a progress analysis tool.
- [x] Fixed the assignment of state to the options frame. Wasn't passed to parent. Used "sys.getrefcount()" to debug and "is" to verify.