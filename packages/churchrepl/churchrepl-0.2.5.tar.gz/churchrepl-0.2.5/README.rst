CHURCH-REPL
===========

A simple REPL for lambda calculus

.. image:: https://travis-ci.org/CodeGrimoire/ChurchREPL.svg?branch=master
    :target: https://travis-ci.org/CodeGrimoire/ChurchREPL

Use:
----
when calling churchrepl and new REPL will be opened.

.. code-block::

    churchrepl [-f --file file [file ...]] [-v --verbose]

Flags:

(optional) Read definitions and expressions from a file before loading the normal REPL.

.. code-block::
    
    -f|--file file [file ...]


(optional) print debugging and verbose output.

.. code-block::
    
    -v|--verbose


Church repl file structure:
---------------------------

The EBNF grammar is as follows*:

::

    (* Lambda Program *)
    program     = {line};
    line        = (define | function);
    define      = "@" alias ":" function;
    function    = lambda | application;
    lambda      = ("λ" | "\") variable "." expr;
    application = '(' expr  expr ')';
    expr        = (lambda | application | variable | alias ) ;
    variable    = /[a-z]/;
    alias       = /[_A-Z][_A-Z0-9]*/;

A simple example program:

::

    @ID: λx.x
    @APPLY: λf.λx.(f x)
    @TRUE: λx.λy.x
    @FALSE: λx.λy.y
    @ZERO: λf.λx.x
    @SUCC: λn.λf.λx.(f ((n f) x))
    @ONE: (SUCC ZERO)
    @TWO: (SUCC ONE)
    @THREE: (SUCC TWO)
    @FOUR: (SUCC THREE)
    (SUCC ZERO)
    (SUCC ONE)
    (SUCC TWO)
    (SUCC THREE)
    (SUCC FOUR)

Note: The λ (lambda, unicode u03bb) is equivalent to a backslash as far as this program is concerned.
When using the repl it may be easier to use a backslash.
