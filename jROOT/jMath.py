#!/bin/env python

import functools
import ROOT
from math import sqrt

def jSum(nums, errs):
    totalsum = sum(nums)
    totalerr = sqrt(sum( list(map(lambda x: x**2, errs)) ))
    return (totalsum, totalerr)

def jDiv( x, y, ex, ey):
    if y==0:
        return (0, 0)
    r = x/y
    er = r * sqrt( ex*ex/x/x + ey*ey/y/y)
    return (r, er)

def jPol( a, b, A, eA):
    #f(A) = a * A^b
    r = a* (A**b)
    er = r * b * (A**(b-1)) * eA /A
    return (r, er)

def jSqrt(A, eA):
    return jPol( 1, 0.5, A, eA)
