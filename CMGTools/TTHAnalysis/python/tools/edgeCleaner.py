from CMGTools.TTHAnalysis.treeReAnalyzer import *

class edgeCleaner:
    def __init__(self,label,tightLeptonSel,cleanJet,isMC=True):
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.tightLeptonSel = tightLeptonSel
        self.cleanJet = cleanJet
        self.isMC = isMC
    def listBranches(self):
        label = self.label
        biglist = [ ("nLepTight"+label, "I"), ("nJetSel"+label, "I"), 
                 ("iLT"+label,"I",20,"nLepTight"+label), 
                 ("iJ"+label,"I",20,"nJetSel"+label), # index >= 0 if in Jet; -1-index (<0) if in DiscJet
                 ("nLepGood20"+label, "I"), ("nLepGood20T"+label, "I"),
                 ## ("nJet40"+label, "I"), "htJet40j"+label, ("nBJetLoose40"+label, "I"), ("nBJetMedium40"+label, "I"),
                 ("nJet35"+label, "I"), "htJet35j"+label, ("nBJetLoose35"+label, "I"), ("nBJetMedium35"+label, "I"), 
                 ## ("nJet25"+label, "I"), "htJet25j"+label, ("nBJetLoose25"+label, "I"), ("nBJetMedium25"+label, "I"), 
                 ("iL1T"+label, "I"), ("iL2T"+label, "I"), 
                 "lepsMll"+label,
                 ]
        for jfloat in "pt eta phi mass btagCSV rawPt".split():
            biglist.append( ("JetSel"+label+"_"+jfloat,"F",20,"nJetSel"+label) )
        if self.isMC:
            biglist.append( ("JetSel"+label+"_mcPt",     "F",20,"nJetSel"+label) )
            biglist.append( ("JetSel"+label+"_mcFlavour","I",20,"nJetSel"+label) )
            biglist.append( ("JetSel"+label+"_mcMatchId","I",20,"nJetSel"+label) )
        return biglist
    def __call__(self,event):
        leps = [l for l in Collection(event,"LepGood","nLepGood")]
        jetsc = [j for j in Collection(event,"Jet","nJet")]
        jetsd = [j for j in Collection(event,"DiscJet","nDiscJet")]
        ret = {}; jetret = {}
        #
        ### Define tight leptons
        ret["iLT"] = []; ret["nLepGood20T"] = 0
        for il,lep in enumerate(leps):
            if self.tightLeptonSel(lep):
                ret["iLT"].append(il)
                if lep.pt < 20: ret["nLepGood20T"] += 1
        ret["nLepTight"] = len(ret["iLT"])
        #
        ### Define jets
        ret["iJ"] = []
        # 0. mark each jet as clean
        for j in jetsc+jetsd: j._clean = True
        # 1. associate to each tight lepton its nearest jet 
        for il in ret["iLT"]:
            lep = leps[il]
            best = None; bestdr = 0.4
            for j in jetsc+jetsd:
                dr = deltaR(lep,j)
                if dr < bestdr:
                    best = j; bestdr = dr
            if best is not None and self.cleanJet(lep,best,bestdr):
                best._clean = False
        # 2. compute the jet list
        for ijc,j in enumerate(jetsc):
            if not j._clean: continue
            ret["iJ"].append(ijc)
        for ijd,j in enumerate(jetsd):
            if not j._clean: continue
            ret["iJ"].append(-1-ijd)
        # 3. sort the jets by pt
        ret["iJ"].sort(key = lambda idx : jetsc[idx].pt if idx >= 0 else jetsd[-1-idx].pt, reverse = True)
        # 4. compute the variables
        for jfloat in "pt eta phi mass btagCSV rawPt".split():
            jetret[jfloat] = []
        if self.isMC:
            for jmc in "mcPt mcFlavour mcMatchId".split():
                jetret[jmc] = []
        for idx in ret["iJ"]:
            jet = jetsc[idx] if idx >= 0 else jetsd[-1-idx]
            for jfloat in "pt eta phi mass btagCSV rawPt".split():
                jetret[jfloat].append( getattr(jet,jfloat) )
            if self.isMC:
                for jmc in "mcPt mcFlavour mcMatchId".split():
                    jetret[jmc].append( getattr(jet,jmc) )
        # 5. compute the sums
        ret["nJet35"] = 0; ret["htJet35j"] = 0; ret["nBJetLoose35"] = 0; ret["nBJetMedium35"] = 0
        for j in jetsc+jetsd:
            if not j._clean: continue
            if j.pt > 35 and abs(j.eta) < 2.4:
                ret["nJet35"] += 1; ret["htJet35j"] += j.pt; 
                if j.btagCSV>0.423: ret["nBJetLoose35"] += 1
                if j.btagCSV>0.814: ret["nBJetMedium35"] += 1
        #
        ### edge specific things
        lepst = [ leps[il] for il in ret["iLT"] ]
        ## ret['mZ1'] = self.bestZ1TL(lepsl, lepsl)
        ## ret['mZ1cut10TL'] = self.bestZ1TL(lepsl, lepst, cut=lambda l:l.pt>10)
        ## ret['minMllAFAS'] = self.minMllTL(lepsl, lepsl) 
        ## ret['minMllAFOS'] = self.minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.charge !=  l2.charge) 
        ## ret['minMllSFOS'] = self.minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.pdgId  == -l2.pdgId) 
        ## ret['minMllAFASTL'] = self.minMllTL(lepsl, lepst) 
        ## ret['minMllAFOSTL'] = self.minMllTL(lepsl, lepst, paircut = lambda l1,l2 : l1.charge !=  l2.charge) 
        ## ret['minMllSFOSTL'] = self.minMllTL(lepsl, lepst, paircut = lambda l1,l2 : l1.pdgId  == -l2.pdgId) 
        ## for (name,lepcoll) in ("T",lepst):
        iL1iL2 = self.findPair(lepst)
        ret['iL1'+'T'] = ret["iLT"][ iL1iL2[0] ] if len(ret["iLT"]) >=1 else -1
        ret['iL2'+'T'] = ret["iLT"][ iL1iL2[1] ] if len(ret["iLT"]) >=2 else -1
        ret['lepsMll'] = iL1iL2[2] 
        #
        ### attach labels and return
        fullret = {}
        for k,v in ret.iteritems(): 
            fullret[k+self.label] = v
        for k,v in jetret.iteritems(): 
            fullret["JetSel%s_%s" % (self.label,k)] = v
        return fullret

    def findPair(self,leps):
        ret = (-1,-1,-999.)
        if len(leps) == 2:
            if leps[0].pt < 25:  ret=(-1,-1,-999.)
            else: ret = (0, 1, (leps[0].p4() + leps[1].p4()).M() )
        if len(leps) > 2:
            pairs = []
            for il1 in xrange(len(leps)-1):
                for il2 in xrange(il1+1,len(leps)): 
                    l1 = leps[il1]
                    l2 = leps[il2]
                    #if l1.pt < 20 or l2.pt < 20: continue
                    if l1.pt < 25: continue
                    if (l1.charge != l2.charge and deltaR(l1,l2) > 0.3 ):
                        ht   = l1.pt + l2.pt
                        mll  = (l1.p4() + l2.p4()).M()
                        pairs.append( (-ht,il1,il2,mll) )
            if len(pairs):
                pairs.sort()
                ret = (pairs[0][1],pairs[0][2],pairs[0][3])
        return ret


def _susyEdge(lep):
        if lep.pt <= 20.: return False
        if abs(lep.eta) > 1.4 and abs(lep.eta) < 1.6: return False
        if abs(lep.pdgId) == 13 and lep.tightId != 1: return False
        if abs(lep.pdgId) == 11 and lep.tightId < 1: return False
        if lep.relIso03 > 0.15: return False
        return True

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf1 = edgeCleaner("Edge", 
                lambda lep : lep.relIso03 < 0.15 and _susyEdge(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf1(ev)
            print self.sf2(ev)
            print self.sf3(ev)
            print self.sf4(ev)
            print self.sf5(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
