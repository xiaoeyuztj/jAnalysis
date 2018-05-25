#!/bin/env python
import jROOT.Setting
import ROOT
import os
from math import sqrt
from jROOT.AtlasUtil import AtlasLabelPreliminary, DrawTextOneLine, DrawLuminosity

def getMCYield( sample_list , cut = None):
    total = ROOT.TH1F("total","total", 1,-10,10)
    for sample in sample_list.List:
        _file_ = ROOT.TFile( sample.get_file_link() )
        tmp = ROOT.TH1F("tmp","tmp", 1,-10,10)
        tree = _file_.Get("tree_NOMINAL")
        if cut is not None:
            finalcut = "weight*( %s )" %(cut)
        else:
            finalcut = "weight"
        tree.Draw("isMC>>tmp", finalcut)
        tmp.Sumw2()
        tmp.Scale( sample.normal361() )
        total.Add(tmp)
        _file_.Close()
    return  (total.Integral(), total.GetBinError(1))

def getMCFileYield( sample, cut = None):
    _file_ = ROOT.TFile( sample.get_file_link() )
    tmp = ROOT.TH1F("tmp","tmp", 1,-10,10)
    tree = _file_.Get("tree_NOMINAL")
    if cut is not None:
        finalcut = "weight*( %s )" %(cut)
    else:
        finalcut = "weight"
    tree.Draw("isMC>>tmp", finalcut)
    tmp.Sumw2()
    tmp.Scale( sample.normal361() )
    _file_.Close()
    return  ( tmp.Integral(), tmp.GetBinError(1) )

def getDataYield( sample_list , cut = None):
    total = ROOT.TH1F("total","total", 1,-10,10)
    for sample in sample_list.List:
        _file_ = ROOT.TFile( sample.get_file_link() )
        tmp = ROOT.TH1F("tmp","tmp", 1,-10,10)
        tree = _file_.Get("tree_NOMINAL")
        if cut is not None:
            finalcut = "weight*( %s )" %(cut)
        else:
            finalcut = "weight"
        tree.Draw("isMC>>tmp", finalcut)
        tmp.Sumw2()
        total.Add(tmp)
        _file_.Close()
    return  (total.Integral(), sqrt( total.Integral()) )

def getDataFileYield( sample, cut = None):
    _file_ = ROOT.TFile( sample.get_file_link() )
    tmp = ROOT.TH1F("tmp","tmp", 1,-10,10)
    tree = _file_.Get("tree_NOMINAL")
    if cut is not None:
        finalcut = "weight*( %s )" %(cut)
    else:
        finalcut = "weight"
    tree.Draw("isMC>>tmp", finalcut)
    tmp.Sumw2()
    _file_.Close()
    return  ( tmp.Integral(), sqrt( total.Integral()) )

