# PyEDGE
PyEDGE is a rewrite of the Embryo Development Geometry Explorer in Python. This package is currently in it's late alpha stages.

The TODO and notes.txt are the two most important documents at this time. I do not have access to software such as Jira, so these are the lifeblood of my productivity.

# Major Release Planning
These are the mile high goals for the next few versions of PyEDGE. No definite timeline is available and the goals are subject to change.

## Release 1
Main program functionality release.
- Loads and analyzes time and z level data using system states.
- Filters can isolate cells, and not produce false positive data.
- Outputs data with pandas.

## Release 2
Polish and improved accuracy release.
- Integrate with pytest for program integrity.
- Polish single image filters.
- Implement algorithms to improve multi-state analysis

## Release 3
Efficiency and framework stability release.
- Possible parallel cpu/gpu support
- Stable userspace and module support
- General improvements as need arises