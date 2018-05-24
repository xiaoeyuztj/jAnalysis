#! /bin/env python

class hinfo:
    def __init__(self, sample, sumofweight, xsec, filter_efficiency, k_factor):
        self.sample = sample
        self.sumofweight = sumofweight
        self.xsec = xsec
        self.filter_efficiency = filter_efficiency
        self.k_factor = k_factor

class MC:
    #def __init__(self, MC_Info = "/home/liji/jPlots/lib/MC_Info.txt"):
    def __init__(self, MC_Info = "/home/liji/Tools/VBSZZ/Samples.list"):
        self.f = open( MC_Info )
        self.mc_info = dict()
        for line in self.f:
            if line[-1]=="\n":
                line = line[:-1]
            tmp = line.split()
            sample = tmp[0]
            if len(tmp)>=3 and self.is_number(tmp[2]):
                xsec = float(tmp[2])
            else:
                xsec = -1
            if len(tmp)>=4 and self.is_number(tmp[3]):
                sumofweight = float(tmp[3])
            else:
                sumofweight = -1
            if len(tmp)>=5 and self.is_number(tmp[4]):
                filter_efficiency = float(tmp[4])
            else:
                filter_efficiency = 1
            if len(tmp)>=6 and self.is_number(tmp[5]):
                k_factor = float(tmp[5])
            else:
                k_factor = 1
            _tmp_ = hinfo(sample, sumofweight, xsec, filter_efficiency, k_factor)
            self.mc_info[sample] = _tmp_

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        return False

    def getInfo(self, sample_name):
        if ".root" in sample_name:
            sample_name = sample_name[:-5]
        if sample_name in self.mc_info:
            return self.mc_info[sample_name]
        return None

