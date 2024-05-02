from sympy.core.function import Function
from sympy.core.power import Pow

class elliptic_k(Function):
    @classmethod
    def eval(cls, m) -> None:
        ...
    
    def fdiff(self, argindex=...):
        ...
    


class elliptic_f(Function):
    @classmethod
    def eval(cls, z, m) -> None:
        ...
    
    def fdiff(self, argindex=...):
        ...
    


class elliptic_e(Function):
    @classmethod
    def eval(cls, m, z=...) -> None:
        ...
    
    def fdiff(self, argindex=...) -> Pow:
        ...
    


class elliptic_pi(Function):
    @classmethod
    def eval(cls, n, m, z=...):
        ...
    
    def fdiff(self, argindex=...):
        ...
    


