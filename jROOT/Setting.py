#!/bin/env python

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import ROOT

ROOT.gROOT.SetBatch()
# ignore INFO
# ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 1001;")
# ignore WARNING
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")

