Subp: Python subprocess optimized for your happiness.
=====================================================

This is a convenience wrapper around the `subprocess` module.


Usage
-----

Run a command, get the response::

    >>> r = subp.run('git config', data='data to pipe in', timeout=2)

    >>> r.status_code
    129
    >>> r.std_out
    'usage: git config [options]'
    >>> r.std_err
    ''

Pipe stuff around too::

    >>> r = subp.run('uptime | pbcopy')

    >>> r.command
    'pbcopy'
    >>> r.status_code
    0

    >>> r.history
    [<Response 'uptime'>]


 Forked from: https://github.com/kennethreitz/envoy
