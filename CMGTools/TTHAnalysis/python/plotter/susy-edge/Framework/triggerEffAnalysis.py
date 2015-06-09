############################################################
############################################################
##          _          _            _              _      ##
##         /\ \       /\ \         /\ \           /\ \    ##
##        /  \ \     /  \ \____   /  \ \         /  \ \   ##
##       / /\ \ \   / /\ \_____\ / /\ \_\       / /\ \ \  ##
##      / / /\ \_\ / / /\/___  // / /\/_/      / / /\ \_\ ##
##     / /_/_ \/_// / /   / / // / / ______   / /_/_ \/_/ ##
##    / /____/\  / / /   / / // / / /\_____\ / /____/\    ##
##   / /\____\/ / / /   / / // / /  \/____ // /\____\/    ##
##  / / /______ \ \ \__/ / // / /_____/ / // / /______    ##
## / / /_______\ \ \___\/ // / /______\/ // / /_______\   ##
## \/__________/  \/_____/ \/___________/ \/__________/   ##
############################################################
############################################################
                                                       

import ROOT as r
import math as math

from optparse import OptionParser
from ROOT import gROOT, TCanvas, TFile, TF1, TGraphAsymmErrors
from Sample import Sample, Block, Tree
from CutManager import CutManager
from Canvas import Canvas


def getTriggerEffs(tree, cut, addCut, var, varname, binning, lumi):


    passHisto = tree.getTH1F(lumi, "passHisto", var, binning[0], binning[1], binning[2], cut[:-1]+'&&'+addCut+')', '', varname)
    allHisto  = tree.getTH1F(lumi, "allHisto",  var, binning[0], binning[1], binning[2], cut                     , '', varname)

    for i in range(1,passHisto.GetNbinsX()+1):
        print 'at variable %s events passing/total %.2f  of  %.2f' %(varname, passHisto.GetBinContent(i), allHisto.GetBinContent(i) )

    ratio = passHisto.Clone("eff_" + passHisto.GetName())
    ratio.Divide(allHisto)
    ratio.GetYaxis().SetTitle("trigger eff.")

    errs = TGraphAsymmErrors(passHisto, allHisto, 'a')

    return errs


if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options] FilenameWithSamples", version="%prog 1.0")
    parser.add_option("-m", "--mode", action="store", dest="mode", default="rsfof", help="Operation mode")
    (options, args) = parser.parse_args()

    if len(args) != 1:
      parser.error("wrong number of arguments")

    inputFileName = args[0]
    tree = Tree(inputFileName, "MC", 0)
   
    gROOT.ProcessLine('.L tdrstyle.C')
    ## gROOT.SetBatch(1)
    r.setTDRStyle() 
    cuts = CutManager()

    ht_ht = getTriggerEffs(tree, cuts.AddList([cuts.GoodLeptonmm(),cuts.Central()])                  , 'HLT_HT900 > 0', 't.htJet35j_Edge', 'H_{T} (GeV)', [20, 400, 1200], 4.)
   
    plot_ht_ht = Canvas("plot_eff_ht_ht", "png", 0.6, 0.6, 0.8, 0.8)
    ht_ht.GetHistogram().Draw()
    ht_ht.Draw('apz')
    plot_ht_ht.save(0, 0, 0, 4.0)
    

    ## mm_ht   = getTriggerEffs(tree, cuts.AddList([cuts.GoodLeptonmm(),cuts.Central(),'HLT_HT900 > 0']), 'HLT_DoubleMu', 't.htJet35j_Edge' , 'H_{T} (GeV)', [20, 800, 1200], 4.)
    ## mm_mll  = getTriggerEffs(tree, cuts.AddList([cuts.GoodLeptonmm(),cuts.Central(),'HLT_HT900 > 0', 't.htJet35j_Edge > 850']), 'HLT_DoubleMu', 't.lepsMll_Edge'  , 'm_{ll} (GeV)'       , [20, 0, 200], 4.)
    ## mm_l1pt = getTriggerEffs(tree, cuts.AddList([cuts.GoodLeptonmm(),cuts.Central(),'HLT_HT900 > 0', 't.htJet35j_Edge > 850']), 'HLT_DoubleMu', 't.Lep_Edge_pt[0]', 'p_{T}^{lead} (GeV)' , [20, 0, 100], 4.)
    ## mm_l2pt = getTriggerEffs(tree, cuts.AddList([cuts.GoodLeptonmm(),cuts.Central(),'HLT_HT900 > 0', 't.htJet35j_Edge > 850']), 'HLT_DoubleMu', 't.Lep_Edge_pt[1]', 'p_{T}^{trail} (GeV)', [20, 0, 100], 4.)

    ## 
    ## plot_mm_mll = Canvas("plot_eff_mm_mll", "png", 0.6, 0.6, 0.8, 0.8)
    ## mm_mll.GetHistogram().Draw()
    ## mm_mll.Draw('apz')
    ## plot_mm_mll.save(0, 0, 0, 4.0)

    ## plot_mm_l1pt = Canvas("plot_eff_mm_l1pt", "png", 0.6, 0.6, 0.8, 0.8)
    ## mm_l1pt.GetHistogram().Draw()
    ## mm_l1pt.Draw('apz')
    ## plot_mm_l1pt.save(0, 0, 0, 4.0)

    ## plot_mm_l2pt = Canvas("plot_eff_mm_l2pt", "png", 0.6, 0.6, 0.8, 0.8)
    ## mm_l2pt.GetHistogram().Draw()
    ## mm_l2pt.Draw('apz')
    ## plot_mm_l2pt.save(0, 0, 0, 4.0)


