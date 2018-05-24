#!/bin/env python
import setting
import ROOT
import os
from math import sqrt
from AtlasUtil import AtlasLabelPreliminary, DrawTextOneLine, DrawLuminosity

class jPlot:
    def __init__(self, Datas, MCs, output="out.pdf", path="./", up=None, down=None, linewidth=2, MCPlotStyle="f",
            info=None, ratioYup=None, ratioYdown=None):
        import AtlasStyle
        ROOT.gStyle.SetLegendBorderSize(0)
        self.c = ROOT.TCanvas("c", "c")
        self.Datas = Datas
        self.MCs = MCs
        self.outputfile = os.path.join( path + output )
        self.c.Print(self.outputfile + "[")
        self.histMCs= []
        self.up = up
        self.down = down
        self.linewidth = linewidth
        self.MCPlotStyle = MCPlotStyle
        self.info = info
        self.ratioYdown = ratioYdown
        self.ratioYup = ratioYup
        class jPadConfig:
            def __init__(self):
                self.ymin = 0.0
                self.ymax = 1.0
                self.k = 0.25
                self.pady = 0.1 + (self.ymax - 0.1) * self.k
                self.xmin = 0.05
                self.xmax = 0.95
                self.labelSizeHistOnly = 0.06
                self.titleSizeHistOnly = 0.06
                self.labelSizeHist = 0.06
                self.titleSizeHist = 0.06
                self.labelSizeRatio= 0.06
                self.titleSizeRatio= 0.06
                self.offsetHistOnly = 0.8
                self.offsetHist= 0.8
                self.offsetRatio= 0.8
                self.fontFactorRatio = None
                self.fontFactorTotal= None
                self.initFontSize()

            def __del__(self):
                pass
            def setFontFactorRatio(self, fontFactor):
                self.fontFactorRatio = fontFactor
            def setFontFactorTotal(self, fontFactor):
                self.fontFactorTotal= fontFactor

            def initFontSize(self):
                c = ROOT.TCanvas()
                pad1 = ROOT.TPad("pad1", "hists", self.xmin, self.pady, self.xmax, self.ymax)
                pad2 = ROOT.TPad("pad2", "ratio", self.xmin, self.ymin, self.xmax, self.pady )
                pad1.Draw()
                pad2.Draw()
                pad1.SetBottomMargin(0.03)
                pad2.SetTopMargin(0.03)
                pad2.SetBottomMargin(0.35)
                pad1Width = pad1.XtoPixel(pad1.GetX2())
                pad1Height = pad1.YtoPixel(pad1.GetY1())
                if (pad1Width<pad1Height):
                    pad1FontFactor = pad1Width
                else:
                    pad1FontFactor = pad1Height
                pad2Width = pad2.XtoPixel(pad2.GetX2())
                pad2Height = pad2.YtoPixel(pad2.GetY1())
                if (pad2Width<pad2Height):
                    pad2FontFactor = pad2Width
                else:
                    pad2FontFactor = pad2Height
                self.labelSizeRatio = self.labelSizeHist * pad1FontFactor / float(pad2FontFactor)
                self.titleSizeRatio = self.titleSizeHist * pad1FontFactor / float(pad2FontFactor)
                self.offsetRatio = self.offsetHist /( pad1FontFactor / float(pad2FontFactor))
                pad3 = ROOT.TPad("pad3", "histsonly", self.xmin, self.ymin, self.xmax, self.ymax)
                pad3.Draw()
                pad3Width = pad3.XtoPixel(pad3.GetX2())
                pad3Height = pad3.YtoPixel(pad3.GetY1())
                if (pad3Width<pad3Height):
                    pad3FontFactor = pad3Width
                else:
                    pad3FontFactor = pad3Height
                self.labelSizeHistOnly= self.labelSizeHist * pad1FontFactor / float(pad3FontFactor)
                self.titleSizeHistOnly= self.titleSizeHist * pad1FontFactor / float(pad3FontFactor)
                self.offsetHistOnly= self.offsetHist /( pad1FontFactor / float(pad3FontFactor))

        self.jPad= jPadConfig()


    def __del__(self):
        self.c.Print( self.outputfile + "]" )

    def plotDataMC(self, cut=None, variable="isMC", left=-10, right=10, up=None, down=None, nBins=1, xlabel="isMC",
            ylabel="events", ratio=True, ratioYLabel="Data/MC", logY=True, treename="tree_NOMINAL", MCsort=True,
            info=None, ratioYup=None, ratioYdown=None):
        self.c.Clear()
        self.histMCs = []
        if ratio:
            histPad = ROOT.TPad("histPad", "histPad", self.jPad.xmin, self.jPad.pady, self.jPad.xmax, self.jPad.ymax)
            ratioPad = ROOT.TPad("ratioPad", "ratioPad", self.jPad.xmin, self.jPad.ymin, self.jPad.xmax, self.jPad.pady )
            histPad.Draw()
            ratioPad.Draw()
            histPad.SetBottomMargin(0.03)
            ratioPad.SetTopMargin(0.03)
            ratioPad.SetBottomMargin(0.35)
        else:
            histPad = ROOT.TPad("histPad", "histPad", self.jPad.xmin, self.jPad.ymin, self.jPad.xmax, self.jPad.ymax)
            histPad.Draw()

        histPad.cd()
        if logY:
		    histPad.SetLogy()

        leg1 = ROOT.TLegend(0.7,0.70,0.8,0.9)
        leg2 = ROOT.TLegend(0.8,0.75,0.9,0.9)
        leg1.Clear()
        leg2.Clear()
        ROOT.gStyle.SetLegendTextSize(self.jPad.titleSize* 0.8)

        if cut is not None:
            finalcut = "weight*( %s )" %(cut)
        else:
            finalcut = "weight"

        data = ROOT.TH1F("data", "data", nBins, left, right)
        for item in self.Datas.List:
            r = ROOT.TFile( item.get_file_link() )
            tmp = ROOT.TH1F("tmp", "tmp", nBins, left, right)
            tree = r.Get(treename)
            tree.Draw( variable + ">>" + "tmp", finalcut)
            tmp.Sumw2()
            data.Add(tmp, 1)
            r.Close()
        data.SetLineColor( ROOT.kBlack)

        for _mc_ in self.MCs:
            mc = _mc_.List
            leg = _mc_.leg
            color = _mc_.color
            mc_tmp = ROOT.TH1F(leg, leg, nBins, left, right)

            for item in mc:
                r = ROOT.TFile( item.get_file_link() )
                new_tmp = ROOT.TH1F(leg, leg, nBins, left, right)
                tree = r.Get(treename)
                tree.Draw( variable + ">>" + leg, finalcut)
                new_tmp.Sumw2()
                new_tmp.Scale(item.normal361())
                mc_tmp.Add(new_tmp, 1)
                r.Close()

            mc_tmp.SetLineColor(color)
            mc_tmp.SetFillColor(color)
            mc_tmp.SetLineWidth( self.linewidth )
            self.histMCs.append( (mc_tmp, leg))

        hsMC = ROOT.THStack( "hsMC", "hsMC")
        if up is not None:
            hsMC.SetMaximum(up)
        elif self.up is not None:
            hsMC.SetMaximum( self.up)
        if down is not None:
            hsMS.SetMinimum(down)
        elif self.down is not None:
            hsMC.SetMinimum(self.down)

        if MCsort:
            tmp_list = []
            while self.histMCs:
                ( minhist , leg, self.histMCs ) = self.minIntegralHist(self.histMCs)
                tmp_list.append( (minhist, leg))
            self.histMCs = tmp_list

        leg1.AddEntry( data, self.Datas.leg, "ep")

        totalMC = ROOT.TH1F("totalMC", "totalMC", nBins, left, right)
        totalData = ROOT.TH1F("totalData", "totalData", nBins, left, right)
        totalData.Add( data, 1)
        for (hist, leg) in self.histMCs:
            hsMC.Add(hist)
            totalMC.Add( hist, 1)
        hsMC.Draw("hist f")
        hsMC.SetTitle("")
        hsMC.GetYaxis().SetTitle(ylabel)
        if ratio:
            hsMC.GetXaxis().SetTitleSize(0)
            hsMC.GetXaxis().SetLabelSize(0)
            hsMC.GetYaxis().SetTitleOffset(self.jPad.offsetHistHist)
            hsMC.GetYaxis().SetTitleSize(self.jPad.titleSizeHistHist)
            hsMC.GetYaxis().SetLabelSize(self.jPad.labelSizeHistHist)
        else:
            hsMC.GetXaxis().SetTitle(xlabel)
            hsMC.GetXaxis().SetTitleOffset(self.jPad.offsetHistOnly)
            hsMC.GetXaxis().SetTitleSize(self.jPad.titleSizeHistHistOnly)
            hsMC.GetXaxis().SetLabelSize(self.jPad.labelSizeHistHistOnly)
            hsMC.GetYaxis().SetTitleOffset(self.jPad.offsetHistOnly)
            hsMC.GetYaxis().SetTitleSize(self.jPad.titleSizeHistHistOnly)
            hsMC.GetYaxis().SetLabelSize(self.jPad.labelSizeHistHistOnly)

        data.Draw("same hist ep")
        for i in range(len(self.histMCs)):
            (hist, leg) = self.histMCs[-i-1]
            if i+1 <= len(self.histMCs)*0.5:
                leg1.AddEntry( hist, leg, "f")
            else:
                leg2.AddEntry( hist, leg, "f")

        leg1.Draw("same")
        leg2.Draw("same")
        if ratio:
            DrawLuminosity(0.25, 0.85, 36.1, size = self.jPad.titleSizeHist)
        else:
            DrawLuminosity(0.25, 0.85, 36.1, size = self.jPad.titleSizeHistOnly)

        if info is not None:
            if ratio:
                DrawTextOneLine(0.25, 0.75, info, size=self.jPad.titleSizeHist)
            else:
                DrawTextOneLine(0.25, 0.75, info, size=self.jPad.titleSizeHistOnly)
        elif self.info is not None:
            if ratio:
                DrawTextOneLine(0.25, 0.75, self.info, size=self.jPad.titleSizeHist)
            else:
                DrawTextOneLine(0.25, 0.75, self.info, size=self.jPad.titleSizeHistOnly)

        if ratio:
            ratioPad.cd()
            ratioPad.SetGrid()

            totalData.Sumw2()
            totalMC.Sumw2()
            totalData.Divide( totalMC )
            if self.ratioYup is not None:
                totalData.SetMaximum(self.ratioYup)
            elif ratioYup is not None:
                totalData.SetMaximum(ratioYup)
            else:
                totalData.SetMaximum(2)
            if self.ratioYdown is not None:
                totalData.SetMinimum(self.ratioYdown)
            elif ratioYdown is not None:
                totalData.SetMinimum(ratioYdown)
            else:
                totalData.SetMinimum(0)
            totalData.GetYaxis().SetTitle( ratioYLabel )
            totalData.GetYaxis().SetTitleOffset(self.jPad.offsetRatio)
            totalData.GetYaxis().SetTitleSize(self.jPad.titleSizeRatio)
            totalData.GetYaxis().SetLabelSize(self.jPad.labelSizeRatio)
            totalData.GetYaxis().CenterTitle()
            totalData.GetYaxis().SetNdivisions(502)
            totalData.GetXaxis().SetTitle( xlabel)
            totalData.GetXaxis().SetTitleSize(self.jPad.titleSizeRatio)
            totalData.GetXaxis().SetLabelSize(self.jPad.labelSizeRatio)
            totalData.SetFillColor(-1)
            totalData.SetLineColor(1)
            totalData.SetTitle("")
            totalData.Draw("le")

        self.c.Print(self.outputfile )

    def minIntegralHist(self, histMCs):
        (minhist, itsleg) = histMCs[0]
        integral = minhist.Integral()
        for (_hist_, _leg_) in histMCs[1:]:
            if _hist_.Integral() < integral:
                minhist = _hist_
                integral = minhist.Integral()
                itsleg = _leg_
        histMCs.remove(( minhist, itsleg))
        return (minhist, itsleg, histMCs)

    def plotMCs(self, MCs=None, cut=None, colors=None, legs=None, variable="isMC", left=-10, right=10, up=None, down=None, nBins=1,
            xlabel="isMC", ylabel="events", ratio=True, ratioYLabel="Data/MC", logY=True, treename="tree_NOMINAL", MCsort=False,
            info=None, ratioYup=None, ratioYdown=None, normal1=False):
        self.c.Clear()
        self.histMCs = []
        if ratio:
            histPad = ROOT.TPad("histPad", "histPad", self.jPad.xmin, self.jPad.pady, self.jPad.xmax, self.jPad.ymax)
            ratioPad = ROOT.TPad("ratioPad", "ratioPad", self.jPad.xmin, self.jPad.ymin, self.jPad.xmax, self.jPad.pady )
            histPad.Draw()
            ratioPad.Draw()
            histPad.SetBottomMargin(0.03)
            ratioPad.SetTopMargin(0.03)
            ratioPad.SetBottomMargin(0.35)
        else:
            histPad = ROOT.TPad("histPad", "histPad", self.jPad.xmin, self.jPad.ymin, self.jPad.xmax, self.jPad.ymax)
            histPad.Draw()

        histPad.cd()
        if logY:
		    histPad.SetLogy()

        leg1 = ROOT.TLegend(0.7,0.70,0.8,0.9)
        leg2 = ROOT.TLegend(0.8,0.75,0.9,0.9)
        leg1.Clear()
        leg2.Clear()
        if ratio:
            ROOT.gStyle.SetLegendTextSize(self.jPad.titleSizeHist* 0.8)
        else:
            ROOT.gStyle.SetLegendTextSize(self.jPad.titleSizeHistOnly* 0.8)

        MC_to_plot = self.MCs
        if MCs is not None:
            MC_to_plot = MCs

        finalVari = None
        if type(variable) is str:
            finalVari = []
            for item in MC_to_plot:
                finalVari.append(variable)
        elif type(variable) is list:
            finalVari = variable

        finalcut = None
        if cut is None:
            finalcut = []
            for item in MC_to_plot:
                finalcut = "weight"
        elif type(cut) is str:
            finalcut = []
            if cut[0:6] is "weight":
                finalcut.append( cut)
            else:
                finalcut.append("weight*( %s )" %(cut))
        elif type(cut) is list:
            finalcut = []
            for _cut_ in cut:
                if type(_cut_) is str:
                    if _cut_[0:6] is "weight":
                        finalcut.append(_cut_)
                    else:
                        finalcut.append("weight*( %s )" %(_cut_) )
                elif type(_cut_) is list:
                    tmp = []
                    for item in _cut_:
                        if item[0:6] is "weight":
                            tmp.append(item)
                        else:
                            tmp.append("weight*( %s )" %(item))
                    finalcut.append(tmp)

        for (_mc_, _finalcut_, index, vari) in zip(MC_to_plot, finalcut, range(len(finalcut)), finalVari):
            mc = _mc_.List
            if colors is not None:
                color = colors[index]
            else:
                color = _mc_.color
            if legs is not None:
                leg = legs[index]
            else:
                leg = _mc_.leg

            mc_tmp = ROOT.TH1F(leg, leg, nBins, left, right)
            for item in mc:
                r = ROOT.TFile( item.get_file_link() )
                if type(vari) is str:
                    new_tmp = ROOT.TH1F(leg, leg, nBins, left, right)
                    tree = r.Get(treename)
                    tree.Draw( vari+ ">>" + leg, _finalcut_)
                    new_tmp.Sumw2()
                    new_tmp.Scale(item.normal361())
                    mc_tmp.Add(new_tmp, 1)
                elif type(vari) is list:
                    if type( _finalcut_) is str:
                        for _vari_ in vari:
                            new_tmp = ROOT.TH1F(leg, leg, nBins, left, right)
                            tree = r.Get(treename)
                            tree.Draw( _vari_+ ">>" + leg, _finalcut_)
                            new_tmp.Sumw2()
                            new_tmp.Scale(item.normal361())
                            mc_tmp.Add(new_tmp, 1)
                    elif type( _finalcut_) is list:
                        for _vari_, _cut_ in zip(vari, _finalcut_):
                            new_tmp = ROOT.TH1F(leg, leg, nBins, left, right)
                            tree = r.Get(treename)
                            tree.Draw( _vari_+ ">>" + leg, _cut_)
                            new_tmp.Sumw2()
                            new_tmp.Scale(item.normal361())
                            mc_tmp.Add(new_tmp, 1)
                r.Close()

            mc_tmp.SetLineColor(color)
            mc_tmp.SetLineWidth( self.linewidth )
            if normal1:
                mc_tmp.Scale( 1.0/mc_tmp.Integral() )
            self.histMCs.append( (mc_tmp, leg, color))

        r = dict()
        for ((hist, leg, color), index) in zip( self.histMCs, range(len(self.histMCs))):
            r[leg] = hist.Integral()
            if index ==0:
                hist.Draw("hist")
                hist.SetTitle("")
                hist.GetYaxis().SetTitle(ylabel)
                if ratio:
                    hist.GetXaxis().SetTitleSize(0)
                    hist.GetXaxis().SetLabelSize(0)
                    hist.GetYaxis().SetTitleOffset(self.jPad.offsetHist)
                    hist.GetYaxis().SetTitleSize(self.jPad.titleSizeHist)
                    hist.GetYaxis().SetLabelSize(self.jPad.labelSizeHist)
                else:
                    hist.GetXaxis().SetTitle(xlabel)
                    hist.GetXaxis().SetTitleOffset(self.jPad.offsetHistOnly)
                    hist.GetXaxis().SetTitleSize(self.jPad.titleSizeHistOnly)
                    hist.GetXaxis().SetLabelSize(self.jPad.labelSizeHistOnly)
                    hist.GetYaxis().SetTitleOffset(self.jPad.offsetHistOnly)
                    hist.GetYaxis().SetTitleSize(self.jPad.titleSizeHistOnly)
                    hist.GetYaxis().SetLabelSize(self.jPad.labelSizeHistOnly)
                if up is not None:
                    hist.SetMaximum(up)
                elif self.up is not None:
                    hist.SetMaximum(self.up)
                if down is not None:
                    hist.SetMinimum(down)
                elif self.down is not None:
                    hist.SetMinimum(self.down)
            else:
                hist.Draw( "hist same")

        for i in range(len(self.histMCs)):
            (hist, leg, color) = self.histMCs[-i-1]
            if len(self.histMCs) <=4:
                leg2.AddEntry( hist, leg, "l")
            else:
                if i+1 <= len(self.histMCs)*0.5:
                    leg1.AddEntry( hist, leg, "l")
                else:
                    leg2.AddEntry( hist, leg, "l")

        leg1.SetFillStyle(0)
        leg2.SetFillStyle(0)
        leg1.Draw("same")
        leg2.Draw("same")
        if ratio:
            DrawLuminosity(0.25, 0.85, 36.1, size = self.jPad.titleSizeHist)
        else:
            DrawLuminosity(0.25, 0.85, 36.1, size = self.jPad.titleSizeHistOnly)

        if info is not None:
            if ratio:
                DrawTextOneLine(0.25, 0.75, info, size=self.jPad.titleSizeHist)
            else:
                DrawTextOneLine(0.25, 0.75, info, size=self.jPad.titleSizeHistOnly)
        elif self.info is not None:
            if ratio:
                DrawTextOneLine(0.25, 0.75, self.info, size=self.jPad.titleSizeHist)
            else:
                DrawTextOneLine(0.25, 0.75, self.info, size=self.jPad.titleSizeHistOnly)

        if ratio:
            ratioPad.cd()
            ratioPad.SetGrid()

            histRatios = []
            for (hist, leg, color) in self.histMCs:
                tmp = hist.Clone(leg)
                histRatios.append((tmp, color))
            (hist0, color0) = histRatios[0]
            (histlast, colorlast) = histRatios[-1]
            for (hist, color) in histRatios[:-1]:
                hist.Divide(histlast)
            hist0.Draw("hist")
            hist0.SetLineColor(color0)
            hist0.GetYaxis().SetTitle( ratioYLabel )
            hist0.GetYaxis().SetTitleOffset(self.jPad.offsetRatio)
            hist0.GetYaxis().SetTitleSize(self.jPad.titleSizeRatio)
            hist0.GetYaxis().SetLabelSize(self.jPad.labelSizeRatio)
            hist0.GetYaxis().CenterTitle()
            hist0.GetYaxis().SetNdivisions(502)
            hist0.GetXaxis().SetTitle( xlabel)
            hist0.GetXaxis().SetTitleSize(self.jPad.titleSizeRatio)
            hist0.GetXaxis().SetLabelSize(self.jPad.labelSizeRatio)
            hist0.SetFillColor(0)
            hist0.SetTitle("")
            for (hist, color) in histRatios[1:-1]:
                #hist.SetFillColorAlpha(ROOT.kWhite, 0.1)
                hist.SetFillColor(0)
                hist.SetLineColor(color)
                hist.Draw("hist same")

            if self.ratioYup is not None:
                hist0.SetMaximum(self.ratioYup)
            elif ratioYup is not None:
                hist0.SetMaximum(ratioYup)
            else:
                hist0.SetMaximum(2)
            if self.ratioYdown is not None:
                hist0.SetMinimum(self.ratioYdown)
            elif ratioYdown is not None:
                hist0.SetMinimum(ratioYdown)
            else:
                hist0.SetMinimum(0)

        self.c.Print(self.outputfile )
        return r

