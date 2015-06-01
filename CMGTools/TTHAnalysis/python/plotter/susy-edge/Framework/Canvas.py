from ROOT import TCanvas, TLegend, TPad, TLine, TLatex
import ROOT as r

class Canvas:
   'Common base class for all Samples'

   def __init__(self, name, format, x1, y1, x2, y2):
      self.Name = name
      self.Format = format
      self.PlotName = name + "." + format
      self.myCanvas = TCanvas(name, name)
      self.histos = []
      self.options = []
      self.labels = []      
      self.labelsOption = []
      self.myLegend = TLegend(x1, y1, x2, y2)
      self.myLegend.SetFillColor(r.kWhite)
      self.myLegend.SetTextFont(42)
      self.myLegend.SetTextSize(0.028)
      self.myLegend.SetLineWidth(0)
      self.myLegend.SetBorderSize(0)


   def banner(self, isData, lumi):
    
      latex = TLatex()
      latex.SetNDC();
      latex.SetTextAngle(0);
      latex.SetTextColor(r.kBlack);
      latex.SetTextFont(42);
      latex.SetTextAlign(31);
      latex.SetTextSize(0.07);
      latex.DrawLatex(0.25, 0.93, "CMS")

      latexb = TLatex()
      latexb.SetNDC();
      latexb.SetTextAngle(0);
      latexb.SetTextColor(r.kBlack);
      latexb.SetTextFont(42);
      latexb.SetTextAlign(31);
      latexb.SetTextSize(0.05);
 
      if(isData):
        latexb.DrawLatex(0.45, 0.93, "Preliminary")
      else:
        latexb.DrawLatex(0.45, 0.93, "Simulation")

      text_lumi = str(lumi) + " fb^{-1} (13 TeV)"
      latexc = TLatex()
      latexc.SetNDC();
      latexc.SetTextAngle(0);
      latexc.SetTextColor(r.kBlack);
      latexc.SetTextFont(42);
      latexc.SetTextAlign(31);
      latexc.SetTextSize(0.05);
      latexc.DrawLatex(0.82, 0.93, text_lumi)

   def banner2(self, isData, lumi):
    
      latex = TLatex()
      latex.SetNDC();
      latex.SetTextAngle(0);
      latex.SetTextColor(r.kBlack);
      latex.SetTextFont(42);
      latex.SetTextAlign(31);
      latex.SetTextSize(0.06);
      latex.DrawLatex(0.25, 0.93, "CMS")

      latexb = TLatex()
      latexb.SetNDC();
      latexb.SetTextAngle(0);
      latexb.SetTextColor(r.kBlack);
      latexb.SetTextFont(42);
      latexb.SetTextAlign(31);
      latexb.SetTextSize(0.04);
 
      if(isData):
        latexb.DrawLatex(0.45, 0.93, "Preliminary")
      else:
        latexb.DrawLatex(0.45, 0.93, "Simulation")

      text_lumi = str(lumi) + " fb^{-1} (13 TeV)"
      latexc = TLatex()
      latexc.SetNDC();
      latexc.SetTextAngle(0);
      latexc.SetTextColor(r.kBlack);
      latexc.SetTextFont(42);
      latexc.SetTextAlign(31);
      latexc.SetTextSize(0.04);
      latexc.DrawLatex(0.82, 0.93, text_lumi)


 

   def addHisto(self, h, option, label, labelOption, color):
      h.SetLineColor(color)
      h.SetMarkerColor(color)
      self.histos.append(h)
      self.options.append(option)
      self.labels.append(label)
      self.labelsOption.append(labelOption)
      

   def saveRatio(self, legend, isData, log, lumi):

      self.myCanvas.cd()

      pad1 = TPad("pad1", "pad1", 0, 0.2, 1, 1.0)
      pad1.SetBottomMargin(0.1)
      pad1.Draw()
      pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.2)
      pad2.SetTopMargin(0.1);
      pad2.SetBottomMargin(0.3);
      pad2.Draw();

      pad1.cd()
      if(log):
        pad1.SetLogy(1)
      


      self.histos[0].Draw(self.options[0])
      self.myLegend.AddEntry(self.histos[0], self.labels[0], self.labelsOption[0])
      self.histos[1].Draw(self.options[1])
      self.myLegend.AddEntry(self.histos[1], self.labels[1], self.labelsOption[1])
      
      if(legend):
        self.myLegend.Draw()
       
      ratio = self.histos[0].Clone("ratio")
      ratio.Divide(self.histos[1])
      ratio.SetTitle("")
      ratio.GetYaxis().SetRangeUser(0, 2);
      ratio.GetYaxis().SetTitle("Ratio");
      ratio.GetYaxis().CenterTitle();
      ratio.GetYaxis().SetLabelSize(0.12);
      ratio.GetXaxis().SetLabelSize(0.12);
      ratio.GetYaxis().SetTitleOffset(0.3);
      ratio.GetYaxis().SetNdivisions(4);
      ratio.GetYaxis().SetTitleSize(0.12);
      ratio.GetXaxis().SetTitleSize(0.12);
      ratio.SetMarkerStyle(21);
      ratio.SetMarkerColor(r.kBlue);
      ratio.SetLineColor(r.kBlue);


      pad2.cd();  
      line = TLine(ratio.GetBinLowEdge(1), 1, ratio.GetBinLowEdge(ratio.GetNbinsX()+1), 1)
      line.SetLineColor(r.kRed);
      ratio.Draw();
      line.Draw();
      ratio.Draw("SAME");

      #r.CMS_lumi(self.myCanvas, 4, 10)
      pad1.cd()
      self.banner(isData, lumi)
      self.myCanvas.SaveAs(self.PlotName)



   def save(self, legend, isData, log, lumi):

      self.myCanvas.cd()
      
      if(log):
        self.myCanvas.GetPad(0).SetLogy(1)

      for i in range(0, len(self.histos)):
        self.histos[i].Draw(self.options[i])
        self.myLegend.AddEntry(self.histos[i], self.labels[i], self.labelsOption[i])

      if(legend):
        self.myLegend.Draw()

      self.banner2(isData, lumi)
      self.myCanvas.SaveAs(self.PlotName)





