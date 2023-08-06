pytranspose
=========

Transpose nested dict and list.

Usage
-----

.. code:: python

    from pytranspose import transpose

    # assume you have time serise data of temperature in variouse city.
    #
    # a[city][time] -> temperature
    #
    # now you want to compare temperature in different city at the same time point.
    # transpose function meets this requirement.
    #
    # b = transpose(a, [1, 0])
    # b[time][city] -> temperature

    # print(a["Tokyo"][2]) -> 28
    a = {"Tokyo": [27, 28, 29], "New York": [25, 24, 28]}

    # print(b[1]["New York"]) -> 24
    b = transpose(a)

License
-------

These codes are licensed under
`CC0 <https://creativecommons.org/publicdomain/zero/1.0/deed>`__.


