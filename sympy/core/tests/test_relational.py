from sympy.utilities.pytest import XFAIL, raises
from sympy import (S, Symbol, symbols, oo, I, pi, Float, And, Or, Not, Implies,
    Xor)
from sympy.core.relational import ( Relational, Equality, Unequality,
    GreaterThan, LessThan, StrictGreaterThan, StrictLessThan, Rel, Eq, Lt, Le,
    Gt, Ge, Ne, EqualityNonEval, Eqn )
from sympy.sets.sets import Interval, FiniteSet

x, y, z, t = symbols('x,y,z,t')


def test_rel_ne():
    assert Relational(x, y, '!=') == Ne(x, y)


def test_rel_subs():
    e = Relational(x, y, '==')
    e = e.subs(x, z)

    assert isinstance(e, Equality)
    assert e.lhs == z
    assert e.rhs == y

    e = Relational(x, y, '>=')
    e = e.subs(x, z)

    assert isinstance(e, GreaterThan)
    assert e.lhs == z
    assert e.rhs == y

    e = Relational(x, y, '<=')
    e = e.subs(x, z)

    assert isinstance(e, LessThan)
    assert e.lhs == z
    assert e.rhs == y

    e = Relational(x, y, '>')
    e = e.subs(x, z)

    assert isinstance(e, StrictGreaterThan)
    assert e.lhs == z
    assert e.rhs == y

    e = Relational(x, y, '<')
    e = e.subs(x, z)

    assert isinstance(e, StrictLessThan)
    assert e.lhs == z
    assert e.rhs == y

    e = Eq(x, 0)
    assert e.subs(x, 0) is S.true
    assert e.subs(x, 1) is S.false


def test_wrappers():
    e = x + x**2

    res = Relational(y, e, '==')
    assert Rel(y, x + x**2, '==') == res
    assert Eq(y, x + x**2) == res

    res = Relational(y, e, '<')
    assert Lt(y, x + x**2) == res

    res = Relational(y, e, '<=')
    assert Le(y, x + x**2) == res

    res = Relational(y, e, '>')
    assert Gt(y, x + x**2) == res

    res = Relational(y, e, '>=')
    assert Ge(y, x + x**2) == res

    res = Relational(y, e, '!=')
    assert Ne(y, x + x**2) == res


def test_Eq():

    assert Eq(x**2) == Eq(x**2, 0)
    assert Eq(x**2) != Eq(x**2, 1)


def test_rel_Infinity():
    # NOTE: All of these are actually handled by sympy.core.Number, and do
    # not create Relational objects.
    assert (oo > oo) is S.false
    assert (oo > -oo) is S.true
    assert (oo > 1) is S.true
    assert (oo < oo) is S.false
    assert (oo < -oo) is S.false
    assert (oo < 1) is S.false
    assert (oo >= oo) is S.true
    assert (oo >= -oo) is S.true
    assert (oo >= 1) is S.true
    assert (oo <= oo) is S.true
    assert (oo <= -oo) is S.false
    assert (oo <= 1) is S.false
    assert (-oo > oo) is S.false
    assert (-oo > -oo) is S.false
    assert (-oo > 1) is S.false
    assert (-oo < oo) is S.true
    assert (-oo < -oo) is S.false
    assert (-oo < 1) is S.true
    assert (-oo >= oo) is S.false
    assert (-oo >= -oo) is S.true
    assert (-oo >= 1) is S.false
    assert (-oo <= oo) is S.true
    assert (-oo <= -oo) is S.true
    assert (-oo <= 1) is S.true


def test_bool():
    assert Eq(0, 0) is S.true
    assert Eq(1, 0) is S.false
    assert Ne(0, 0) is S.false
    assert Ne(1, 0) is S.true
    assert Lt(0, 1) is S.true
    assert Lt(1, 0) is S.false
    assert Le(0, 1) is S.true
    assert Le(1, 0) is S.false
    assert Le(0, 0) is S.true
    assert Gt(1, 0) is S.true
    assert Gt(0, 1) is S.false
    assert Ge(1, 0) is S.true
    assert Ge(0, 1) is S.false
    assert Ge(1, 1) is S.true
    assert Eq(I, 2) is S.false
    assert Ne(I, 2) is S.true
    assert Gt(I, 2) not in [S.true, S.false]
    assert Ge(I, 2) not in [S.true, S.false]
    assert Lt(I, 2) not in [S.true, S.false]
    assert Le(I, 2) not in [S.true, S.false]
    a = Float('.000000000000000000001', '')
    b = Float('.0000000000000000000001', '')
    assert Eq(pi + a, pi + b) is S.false


def test_rich_cmp():
    assert (x < y) == Lt(x, y)
    assert (x <= y) == Le(x, y)
    assert (x > y) == Gt(x, y)
    assert (x >= y) == Ge(x, y)


def test_doit():
    from sympy import Symbol
    p = Symbol('p', positive=True)
    n = Symbol('n', negative=True)
    np = Symbol('np', nonpositive=True)
    nn = Symbol('nn', nonnegative=True)

    assert Gt(p, 0).doit() is S.true
    assert Gt(p, 1).doit() == Gt(p, 1)
    assert Ge(p, 0).doit() is S.true
    assert Le(p, 0).doit() is S.false
    assert Lt(n, 0).doit() is S.true
    assert Le(np, 0).doit() is S.true
    assert Gt(nn, 0).doit() == Gt(nn, 0)
    assert Lt(nn, 0).doit() is S.false

    assert Eq(x, 0).doit() == Eq(x, 0)


def test_new_relational():
    x = Symbol('x')

    assert Eq(x) == Relational(x, 0)       # None ==> Equality
    assert Eq(x) == Relational(x, 0, '==')
    assert Eq(x) == Relational(x, 0, 'eq')
    assert Eq(x) == Equality(x, 0)
    assert Eq(x, -1) == Relational(x, -1)       # None ==> Equality
    assert Eq(x, -1) == Relational(x, -1, '==')
    assert Eq(x, -1) == Relational(x, -1, 'eq')
    assert Eq(x, -1) == Equality(x, -1)
    assert Eq(x) != Relational(x, 1)       # None ==> Equality
    assert Eq(x) != Relational(x, 1, '==')
    assert Eq(x) != Relational(x, 1, 'eq')
    assert Eq(x) != Equality(x, 1)
    assert Eq(x, -1) != Relational(x, 1)       # None ==> Equality
    assert Eq(x, -1) != Relational(x, 1, '==')
    assert Eq(x, -1) != Relational(x, 1, 'eq')
    assert Eq(x, -1) != Equality(x, 1)

    assert Ne(x, 0) == Relational(x, 0, '!=')
    assert Ne(x, 0) == Relational(x, 0, '<>')
    assert Ne(x, 0) == Relational(x, 0, 'ne')
    assert Ne(x, 0) == Unequality(x, 0)
    assert Ne(x, 0) != Relational(x, 1, '!=')
    assert Ne(x, 0) != Relational(x, 1, '<>')
    assert Ne(x, 0) != Relational(x, 1, 'ne')
    assert Ne(x, 0) != Unequality(x, 1)

    assert Ge(x, 0) == Relational(x, 0, '>=')
    assert Ge(x, 0) == Relational(x, 0, 'ge')
    assert Ge(x, 0) == GreaterThan(x, 0)
    assert Ge(x, 1) != Relational(x, 0, '>=')
    assert Ge(x, 1) != Relational(x, 0, 'ge')
    assert Ge(x, 1) != GreaterThan(x, 0)
    assert (x >= 1) == Relational(x, 1, '>=')
    assert (x >= 1) == Relational(x, 1, 'ge')
    assert (x >= 1) == GreaterThan(x, 1)
    assert (x >= 0) != Relational(x, 1, '>=')
    assert (x >= 0) != Relational(x, 1, 'ge')
    assert (x >= 0) != GreaterThan(x, 1)

    assert Le(x, 0) == Relational(x, 0, '<=')
    assert Le(x, 0) == Relational(x, 0, 'le')
    assert Le(x, 0) == LessThan(x, 0)
    assert Le(x, 1) != Relational(x, 0, '<=')
    assert Le(x, 1) != Relational(x, 0, 'le')
    assert Le(x, 1) != LessThan(x, 0)
    assert (x <= 1) == Relational(x, 1, '<=')
    assert (x <= 1) == Relational(x, 1, 'le')
    assert (x <= 1) == LessThan(x, 1)
    assert (x <= 0) != Relational(x, 1, '<=')
    assert (x <= 0) != Relational(x, 1, 'le')
    assert (x <= 0) != LessThan(x, 1)

    assert Gt(x, 0) == Relational(x, 0, '>')
    assert Gt(x, 0) == Relational(x, 0, 'gt')
    assert Gt(x, 0) == StrictGreaterThan(x, 0)
    assert Gt(x, 1) != Relational(x, 0, '>')
    assert Gt(x, 1) != Relational(x, 0, 'gt')
    assert Gt(x, 1) != StrictGreaterThan(x, 0)
    assert (x > 1) == Relational(x, 1, '>')
    assert (x > 1) == Relational(x, 1, 'gt')
    assert (x > 1) == StrictGreaterThan(x, 1)
    assert (x > 0) != Relational(x, 1, '>')
    assert (x > 0) != Relational(x, 1, 'gt')
    assert (x > 0) != StrictGreaterThan(x, 1)

    assert Lt(x, 0) == Relational(x, 0, '<')
    assert Lt(x, 0) == Relational(x, 0, 'lt')
    assert Lt(x, 0) == StrictLessThan(x, 0)
    assert Lt(x, 1) != Relational(x, 0, '<')
    assert Lt(x, 1) != Relational(x, 0, 'lt')
    assert Lt(x, 1) != StrictLessThan(x, 0)
    assert (x < 1) == Relational(x, 1, '<')
    assert (x < 1) == Relational(x, 1, 'lt')
    assert (x < 1) == StrictLessThan(x, 1)
    assert (x < 0) != Relational(x, 1, '<')
    assert (x < 0) != Relational(x, 1, 'lt')
    assert (x < 0) != StrictLessThan(x, 1)

    # finally, some fuzz testing
    from random import randint
    from sympy.core.compatibility import unichr
    for i in range(100):
        while 1:
            strtype, length = (unichr, 65535) if randint(0, 1) else (chr, 255)
            relation_type = strtype( randint(0, length) )
            if randint(0, 1):
                relation_type += strtype( randint(0, length) )
            if relation_type not in ('==', 'eq', '!=', '<>', 'ne', '>=', 'ge',
                                     '<=', 'le', '>', 'gt', '<', 'lt'):
                break

        raises(ValueError, lambda: Relational(x, 1, relation_type))


def test_relational_bool_output():
    # https://github.com/sympy/sympy/issues/5931
    raises(TypeError, lambda: bool(x > 3))
    raises(TypeError, lambda: bool(x >= 3))
    raises(TypeError, lambda: bool(x < 3))
    raises(TypeError, lambda: bool(x <= 3))
    raises(TypeError, lambda: bool(Eq(x, 3)))
    raises(TypeError, lambda: bool(Ne(x, 3)))


def test_relational_logic_symbols():
    # See issue 6204
    assert (x < y) & (z < t) == And(x < y, z < t)
    assert (x < y) | (z < t) == Or(x < y, z < t)
    assert ~(x < y) == Not(x < y)
    assert (x < y) >> (z < t) == Implies(x < y, z < t)
    assert (x < y) << (z < t) == Implies(z < t, x < y)
    assert (x < y) ^ (z < t) == Xor(x < y, z < t)

    assert isinstance((x < y) & (z < t), And)
    assert isinstance((x < y) | (z < t), Or)
    assert isinstance(~(x < y), GreaterThan)
    assert isinstance((x < y) >> (z < t), Implies)
    assert isinstance((x < y) << (z < t), Implies)
    assert isinstance((x < y) ^ (z < t), (Or, Xor))


def test_univariate_relational_as_set():
    assert (x > 0).as_set() == Interval(0, oo, True, True)
    assert (x >= 0).as_set() == Interval(0, oo)
    assert (x < 0).as_set() == Interval(-oo, 0, True, True)
    assert (x <= 0).as_set() == Interval(-oo, 0)
    assert Eq(x, 0).as_set() == FiniteSet(0)
    assert Ne(x, 0).as_set() == Interval(-oo, 0, True, True) + \
        Interval(0, oo, True, True)

    assert (x**2 >= 4).as_set() == Interval(-oo, -2) + Interval(2, oo)


@XFAIL
def test_multivariate_relational_as_set():
    assert (x*y >= 0).as_set() == Interval(0, oo)*Interval(0, oo) + \
        Interval(-oo, 0)*Interval(-oo, 0)


def test_Not():
    assert Not(Equality(x, y)) == Unequality(x, y)
    assert Not(Unequality(x, y)) == Equality(x, y)
    assert Not(StrictGreaterThan(x, y)) == LessThan(x, y)
    assert Not(StrictLessThan(x, y)) == GreaterThan(x, y)
    assert Not(GreaterThan(x, y)) == StrictLessThan(x, y)
    assert Not(LessThan(x, y)) == StrictGreaterThan(x, y)


def test_EqualityNonEval_really_noneval():
    en = Eqn(x,x)
    assert en not in [S.true, S.false, True, False]
    assert en.doit() not in [S.true, S.false, True, False]
    en = Eqn(S(5),S(2))
    assert en not in [S.true, S.false, True, False]
    assert en.doit() not in [S.true, S.false, True, False]


def test_EqualityNonEval_solvers():
    # FIXME: move to solvers tests?
    from sympy import (solve, solve_linear, solve_undetermined_coeffs,
        nsolve)
    a, b = symbols('a, b')

    e = Eq(x, 9)
    en = Eqn(x, 9)
    assert solve(e, x) == solve(en, x)

    e = Eq(x*x, 9*x)
    en = Eqn(x*x, 9*x)
    assert solve(e, x) == solve(en, x)

    e = Eq(x+y, 0)
    en = Eqn(x+y, 0)
    assert solve_linear(e) == solve_linear(en)

    e = Eq(x, 0)
    en = Eqn(x, 0)
    assert solve_linear(e) == solve_linear(en)

    e = Eq(2*a*x + a+b, x)
    en = Eqn(2*a*x + a+b, x)
    assert solve_undetermined_coeffs(e,  [a, b], x) == \
           solve_undetermined_coeffs(en, [a, b], x)

    f1 = 3 * x**2 - 2 * y**2 - 1
    f2 = x**2 - 2 * x + y**2 + 2 * y - 8
    e1 = Eq(f1, 0)
    e2 = Eq(f2, 0)
    e1n = Eqn(f1, 0)
    e2n = Eqn(f2, 0)
    # this is a floating point equality test but they should really do
    # exactly the same thing, so reasonable to expect exact
    # equality---on a determininistic platform anyway :-)
    assert nsolve((e1, e2),   (x, y), (-1, 1)) == \
           nsolve((e1n, e2n), (x, y), (-1, 1))


def test_EqualityNonEval_solvers_xeqx():
    from sympy import solve, solve_linear
    # should be the empty list
    en = Eqn(x, x)
    soln = solve(en, x)
    assert soln == []
    assert soln not in [S.false, False]
    # why is this good output?  Consider:
    x2 = Symbol('x', positive=True)
    soln = solve(Eq(x2, -4), x2)
    assert soln == []
    assert soln not in [S.false, False]


@XFAIL  # mark or not?
def test_EqualityNonEval_solvers_no_soln():
    from sympy import solve, solve_linear
    # should be False not empty?
    en = Eqn(x, x-1)
    soln = solve(en, x)
    assert soln in [S.false, False]
    assert not soln == []

@XFAIL  # mark or not?
def test_EqualityNonEval_solve_linear():
    # even worse than above, this gives tuple (0,1)
    from sympy import solve_linear
    en = Eqn(x, x)
    soln = solve_linear(en, S(0), symbols=x)
    assert soln
    assert not soln == (0, 1)  # fails

@XFAIL  # mark or not?
def test_EqualityNonEval_solve_linear2():
    # just errors out, excepting no soln
    from sympy import solve_linear
    en = Eqn(x-1, x-2)
    soln = solve_linear(en, S(0), symbols=x)
    assert not soln
