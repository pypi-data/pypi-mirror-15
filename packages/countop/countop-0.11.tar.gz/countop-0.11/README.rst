countop
--------

Count the number of operations in your algorithm implementation.

    >>> from countop import Integer
    >>> print Integer.reset_counts()
    >>> print Integer.additions()
    # 0
    >>> a = Integer(1)
    >>> b = a + 1
    >>> print Integer.additions()
    # 1

