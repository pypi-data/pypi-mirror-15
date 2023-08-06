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

   (* church-lambda EBNF *)
                     (* --- meta --- *)
                (* line or line, line, line... *)
    program = {line};

                (* define or function *)
    line = (define | function);

                (* ex: @ID: λx.x *)
    define = "@" alias ":" function;

                     (* --- lambdas --- *)
                (* lambda or an application *)
    function = lambda | application;

                (* ex: λx.x)
    lambda = "λ" variable "." expr;

                (* ex: '(λx.x λy.y)
    application = '(' expr  expr ')';

                (* lambda or application or variable or alias *)
    expr = (lambda | application | variable | alias );

                     (* --- primitives --- *)
                (* one lowercase letter *)
    variable = /[a-z]/;

                (* one underscore or capital followed by zero
                or more [underscores, captials, or digits] *)
    alias = /[_A-Z][_A-Z0-9]*/;

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
