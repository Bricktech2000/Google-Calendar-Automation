priority calculations
=====================

parameters:

* event start
* event end
* event now (current date)
* event progress
* event complexity?
* ...

```
duration total = (event end - event start)
duration completed = (event now - event start)
duration progress = duration completed / duration total

event progress = event completed / event total

//event complexity = ...
//() * event complexity

priority = atan2(1 - event progress, 1 - duration progress) * 2 / pi
```
