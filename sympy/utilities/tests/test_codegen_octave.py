from sympy.core import S, symbols, Eq, pi, Catalan, Lambda, Dummy
from sympy.core.compatibility import StringIO
from sympy import erf, Integral, Piecewise
from sympy import Equality
from sympy.matrices import Matrix, MatrixSymbol
from sympy.printing.codeprinter import Assignment
from sympy.utilities.codegen import (CCodeGen, Routine,
                                     InputArgument, CodeGenError,
                                     FCodeGen, OctaveCodeGen, codegen,
                                     CodeGenArgumentListError,
                                     OutputArgument, InOutArgument)
from sympy.utilities.pytest import raises
from sympy.utilities.lambdify import implemented_function
import sympy
from sympy.utilities.pytest import XFAIL


x, y, z = symbols('x,y,z')


def test_empty_m_code():
    code_gen = OctaveCodeGen()
    output = StringIO()
    code_gen.dump_m([], output, "file", header=False, empty=False)
    source = output.getvalue()
    assert source == ""


def test_empty_m_code_with_header():
    code_gen = OctaveCodeGen()
    output = StringIO()
    code_gen.dump_m([], output, "file", header=True, empty=False)
    source = output.getvalue()
    expected = (
        "%% Code generated with sympy " + sympy.__version__ + "\n"
        "% \n"
        "% See http://www.sympy.org/ for more information.\n"
        "% \n"
        "% This file is part of 'project'\n")
    assert source == expected


def test_simple_m_code():
    name_expr = ("test", (x + y)*z)
    result, = codegen(name_expr, "Octave", "test", header=False, empty=False)
    assert result[0] == "test.m"
    source = result[1]
    expected = (
        "function out1 = test(x, y, z)\n"
        "  out1 = z.*(x + y);\n"
        "end\n"
    )
    assert source == expected


def test_m_simple_code_nameout():
    expr = Equality(z, (x + y))
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Octave", "test", header=False, empty=False)
    source = result[1]
    expected = (
        "function z = test(x, y)\n"
        "  z = x + y;\n"
        "end\n"
    )
    assert source == expected


def test_numbersymbol_m_code():
    name_expr = ("test", pi**Catalan)
    result, = codegen(name_expr, "Octave", "test", header=False, empty=False)
    source = result[1]
    # FIXME: see comments in _print_NumberSymbol
    # expected = (
    #     "function out1 = test()\n"
    #     "  Catalan = 0.915965594177219011;\n"
    #     "  out1 = pi^Catalan;\n"
    #     "end\n"
    # )
    expected = (
        "function out1 = test()\n"
        "  out1 = pi^0.915965594177219011;\n"
        "end\n"
    )
    assert source == expected


def test_m_code_argument_order():
    expr = x + y
    routine = Routine("test", expr, argument_sequence=[z, x, y])
    code_gen = OctaveCodeGen()
    output = StringIO()
    code_gen.dump_m([routine], output, "test", header=False, empty=False)
    source = output.getvalue()
    expected = (
        "function out1 = test(z, x, y)\n"
        "  out1 = x + y;\n"
        "end\n"
    )
    assert source == expected


def test_multiple_results_m():
    # FIXME: is output order deterministic here, presumably input order?
    expr1 = (x + y)*z
    expr2 = (x - y)*z
    name_expr = ("test", [expr1, expr2])
    result, = codegen(name_expr, "Octave", "test", header=False, empty=False)
    source = result[1]
    expected = (
        "function [out1, out2] = test(x, y, z)\n"
        "  out1 = z.*(x + y);\n"
        "  out2 = z.*(x - y);\n"
        "end\n"
    )
    assert source == expected


def test_results_named_unordered():
    A, B, C = symbols('A,B,C')
    expr1 = Equality(C, (x + y)*z)
    expr2 = Equality(A, (x - y)*z)
    expr3 = Equality(B, 2*x)
    name_expr = ("test", [expr1, expr2, expr3])
    result, = codegen(name_expr, "Octave", "test", header=False, empty=False)
    source = result[1]
    expected = (
        "function [A, B, C] = test(x, y, z)\n"
        "  A = z.*(x - y);\n"
        "  B = 2*x;\n"
        "  C = z.*(x + y);\n"
        "end\n"
    )
    assert source == expected

def test_results_named_ordered():
    A, B, C = symbols('A,B,C')
    expr1 = Equality(C, (x + y)*z)
    expr2 = Equality(A, (x - y)*z)
    expr3 = Equality(B, 2*x)
    name_expr = ("test", [expr1, expr2, expr3])
    result = codegen(name_expr, "Octave", "test", header=False, empty=False,
                     argument_sequence=(x, z, y, C, A, B))
    assert result[0][0] == "test.m"
    source = result[0][1]
    expected = (
        "function [C, A, B] = test(x, z, y)\n"
        "  C = z.*(x + y);\n"
        "  A = z.*(x - y);\n"
        "  B = 2*x;\n"
        "end\n"
    )
    assert source == expected


def test_complicated_m_codegen():
    from sympy import sin, cos, tan
    name_expr = ("testlong",
            [ ((sin(x) + cos(y) + tan(z))**3).expand(),
            cos(cos(cos(cos(cos(cos(cos(cos(x + y + z))))))))
    ])
    result = codegen(name_expr, "Octave", "testlong", header=False, empty=False)
    assert result[0][0] == "testlong.m"
    source = result[0][1]
    expected = (
        "function [out1, out2] = testlong(x, y, z)\n"
        "  out1 = sin(x).^3 + 3*sin(x).^2.*cos(y) + 3*sin(x).^2.*tan(z)"
        " + 3*sin(x).*cos(y).^2 + 6*sin(x).*cos(y).*tan(z) + 3*sin(x).*tan(z).^2"
        " + cos(y).^3 + 3*cos(y).^2.*tan(z) + 3*cos(y).*tan(z).^2 + tan(z).^3;\n"
        "  out2 = cos(cos(cos(cos(cos(cos(cos(cos(x + y + z))))))));\n"
        "end\n"
    )
    assert source == expected


def test_m_output_arg_mixed_unordered():
    from sympy import sin, cos, tan
    a = symbols("a")
    r = Routine("foo", [cos(2*x), Equality(y, sin(x)), cos(x), Equality(a, sin(2*x))])
    ocg = OctaveCodeGen()
    result = ocg.write([r], "foo", header=False, empty=False)
    assert result[0][0] == "foo.m"
    source = result[0][1];
    expected = (
        'function [a, y, out3, out4] = foo(x)\n'
        '  a = sin(2*x);\n'
        '  y = sin(x);\n'
        '  out3 = cos(2*x);\n'
        '  out4 = cos(x);\n'
        'end\n'
    )
    assert source == expected


def test_piecewise_m():
    pw = Piecewise((0, x < -1), (x**2, x <= 1), (-x+2, x > 1), (1, True))
    name_expr = ("pwtest", pw)
    result, = codegen(name_expr, "Octave", "pwtest", header=False, empty=False)
    source = result[1]
    expected = (
        "function out1 = pwtest(x)\n"
        "  if (x < -1)\n"
        "    out1 = 0;\n"
        "  elseif (x <= 1)\n"
        "    out1 = x.^2;\n"
        "  elseif (x > 1)\n"
        "    out1 = -x + 2;\n"
        "  else\n"
        "    out1 = 1;\n"
        "  end\n"
        "end\n"
    )
    assert source == expected


def test_m_multifcns_per_file():
    name_expr = [ ("foo", [2*x, 3*y]), ("bar", [y**2, 4*y]) ]
    result = codegen(name_expr, "Octave", "foo", header=False, empty=False)
    assert result[0][0] == "foo.m"
    source = result[0][1];
    expected = (
        "function [out1, out2] = foo(x, y)\n"
        "  out1 = 2*x;\n"
        "  out2 = 3*y;\n"
        "end\n"
        "function [out1, out2] = bar(y)\n"
        "  out1 = y.^2;\n"
        "  out2 = 4*y;\n"
        "end\n"
    )
    assert source == expected


@XFAIL
def test_m_filename_match_first_fcn():
    # FIXME: implement this check, foo and bar should match.  In fact, we
    # should default "bar" here to the first fcn name---"foo".
    name_expr = [ ("foo", [2*x, 3*y]), ("bar", [y**2, 4*y]) ]
    raises(NameError, lambda: codegen(name_expr,
                        "Octave", "bar", header=False, empty=False))


def test_m_matrix_named():
    # FIXME: myout1 should be MatrixSymbol?  Well maybe we want this to work too.
    e2 = Matrix([[x, 2*y, pi*z]])
    name_expr = ("test", Equality(S('myout1'), e2, evaluate=False))
    result = codegen(name_expr, "Octave", "test", header=False, empty=False)
    assert result[0][0] == "test.m"
    source = result[0][1]
    expected = (
        "function myout1 = test(x, y, z)\n"
        "  myout1 = [x 2*y pi*z];\n"
        "end\n"
    )
    assert source == expected


@XFAIL
def test_m_matrix_named_matsym():
    # does component-by-component
    myout1 = MatrixSymbol('myout1', 1, 3)
    e2 = Matrix([[x, 2*y, pi*z]])
    name_expr = ("test", Equality(myout1, e2, evaluate=False))
    result = codegen(name_expr, "Octave", "test", header=False, empty=False)
    assert result[0][0] == "test.m"
    source = result[0][1]
    expected = (
        "function myout1 = test(x, y, z)\n"
        "  myout1 = [x 2*y pi*z];\n"
        "end\n"
    )
    assert source == expected


@XFAIL
def test_m_matrix_output_autoname():
    #FIXME: codegen gives weird name and works componentwise
    expr = Matrix([[x, x+y, 3]])
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Octave", "test", header=False, empty=False)
    source = result[1]
    expected = (
        "function out1 = test(x, y, z)\n"
        "  out1 = [x x + y 3];\n"
        "end\n"
    )
    assert source == expected


@XFAIL
def test_m_matrix_named_ordered_BROKEN():
    #FIXME: codegen wants to do component-wise stuff here, we must stop it
    e1 = (x + y)
    e2 = Matrix([[2*x, 2*y, 2*z]])
    e3 = Matrix([[x], [y], [z]])
    e4 = Matrix([[x, y], [z, 16]])
    #routine = Routine("test", (e1, e2, e3, e4))
    name_expr = ("test", (e1, e2, e3, e4))
    result, = codegen(name_expr, "Octave", "test", header=False, empty=False)
    source = result[1]
    expected = (
        "function [out1, out2, out3, out4] = test(x, y, z)\n"
        "  out1 = x + y;\n"
        "  out2 = [2*x 2*y 2*z];\n"
        "  out3 = [x; y; z];\n"
        "  out4 = [x y; ...\n"
        "z 16];\n"
        "end\n"
    )
    assert source == expected
