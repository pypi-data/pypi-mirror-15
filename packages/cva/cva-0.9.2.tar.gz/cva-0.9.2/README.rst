cva -- Calculus of Variations
=============================

The cva library (pronounced see-va) implements a solver for problems 
in the domain of the calculus of variations.  This includes such
problems as finding geodesics on arbitrary surfaces, finding minimal
paths in curved spacetime, or basically any path minimization problem 
that can be defined in terms of a surface or hypersurface model with an 
attached metric.

Quickstart
----
import cva
cva.examples.case01_torus()
----

Provides:
  1. Models
  2. Metrics
  3. Views
  4. Solver

Documentation:
  1. Docstrings are provided with the library functions
  2. A paper describing the mathematical foundations on which this
     library is based is nearing release.
  3. Runable examples are provided as starting points

Utilities:
  do_test
    run the cva test suite