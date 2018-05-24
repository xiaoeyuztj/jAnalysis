#!/bin/env python

import os

def MergeSampleList(lists = [], color=None):
    legs = [samplelist.leg for samplelist in lists]
    r = SampleList( color = color , leg = "+".join(legs))
    for samplelist in lists:
        for sample in samplelist.List:
            r.Add(sample)
    return r

class SampleList:
    def __init__(self, color, leg):
        self.color = color
        self.leg = leg
        self.List = []

    def Add(self, sample):
        self.List.append(sample)

class Sample:
    global_path = None
    def __init__(self, name, kfactor=1, filterefficiency=1,xsec=1, nevt=0, sumofweight=1, extraFactor=1, path=None, global_path = None):
        self.name = name
        self.kfactor = kfactor
        self.filterefficiency = filterefficiency
        self.xsec = xsec
        self.path = path
        self.sumofweight = sumofweight
        self.nevt = nevt
        self.extraFactor = extraFactor

        if Sample.global_path is None:
            Sample.global_path = global_path

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_extraFactor(self, extraFactor):
        self.extraFactor = extraFactor

    def get_extraFactor(self):
        return self.extraFactor

    def set_nevt(self, nevt):
        self.nevt = nevt

    def get_nevt(self):
        return self.nevt

    def set_kfactor(self,kfactor):
        self.kfactor = kfactor

    def get_kfactor(self):
        return self.kfactor

    def set_filterefficiency(self, filterefficiency):
        self.filterefficiency = filterefficiency

    def get_filterefficiency(self):
        return self.filterefficiency

    def set_xsec(self, xsec):
        self.xsec = xsec

    def get_xsec(self):
        return self.xsec

    def set_sumofweight(self, sumofweight):
        self.sumofweight = sumofweight

    def get_sumofweight(self):
        return self.sumofweight

    def set_path(self, path):
        self.path = path

    def normal361(self):
        r = self.kfactor * self.filterefficiency * self.xsec * 36.1 * self.extraFactor /self.sumofweight
        #print( self.kfactor , self.filterefficiency , self.xsec , self.sumofweight, tmp)
        return r

    @classmethod
    def set_global_path(cls, global_path):
        cls.global_path = global_path

    @classmethod
    def get_global_path(cls):
        return cls.global_path

    def get_file_link(self):
        if Sample.global_path is not None:
            return os.path.join(Sample.global_path, self.name)
        if self.path is not None:
            return os.path.join(self.path, self.name)
        return self.name

    def printInfo(self):
        print( "%s %20f %20f %20f %20f %20f" %( self.name,self.nevt, self.xsec, self.sumofweight, self.filterefficiency ,\
            self.kfactor) )
