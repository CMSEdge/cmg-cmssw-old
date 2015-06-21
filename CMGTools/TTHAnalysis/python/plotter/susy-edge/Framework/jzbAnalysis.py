import ROOT as r
import math as math

from optparse import OptionParser
from ROOT import gROOT, TCanvas, TFile, TF1, TH1F, TLine
from Sample import Sample, Block, Tree
from CutManager import CutManager
from Canvas import Canvas


def make_jzbDependencies(histo2d, xvar, opt = 'dep'):

    print '==========================================================='
    print '===== at variable %s ====================================' %(xvar)
    print '==========================================================='

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
        if opt == 'dep':
            fit_tf1 = r.TF1('mygaus','gaus(0)')
            fit_tf1.SetParameter(1, tmp_histo.GetMean())
            fit_tf1.SetParameter(2, 10.)
            tmp_histo.Fit('mygaus')#,'','', -15., 15)
            tmp_histo.Draw()
            c.SaveAs('plots/controlHistos/'+tmp_histo.GetName()+'.png')
            ff = tmp_histo.GetFunction('mygaus')

            if ff and ff.GetNDF() and ff.GetChisquare()/ff.GetNDF() < 2.5:
                means .append(ff.GetParameter(1))
                meanes.append(ff.GetParError(1))
            else:
                print '==========================================='
                print 'ATTENTION FIT DID NOT CONVERGE OR SOMETHING'
                print '==========================================='
                means .append(tmp_histo.GetMean())
                meanes.append(tmp_histo.GetRMS())

        elif opt == 'response':
            means.append(tmp_histo.GetMean())
            meanes.append(tmp_histo.GetRMS())

        i+= bin_div

        del tmp_histo

    h = TH1F(histo2d.GetName(),histo2d.GetName(), len(means), histo2d.GetXaxis().GetXmin(), histo2d.GetXaxis().GetXmax())
    h.GetXaxis().SetTitle(histo2d.GetXaxis().GetTitle())
    
    for mean in means:
        idx = means.index(mean)
        h.SetBinContent(idx+1, mean)
        h.SetBinError(idx+1, meanes[idx])
    if opt == 'response':
        h.Fit('pol1', '', '', 100., 400.)

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
    r.gStyle.SetStatX(0.7)
    r.gStyle.SetStatY(0.85)
    r.gStyle.SetStatH(0.1)
    r.gStyle.SetStatW(0.2)
    cuts = CutManager()

    nvxSlope = 0.
    for var in ['nvx']:#, 'met', 'mll', 'zpt']:

        if   var == 'nvx':
            varTree = 't.lepsJZB_Edge:nVert'
            varName = 'n_{vertices}'
            varBins = [ 5, 10.,  20.]

        elif var == 'mll':
            varTree = 't.lepsJZB_Edge:t.lepsMll_Edge'
            varName = 'm_{ll}'
            varBins = [20, 80., 100.]

        elif var == 'zpt':
            varTree = 't.lepsJZB_Edge:t.lepsZPt_Edge'
            varName = 'm_{ll}'
            varBins = [15,  0., 150.]

        elif var == 'nj':
            varTree = 't.lepsJZB_Edge:t.nJetSel_Edge'
            varName = 'm_{ll}'
            varBins = [10,  0.,  10.]

        jzb_dep  = tree.getTH2F(4, 'jzb_vs_'+var, varTree, varBins[0], varBins[1],  varBins[2], 20, -100., 100., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', varName, 'JZB')
        jzb_dep_proj = make_jzbDependencies(jzb_dep, var)
        jzb_dep_proj.GetYaxis().SetRangeUser(-5., 10.)
        if   var == 'nvx':
            jzb_dep_proj.Fit('pol1', '')
            nvxSlope = jzb_dep_proj.GetFunction('pol1').GetParameter(1)
        plot_jzb_dep_proj = Canvas('plot_jzb_vs_'+var, 'png,pdf', 0.6, 0.6, 0.8, 0.8)
        plot_jzb_dep_proj.addHisto(jzb_dep_proj, 'E1', 'OF', 'L', r.kBlack, 1, 0)
        plot_jzb_dep_proj.addLine(jzb_dep_proj.GetXaxis().GetXmin(), 0., jzb_dep_proj.GetXaxis().GetXmax(),0., 3)
        plot_jzb_dep_proj.save(0, 0, 0, 4.0)

        del plot_jzb_dep_proj, jzb_dep, jzb_dep_proj
    
    r.gStyle.SetPalette(53)
    r.gStyle.SetNumberContours( 999 )


    # response correction
    response_histo  = tree.getTH2F(4, 'response_vs_zpt', 't.lepsMETRec_Edge/t.lepsZPt_Edge:t.lepsZPt_Edge', 100, 0.,  600., 100, 0., 10., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'p_{T} (Z)', 'MET recoil')
    response_proj = make_jzbDependencies(response_histo, 'zpt', 'response')
    plot_response = Canvas('response', 'png,pdf', 0.6, 0.6, 0.8, 0.8)
    plot_response.addHisto(response_histo, 'colz', 'OF', 'L', r.kBlack, 1, 0)
    plot_response.addHisto(response_proj , 'e1 sames', 'OF', 'L', r.kGray, 1, 0)
    plot_response.save(0, 0, 0, 4.0)
    
    responseCorr = response_proj.GetFunction('pol1').GetParameter(0)

    print 'slope fo nVx: %.3f , response: %.3f' %(nvxSlope, responseCorr)

    rawJZB = 't.lepsJZB_Edge'
    resCor = '(t.lepsZPt_Edge*(1-'+str(responseCorr)+'))'
    nvxCor = '(nVert*'+str(nvxSlope)+')'
    corJZB = rawJZB+'+'+resCor+'-'+nvxCor
    resJZB = rawJZB+'+'+resCor
    nvxJZB = rawJZB+'+'+nvxCor

    jzb_devel_before = tree.getTH1F(4, 'jzb_devel_before', rawJZB, 40, -60., 60., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'JZB')
    jzb_devel_after  = tree.getTH1F(4, 'jzb_devel_after' , corJZB, 40, -60., 60., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'JZB')
    jzb_devel_resCor = tree.getTH1F(4, 'jzb_devel_resCor', resJZB, 40, -60., 60., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'JZB')
    jzb_devel_nvxCor = tree.getTH1F(4, 'jzb_devel_nvxCor', nvxJZB, 40, -60., 60., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'JZB')

    jzb_devel_after.Fit('gaus','0')
    mu = jzb_devel_after.GetFunction('gaus').GetParameter(1)
    print 'residual correction', mu
    
    jzb_devel_corrected  = tree.getTH1F(4, 'jzb_devel_corrected' , corJZB+'-'+str(mu), 40, -60., 60., cuts.Add(cuts.DYControlNoMassLeptonSF(), cuts.Central()), '', 'JZB')

    plot_jzb_devel = Canvas('plot_jzb_devel', 'png,pdf', 0.4, 0.2, 0.7, 0.4)
    plot_jzb_devel.addHisto(jzb_devel_before    , 'e1'       , 'uncor.'        , 'PEL' , r.kBlack , 1 , 0)
    plot_jzb_devel.addHisto(jzb_devel_resCor    , 'e1 same'  , 'response cor.' , 'PEL' , r.kGray  , 1 , 1)
    plot_jzb_devel.addHisto(jzb_devel_nvxCor    , 'e1 same'  , 'nvx cor.'      , 'PEL' , r.kGreen , 1 , 2)
    plot_jzb_devel.addHisto(jzb_devel_after     , 'e1 same'  , 'resnvx cor.'   , 'PEL' , r.kBlue  , 1 , 3)
    plot_jzb_devel.addHisto(jzb_devel_corrected , 'e1 sames' , 'full cor'      , 'PEL' , r.kRed   , 1 , 4)
   
    plot_jzb_devel.save(1, 0, 0, 4.0)
