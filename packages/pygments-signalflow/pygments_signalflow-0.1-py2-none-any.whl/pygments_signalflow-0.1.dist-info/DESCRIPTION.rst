pygments-signalflow
===================

A Pygments_ syntax lexer for the SignalFx_ SignalFlow_ real-time streaming
analytics language.

.. _Pygments: http://pygments.org
.. _SignalFx: https://signalfx.com
.. _SignalFlow: https://developers.signalfx.com/docs/signalflow-overview

Installation
------------

.. code::

    $ pip install pygments-signalflow

Usage
-----

The ``pygments-signalflow`` package is setup to include the proper entrypoints
so that ``pygmentize`` can use the lexer out of the box:

.. code::

    $ cat example.flow
    data('cpu.utilization').mean().publish()
    $ pymentize example.flow  # This will show in fancy colors!
    data('cpu.utilization').mean().publish()

>From source
~~~~~~~~~~~

To use the lexer from source (for example with the excellent `Prompt Toolkit`_):

.. _Prompt Toolkit: https://github.com/jonathanslenders/python-prompt-toolkit

.. code:: python

    import prompt_toolkit
    import pygments
    import pygments_signalflow

    ...

    prompt_toolkit.shortcuts.prompt('> ',
        lexer=prompt_toolkit.layout.lexers.PygmensLexer(
            pygments_signalflow.SignalFlowLexer()))


