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

from optparse import OptionParser
from ROOT import gROOT, TCanvas, TFile
from Sample import Sample, Block, Tree
from CutManager import CutManager
from Canvas import Canvas


def parseFileName(fileName, name, isData):

  f = open(inputFileName)

  tree = Tree(name, isData)

  for l in f.readlines():

    if (l[0] == "#"):
      continue
    
    splitedLine = str.split(l)
    block       = splitedLine[0]
    color       = eval(splitedLine[1]) 
    name        = splitedLine[2]
    location    = splitedLine[3]
    xsection    = float(splitedLine[4])
    isdata      = int(splitedLine[5])

    
    sample = Sample(name, location, xsection, isdata)
    coincidentBlock = [l for l in tree.blocks if l.Name == block]
    
    
    if(coincidentBlock == []):
    
      newBlock = Block(block, color, isdata)
      newBlock.addSample(sample)
      tree.addBlock(newBlock)

    else:

      coincidentBlock[0].addSample(sample)
        
    
  return tree



if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options] FilenameWithSamples", version="%prog 1.0")
    parser.add_option("-m", "--mode", action="store", dest="mode", default="rmue", help="Operation mode")
    (options, args) = parser.parse_args()

    if len(args) != 1:
      parser.error("wrong number of arguments")

    inputFileName = args[0]
    tree = parseFileName(inputFileName, "MC", 0)
   
    gROOT.ProcessLine('.L tdrstyle.C')
    gROOT.SetBatch(1)
    r.setTDRStyle() 
    cuts = CutManager()

    mll_SF = tree.getTH1F(4, "mll_SF", "l1l2_m", 40, 20, 300, cuts.DYControlNoMassLeptonSF(), "", "m_{ll} [GeV]")
    mll_OF = tree.getTH1F(4, "mll_OF", "l1l2_m", 40, 20, 300, cuts.DYControlNoMassLeptonOF(), "", "m_{ll} [GeV]")

    plot = Canvas("mll", "png", 0.6, 0.6, 0.8, 0.8)
    plot.addHisto(mll_OF, "HISTO", "OF", "L", r.kBlack)
    plot.addHisto(mll_SF, "E1,SAME", "SF", "P", r.kBlue)
    plot.saveRatio(1, 0, 1, 4.0)
    
    plot2 = Canvas("pt", "png", 0.6, 0.6, 0.8, 0.8)
    plot2.addHisto(mll_OF, "HISTO", "OF", "L", r.kBlack)
    plot2.save(0, 0, 1, 4.0)
    











