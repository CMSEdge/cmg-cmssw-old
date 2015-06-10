import ROOT as r
import math as math

from optparse import OptionParser
from ROOT import gROOT, TCanvas, TFile, TF1, TH1F, TLine
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
        bin_div = 1
    elif xvar == 'nvx':
        bin_div = 1
    i = 1

    c = TCanvas()
    c.cd()
    while i+bin_div-1 <= histo2d.GetXaxis().GetNbins():
        tmp_histo = histo2d.ProjectionY(histo2d.GetName()+'_py'+str(i), i, i+bin_div-1, 'e')
        tmp_histo.Sumw2()
        tmp_histo.Fit('gaus')#,'','', -15., 15)
        tmp_histo.Draw()
        c.SaveAs('plots/controlHistos/'+tmp_histo.GetName()+'.png')
        ff = tmp_histo.GetFunction('gaus')

        if ff and ff.GetNDF() and ff.GetChisquare()/ff.GetNDF() < 2:
            means .append(ff.GetParameter(1))
            meanes.append(ff.GetParError(1))
        else:
            print '==========================================='
            print 'ATTENTION FIT DID NOT CONVERGE OR SOMETHING'
            print '==========================================='
            means .append(tmp_histo.GetMean())
            meanes.append(tmp_histo.GetRMS())

        slicedhistos.append(tmp_histo)
        i+= bin_div

    h = TH1F(histo2d.GetName(),histo2d.GetName(), len(means), histo2d.GetXaxis().GetXmin(), histo2d.GetXaxis().GetXmax())
    h.GetXaxis().SetTitle(histo2d.GetXaxis().GetTitle())

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


    jzb_vs_nvx  = tree.getTH2F(4, 'jzb_vs_nvx', 't.lepsJZB_Edge:nVert'         , 10, 0.,  30., 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'n_{vertices}', 'JZB')
    jzb_vs_met  = tree.getTH2F(4, 'jzb_vs_met', 't.lepsJZB_Edge:met_pt'        ,  5, 0.,  50., 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'MET'         , 'JZB')
    jzb_vs_mll  = tree.getTH2F(4, 'jzb_vs_mll', 't.lepsJZB_Edge:t.lepsMll_Edge', 20,80., 100., 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'm_{ll}'      , 'JZB')
    jzb_vs_spt  = tree.getTH2F(4, 'jzb_vs_spt', 't.lepsJZB_Edge:(t.Lep_Edge_pt[0]+t.Lep_Edge_pt[1])' ,  20, 0, 200., 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'sum lepton pT'         , 'JZB')

    jzb_vs_zpt  = tree.getTH2F(4, 'jzb_vs_zpt', 't.lepsJZB_Edge:t.lepsZPt_Edge', 15, 0., 150., 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'p_{T}(Z)'    , 'JZB')
    jzb_vs_zpt_mm  = tree.getTH2F(4, 'jzb_vs_zpt_mm', 't.lepsJZB_Edge:t.lepsZPt_Edge', 15, 0., 150., 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonmm(), cuts.Central()), '', 'p_{T}(Z) (#mu#mu)'    , 'JZB')
    jzb_vs_zpt_ee  = tree.getTH2F(4, 'jzb_vs_zpt_ee', 't.lepsJZB_Edge:t.lepsZPt_Edge', 15, 0., 150., 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonee(), cuts.Central()), '', 'p_{T}(Z) (ee)'    , 'JZB')

   
    jzb_vs_nvx_proj = make_jzbDependencies(jzb_vs_nvx, 'nvx')
    plot_jzb_vs_nvx_proj = Canvas('plot_jzb_vs_nvx', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_jzb_vs_nvx_proj.addHisto(jzb_vs_nvx_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
    plot_jzb_vs_nvx_proj.addLine(jzb_vs_nvx_proj.GetXaxis().GetXmin(), 0., jzb_vs_nvx_proj.GetXaxis().GetXmax(),0., 3)
    plot_jzb_vs_nvx_proj.save(0, 0, 0, 4.0)
    
    jzb_vs_zpt_proj = make_jzbDependencies(jzb_vs_zpt, 'zpt')
    plot_jzb_vs_zpt_proj = Canvas('plot_jzb_vs_zpt', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_jzb_vs_zpt_proj.addHisto(jzb_vs_zpt_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
    plot_jzb_vs_zpt_proj.addLine(jzb_vs_zpt_proj.GetXaxis().GetXmin(), 0., jzb_vs_zpt_proj.GetXaxis().GetXmax(),0., 3)
    plot_jzb_vs_zpt_proj.save(0, 0, 0, 4.0)
    
    jzb_vs_zpt_mm_proj = make_jzbDependencies(jzb_vs_zpt_mm, 'zpt_mm')
    plot_jzb_vs_zpt_mm_proj = Canvas('plot_jzb_vs_zpt_mm', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_jzb_vs_zpt_mm_proj.addHisto(jzb_vs_zpt_mm_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
    plot_jzb_vs_zpt_mm_proj.addLine(jzb_vs_zpt_mm_proj.GetXaxis().GetXmin(), 0., jzb_vs_zpt_mm_proj.GetXaxis().GetXmax(),0., 3)
    plot_jzb_vs_zpt_mm_proj.save(0, 0, 0, 4.0)
    
    jzb_vs_zpt_ee_proj = make_jzbDependencies(jzb_vs_zpt_ee, 'zpt_ee')
    plot_jzb_vs_zpt_ee_proj = Canvas('plot_jzb_vs_zpt_ee', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_jzb_vs_zpt_ee_proj.addHisto(jzb_vs_zpt_ee_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
    plot_jzb_vs_zpt_ee_proj.addLine(jzb_vs_zpt_ee_proj.GetXaxis().GetXmin(), 0., jzb_vs_zpt_ee_proj.GetXaxis().GetXmax(),0., 3)
    plot_jzb_vs_zpt_ee_proj.save(0, 0, 0, 4.0)
    
    jzb_vs_met_proj = make_jzbDependencies(jzb_vs_met, 'met')
    plot_jzb_vs_met_proj = Canvas('plot_jzb_vs_met', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_jzb_vs_met_proj.addHisto(jzb_vs_met_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
    plot_jzb_vs_met_proj.addLine(jzb_vs_met_proj.GetXaxis().GetXmin(), 0., jzb_vs_met_proj.GetXaxis().GetXmax(),0., 3)
    plot_jzb_vs_met_proj.save(0, 0, 0, 4.0)
    
    jzb_vs_mll_proj = make_jzbDependencies(jzb_vs_mll, 'mll')
    plot_jzb_vs_mll_proj = Canvas('plot_jzb_vs_mll', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_jzb_vs_mll_proj.addHisto(jzb_vs_mll_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
    plot_jzb_vs_mll_proj.addLine(jzb_vs_mll_proj.GetXaxis().GetXmin(), 0., jzb_vs_mll_proj.GetXaxis().GetXmax(),0., 3)
    plot_jzb_vs_mll_proj.save(0, 0, 0, 4.0)
    
    jzb_vs_spt_proj = make_jzbDependencies(jzb_vs_spt, 'spt')
    plot_jzb_vs_spt_proj = Canvas('plot_jzb_vs_spt', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_jzb_vs_spt_proj.addHisto(jzb_vs_spt_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
    plot_jzb_vs_spt_proj.addLine(jzb_vs_spt_proj.GetXaxis().GetXmin(), 0., jzb_vs_spt_proj.GetXaxis().GetXmax(),0., 3)
    plot_jzb_vs_spt_proj.save(0, 0, 0, 4.0)
    
    

