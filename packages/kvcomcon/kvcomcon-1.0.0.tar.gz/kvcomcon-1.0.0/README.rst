kvcomcon: key-value-comment config

Example:
::
    # My cool config
    foo = bar
    sentence = This is my cool sentence.

The config format is line-based. Each line must be one of these:

1. A comment line (the first non-whitespace character is '#'
2. An empty line (whitespace is allowed)
3. somekey = somevalue

Leading and trailing whitespace is stripped from each line, as well as
around each key and value. For example, these two lines are equivalent:
::
    "key=val 123"
    "  key  = val 123     "
