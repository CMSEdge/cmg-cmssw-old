#####################################################################
######                                                              #
###### 8=========D         OO                        8==========D   #  
###### OO                  ||                                ,88   #
###### ||                  ||                              ,88"    #  
###### ||O---\     ,adPPYb,|| ,adPPYb,d8  ,adPPYba,      ,88"      #
###### ||O---/    a8"    `Y||a8"    `Y88 a8P_____88    ,88"        #
###### ||         8b       ||8b       88 8PP"""""""  ,88"          #
###### \/         "8a,   ,d||"8a,   ,d88 "8b,   ,aa 88"            #
###### 8=========D `"8bbdP"\/  `"YbbdP"Y8  `"Ybbd8"' 8==========D   #
######                       aa,    ,88                             #
######                         "Y8bbdP"                             #
######                                                              #
#####################################################################

import ROOT as r
import math as math

from optparse import OptionParser
from ROOT import gROOT, TCanvas, TFile, TF1
from Sample import Sample, Block, Tree
from CutManager import CutManager
from Canvas import Canvas


def make_rsfof(histo_sf, histo_of):

    ratio = histo_sf.Clone("rsfof_" + histo_sf.GetName())
    ratio.Divide(histo_of)
    ratio.GetYaxis().SetTitle("r_{SFOF}")

    fit = TF1('myfit','pol0', ratio.GetXaxis().GetXmin(), ratio.GetXaxis().GetXmax())
    
    ratio.Fit('myfit')
    
    f = open(ratio.GetName()+'_values.txt', 'w')
    for i in range(1, ratio.GetNbinsX()+1):
        min, max = ratio.GetBinLowEdge(i), ratio.GetBinLowEdge(i)+ratio.GetBinWidth(i)
        print    'R_SFOF in [%.2f, %.2f] GeV:\t%.3f +- %.3f'    %(min, max, ratio.GetBinContent(i), ratio.GetBinError(i) )
        f.write( 'R_SFOF in [%.2f, %.2f] GeV:\t%.3f +- %.3f \n' %(min, max, ratio.GetBinContent(i), ratio.GetBinError(i) ) )
    f.close()
    return ratio



if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options] FilenameWithSamples", version="%prog 1.0")
    parser.add_option("-m", "--mode", action="store", dest="mode", default="rsfof", help="Operation mode")
    (options, args) = parser.parse_args()

    if len(args) != 1:
      parser.error("wrong number of arguments")

    inputFileName = args[0]
    tree = Tree(inputFileName, "MC", 0)
   
    gROOT.ProcessLine('.L tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle() 
    cuts = CutManager()

    mll_sf_central = tree.getTH1F(4, "mll_sf_central", "t.lepsMll_Edge", 20, 20, 250, cuts.Add(cuts.ControlNoMassLeptonSF(), cuts.Central()), "", "m_{ll} (GeV)")
    met_sf_central = tree.getTH1F(4, "met_sf_central", "met_pt"        , 20, 20, 250, cuts.Add(cuts.ControlNoMassLeptonSF(), cuts.Central()), "", "E_{T}^{miss} (GeV)")
    mll_of_central = tree.getTH1F(4, "mll_of_central", "t.lepsMll_Edge", 20, 20, 250, cuts.Add(cuts.ControlNoMassLeptonOF(), cuts.Central()), "", "m_{ll} (GeV)")
    met_of_central = tree.getTH1F(4, "met_of_central", "met_pt"        , 20, 20, 250, cuts.Add(cuts.ControlNoMassLeptonOF(), cuts.Central()), "", "E_{T}^{miss} (GeV)")

   
    rsfof_mll_central = make_rsfof(mll_sf_central, mll_of_central)
    plot_rsfof_mll_central = Canvas("plot_rsfof_mll_central", "png,pdf", 0.6, 0.6, 0.8, 0.8)
    plot_rsfof_mll_central.addHisto(rsfof_mll_central, "PEZ1", "OF", "L", r.kBlack, 1, 0)
    plot_rsfof_mll_central.save(0, 0, 0, 4.0)
    
    rsfof_met_central = make_rsfof(met_sf_central, met_of_central)
    plot_rsfof_met_central = Canvas("plot_rsfof_met_central", "png,pdf", 0.6, 0.6, 0.8, 0.8)
    plot_rsfof_met_central.addHisto(rsfof_met_central, "PEZ1", "OF", "L", r.kBlack, 0 ,1)
    plot_rsfof_met_central.save(0, 0, 0, 4.0)
    
    ## mll_sf_forward = tree.getTH1F(4, "mll_sf_forward", "t.lepsMll_Edge", 20, 20, 250, cuts.Add(cuts.ControlNoMassLeptonSF(), cuts.Forward()), "", "m_{ll} (GeV)")
    ## met_sf_forward = tree.getTH1F(4, "met_sf_forward", "met_pt"        , 20, 20, 250, cuts.Add(cuts.ControlNoMassLeptonSF(), cuts.Forward()), "", "E_{T}^{miss} (GeV)")
    ## mll_of_forward = tree.getTH1F(4, "mll_of_forward", "t.lepsMll_Edge", 20, 20, 250, cuts.Add(cuts.ControlNoMassLeptonOF(), cuts.Forward()), "", "m_{ll} (GeV)")
    ## met_of_forward = tree.getTH1F(4, "met_of_forward", "met_pt"        , 20, 20, 250, cuts.Add(cuts.ControlNoMassLeptonOF(), cuts.Forward()), "", "E_{T}^{miss} (GeV)")
    ## 

    ## rsfof_mll_forward = make_rsfof(mll_sf_forward, mll_of_forward)
    ## plot_rsfof_mll_forward = Canvas("plot_rsfof_mll_forward", "png", 0.6, 0.6, 0.8, 0.8)
    ## plot_rsfof_mll_forward.addHisto(rsfof_mll_forward, "E1,SAME", "OF", "L", r.kBlack)
    ## plot_rsfof_mll_forward.save(0, 0, 0, 4.0)
    ## 
    ## rsfof_met_forward = make_rsfof(met_sf_forward, met_of_forward)
    ## plot_rsfof_met_forward = Canvas("plot_rsfof_met_forward", "png", 0.6, 0.6, 0.8, 0.8)
    ## plot_rsfof_met_forward.addHisto(rsfof_met_forward, "E1,SAME", "OF", "L", r.kBlack)
    ## plot_rsfof_met_forward.save(0, 0, 0, 4.0)
    




