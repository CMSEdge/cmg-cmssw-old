#####################################################################
######                                                              #
###### 88888888888         88                        888888888888   #  
###### 88                  88                                 ,88   #
###### 88                  88                               ,88"    #  
###### 88aaaaa     ,adPPYb,88  ,adPPYb,d8  ,adPPYba,      ,88"      #
###### 88"""""    a8"    `Y88 a8"    `Y88 a8P_____88    ,88"        #
###### 88         8b       88 8b       88 8PP"""""""  ,88"          #
###### 88         "8a,   ,d88 "8a,   ,d88 "8b,   ,aa 88"            #
###### 88888888888 `"8bbdP"Y8  `"YbbdP"Y8  `"Ybbd8"' 888888888888   #
######                       aa,    ,88                             #
######                         "Y8bbdP"                             #
######                                                              #
#####################################################################

import ROOT as r
import math as math

from optparse import OptionParser
from ROOT import gROOT, TCanvas, TFile
from Sample import Sample, Block, Tree
from CutManager import CutManager
from Canvas import Canvas


def make_rmue(histo_mm, histo_ee):

  ratio = histo_mm.Clone("rmue_" + histo_mm.GetName())
  ratio.Divide(histo_ee)
  ratio.GetYaxis().SetTitle("r_{#mu e}")
  
  for i in range(0, ratio.GetNbinsX()):
      ratio.SetBinContent(i, math.sqrt(ratio.GetBinContent(i)))

  return ratio



if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options] FilenameWithSamples", version="%prog 1.0")
    parser.add_option("-m", "--mode", action="store", dest="mode", default="rmue", help="Operation mode")
    (options, args) = parser.parse_args()

    if len(args) != 1:
      parser.error("wrong number of arguments")

    inputFileName = args[0]
    tree = Tree(inputFileName, "MC", 0)
   
    gROOT.ProcessLine('.L tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle() 
    cuts = CutManager()


    mll_ee_central = tree.getTH1F(4, "mll_ee_central", "t.lepsMll_Edge", 40, 20, 300, cuts.Add(cuts.DYControlNoMassLeptonee(), cuts.Central()), "", "m_{ll} [GeV]")
    mll_mm_central = tree.getTH1F(4, "mll_mm_central", "t.lepsMll_Edge", 40, 20, 300, cuts.Add(cuts.DYControlNoMassLeptonmm(), cuts.Central()), "", "m_{ll} [GeV]")
    met_ee_central = tree.getTH1F(4, "met_ee_central", "met_pt", 40, 20, 300, cuts.Add(cuts.DYControlNoMassLeptonee(), cuts.Central()), "", "m_{ll} [GeV]")
    met_mm_central = tree.getTH1F(4, "met_mm_central", "met_pt", 40, 20, 300, cuts.Add(cuts.DYControlNoMassLeptonmm(), cuts.Central()), "", "m_{ll} [GeV]")
    
    mll_ee_forward = tree.getTH1F(4, "mll_ee_forward", "t.lepsMll_Edge", 40, 20, 300, cuts.Add(cuts.DYControlNoMassLeptonee(), cuts.Forward()), "", "m_{ll} [GeV]")
    mll_mm_forward = tree.getTH1F(4, "mll_mm_forward", "t.lepsMll_Edge", 40, 20, 300, cuts.Add(cuts.DYControlNoMassLeptonmm(), cuts.Forward()), "", "m_{ll} [GeV]")
    met_ee_forward = tree.getTH1F(4, "met_ee_forward", "met_pt", 20, 0, 200, cuts.Add(cuts.DYControlNoMassLeptonee(), cuts.Forward()), "", "m_{ll} [GeV]")
    met_mm_forward = tree.getTH1F(4, "met_mm_forward", "met_pt", 20, 0, 200, cuts.Add(cuts.DYControlNoMassLeptonmm(), cuts.Forward()), "", "m_{ll} [GeV]")
   
    rmue_mll_central = make_rmue(mll_mm_central, mll_ee_central)
    plot_rmue_mll_central = Canvas("plot_rmue_mll_central", "png", 0.6, 0.6, 0.8, 0.8)
    plot_rmue_mll_central.addHisto(rmue_mll_central, "E1,SAME", "OF", "L", r.kBlack)
    plot_rmue_mll_central.save(0, 0, 0, 4.0)
    
    rmue_met_central = make_rmue(met_mm_central, met_ee_central)
    plot_rmue_met_central = Canvas("plot_rmue_met_central", "png", 0.6, 0.6, 0.8, 0.8)
    plot_rmue_met_central.addHisto(rmue_met_central, "E1,SAME", "OF", "L", r.kBlack)
    plot_rmue_met_central.save(0, 0, 0, 4.0)
    
    rmue_mll_forward = make_rmue(mll_mm_forward, mll_ee_forward)
    plot_rmue_mll_forward = Canvas("plot_rmue_mll_forward", "png", 0.6, 0.6, 0.8, 0.8)
    plot_rmue_mll_forward.addHisto(rmue_mll_forward, "E1,SAME", "OF", "L", r.kBlack)
    plot_rmue_mll_forward.save(0, 0, 0, 4.0)
    
    rmue_met_forward = make_rmue(met_mm_forward, met_ee_forward)
    plot_rmue_met_forward = Canvas("plot_rmue_met_forward", "png", 0.6, 0.6, 0.8, 0.8)
    plot_rmue_met_forward.addHisto(rmue_met_forward, "E1,SAME", "OF", "L", r.kBlack)
    plot_rmue_met_forward.save(0, 0, 0, 4.0)
    




