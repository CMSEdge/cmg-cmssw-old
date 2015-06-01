from ROOT import TTree, TFile, TCut, TH1F


class Sample:
   'Common base class for all Samples'

   def __init__(self, name, location, xsection, isdata):
      self.Name = name
      self.Location = location
      self.XSection = xsection
      self.IsData = isdata
      self.tfile = TFile(self.Location)
      self.ttree = self.tfile.Get("tree")
      self.lumWeight = 1.0
      if(self.IsData == 0):
        self.lumWeight = self.XSection / self.ttree.GetEntries()

   def printSample(self):
      print "#################################"
      print "Sample Name: ", self.Name
      print "Sample Location: ", self.Location
      print "Sample XSection: ", self.XSection
      print "Sample IsData: ", self.IsData
      print "Sample LumWeight: ", self.lumWeight
      print "#################################"


   def getTH1F(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel):
 
      h = TH1F(name, "", nbin, xmin, xmax)
      h.Sumw2()
      h.GetXaxis().SetTitle(xlabel)
      b = int((xmax-xmin)/nbin)
      ylabel = "Events / " + str(b) + " GeV"
      h.GetYaxis().SetTitle(ylabel)
      
      if(self.IsData == 0):
        cut = cut + "* ( " + str(self.lumWeight*lumi) + " )" 
      
      self.ttree.Project(name, var, cut, options) 
      return h


class Block:
   'Common base class for all Sample Blocks'

   def __init__(self, name, color, isdata):
      self.Name  = name
      self.Color = color
      self.IsData = isdata
      self.samples = []

   def printBlock(self):

      print "####################"
      print "Block Name: ", self.Name
      print "Block Color: ", self.Color
      print "Block IsData: ", self.IsData
      print "####################"
      print "This block contains the following Samples"

      for l in self.samples:
        l.printSample()
     

   def addSample(self, s):
      self.samples.append(s)

   def getTH1F(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel):

     h = TH1F(name, "", nbin, xmin, xmax)
     h.Sumw2()
     h.GetXaxis().SetTitle(xlabel)
     b = int((xmax-xmin)/nbin)
     ylabel = "Events / " + str(b) + " GeV"
     h.GetYaxis().SetTitle(ylabel)

     for s in self.samples:
       AuxName = "aux_sample" + s.Name
       haux = s.getTH1F(lumi, AuxName, var, nbin, xmin, xmax, cut, options, xlabel)
       h.Add(haux)
       del haux

     return h
       

class Tree:
   'Common base class for a physics meaningful tree'

   def __init__(self, name, isdata):
      self.Name  = name
      self.IsData = isdata
      self.blocks = []

   def printTree(self):

      print "######"
      print "Tree Name: ", self.Name
      print "Tree IsData: ", self.IsData
      print "######"
      print "This Tree contains the following Blocks"

      for l in self.blocks:
        l.printBlock()
     

   def addBlock(self, b):
      self.blocks.append(b)


   def getTH1F(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel):
   
     h = TH1F(name, "", nbin, xmin, xmax)
     h.Sumw2()
     h.GetXaxis().SetTitle(xlabel)
     b = int((xmax-xmin)/nbin)
     ylabel = "Events / " + str(b) + " GeV"
     h.GetYaxis().SetTitle(ylabel)
     
     for b in self.blocks:
     
       AuxName = "aux_block" + b.Name
       haux = b.getTH1F(lumi, AuxName, var, nbin, xmin, xmax, cut, options, xlabel)
       h.Add(haux)
       del haux

     return h   










