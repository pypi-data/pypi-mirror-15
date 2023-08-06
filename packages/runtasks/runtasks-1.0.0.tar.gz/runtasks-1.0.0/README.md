
# runtasks

A simple task runner for Python that is useful for build scripts.

The primary purposes are to provide (1) a single utility for running utility functions /
scripts, (2) a convenient command line parser for them, that (3) works with Python 3.

The "run" utility searches for a file named "tasks.py".  Any Python functions decorated with
`@task` are callable by passing their name, and optionally any arguments, to run:

    $ run hello who=Bob

The tasks.py file might look like this:

    from runtasks import task

    @task
    def hello(who='World'):
        "Prints a friendly greeting"
        print('Hello, {}!'.format(who))

Use the `--list` option to print the list of tasks, their options, and documentation strings:

    $ run --list

    Available tasks:

    hello
      who='World'
      Prints a friendly greeting

## Command Line Parsing

One of the most important features is making your command line input as simple as possible, so
the parser is as flexible as possible.

First, multiple tasks can be passed on the command line and they are executed in the order
specified:

    $ run createdb testdb smoketests

Arguments can be passed to tasks in a number of formats:

 * Name and Value:
   * `run hello --who=Bob`
   * `run hello --who Bob`
   * `run hello who=Bob`
 * Value:
   * `run hello Bob`
 * Flags:
   * `run hello --debug`
   * `run hello --no-debug`

### Value Parameters

A parameter that has no default value or has a default value that is not `True` or `False` can
accept a value on the command line.  If no default value is provided, a value must be provided
when running the task.

    @task
    def sometask(arg1, arg2='defvalue'):
        print('arg1={} arg2={}'.format(arg1, arg2))

Values can be provided in a few ways:

    $ run sometask --arg1=value1 --arg2=value2
    arg1=value1 arg2=value2

    $ run sometask --arg2=value2 --arg1=value1
    arg1=value1 arg2=value2

    $ run sometask --arg1 value1
    arg1=value1 arg2=defvalue

    $ run sometask arg1=value1
    arg1=value1 arg2=defvalue

    $ run sometask value1
    arg1=value1 arg2=defvalue

    $ run sometask value1 value2
    arg1=value1 arg2=value2

    $ runtask sometask
    Task sometask argument arg1 was not provided a value

Notice that arguments can be provided in any order when providing the name of the argument.  To
provide values without names (e.g. `runtask sometask value1 value2`), the arguments must be in
order.  These are only accepted before arguments with names, so the following is not valid:

    # NOT VALID
    $ run sometask --arg1=value1 value2

Since arg1 was provided with a name, "value2" will be assumed to be the next task name to run.

### Flag Parameters

When a default parameter is set to `True` or `False`, the argument does not accept a value on
the command line.  Instead, the argument name itself is accepted to mean the flag should be set
to `True` and the argument name preceded by "no-" is accepted to mean the flag should be set to
`False`.

    @task
    def sometask(flag1=False, flag2=True):
        print(flag1, flag2)

    $ run sometask
    False True

    $ run sometask --flag1
    True True

    $ run sometask --no-flag2
    False False

    $ run sometask --no-flag1
    False true

Note that flag parameters require dashes.  The following does not work because it will try to
pass the value "flag1" to the first parameter, but values are not accepted for flags:

    $ run sometask flag1
    Task sometask argument flag1 does not accept a value


### Short Flags

Arguments can also be provided using a single dash and the first letter of the parameter, as
long as the first letter is unique.

    @task
    def sometask(arg1=None, flag=False):
        print('arg1={} flag={}'.format(arg1, flag))

    $ run sometask -a value1
    arg1=value1 flag=False

    $ run sometask -a=value1
    arg1=value1 flag=False

    $ run sometask -f
    arg1=None flag=True

    $ run sometask -fa=value1
    arg1=value1 flag=True

    $ run sometask -fa value1
    arg1=value1 flag=True

You can override the flags assigned to a parameter using the task decorator, which is
particularly handy when the first letters are not unique.

    @task(flags={'x': 'flag'})
    def sometask(flag=False, forward=False):
        print('flag={} forward={}'.format(flag, forward))

    $ run sometask
    flag=False forward=False

    $ run sometask -x
    flag=True forward=False

    $ run sometask -f
    flag=False forward=True

    $ run sometask -fx
    flag=True forward=True

Notice that "f" is assigned to the "forward" parameter since it is the only remaining parameter
that starts with "f" now that "flag" is assigned to "x".


## Potential Future Features

Dependent tasks:

    @task(dep=othertask)
    def sometask():
        ...

A default task that is run when no task names are provided on the command line.

An @init decorator for functions to be called after parsing but before tasks are run.  Any code
defined in the script is run before command line parsing, so initial setup is performed as in
any Python script.  However, if you want conditional setup only if certain tasks are going to
be run you'd need the output of parsing.

## Rationale

The distutils package is great for packaging, but in the past I'd also used it for defining a
myriad of per-project utility scripts (setup a test database, etc.).  I'd used distutils
because it was built-in, but, honestly, it's design is terrible, the command line parsing
always requires some option name with dashes, and it does bizarre things without telling you.
For example, if you define a user option named "user", it will be silently ignored when
running in a virtual environment!  This was the last straw.

All I really wanted was a single script I could invoke with command line parsing that "does
what I want".  I looked at many other packages but the only one close to this simplicity was
Invoke.  Unfortunately the configuration for Invoke was way to complicated for
me to figure out, particularly how to update the configuration in one task for later tasks to
use.
