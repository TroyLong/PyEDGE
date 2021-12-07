# PyEDGE TODO List

### Analysis Goals by Priority
- [] Fix the neighbor analysis so it removes neighbors when analysis is rerun.
- [] Fix the intersection neighbor filter.

### GUI Goals by Priority
- [] Catch ValueErrors when strings are typed where floats belong in setting panels.
- [] Fix the open menu so it does not throw an error if canceled.
- [] Introduce multi-file image open support.
- [] Set values of the gui to be rescalable. Not important now, but will help small screen users.

### Resently Completed Goals
- [x] Documented import libraries, so they can more easily be traced to intent by users wishing to modify the code.
- [x] Provided an about section at the top of each program file, so programs can be identified by users wishing to modify the code.
- [x] Lock setting input until image is loaded.
- [x] Auto remember -- but not submit -- setting input when state is changed.
- [x] Re-connected neighbor analysis settings.
- [x] Auto clear image when blank state is set.