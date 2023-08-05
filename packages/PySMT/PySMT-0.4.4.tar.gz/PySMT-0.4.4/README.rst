===========================
pySMT: a Python API for SMT
===========================

.. image:: https://travis-ci.org/pysmt/pysmt.svg?branch=master
           :target: https://travis-ci.org/pysmt/pysmt
           :alt: Build Status

.. image:: https://readthedocs.org/projects/pysmt/badge/?version=latest
           :target: https://readthedocs.org/projects/pysmt/?badge=latest
           :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/pysmt.svg
           :target: https://pypi.python.org/pypi/pySMT/
           :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/pysmt.svg
           :target: https://pypi.python.org/pypi/pySMT/
           :alt: Monthly Downloads

.. image:: https://img.shields.io/pypi/l/pysmt.svg
           :target: /LICENSE
           :alt: Apache License


pySMT makes working with **Satisfiability Modulo Theory** simple:

* Define formulae in a *simple*, *intuitive*, and *solver independent* way
* Solve your formulae using one of the native solvers, or by wrapping
  any SMT-Lib complaint solver,
* Dump your problems in the SMT-Lib format,
* and more...

.. image:: https://cdn.rawgit.com/pysmt/pysmt/master/docs/architecture.svg
           :alt: PySMT Architecture Overview

Usage
=====

.. code:: python

   >>> from pysmt.shortcuts import Symbol, And, Not, is_sat
   >>>
   >>> varA = Symbol("A") # Default type is Boolean
   >>> varB = Symbol("B")
   >>> f = And(varA, Not(varB))
   >>> f
   (A & (! B))
   >>> is_sat(f)
   True
   >>> g = f.substitute({varB: varA})
   >>> g
   (A & (! A))
   >>> is_sat(g)
   False


A More Complex Example
----------------------

Is there a value for each letter (between 1 and 9) so that H+E+L+L+O = W+O+R+L+D = 25?

.. code:: python

  from pysmt.shortcuts import Symbol, And, GE, LT, Plus, Equals, Int, get_model
  from pysmt.typing import INT

  hello = [Symbol(s, INT) for s in "hello"]
  world = [Symbol(s, INT) for s in "world"]
  letters = set(hello+world)
  domains = And([And(GE(l, Int(1)),
                     LT(l, Int(10))) for l in letters])

  sum_hello = Plus(hello) # n-ary operators can take lists
  sum_world = Plus(world) # as arguments
  problem = And(Equals(sum_hello, sum_world),
                Equals(sum_hello, Int(25)))
  formula = And(domains, problem)

  print("Serialization of the formula:")
  print(formula)

  model = get_model(formula)
  if model:
    print(model)
  else:
    print("No solution found")

Check out more examples in the `examples/ directory
</examples>`_.

Supported Theories and Solvers
==============================

pySMT provides methods to define a formula in Linear Real Arithmetic
(LRA), Real Difference Logic (RDL), Equalities and Uninterpreted
Functions (EUF), Bit-Vectors (BV), and their combinations. The
following solvers are supported through native APIs:

* MathSAT (http://mathsat.fbk.eu/)
* Z3 (https://github.com/Z3Prover/z3/)
* CVC4 (http://cvc4.cs.nyu.edu/web/)
* Yices 2 (http://yices.csl.sri.com/)
* CUDD (http://vlsi.colorado.edu/~fabio/CUDD/)
* PicoSAT (http://fmv.jku.at/picosat/)
* Boolector (http://fmv.jku.at/boolector/)

Additionally, you can use any SMT-LIB 2 compliant solver.

PySMT assumes that the python bindings for the SMT Solver are
installed and accessible from your ```PYTHONPATH```. For Yices 2 we
rely on pyices (https://github.com/cheshire/pyices). For CUDD we use
repycudd (https://github.com/pysmt/repycudd).

pySMT works on both Python 2 and Python 3. Some solvers support both
versions (e.g., MathSAT) but in general, many solvers still support
only Python 2.


Installation
============
You can install the latest stable release of pySMT from PyPI:

  # pip install pysmt

this will additionally install the *pysmt-install* command, that can
be used to install the solvers: e.g.,

  $ pysmt-install --check

will show you which solvers have been found in your ```PYTHONPATH```.
PySMT does not depend directly on any solver, but if you want to
perform solving, you need to have at least one solver installed. This
can be used by PySMT via its native API, or passing through an SMT-LIB
file.

The script *pysmt-install* can be used to simplify the installation of the solvers:

 $ pysmt-install --msat

will install MathSAT 5. This script does not install required
dependencies for building the solver (e.g., make or gcc) and has been
tested mainly on Linux Debian/Ubuntu systems. We suggest that you
refer to the documentation of each solver to understand how to install
it with its python bindings. Nevertheless, we try to keep
*pysmt/cmd/install.py* as readable and documented as possible.

For CVC4 we have a patch that needs to be applied. The patches are
available in the repository 'pysmt/solvers_patches' and should be
applied against the following versions of the solvers:

- CVC4: Git revision 68f22235a62f5276b206e9a6692a85001beb8d42

For picosat and cudd, we use custom wrappers:

- repycudd (https://github.com/pysmt/repycudd)
- pyPicoSAT (https://github.com/pysmt/pyPicoSAT)

For instruction on how to use any SMT-LIB complaint solver with pySMT
see `examples/generic_smtlib.py </examples/generic_smtlib.py>`_

The following table summarizes the features supported via pySMT for
each of the available solvers. (We indicate with square brackets the
features that are supported by the solver itself by not by the current
wrapper used within pySMT).

  =================   ==========   ==================   ==============   ==================   ==========
  Solver              pySMT name   Supported Logics     Satisfiability   Model Construction   UNSAT-Core
  =================   ==========   ==================   ==============   ==================   ==========
  MathSAT             msat         QF_UFLIRA, QF_BV     Yes              Yes                  Yes
  Z3                  z3           UFLIRA, QF_BV        Yes              Yes                  Yes
  CVC4                cvc4         QF_UFLIRA, QF_BV     Yes              Yes                  No
  Yices               yices        QF_UFLIRA, QF_BV     Yes              Yes                  No
  SMT-Lib Interface   <custom>     UFLIRA, [QF_BV]      Yes              Yes                  No [Yes]
  PicoSAT             picosat      QF_BOOL              Yes              Yes                  No [Yes]
  Boolector           btor         QF_UFBV              Yes              Yes                  No
  BDD (CUDD)          bdd          BOOL                 Yes              Yes                  No
  =================   ==========   ==================   ==============   ==================   ==========

The following table summarizes the features supported via pySMT for
each of the available quantifier eliminators

  =====================   ==========   ================
  Quantifier Eliminator   pySMT name   Supported Logics
  =====================   ==========   ================
  MathSAT FM              msat-fm      LRA
  MathSAT LW              msat-lw      LRA
  Z3                      z3           LRA, LIA
  BDD (CUDD)              bdd          BOOL
  =====================   ==========   ================

The following table summarizes the features supported via pySMT for
each of the available Craig interpolators

  ============   ==========   =========================
  Interpolator   pySMT name   Supported Logics
  ============   ==========   =========================
  MathSAT        msat         QF_UFLIA, QF_UFLRA, QF_BV
  Z3             z3           QF_UFLIA, QF_UFLRA
  ============   ==========   =========================

License
=======

pySMT is release under the APACHE 2.0 License.

For further questions, feel free to open an issue, or write to
info@pysmt.org
