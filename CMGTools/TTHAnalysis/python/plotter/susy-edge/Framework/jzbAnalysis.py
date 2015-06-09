import ROOT as r
import math as math

from optparse import OptionParser
from ROOT import gROOT, TCanvas, TFile, TF1, TH1F
from Sample import Sample, Block, Tree
from CutManager import CutManager
from Canvas import Canvas


def make_jzbDependencies(histo2d, xvar):

    print '==========================================================='
    print '===== at variable %s ====================================' %(xvar)
    print '==========================================================='

    slicedhistos = []
    means = []
    meanes = []
    bin_div = 1
    if xvar == 'met':
        bin_div = 1
    elif xvar == 'zpt':
        bin_div = 2
    i = 1

    while i+bin_div <= histo2d.GetXaxis().GetNbins():
        tmp_histo = histo2d.ProjectionY('_py'+str(i), i, i+bin_div-1, 'e')
        tmp_histo.Sumw2()
        tmp_histo.Fit('gaus')#,'','', -15., 15)
        ff = tmp_histo.GetFunction('gaus')

        if ff:
            means .append(ff.GetParameter(1))
            meanes.append(ff.GetParError(1))
        else:
            print '==========================================='
            print 'ATTENTION FIT DID NOT CONVERGE OR SOMETHING'
            print '==========================================='
            means .append(0.)
            meanes.append(0.)

        slicedhistos.append(tmp_histo)
        i+= bin_div

    h = TH1F(histo2d.GetName(),histo2d.GetName(), len(means), histo2d.GetXaxis().GetXmin(), histo2d.GetXaxis().GetXmax())

    for mean in means:
        binidx = means.index(mean)
        h.SetBinContent(binidx+1, mean)
        h.SetBinError(binidx+1, meanes[binidx])

    return h



if __name__ == '__main__':

    parser = OptionParser(usage='usage: %prog [options] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-m', '--mode', action='store', dest='mode', default='rsfof', help='Operation mode')
    (options, args) = parser.parse_args()

    if len(args) != 1:
      parser.error('wrong number of arguments')

    inputFileName = args[0]
    tree = Tree(inputFileName, 'MC', 0)
   
    gROOT.ProcessLine('.L tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle() 
    cuts = CutManager()


    jzb_vs_nvx  = tree.getTH2F(4, 'jzb_vs_nvx', 't.lepsJZB_Edge:nVert'         , 10, 0,  30., 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'n_{vertices}', 'JZB')
    jzb_vs_zpt  = tree.getTH2F(4, 'jzb_vs_zpt', 't.lepsJZB_Edge:t.lepsZPt_Edge', 20, 0, 150., 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'p_{T}(Z)'    , 'JZB')
    jzb_vs_met  = tree.getTH2F(4, 'jzb_vs_met', 't.lepsJZB_Edge:met_pt'        ,  5, 0,  50., 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'MET'         , 'JZB')

   
    jzb_vs_nvx_proj = make_jzbDependencies(jzb_vs_nvx, 'nvx')
    plot_jzb_vs_nvx_proj = Canvas('plot_jzb_vs_nvx', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_jzb_vs_nvx_proj.addHisto(jzb_vs_nvx_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
    plot_jzb_vs_nvx_proj.save(0, 0, 0, 4.0)
    
    jzb_vs_zpt_proj = make_jzbDependencies(jzb_vs_zpt, 'zpt')
    plot_jzb_vs_zpt_proj = Canvas('plot_jzb_vs_zpt', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_jzb_vs_zpt_proj.addHisto(jzb_vs_zpt_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
    plot_jzb_vs_zpt_proj.save(0, 0, 0, 4.0)
    
    jzb_vs_met_proj = make_jzbDependencies(jzb_vs_met, 'met')
    plot_jzb_vs_met_proj = Canvas('plot_jzb_vs_met', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_jzb_vs_met_proj.addHisto(jzb_vs_met_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
    plot_jzb_vs_met_proj.save(0, 0, 0, 4.0)
    
    




