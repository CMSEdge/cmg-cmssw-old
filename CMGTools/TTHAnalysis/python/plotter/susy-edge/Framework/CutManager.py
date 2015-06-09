

class CutManager:
   'This class serves as an on-demand cut server'

   def __init__(self):

      self.twoLeptons = "t.nPairLep_Edge > 0"
      self.leptonPt = "t.Lep_Edge_pt[0] > 25. && t.Lep_Edge_pt[1] > 20."
      self.leptonDR = "t.lepsDR_Edge > 0.3"       
      self.ECALCrack = "abs(abs(Lep_Edge_eta[0]) - 1.5) > 0.1 && abs(abs(Lep_Edge_eta[1]) - 1.5) > 0.1"
      self.leptonsMll = "t.lepsMll_Edge > 20"
      ## self.leptonEta = "abs(LepGood_eta[0]) < 2.4 && abs(LepGood_eta[1]) < 2.4"
      ## self.leptonID = "LepGood_tightId[0] > 0 && LepGood_tightId[1] > 0"
      ## self.goodLepton = self.twoLeptons + " && " + self.leptonPt + " && " + self.leptonEta + " && " + self.ECALCrack  + " && " + self.leptonDR + " && " + self.leptonID
      self.goodLepton = self.twoLeptons + "&&" + self.leptonPt + "&&" + self.leptonDR + "&&" + self.ECALCrack + "&&" + self.leptonsMll
      self.ee = "Lep_Edge_pdgId[0] * Lep_Edge_pdgId[1] == -121"
      self.mm = "Lep_Edge_pdgId[0] * Lep_Edge_pdgId[1] == -169"
      self.OF = "Lep_Edge_pdgId[0] * Lep_Edge_pdgId[1] == -143"
      self.SF = "(" + self.ee + " || " +  self.mm + ")"
      self.METJetsSignalRegion = "((met_pt > 150 && t.nJetSel_Edge > 1) || (met_pt > 100 && t.nJetSel_Edge > 2))"
      self.METJetsControlRegion = "(met_pt > 100 && met_pt < 150 && t.nJetSel_Edge == 2)"
      self.DYControlRegion = "(met_pt < 50 && t.nJetSel_Edge == 2)"
      self.lowmass = "t.lepsMll_Edge > 20 && t.lepsMll_Edge < 70"
      self.Zmass = "t.lepsMll_Edge > 81 && t.lepsMll_Edge < 101"
      self.highmass = "t.lepsMll_Edge > 120"
      self.central = "(abs(t.Lep_Edge_eta[0])<1.4 && abs(t.Lep_Edge_eta[1])<1.4)"
      self.forward = "(abs(t.Lep_Edge_eta[0])>1.4 || abs(t.Lep_Edge_eta[1])>1.4)"


   def AddList(self, cutlist):
      returncut = ''
      for cut in cutlist:
          returncut += cut
          if not cutlist.index(cut) == len(cutlist):
            returncut += ' && '
      return returncut
  
   def Add(self, cut1, cut2):

      return cut1 + " && " + cut2  
  
   def Central(self):
      
      return self.central
 
   def Forward(self):
      
      return self.forward
 
   def GoodLeptonSF(self):

      return self.goodLepton + " && " + self.SF

   def GoodLeptonOF(self):

      return self.goodLepton + " && " + self.OF

   def GoodLeptonee(self):

      return self.goodLepton + " && " + self.ee

   def GoodLeptonmm(self):

      return self.goodLepton + " && " + self.mm

   def SignalNoMassLeptonSF(self):

      return self.GoodLeptonSF() + " && " + self.METJetsSignalRegion
   
   def SignalNoMassLeptonOF(self):

      return self.GoodLeptonOF() + " && " + self.METJetsSignalRegion
   
   def SignalNoMassLeptonee(self):

      return self.GoodLeptonee() + " && " + self.METJetsSignalRegion

   def SignalNoMassLeptonmm(self):

      return self.GoodLeptonmm() + " && " + self.METJetsSignalRegion

   def ControlNoMassLeptonSF(self):

      return self.GoodLeptonSF() + " && " + self.METJetsControlRegion
   
   def ControlNoMassLeptonOF(self):

      return self.GoodLeptonOF() + " && " + self.METJetsControlRegion
   
   def ControlNoMassLeptonee(self):

      return self.GoodLeptonee() + " && " + self.METJetsControlRegion

   def ControlNoMassLeptonmm(self):

      return self.GoodLeptonmm() + " && " + self.METJetsControlRegion

   def DYControlNoMassLeptonSF(self):

      return self.GoodLeptonSF() + " && " + self.DYControlRegion
   
   def DYControlNoMassLeptonOF(self):

      return self.GoodLeptonOF() + " && " + self.DYControlRegion
   
   def DYControlNoMassLeptonee(self):

      return self.GoodLeptonee() + " && " + self.DYControlRegion

   def DYControlNoMassLeptonmm(self):

      return self.GoodLeptonmm() + " && " + self.DYControlRegion

   def SignalLowMassSF(self):

      return self.SignalNoMassLeptonSF() + " && " + self.lowmass
   
   def SignalLowMassOF(self):

      return self.SignalNoMassLeptonOF() + " && " + self.lowmass
   
   def SignalLowMassee(self):

      return self.SignalNoMassLeptonee() + " && " + self.lowmass
   
   def SignalLowMassmm(self):

      return self.SignalNoMassLeptonmm() + " && " + self.lowmass

   def SignalZMassSF(self):

      return self.SignalZMassLeptonSF() + " && " + self.Zmass
   
   def SignalZMassOF(self):

      return self.SignalZMassLeptonOF() + " && " + self.Zmass
   
   def SignalZMassee(self):

      return self.SignalZMassLeptonee() + " && " + self.Zmass
   
   def SignalZMassmm(self):

      return self.SignalNoMassLeptonmm() + " && " + self.Zmass

   def SignalHighMassSF(self):

      return self.SignalNoMassLeptonSF() + " && " + self.highmass
   
   def SignalHighMassOF(self):

      return self.SignalNoMassLeptonOF() + " && " + self.highmass
   
   def SignalHighMassee(self):

      return self.SignalNoMassLeptonee() + " && " + self.highmass
 
   def ControlLowMassSF(self):

      return self.ControlNoMassLeptonSF() + " && " + self.lowmass
   
   def ControlLowMassOF(self):

      return self.ControlNoMassLeptonOF() + " && " + self.lowmass
   
   def ControlLowMassee(self):

      return self.ControlNoMassLeptonee() + " && " + self.lowmass
   
   def ControlLowMassmm(self):

      return self.ControlNoMassLeptonmm() + " && " + self.lowmass

   def ControlZMassSF(self):

      return self.ControlZMassLeptonSF() + " && " + self.Zmass
   
   def ControlZMassOF(self):

      return self.ControlZMassLeptonOF() + " && " + self.Zmass
   
   def ControlZMassee(self):

      return self.ControlZMassLeptonee() + " && " + self.Zmass
   
   def ControlZMassmm(self):

      return self.ControlNoMassLeptonmm() + " && " + self.Zmass

   def ControlHighMassSF(self):

      return self.ControlNoMassLeptonSF() + " && " + self.highmass
   
   def ControlHighMassOF(self):

      return self.ControlNoMassLeptonOF() + " && " + self.highmass
   
   def ControlHighMassee(self):

      return self.ControlNoMassLeptonee() + " && " + self.highmass
   
   










