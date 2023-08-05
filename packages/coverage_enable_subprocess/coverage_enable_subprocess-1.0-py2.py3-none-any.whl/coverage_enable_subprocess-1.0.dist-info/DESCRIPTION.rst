This package installs a pth file that enables the coveragepy process_startup
feature in this python prefix/virtualenv in subsequent runs.

See: http://nedbatchelder.com/code/coverage/subprocess.html


Demo::

    $ virtualenv tmpenv
    $ . tmpenv/bin/activate
    $ pip install coverage-enable-subprocess
    $ touch .coveragerc
    $ export COVERAGE_PROCESS_START=$PWD/.coveragerc
    $ echo 'print("oh, hi!")' > ohhi.py
    $ python ohhi.py
    oh, hi!

    $ coverage report
    Name                              Stmts   Miss  Cover
    -----------------------------------------------------
    /etc/python2.6/sitecustomize.py       5      1    80%
    ohhi.py                               1      0   100%
    tmpenv/lib/python2.6/site.py        433    392     9%
    -----------------------------------------------------
    TOTAL                               439    393    10%


For projects that need to cd during their test runs, and run many processes in parallel,
I ensure a ``$TOP`` variable is exported, and I use this .coveragerc::

    [run]
    parallel = True
    branch = True
    data_file = $TOP/.coverage

    [report]
    exclude_lines =
        # Have to re-enable the standard pragma
        \#.*pragma:\s*no.?cover

        # we can't get coverage for functions that don't return:
        \#.*never returns
        \#.*doesn't return

        # Don't complain if tests don't hit defensive assertion code:
        ^\s*raise Impossible\b
        ^\s*raise AssertionError\b
        ^\s*raise NotImplementedError\b
        ^\s*return NotImplemented\b

        # Don't complain if tests don't hit re-raise of unexpected errors:
        ^\s*raise$

        # if main is covered, we're good:
        ^\s*exit\(main\(\)\)$
    show_missing = True

    [html]
    directory = $TOP/coverage-html

    # vim:ft=dosini


