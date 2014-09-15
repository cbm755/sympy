from sympy.core import (S, pi, oo, symbols, Function,
                        Rational, Integer, Tuple, Symbol)
from sympy.core import EulerGamma, GoldenRatio, Catalan, Lambda
from sympy.functions import Piecewise, sqrt, Abs, ceiling, exp, sin, cos
from sympy.utilities.pytest import raises
from sympy.utilities.lambdify import implemented_function
from sympy.matrices import eye, Matrix, MatrixSymbol, Identity
from sympy.integrals import Integral
from sympy.concrete import Sum
from sympy.utilities.pytest import XFAIL

from sympy import octave_code as mcode

x, y, z = symbols('x,y,z')


def test_Integer():
    assert mcode(Integer(67)) == "67"
    assert mcode(Integer(-1)) == "-1"


def test_Rational():
    assert mcode(Rational(3, 7)) == "3/7"
    assert mcode(Rational(18, 9)) == "2"
    assert mcode(Rational(3, -7)) == "-3/7"
    assert mcode(Rational(-3, -7)) == "3/7"
    assert mcode(x + Rational(3, 7)) == "x + 3/7"
    assert mcode(Rational(3, 7)*x) == "3*x/7"


def test_Function():
    assert mcode(sin(x) ** cos(x)) == "sin(x).^cos(x)"
    assert mcode(abs(x)) == "abs(x)"
    assert mcode(ceiling(x)) == "ceil(x)"


def test_Pow():
    assert mcode(x**3) == "x.^3"
    assert mcode(x**(y**3)) == "x.^(y.^3)"
    # FIXME:
    #g = implemented_function('g', Lambda(x, 2*x))
    #print(mcode(1/(g(x)*3.5)**(x - y**x)/(x**2 + y)))
    #assert mcode(1/(g(x)*3.5)**(x - y**x)/(x**2 + y)) == \
    #    "(3.5*2*x).^(-x + y.^x)/(x.^2 + y)"
    assert mcode(x**Rational(2, 3)) == 'x.^(2/3)'
    # FIXME:
    #assert mcode(x**-1) == '1./x'
    #assert mcode(x**-1.0) == 'x.^-1.0'
    assert mcode(x**S.Half) == 'sqrt(x)'
    assert mcode(sqrt(x)) == "sqrt(x)"
    assert mcode(x**-S.Half) == '1/sqrt(x)'


def test_basic_ops():
    assert mcode(x*y) == "x.*y"
    assert mcode(x + y) == "x + y"
    assert mcode(x - y) == "x - y"
    assert mcode(-x) == "-x"


@XFAIL
def test_override_1_over_x():
    # FIXME
    assert mcode(1/x) == "1./x"


def test_mix_number_mult_symbols():
    assert mcode(3*x) == "3*x"
    assert mcode(pi*x) == "pi*x"
    assert mcode(3/x) == "3./x"
    assert mcode(pi/x) == "pi./x"
    assert mcode(x/3) == "x/3"
    assert mcode(x/pi) == "x/pi"
    assert mcode(x*y) == "x.*y"
    assert mcode(3*x*y) == "3*x.*y"
    assert mcode(3*pi*x*y) == "3*pi*x.*y"
    assert mcode(x/y) == "x./y"
    assert mcode(3*x/y) == "3*x./y"
    assert mcode(x*y/z) == "x.*y./z"
    assert mcode(x/y*z) == "x.*z./y"
    assert mcode(1/x/y) == "1./(x.*y)"
    assert mcode(2*pi*x/y/z) == "2*pi*x./(y.*z)"
    assert mcode(3*pi/x) == "3*pi./x"
    assert mcode(S(3)/5) == "3/5"
    assert mcode(S(3)/5*x) == "3*x/5"
    assert mcode(x/y/z) == "x./(y.*z)"
    assert mcode((x+y)/z) == "(x + y)./z"
    assert mcode((x+y)/(z+x)) == "(x + y)./(x + z)"
    assert mcode((x+y)/EulerGamma) == "(x + y)/0.577215664901532866"
    assert mcode(x/3/pi) == "x/(3*pi)"
    assert mcode(S(3)/5*x*y/pi) == "3*x.*y/(5*pi)"


def test_mix_number_pow_symbols():
    assert mcode(pi**3) == 'pi^3'
    assert mcode(x**2) == 'x.^2'
    assert mcode(x**(pi**3)) == 'x.^(pi^3)'
    assert mcode(x**y) == 'x.^y'
    assert mcode(x**(y**z)) == 'x.^(y.^z)'
    assert mcode((x**y)**z) == '(x.^y).^z'


def test_imag():
    I = S('I')
    assert mcode(I) == "1i"
    assert mcode(5*I) == "5i"
    assert mcode((S(3)/2)*I) == "3*1i/2"
    assert mcode(3+4*I) == "3 + 4i"


def test_constants():
    assert mcode(pi) == "pi"
    assert mcode(oo) == "inf"
    assert mcode(-oo) == "-inf"
    assert mcode(S.NegativeInfinity) == "-inf"
    assert mcode(S.NaN) == "NaN"
    assert mcode(S.Exp1) == "exp(1)"
    assert mcode(exp(1)) == "exp(1)"


def test_constants_other():
    assert mcode(2*GoldenRatio) == "2*(1+sqrt(5))/2"
    assert mcode(2*Catalan) == "2*0.915965594177219011"
    assert mcode(2*EulerGamma) == "2*0.577215664901532866"


def test_boolean():
    assert mcode(x & y) == "x && y"
    assert mcode(x | y) == "x || y"
    assert mcode(~x) == "~x"
    assert mcode(x & y & z) == "x && y && z"
    assert mcode(x | y | z) == "x || y || z"
    assert mcode((x & y) | z) == "z || x && y"
    assert mcode((x | y) & z) == "z && (x || y)"


def test_Matrices():
    assert mcode(Matrix(1, 1, [10])) == "10"
    A = Matrix([[1, sin(x/2), abs(x)],
                [0, 1, pi],
                [0, exp(1), ceiling(x)]]);
    expected = ("[1 sin(x/2)  abs(x); ...\n"
                "0        1      pi; ...\n"
                "0   exp(1) ceil(x)]")
    assert mcode(A) == expected
    # row and columns
    assert mcode(A[:,0]) == "[1; 0; 0]"
    assert mcode(A[0,:]) == "[1 sin(x/2) abs(x)]"
    # empty matrices
    assert mcode(Matrix(0, 0, [])) == '[]'
    assert mcode(Matrix(0, 3, [])) == 'zeros(0, 3)'
    # annoying to read but correct
    assert mcode(Matrix([[x, x - y, -y]])) == "[x x - y -y]"


def test_vector_entries_hadamard():
    # For a row or column, user might to use the other dimension
    A = Matrix([[1, sin(2/x), 3*pi/x/5]])
    assert mcode(A) == "[1 sin(2./x) 3*pi./(5*x)]"
    assert mcode(A.T) == "[          1;   sin(2./x); 3*pi./(5*x)]"


@XFAIL
def test_Matrices_entries_not_hadamard():
    # For Matrix with col >= 2, row >= 2, they need to be scalars
    # FIXME: is it worth worrying about this?  Its not wrong, just
    # leave it user's responsibility to put scalar data for x.
    A = Matrix([[1, sin(2/x), 3*pi/x/5], [1, 2, x*y]])
    expected = ("[1 sin(2/x) 3*pi/(5*x); ...\n"
                "1        2        x*y]")
    assert mcode(A) == expected


def test_MatrixSymbol():
    n = Symbol('n', integer=True)
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', n, n)
    assert mcode(A*B) == "A*B"
    assert mcode(B*A) == "B*A"
    assert mcode(2*A*B) == "2*A*B"
    assert mcode(B*2*A) == "2*B*A"
    assert mcode(A*(B + 3*Identity(n))) == "A*(3*eye(n) + B)"
    assert mcode(A**(x**2)) == "A^(x.^2)"
    assert mcode(A**3) == "A^3"
    assert mcode(A**(S.Half)) == "A^(1/2)"


def test_special_matrices():
    assert mcode(6*Identity(3)) == "6*eye(3)"


def test_containers():
    assert mcode([1, 2, 3, [4, 5, [6, 7]], 8, [9, 10], 11]) == \
        "{1, 2, 3, {4, 5, {6, 7}}, 8, {9, 10}, 11}"
    assert mcode((1, 2, (3, 4))) == "{1, 2, {3, 4}}"
    assert mcode([1]) == "{1}"
    assert mcode((1,)) == "{1}"
    assert mcode(Tuple(*[1, 2, 3])) == "{1, 2, 3}"
    assert mcode((1, x*y, (3, x**2))) == "{1, x.*y, {3, x.^2}}"
    # scalar, matrix, empty matrix and empty list
    assert mcode((1, eye(3), Matrix(0, 0, []), [])) == "{1, [1 0 0; ...\n0 1 0; ...\n0 0 1], [], {}}"


def test_octave_piecewise():
    expr = Piecewise((x, x < 1), (x**2, True))
    assert mcode(expr) == ("(x < 1).*(x) + (~(x < 1)).*(x.^2)")
    assert mcode(expr, assign_to="c") == (
            "if (x < 1)\n"
            "  c = x;\n"
            "else\n"
            "  c = x.^2;\n"
            "end")
    expr = Piecewise((x**2, x < 1), (x**3, x < 2), (x**4, x < 3), (x**5, True))
    assert mcode(expr) == (
            "(x < 1).*(x.^2) + (~(x < 1)).*( ...\n"
            "(x < 2).*(x.^3) + (~(x < 2)).*( ...\n"
            "(x < 3).*(x.^4) + (~(x < 3)).*(x.^5)))")
    assert mcode(expr, assign_to='c') == (
            "if (x < 1)\n"
            "  c = x.^2;\n"
            "elseif (x < 2)\n"
            "  c = x.^3;\n"
            "elseif (x < 3)\n"
            "  c = x.^4;\n"
            "else\n"
            "  c = x.^5;\n"
            "end")
    # Check that Piecewise without a True (default) condition error
    expr = Piecewise((x, x < 1), (x**2, x > 1), (sin(x), x > 0))
    raises(ValueError, lambda: mcode(expr))


@XFAIL
def test_octave_piecewise_times_const():
    # FIXME: self.parenthesize something! but where?
    expr = Piecewise((x, x < 1), (x**2, True))
    assert mcode(2*expr) == ("2*((x < 1).*(x) + (~(x < 1)).*(x^2))")


def test_octave_matrix_assign_to():
    A = Matrix([[1, 2, 3]])
    assert mcode(A, assign_to='a') == "a = [1 2 3];"


def test_octave_boolean():
    assert mcode(True) == "true"
    assert mcode(S.true) == "true"
    assert mcode(False) == "false"
    assert mcode(S.false) == "false"
