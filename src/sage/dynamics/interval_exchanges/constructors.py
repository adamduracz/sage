r"""
Class factories for Interval exchange transformations.

This library is designed for the usage and manipulation of interval
exchange transformations and linear involutions. It defines specialized
types of permutation (constructed using :meth:`iet.Permutation`) some
associated graph (constructed using :meth:`iet.RauzyGraph`) and some maps
of intervals (constructed using :meth:`iet.IntervalExchangeTransformation`).


EXAMPLES:

Creation of an interval exchange transformation::

    sage: T = iet.IntervalExchangeTransformation(('a b','b a'),(sqrt(2),1))
    sage: print T
    Interval exchange transformation of [0, sqrt(2) + 1[ with permutation
    a b
    b a

It can also be initialized using permutation (group theoretic ones)::

    sage: p = Permutation([3,2,1])
    sage: T = iet.IntervalExchangeTransformation(p, [1/3,2/3,1])
    sage: print T
    Interval exchange transformation of [0, 2[ with permutation
    1 2 3
    3 2 1

For the manipulation of permutations of iet, there are special types provided
by this module. All of them can be constructed using the constructor
iet.Permutation. For the creation of labelled permutations of interval exchange
transformation::

    sage: p1 =  iet.Permutation('a b c', 'c b a')
    sage: print p1
    a b c
    c b a

They can be used for initialization of an iet::

    sage: p = iet.Permutation('a b','b a')
    sage: T = iet.IntervalExchangeTransformation(p, [1,sqrt(2)])
    sage: print T
    Interval exchange transformation of [0, sqrt(2) + 1[ with permutation
    a b
    b a

You can also, create labelled permutations of linear involutions::

    sage: p = iet.GeneralizedPermutation('a a b', 'b c c')
    sage: print p
    a a b
    b c c

Sometimes it's more easy to deal with reduced permutations::

    sage: p = iet.Permutation('a b c', 'c b a', reduced = True)
    sage: print p
    a b c
    c b a

Permutations with flips::

    sage: p1 = iet.Permutation('a b c', 'c b a', flips = ['a','c'])
    sage: print p1
    -a  b -c
    -c  b -a

Creation of Rauzy diagrams::

    sage: r = iet.RauzyDiagram('a b c', 'c b a')

Reduced Rauzy diagrams are constructed using the same arguments than for
permutations::

    sage: r = iet.RauzyDiagram('a b b','c c a')
    sage: r_red = iet.RauzyDiagram('a b b','c c a',reduced=True)
    sage: r.cardinality()
    12
    sage: r_red.cardinality()
    4

By default, Rauzy diagrams are generated by induction on the right. You can use
several options to enlarge (or restrict) the diagram (try help(iet.RauzyDiagram) for
more precisions)::

    sage: r1 = iet.RauzyDiagram('a b c','c b a',right_induction=True)
    sage: r2 = iet.RauzyDiagram('a b c','c b a',left_right_inversion=True)

You can consider self similar iet using path in Rauzy diagrams and eigenvectors
of the corresponding matrix::

    sage: p = iet.Permutation("a b c d", "d c b a")
    sage: d = p.rauzy_diagram()
    sage: g = d.path(p, 't', 't', 'b', 't', 'b', 'b', 't', 'b')
    sage: g
    Path of length 8 in a Rauzy diagram
    sage: g.is_loop()
    True
    sage: g.is_full()
    True
    sage: m = g.matrix()
    sage: v = m.eigenvectors_right()[-1][1][0]
    sage: T1 = iet.IntervalExchangeTransformation(p, v)
    sage: T2 = T1.rauzy_move(iterations=8)
    sage: T1.normalize(1) == T2.normalize(1)
    True

REFERENCES:

.. [BL08] Corentin Boissy and Erwan Lanneau, "Dynamics and geometry of the
  Rauzy-Veech induction for quadratic differentials" (arxiv:0710.5614) to appear
  in Ergodic Theory and Dynamical Systems

.. [DN90] Claude Danthony and Arnaldo Nogueira "Measured foliations on
  nonorientable surfaces", Annales scientifiques de l'Ecole Normale
  Superieure, Ser. 4, 23, no. 3 (1990) p 469-494

.. [N85] Arnaldo Nogueira, "Almost all Interval Exchange Transformations with
  Flips are Nonergodic" (Ergod. Th. & Dyn. Systems, Vol 5., (1985), 257-271

.. [R79] Gerard Rauzy, "Echanges d'intervalles et transformations induites",
  Acta Arith. 34, no. 3, 203-212, 1980

.. [V78] William Veech, "Interval exchange transformations", J. Analyse Math.
  33, 222-272

.. [Z] Anton Zorich, "Generalized Permutation software"
  (http://perso.univ-rennes1.fr/anton.zorich)


AUTHORS:

- Vincent Delecroix (2009-09-29): initial version

"""
#*****************************************************************************
#       Copyright (C) 2008 Vincent Delecroix <20100.delecroix@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from template import PermutationIET, PermutationLI

def _two_lists(a):
    r"""
    Try to return the input as a list of two lists

    INPUT:

    - ``a`` - either a string, one or two lists, one or two tuples

    OUTPUT:

    -- two lists

    TESTS::

        sage: from sage.dynamics.interval_exchanges.constructors import _two_lists
        sage: _two_lists(('a1 a2','b1 b2'))
        [['a1', 'a2'], ['b1', 'b2']]
        sage: _two_lists('a1 a2\nb1 b2')
        [['a1', 'a2'], ['b1', 'b2']]
        sage: _two_lists(['a b','c'])
        [['a', 'b'], ['c']]

    ..The ValueError and TypeError can be raised if it fails::

        sage: _two_lists('a b')
        Traceback (most recent call last):
        ...
        ValueError: your chain must contain two lines
        sage: _two_lists('a b\nc d\ne f')
        Traceback (most recent call last):
        ...
        ValueError: your chain must contain two lines
        sage: _two_lists(1)
        Traceback (most recent call last):
        ...
        TypeError: argument not accepted
        sage: _two_lists([1,2,3])
        Traceback (most recent call last):
        ...
        ValueError: your argument can not be split in two parts
    """
    from sage.combinat.permutation import Permutation

    res = [None, None]

    if isinstance(a,str):
        a = a.split('\n')
        if len(a) != 2:
            raise ValueError("your chain must contain two lines")
        else :
            res[0] = a[0].split()
            res[1] = a[1].split()

    elif isinstance(a, Permutation):
        res[0] = range(1,len(a)+1)
        res[1] = [a[i] for i in range(len(a))]

    elif not hasattr(a,'__len__'):
        raise TypeError("argument not accepted")

    elif len(a) == 0 or len(a) > 2:
        raise ValueError("your argument can not be split in two parts")

    elif len(a) == 1:
        a = a[0]
        if isinstance(a, Permutation):
            res[0] = range(1,len(a)+1)
            res[1] = [a[i] for i in range(len(a))]

        elif isinstance(a, (list,tuple)):
            if (len(a) != 2):
                raise ValueError("your list must contain two objects")
            for i in range(2):
                if isinstance(a[i], str):
                    res[i] = a[i].split()
                else:
                    res[i] = list(a[i])

        else :
            raise TypeError("argument not accepted")

    else :
        for i in range(2):
            if isinstance(a[i], str):
                res[i] = a[i].split()
            else:
                res[i] = list(a[i])

    return res

def Permutation(*args,**kargs):
    r"""
    Returns a permutation of an interval exchange transformation.

    Those permutations are the combinatoric part of an interval exchange
    transformation (IET). The combinatorial study of those objects starts with
    Gerard Rauzy [R79]_ and William Veech [V78]_.

    The combinatoric part of interval exchange transformation can be taken
    independently from its dynamical origin. It has an important link with
    strata of Abelian differential (see :mod:`~sage.dynamics.interval_exchanges.strata`)

    INPUT:

    - ``intervals`` - string, two strings, list, tuples that can be converted to
      two lists

    - ``reduced`` - boolean (default: False) specifies reduction. False means
      labelled permutation and True means reduced permutation.

    - ``flips`` -  iterable (default: None) the letters which correspond to
      flipped intervals.

    OUTPUT:

    permutation -- the output type depends of the data.

    EXAMPLES:

    Creation of labelled permutations ::

        sage: iet.Permutation('a b c d','d c b a')
        a b c d
        d c b a
        sage: iet.Permutation([[0,1,2,3],[2,1,3,0]])
        0 1 2 3
        2 1 3 0
        sage: iet.Permutation([0, 'A', 'B', 1], ['B', 0, 1, 'A'])
        0 A B 1
        B 0 1 A

    Creation of reduced permutations::

        sage: iet.Permutation('a b c', 'c b a', reduced = True)
        a b c
        c b a
        sage: iet.Permutation([0, 1, 2, 3], [1, 3, 0, 2])
        0 1 2 3
        1 3 0 2

    Creation of flipped permutations::

        sage: iet.Permutation('a b c', 'c b a', flips=['a','b'])
        -a -b  c
         c -b -a
        sage: iet.Permutation('a b c', 'c b a', flips=['a'], reduced=True)
        -a  b  c
         c  b -a

    TESTS:

    ::

        sage: p = iet.Permutation('a b c','c b a')
        sage: iet.Permutation(p) == p
        True
        sage: iet.Permutation(p, reduced=True) == p.reduced()
        True

    ::

        sage: p = iet.Permutation('a','a',flips='a',reduced=True)
        sage: iet.Permutation(p) == p
        True

    ::

        sage: p = iet.Permutation('a b c','c b a',flips='a')
        sage: iet.Permutation(p) == p
        True
        sage: iet.Permutation(p, reduced=True) == p.reduced()
        True

    ::

        sage: p = iet.Permutation('a b c','c b a',reduced=True)
        sage: iet.Permutation(p) == p
        True

        sage: iet.Permutation('a b c','c b a',reduced='badly')
        Traceback (most recent call last):
        ...
        TypeError: reduced must be of type boolean
        sage: iet.Permutation('a','a',flips='b',reduced=True)
        Traceback (most recent call last):
        ...
        ValueError: flips contains not valid letters
        sage: iet.Permutation('a b c','c a a',reduced=True)
        Traceback (most recent call last):
        ...
        ValueError: letters must appear once in each interval
    """
    from labelled import LabelledPermutation
    from labelled import LabelledPermutationIET
    from labelled import FlippedLabelledPermutationIET

    from reduced import ReducedPermutation
    from reduced import ReducedPermutationIET
    from reduced import FlippedReducedPermutationIET

    if 'reduced' not in kargs :
        reduction = None
    elif not isinstance(kargs["reduced"], bool) :
        raise TypeError("reduced must be of type boolean")
    else :
        reduction = kargs["reduced"]

    if 'flips' not in kargs :
        flips = []
    else :
        flips = list(kargs['flips'])


    if 'alphabet' not in kargs :
        alphabet = None
    else :
        alphabet = kargs['alphabet']

    if len(args) == 1:
        args = args[0]
        if isinstance(args, LabelledPermutation):
            if flips == []:
                if reduction is None or not reduction:
                    from copy import copy
                    return copy(args)
                else:
                    return args.reduced()
            else: # conversion not yet implemented
                reduced = reduction in (None, False)
                return PermutationIET(
                    args.list(),
                    reduced=reduced,
                    flips=flips,
                    alphabet=alphabet)

        if isinstance(args, ReducedPermutation):
            if flips == []:
                if reduction is None or reduction:
                    from copy import copy
                    return copy(args)
                else:  # conversion not yet implemented
                    return PermutationIET(
                        args.list(),
                        reduced=True)
            else: # conversion not yet implemented
                reduced = reduction in (None, True)
                return PermutationIET(
                    args.list(),
                    reduced=reduced,
                    flips=flips,
                    alphabet=alphabet)

    a = _two_lists(args)

    l = a[0] + a[1]
    letters = set(l)

    for letter in flips :
        if letter not in letters :
            raise ValueError("flips contains not valid letters")

    for letter in letters :
        if a[0].count(letter) != 1 or a[1].count(letter) != 1:
            raise ValueError("letters must appear once in each interval")

    if reduction :
        if flips == [] :
            return ReducedPermutationIET(a, alphabet=alphabet)
        else :
            return FlippedReducedPermutationIET(a, alphabet=alphabet, flips=flips)
    else :
        if flips == [] :
            return LabelledPermutationIET(a, alphabet=alphabet)
        else :
            return FlippedLabelledPermutationIET(a, alphabet=alphabet, flips=flips)

def GeneralizedPermutation(*args,**kargs):
    r"""
    Returns a permutation of an interval exchange transformation.

    Those permutations are the combinatoric part of linear involutions and were
    introduced by Danthony-Nogueira [DN90]_. The full combinatoric study and
    precise links with strata of quadratic differentials was achieved few years
    later by Boissy-Lanneau [BL08]_.

    INPUT:

    - ``intervals`` - strings, list, tuples

    - ``reduced`` - boolean (default: False) specifies reduction. False means
      labelled permutation and True means reduced permutation.

    - ``flips`` -  iterable (default: None) the letters which correspond to
      flipped intervals.

    OUTPUT:

    generalized permutation -- the output type depends on the data.

    EXAMPLES:

    Creation of labelled generalized permutations::

        sage: iet.GeneralizedPermutation('a b b','c c a')
        a b b
        c c a
        sage: iet.GeneralizedPermutation('a a','b b c c')
        a a
        b b c c
        sage: iet.GeneralizedPermutation([[0,1,2,3,1],[4,2,5,3,5,4,0]])
        0 1 2 3 1
        4 2 5 3 5 4 0

    Creation of reduced generalized permutations::

        sage: iet.GeneralizedPermutation('a b b', 'c c a', reduced = True)
        a b b
        c c a
        sage: iet.GeneralizedPermutation('a a b b', 'c c d d', reduced = True)
        a a b b
        c c d d

    Creation of flipped generalized permutations::

        sage: iet.GeneralizedPermutation('a b c a', 'd c d b', flips = ['a','b'])
        -a -b  c -a
         d  c  d -b

    TESTS::

        sage: iet.GeneralizedPermutation('a a b b', 'c c d d', reduced = 'may')
        Traceback (most recent call last):
        ...
        TypeError: reduced must be of type boolean
        sage: iet.GeneralizedPermutation('a b c a', 'd c d b', flips = ['e','b'])
        Traceback (most recent call last):
        ...
        TypeError: The flip list is not valid
        sage: iet.GeneralizedPermutation('a b c a', 'd c c b', flips = ['a','b'])
        Traceback (most recent call last):
        ...
        ValueError: Letters must reappear twice
    """
    from labelled import LabelledPermutation
    from labelled import LabelledPermutationLI
    from labelled import FlippedLabelledPermutationLI

    from reduced import ReducedPermutation
    from reduced import ReducedPermutationLI
    from reduced import FlippedReducedPermutationLI

    if 'reduced' not in kargs :
        reduction = None
    elif not isinstance(kargs["reduced"], bool) :
        raise TypeError("reduced must be of type boolean")
    else :
        reduction = kargs["reduced"]

    if 'flips' not in kargs :
        flips = []
    else :
        flips = list(kargs['flips'])


    if 'alphabet' not in kargs :
        alphabet = None
    else :
        alphabet = kargs['alphabet']

    if len(args) == 1:
        args = args[0]
        if isinstance(args, LabelledPermutation):
            if flips == []:
                if reduction is None or not reduction:
                    from copy import copy
                    return copy(args)
                else:
                    return args.reduced()
            else: # conversion not yet implemented
                reduced = reduction in (None, False)
                return PermutationLI(
                    args.list(),
                    reduced=reduced,
                    flips=flips,
                    alphabet=alphabet)

        if isinstance(args, ReducedPermutation):
            if flips == []:
                if reduction is None or reduction:
                    from copy import copy
                    return copy(args)
                else:  # conversion not yet implemented
                    return PermutationLI(
                        args.list(),
                        reduced=True)
            else: # conversion not yet implemented
                reduced = reduction in (None, True)
                return PermutationLI(
                    args.list(),
                    reduced=reduced,
                    flips=flips,
                    alphabet=alphabet)

    a = _two_lists(args)

    if 'reduced' not in kargs :
        reduction = False
    elif not isinstance(kargs["reduced"], bool) :
        raise TypeError("reduced must be of type boolean")
    else :
        reduction = kargs["reduced"]

    if 'flips' not in kargs :
        flips = []
    else :
        flips = list(kargs['flips'])

    if 'alphabet' not in kargs :
        alphabet = None
    else :
        alphabet = kargs['alphabet']

    l = a[0] + a[1]
    letters = set(l)

    for letter in flips :
        if letter not in letters :
            raise TypeError("The flip list is not valid")

    for letter in letters :
        if l.count(letter) != 2:
            raise ValueError("Letters must reappear twice")

    # check existence of admissible length
    b0 = a[0][:]
    b1 = a[1][:]
    for letter in letters :
        if b0.count(letter) == 1 :
            del b0[b0.index(letter)]
            del b1[b1.index(letter)]

    if (b0 == []) and (b1 == []):
        return Permutation(a,**kargs)

    elif (b0 == []) or (b1 == []):
        raise ValueError("There is no admissible length")

    if reduction :
        if flips == [] :
            return ReducedPermutationLI(a, alphabet=alphabet)
        else :
            return FlippedReducedPermutationLI(a, alphabet=alphabet, flips=flips)
    else :
        if flips == [] :
            return LabelledPermutationLI(a, alphabet=alphabet)
        else :
            return FlippedLabelledPermutationLI(a, alphabet=alphabet, flips=flips)

def Permutations_iterator(nintervals=None, irreducible=True,
                          reduced=False, alphabet=None):
    r"""
    Returns an iterator over permutations.

    This iterator allows you to iterate over permutations with given
    constraints. If you want to iterate over permutations coming from a given
    stratum you have to use the module :mod:`~sage.dynamics.flat_surfaces.strata` and
    generate Rauzy diagrams from connected components.

    INPUT:

    - ``nintervals`` - non negative integer

    - ``irreducible`` - boolean (default: True)

    - ``reduced`` - boolean (default: False)

    - ``alphabet`` - alphabet (default: None)

    OUTPUT:

    iterator -- an iterator over permutations

    EXAMPLES:

    Generates all reduced permutations with given number of intervals::

        sage: P = iet.Permutations_iterator(nintervals=2,alphabet="ab",reduced=True)
        sage: for p in P: print p, "\n* *"
        a b
        b a
        * *
        sage: P = iet.Permutations_iterator(nintervals=3,alphabet="abc",reduced=True)
        sage: for p in P: print p, "\n* * *"
        a b c
        b c a
        * * *
        a b c
        c a b
        * * *
        a b c
        c b a
        * * *

    TESTS::

        sage: P = iet.Permutations_iterator(nintervals=None, alphabet=None)
        Traceback (most recent call last):
        ...
        ValueError: You must specify an alphabet or a length
        sage: P = iet.Permutations_iterator(nintervals=None, alphabet=ZZ)
        Traceback (most recent call last):
        ...
        ValueError: You must specify a length with infinite alphabet
    """
    from labelled import LabelledPermutationsIET_iterator
    from reduced import ReducedPermutationsIET_iterator
    from sage.combinat.words.alphabet import Alphabet
    from sage.rings.infinity import Infinity

    if nintervals is None:
        if alphabet is None:
            raise ValueError("You must specify an alphabet or a length")
        else:
            alphabet = Alphabet(alphabet)
            if alphabet.cardinality() is Infinity:
                raise ValueError("You must specify a length with infinite alphabet")
            nintervals = alphabet.cardinality()

    elif alphabet is None:
            alphabet = range(1, nintervals+1)

    if reduced:
        return ReducedPermutationsIET_iterator(nintervals,
                                               irreducible=irreducible,
                                               alphabet=alphabet)
    else:
        return LabelledPermutationsIET_iterator(nintervals,
                                                irreducible=irreducible,
                                                alphabet=alphabet)

def RauzyDiagram(*args, **kargs):
    r"""
    Return an object coding a Rauzy diagram.

    The Rauzy diagram is an oriented graph with labelled edges. The set of
    vertices corresponds to the permutations obtained by different operations
    (mainly the .rauzy_move() operations that corresponds to an induction of
    interval exchange transformation). The edges correspond to the action of the
    different operations considered.

    It first appeard in the original article of Rauzy [R79]_.

    INPUT:

    - ``intervals`` - lists, or strings, or tuples

    - ``reduced`` - boolean (default: False) to precise reduction

    - ``flips`` - list (default: []) for flipped permutations

    - ``right_induction`` - boolean (default: True) consideration of left
      induction in the diagram

    - ``left_induction`` - boolean (default: False) consideration of right
      induction in the diagram

    - ``left_right_inversion`` - boolean (default: False) consideration of
      inversion

    - ``top_bottom_inversion`` - boolean (default: False) consideration of
      reversion

    - ``symmetric`` - boolean (default: False) consideration of the symmetric
      operation

    OUTPUT:

    Rauzy diagram -- the Rauzy diagram that corresponds to your request

    EXAMPLES:

    Standard Rauzy diagrams::

        sage: iet.RauzyDiagram('a b c d', 'd b c a')
        Rauzy diagram with 12 permutations
        sage: iet.RauzyDiagram('a b c d', 'd b c a', reduced = True)
        Rauzy diagram with 6 permutations

    Extended Rauzy diagrams::

        sage: iet.RauzyDiagram('a b c d', 'd b c a', symmetric=True)
        Rauzy diagram with 144 permutations

    Using Rauzy diagrams and path in Rauzy diagrams::

        sage: r = iet.RauzyDiagram('a b c', 'c b a')
        sage: print r
        Rauzy diagram with 3 permutations
        sage: p = iet.Permutation('a b c','c b a')
        sage: p in r
        True
        sage: g0 = r.path(p, 'top', 'bottom','top')
        sage: g1 = r.path(p, 'bottom', 'top', 'bottom')
        sage: print g0.is_loop(), g1.is_loop()
        True True
        sage: print g0.is_full(), g1.is_full()
        False False
        sage: g = g0 + g1
        sage: g
        Path of length 6 in a Rauzy diagram
        sage: print g.is_loop(), g.is_full()
        True True
        sage: m = g.matrix()
        sage: print m
        [1 1 1]
        [2 4 1]
        [2 3 2]
        sage: s = g.orbit_substitution()
        sage: s
        WordMorphism: a->acbbc, b->acbbcbbc, c->acbc
        sage: s.incidence_matrix() == m
        True

    We can then create the corresponding interval exchange transformation and
    comparing the orbit of `0` to the fixed point of the orbit substitution::

        sage: v = m.eigenvectors_right()[-1][1][0]
        sage: T = iet.IntervalExchangeTransformation(p, v).normalize()
        sage: print T
        Interval exchange transformation of [0, 1[ with permutation
        a b c
        c b a
        sage: w1 = []
        sage: x = 0
        sage: for i in range(20):
        ....:  w1.append(T.in_which_interval(x))
        ....:  x = T(x)
        sage: w1 = Word(w1)
        sage: w1
        word: acbbcacbcacbbcbbcacb
        sage: w2 = s.fixed_point('a')
        sage: w2[:20]
        word: acbbcacbcacbbcbbcacb
        sage: w2[:20] == w1
        True
    """
    if 'reduced' not in kargs:
        kargs['reduced'] = False
    if 'flips' not in kargs:
        kargs['flips'] = []
    if 'alphabet' not in kargs:
        kargs['alphabet'] = None

    p = GeneralizedPermutation(
        args,
        reduced= kargs['reduced'],
        flips = kargs['flips'],
        alphabet = kargs['alphabet'])

    if 'right_induction' not in kargs:
        kargs['right_induction'] = True
    if 'left_induction' not in kargs:
        kargs['left_induction'] = False
    if 'left_right_inversion' not in kargs:
        kargs['left_right_inversion'] = False
    if 'top_bottom_inversion' not in kargs:
        kargs['top_bottom_inversion'] = False
    if 'symmetric' not in kargs:
        kargs['symmetric'] = False

    return p.rauzy_diagram(
        right_induction = kargs['right_induction'],
        left_induction = kargs['left_induction'],
        left_right_inversion = kargs['left_right_inversion'],
        top_bottom_inversion = kargs['top_bottom_inversion'],
        symmetric = kargs['symmetric'])

#TODO
# def GeneralizedPermutation_iterator():
#     print "gpi"

def IntervalExchangeTransformation(permutation=None, lengths=None):
    """
    Constructs an Interval exchange transformation.

    An interval exchange transformation (or iet) is a map from an
    interval to itself. It is defined on the interval except at a finite
    number of points (the singularities) and is a translation on each
    connected component of the complement of the singularities. Moreover it is a
    bijection on its image (or it is injective).

    An interval exchange transformation is encoded by two datas. A permutation
    (that corresponds to the way we echange the intervals) and a vector of
    positive reals (that corresponds to the lengths of the complement of the
    singularities).

    INPUT:

    - ``permutation`` - a permutation

    - ``lengths`` - a list or a dictionary of lengths

    OUTPUT:

    interval exchange transformation -- an map of an interval

    EXAMPLES:

    Two initialization methods, the first using a iet.Permutation::

        sage: p = iet.Permutation('a b c','c b a')
        sage: t = iet.IntervalExchangeTransformation(p, {'a':1,'b':0.4523,'c':2.8})

    The second is more direct::

        sage: t = iet.IntervalExchangeTransformation(('a b','b a'),{'a':1,'b':4})

    It's also possible to initialize the lengths only with a list::

        sage: t = iet.IntervalExchangeTransformation(('a b c','c b a'),[0.123,0.4,2])

    The two fundamental operations are Rauzy move and normalization::

        sage: t = iet.IntervalExchangeTransformation(('a b c','c b a'),[0.123,0.4,2])
        sage: s = t.rauzy_move()
        sage: s_n = s.normalize(t.length())
        sage: s_n.length() == t.length()
        True

    A not too simple example of a self similar interval exchange transformation::

        sage: p = iet.Permutation('a b c d','d c b a')
        sage: d = p.rauzy_diagram()
        sage: g = d.path(p, 't', 't', 'b', 't', 'b', 'b', 't', 'b')
        sage: m = g.matrix()
        sage: v = m.eigenvectors_right()[-1][1][0]
        sage: t = iet.IntervalExchangeTransformation(p,v)
        sage: s = t.rauzy_move(iterations=8)
        sage: s.normalize() == t.normalize()
        True

    TESTS::

        sage: iet.IntervalExchangeTransformation(('a b c','c b a'),[0.123,2])
        Traceback (most recent call last):
        ...
        ValueError: bad number of lengths
        sage: iet.IntervalExchangeTransformation(('a b c','c b a'),[0.1,'rho',2])
        Traceback (most recent call last):
        ...
        TypeError: unable to convert 'rho' to a float
        sage: iet.IntervalExchangeTransformation(('a b c','c b a'),[0.1,-2,2])
        Traceback (most recent call last):
        ...
        ValueError: lengths must be positive
    """
    from iet import IntervalExchangeTransformation as _IET
    from labelled import LabelledPermutationIET
    from template import FlippedPermutation

    if isinstance(permutation, FlippedPermutation):
        raise TypeError("flips are not yet implemented")
    if isinstance(permutation, LabelledPermutationIET):
        p = permutation
    else:
        p = Permutation(permutation,reduced=False)


    if isinstance(lengths, dict):
        l = [0] * len(p)
        alphabet = p._alphabet
        for letter in lengths:
            l[alphabet.rank(letter)] = lengths[letter]
    else:
        l = list(lengths)

    if len(l) != len(p):
        raise ValueError("bad number of lengths")

    for x in l:
        try:
            y = float(x)
        except ValueError:
            raise TypeError("unable to convert {!r} to a float".format(x))

        if y <= 0:
            raise ValueError("lengths must be positive")

    return _IET(p, l)

IET = IntervalExchangeTransformation

#TODO
# def LinearInvolution(*args,**kargs):
#     r"""
#     Constructs a Linear Involution from the given data
#     """
#     from iet import LinearInvolution as _LI
#     pass

# LI = LinearInvolution
