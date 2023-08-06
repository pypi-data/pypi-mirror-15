
diversipy has been tested with Python 2.7 and 3.4. The recommended version is
Python 3.x, because compatibility is reached by avoiding usage of xrange. So,
the code has a higher memory consumption under Python 2.

Everything in this package is pure Python. For a description of the contents
see DESCRIPTION.rst.


Changes
=======

0.5
---
* Made some sampling and subset selection functions more robust with regard to
  existing points (now also an empty 2-D array is recognized as being empty).

0.4
---
* Added function hausdorff_dist in module indicator.
* Removed __future__ imports.

0.3
---
* Bugfix in select_greedy_maxisum when supplying points as list instead of
  numpy array.
* Added function select_greedy_energy in module subset.
* Slightly refined choice of the first point in select_greedy_maximin and
  select_greedy_maxisum.

0.2
---
* psa_partition and psa_select now raise exceptions when num_clusters or
  num_selected_points are <= 0
* Added functions select_greedy_maximin and select_greedy_maxisum in module
  subset.

0.1.1
-----
* Fixed bug in installation script

0.1
---
* Initial version
