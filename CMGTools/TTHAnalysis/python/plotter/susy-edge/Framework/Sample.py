import ROOT as r

from ROOT import TTree, TFile, TCut, TH1F


class Sample:
   'Common base class for all Samples'

   def __init__(self, name, location, friendlocation, xsection, isdata):
      self.name = name
      self.location = location
      self.xSection = xsection
      self.isData = isdata
      self.tfile = TFile(self.location+self.name+'/treeProducerSusyEdge/tree.root')
      self.ftfile = TFile(self.location+'/'+friendlocation+'/evVarFriend_'+self.name+'.root')
      self.ttree = self.tfile.Get('tree')
      self.ttree.AddFriend('sf/t',self.ftfile)
      self.count = self.tfile.Get('Count')
      self.lumWeight = 1.0
      if(self.isData == 0):
        self.lumWeight = self.xSection / self.count.GetEntries()

   def printSample(self):
      print "#################################"
      print "Sample Name: ", self.name
      print "Sample Location: ", self.location
      print "Sample XSection: ", self.xSection
      print "Sample IsData: ", self.isData
      print "Sample LumWeight: ", self.lumWeight
      print "#################################"


   def getTH1F(self, lumi, name, var, nbin, xmin, xmax, cut, options, xlabel):
 
      h = TH1F(name, "", nbin, xmin, xmax)
      h.Sumw2()
      h.GetXaxis().SetTitle(xlabel)
      b = int((xmax-xmin)/nbin)
      ylabel = "Events / " + str(b) + " GeV"
      h.GetYaxis().SetTitle(ylabel)
      
      if(self.isData == 0):
        cut = cut + "* ( " + str(self.lumWeight*lumi) + " )" 
      
      self.ttree.Project(name, var, cut, options) 
      return h


class Block:
   'Common base class for all Sample Blocks'

   def __init__(self, name, color, isdata):
      self.name  = name
      self.color = color
      self.isData = isdata
      self.samples = []

   def printBlock(self):

      print "####################"
      print "Block Name: ", self.name
      print "Block Color: ", self.color
      print "Block IsData: ", self.isData
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
       AuxName = "aux_sample" + s.name
       haux = s.getTH1F(lumi, AuxName, var, nbin, xmin, xmax, cut, options, xlabel)
       h.Add(haux)
       del haux

     return h
       

class Tree:
   'Common base class for a physics meaningful tree'

   def __init__(self, fileName, name, isdata):
      self.name  = name
      self.isData = isdata
      self.blocks = []
      self.parseFileName(fileName)

   def parseFileName(self, fileName):

      f = open(fileName)

      for l in f.readlines():

        if (l[0] == "#"):
          continue

        splitedLine = str.split(l)
        block       = splitedLine[0]
        color       = eval(splitedLine[1])
        name        = splitedLine[2]
        location    = splitedLine[3]
        flocation   = splitedLine[4]
        xsection    = float(splitedLine[5])
        isdata      = int(splitedLine[6])

        sample = Sample(name, location, flocation, xsection, isdata)
        coincidentBlock = [l for l in self.blocks if l.Name == block]

        if(coincidentBlock == []):

          newBlock = Block(block, color, isdata)
          newBlock.addSample(sample)
          self.addBlock(newBlock)

        else:

          coincidentBlock[0].addSample(sample)





   def printTree(self):

      print "######"
      print "Tree Name: ", self.name
      print "Tree IsData: ", self.isData
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
     
       AuxName = "aux_block" + b.name
       haux = b.getTH1F(lumi, AuxName, var, nbin, xmin, xmax, cut, options, xlabel)
       h.Add(haux)
       del haux

     return h   










