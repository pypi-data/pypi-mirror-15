import unittest
import pygsti
import numpy as np
import warnings
import pickle


class GateSetTestCase(unittest.TestCase):

    def setUp(self):
        #OK for these tests, since we test user interface?
        #Set GateSet objects to "strict" mode for testing
        pygsti.objects.GateSet._strict = False

        self.gateset = pygsti.construction.build_gateset(
            [2], [('Q0',)],['Gi','Gx','Gy'], 
            [ "I(Q0)","X(pi/8,Q0)", "Y(pi/8,Q0)"],
            prepLabels=["rho0"], prepExpressions=["0"],
            effectLabels=["E0"], effectExpressions=["1"], 
            spamdefs={'plus': ('rho0','E0'), 
                           'minus': ('rho0','remainder') } )

        self.tp_gateset = pygsti.construction.build_gateset(
            [2], [('Q0',)],['Gi','Gx','Gy'], 
            [ "I(Q0)","X(pi/8,Q0)", "Y(pi/8,Q0)"],
            prepLabels=["rho0"], prepExpressions=["0"],
            effectLabels=["E0"], effectExpressions=["1"], 
            spamdefs={'plus': ('rho0','E0'), 
                           'minus': ('rho0','remainder') },
            parameterization="TP")

        self.static_gateset = pygsti.construction.build_gateset(
            [2], [('Q0',)],['Gi','Gx','Gy'], 
            [ "I(Q0)","X(pi/8,Q0)", "Y(pi/8,Q0)"],
            prepLabels=["rho0"], prepExpressions=["0"],
            effectLabels=["E0"], effectExpressions=["1"], 
            spamdefs={'plus': ('rho0','E0'), 
                           'minus': ('rho0','remainder') },
            parameterization="static")



    def assertArraysAlmostEqual(self,a,b):
        self.assertAlmostEqual( np.linalg.norm(a-b), 0 )

    def assertNoWarnings(self, callable, *args, **kwds):
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter('always')
            result = callable(*args, **kwds)
            self.assertTrue(len(warning_list) == 0)
        return result

    def assertWarns(self, callable, *args, **kwds):
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter('always')
            result = callable(*args, **kwds)
            self.assertTrue(len(warning_list) > 0)
        return result


class TestGateSetMethods(GateSetTestCase):

  def test_creation(self):
      self.assertIsInstance(self.gateset, pygsti.objects.GateSet)

  def test_pickling(self):
      p = pickle.dumps(self.gateset.preps)
      preps = pickle.loads(p)
      self.assertEqual(preps.keys(), self.gateset.preps.keys())

      p = pickle.dumps(self.gateset.effects)
      effects = pickle.loads(p)
      self.assertEqual(effects.keys(), self.gateset.effects.keys())

      p = pickle.dumps(self.gateset.gates)
      gates = pickle.loads(p)
      self.assertEqual(gates.keys(), self.gateset.gates.keys())

      p = pickle.dumps(self.gateset)
      g = pickle.loads(p)
      self.assertAlmostEqual(self.gateset.frobeniusdist(g), 0.0)

  def test_counting(self):

      self.assertEqual(self.gateset.num_preps(), 1) 
      self.assertEqual(self.gateset.num_effects(), 2) 

      for default_param in ("full","TP","static"):
          nGates = 3 if default_param in ("full","TP") else 0
          nSPVecs = 1 if default_param in ("full","TP") else 0
          nEVecs = 1 if default_param in ("full","TP") else 0
          nParamsPerGate = 16 if default_param == "full" else 12
          nParamsPerSP = 4 if default_param == "full" else 3
          nParams =  nGates * nParamsPerGate + nSPVecs * nParamsPerSP + nEVecs * 4
          self.gateset.set_all_parameterizations(default_param)
          self.assertEqual(self.gateset.num_params(), nParams)  

      self.assertEqual(self.gateset.get_prep_labels(), ["rho0"]) 
      self.assertEqual(self.gateset.get_effect_labels(), ["E0", "remainder"]) 

  def test_getset_full(self):
      self.getset_helper(self.gateset)

  def test_getset_tp(self):
      self.getset_helper(self.tp_gateset)

  def test_getset_static(self):
      self.getset_helper(self.static_gateset)
      
  def getset_helper(self, gs):

      v = np.array( [[1.0/np.sqrt(2)],[0],[0],[1.0/np.sqrt(2)]], 'd')
      
      gs['identity'] = v
      w = gs['identity']
      self.assertArraysAlmostEqual(w,v)

      gs['rho1'] = v
      w = gs['rho1']
      self.assertArraysAlmostEqual(w,v)

      gs['E1'] = v
      w = gs['E1']
      self.assertArraysAlmostEqual(w,v)

      gs.spamdefs["TEST"] = ("rho0","E1")
      self.assertTrue("TEST" in gs.get_spam_labels())
      d = gs.get_reverse_spam_defs()
      self.assertEqual( d[("rho0","E1")], "TEST" )

      Gi_matrix = np.identity(4, 'd')
      self.assertTrue( isinstance(gs['Gi'], pygsti.objects.Gate) )

      Gi_test_matrix = np.random.random( (4,4) )
      Gi_test_matrix[0,:] = [1,0,0,0] # so TP mode works
      Gi_test = pygsti.objects.FullyParameterizedGate( Gi_test_matrix  )
      gs["Gi"] = Gi_test_matrix #set gate matrix
      gs["Gi"] = Gi_test #set gate object
      self.assertArraysAlmostEqual( gs['Gi'], Gi_test_matrix )

      with self.assertRaises(KeyError):
          gs.preps['foobar'] = [1,0,0,0] #bad key prefix

      with self.assertRaises(KeyError):
          gs2 = gs.copy()
          gs2['identity'] = None
          error = gs2.effects['remainder'] #no identity vector set


  def test_copy(self):
      cp = self.gateset.copy()
      self.assertAlmostEqual( self.gateset.frobeniusdist(cp), 0 )
      self.assertAlmostEqual( self.gateset.jtracedist(cp), 0 )
      self.assertAlmostEqual( self.gateset.diamonddist(cp), 0 )


  def test_vectorize(self):
      cp = self.gateset.copy()
      v = cp.to_vector()
      cp.from_vector(v)
      self.assertAlmostEqual( self.gateset.frobeniusdist(cp), 0 )


  def test_transform(self):
      T = np.array([[ 0.36862036,  0.49241519,  0.35903944,  0.90069522],
                    [ 0.12347698,  0.45060548,  0.61671491,  0.64854769],
                    [ 0.4038386 ,  0.89518315,  0.20206879,  0.6484708 ],
                    [ 0.44878029,  0.42095514,  0.27645424,  0.41766033]]) #some random array
      Tinv = np.linalg.inv(T)
      cp = self.gateset.copy()
      cp.transform(T,Tinv)

      self.assertAlmostEqual( self.gateset.frobeniusdist(cp, T), 0 )
      self.assertAlmostEqual( self.gateset.jtracedist(cp, T), 0 )
      self.assertAlmostEqual( self.gateset.diamonddist(cp, T), 0 )

      for gateLabel in cp.gates:
          self.assertArraysAlmostEqual(cp[gateLabel], np.dot(Tinv, np.dot(self.gateset[gateLabel], T)))
      for prepLabel in cp.preps:
          self.assertArraysAlmostEqual(cp[prepLabel], np.dot(Tinv, self.gateset[prepLabel]))
      for effectLabel in cp.effects:
          self.assertArraysAlmostEqual(cp[effectLabel],  np.dot(np.transpose(T), self.gateset[effectLabel]))
      

  def test_simple_multiplicationA(self):
      gatestring = ('Gx','Gy')
      p1 = np.dot( self.gateset['Gy'], self.gateset['Gx'] )
      p2 = self.gateset.product(gatestring, bScale=False)
      p3,scale = self.gateset.product(gatestring, bScale=True)
      self.assertArraysAlmostEqual(p1,p2)
      self.assertArraysAlmostEqual(p1,scale*p3)

      #Artificially reset the "smallness" threshold for scaling to be
      # sure to engate the scaling machinery
      PORIG = pygsti.objects.gscalc.PSMALL; pygsti.objects.gscalc.PSMALL = 10
      p4,scale = self.gateset.product(gatestring, bScale=True)
      pygsti.objects.gscalc.PSMALL = PORIG
      self.assertArraysAlmostEqual(p1,scale*p4)

      dp = self.gateset.dproduct(gatestring)
      dp_flat = self.gateset.dproduct(gatestring,flat=True)


  def test_simple_multiplicationB(self):
      gatestring = ('Gx','Gy','Gy')
      p1 = np.dot( self.gateset['Gy'], np.dot( self.gateset['Gy'], self.gateset['Gx'] ))
      p2 = self.gateset.product(gatestring, bScale=False)
      p3,scale = self.gateset.product(gatestring, bScale=True)
      self.assertArraysAlmostEqual(p1,p2)
      self.assertArraysAlmostEqual(p1,scale*p3)

      #Artificially reset the "smallness" threshold for scaling to be
      # sure to engate the scaling machinery
      PORIG = pygsti.objects.gscalc.PSMALL; pygsti.objects.gscalc.PSMALL = 10
      p4,scale = self.gateset.product(gatestring, bScale=True)
      pygsti.objects.gscalc.PSMALL = PORIG
      self.assertArraysAlmostEqual(p1,scale*p4)


  def test_bulk_multiplication(self):
      gatestring1 = ('Gx','Gy')
      gatestring2 = ('Gx','Gy','Gy')
      evt = self.gateset.bulk_evaltree( [gatestring1,gatestring2] )

      p1 = np.dot( self.gateset['Gy'], self.gateset['Gx'] )
      p2 = np.dot( self.gateset['Gy'], np.dot( self.gateset['Gy'], self.gateset['Gx'] ))

      bulk_prods = self.gateset.bulk_product(evt)
      bulk_prods_scaled, scaleVals = self.gateset.bulk_product(evt, bScale=True)
      bulk_prods2 = scaleVals[:,None,None] * bulk_prods_scaled
      self.assertArraysAlmostEqual(bulk_prods[0],p1)
      self.assertArraysAlmostEqual(bulk_prods[1],p2)
      self.assertArraysAlmostEqual(bulk_prods2[0],p1)
      self.assertArraysAlmostEqual(bulk_prods2[1],p2)

      #Artificially reset the "smallness" threshold for scaling to be
      # sure to engate the scaling machinery
      PORIG = pygsti.objects.gscalc.PSMALL; pygsti.objects.gscalc.PSMALL = 10
      bulk_prods_scaled, scaleVals3 = self.gateset.bulk_product(evt, bScale=True)
      bulk_prods3 = scaleVals3[:,None,None] * bulk_prods_scaled
      pygsti.objects.gscalc.PSMALL = PORIG
      self.assertArraysAlmostEqual(bulk_prods3[0],p1)
      self.assertArraysAlmostEqual(bulk_prods3[1],p2)


      #tag on a few extra EvalTree tests
      iWithinTree = evt.get_tree_index_of_final_value(0)
      debug_stuff = evt.get_analysis_plot_infos()
      

  def test_simple_probabilityA(self):
      gatestring = ('Gx','Gy')
      p1 = np.dot( np.transpose(self.gateset.effects['E0']),
                   np.dot( self.gateset['Gy'],
                           np.dot(self.gateset['Gx'],
                                  self.gateset.preps['rho0'])))
      p2 = self.gateset.pr('plus',gatestring)
      p3 = self.gateset.pr('plus',gatestring,bUseScaling=False)
      self.assertArraysAlmostEqual(p1,p2)
      self.assertArraysAlmostEqual(p1,p3)

      p2 = self.gateset.pr('minus',gatestring)
      p3 = self.gateset.pr('minus',gatestring,bUseScaling=False)
      self.assertArraysAlmostEqual(1.0-p1,p2)
      self.assertArraysAlmostEqual(1.0-p1,p3)

      dp = self.gateset.dpr('plus',gatestring)
      dp4,p4 = self.gateset.dpr('plus',gatestring,returnPr=True)
      self.assertArraysAlmostEqual(dp,dp4)

  def test_simple_probabilityB(self):
      gatestring = ('Gx','Gy','Gy')
      p1 = np.dot( np.transpose(self.gateset.effects['E0']), 
                   np.dot( self.gateset['Gy'], 
                           np.dot( self.gateset['Gy'], 
                                   np.dot(self.gateset['Gx'], 
                                          self.gateset.preps['rho0']))))
      p2 = self.gateset.pr('plus',gatestring)
      self.assertAlmostEqual(p1,p2)

      gateset_with_nan = self.gateset.copy()
      gateset_with_nan['rho0'][:] = np.nan
      self.assertWarns(gateset_with_nan.pr,'plus',gatestring)

  def test_bulk_probabilities(self):
      gatestring1 = ('Gx','Gy')
      gatestring2 = ('Gx','Gy','Gy')
      evt = self.gateset.bulk_evaltree( [gatestring1,gatestring2] )      

      p1 = np.dot( np.transpose(self.gateset.effects['E0']),
                   np.dot( self.gateset['Gy'],
                           np.dot(self.gateset['Gx'],
                                  self.gateset.preps['rho0'])))

      p2 = np.dot( np.transpose(self.gateset.effects['E0']), 
                   np.dot( self.gateset['Gy'], 
                           np.dot( self.gateset['Gy'], 
                                   np.dot(self.gateset['Gx'], 
                                          self.gateset.preps['rho0']))))

      #check == true could raise a warning if a mismatch is detected
      bulk_pr = self.assertNoWarnings(self.gateset.bulk_pr,'plus',evt,check=True)
      bulk_pr_m = self.assertNoWarnings(self.gateset.bulk_pr,'minus',evt,check=True)
      self.assertAlmostEqual(bulk_pr[0],p1)
      self.assertAlmostEqual(bulk_pr[1],p2)
      self.assertAlmostEqual(bulk_pr_m[0],1.0-p1)
      self.assertAlmostEqual(bulk_pr_m[1],1.0-p2)

      probs1 = self.gateset.probs(gatestring1)
      probs2 = self.gateset.probs(gatestring2)
      self.assertAlmostEqual(probs1['plus'],p1)
      self.assertAlmostEqual(probs2['plus'],p2)
      self.assertAlmostEqual(probs1['minus'],1.0-p1)
      self.assertAlmostEqual(probs2['minus'],1.0-p2)

      bulk_probs = self.assertNoWarnings(self.gateset.bulk_probs,evt,check=True)
      self.assertAlmostEqual(bulk_probs['plus'][0],p1)
      self.assertAlmostEqual(bulk_probs['plus'][1],p2)
      self.assertAlmostEqual(bulk_probs['minus'][0],1.0-p1)
      self.assertAlmostEqual(bulk_probs['minus'][1],1.0-p2)

      #test with split eval tree
      evt_split = evt.copy(); evt_split.split(numSubTrees=2)
      bulk_probs_splt = self.assertNoWarnings(self.gateset.bulk_probs,
                                   evt_split, check=True)
      self.assertArraysAlmostEqual(bulk_probs['plus'], bulk_probs_splt['plus'])
      self.assertArraysAlmostEqual(bulk_probs['minus'], bulk_probs_splt['minus'])


      nGateStrings = 2; nSpamLabels = 2
      probs_to_fill = np.empty( (nSpamLabels,nGateStrings), 'd')
      spam_label_rows = { 'plus': 0, 'minus': 1 }
      self.assertNoWarnings(self.gateset.bulk_fill_probs, probs_to_fill, spam_label_rows, evt, check=True)
      self.assertAlmostEqual(probs_to_fill[0,0],p1)
      self.assertAlmostEqual(probs_to_fill[0,1],p2)
      self.assertAlmostEqual(probs_to_fill[1,0],1-p1)
      self.assertAlmostEqual(probs_to_fill[1,1],1-p2)

      prods = self.gateset.bulk_product(evt) #TODO: test output?



  def test_derivatives(self):
      gatestring0 = ('Gi','Gx')
      gatestring1 = ('Gx','Gy')
      gatestring2 = ('Gx','Gy','Gy')

      evt = self.gateset.bulk_evaltree( [gatestring0,gatestring1,gatestring2] )

      dP0 = self.gateset.dpr("plus", gatestring0)
      dP1 = self.gateset.dpr("plus", gatestring1)
      dP2 = self.gateset.dpr("plus", gatestring2)
      dP0m = self.gateset.dpr("minus", gatestring0)
      dP1m = self.gateset.dpr("minus", gatestring1)
      dP2m = self.gateset.dpr("minus", gatestring2)


      bulk_dP = self.gateset.bulk_dpr("plus", evt, returnPr=False, check=True)
      bulk_dP_m = self.gateset.bulk_dpr("minus", evt, returnPr=False, check=True)
      bulk_dP_chk, bulk_P = self.gateset.bulk_dpr("plus", evt, returnPr=True, check=False)
      bulk_dP_m_chk, bulk_Pm = self.gateset.bulk_dpr("minus", evt, returnPr=True, check=False)
      self.assertArraysAlmostEqual(bulk_dP,bulk_dP_chk)
      self.assertArraysAlmostEqual(bulk_dP[0,:],dP0)
      self.assertArraysAlmostEqual(bulk_dP[1,:],dP1)
      self.assertArraysAlmostEqual(bulk_dP[2,:],dP2)
      self.assertArraysAlmostEqual(bulk_dP_m,bulk_dP_m_chk)
      self.assertArraysAlmostEqual(bulk_dP_m[0,:],dP0m)
      self.assertArraysAlmostEqual(bulk_dP_m[1,:],dP1m)
      self.assertArraysAlmostEqual(bulk_dP_m[2,:],dP2m)

      #Artificially reset the "smallness" threshold for scaling
      # to be sure to engate the scaling machinery
      PORIG = pygsti.objects.gscalc.PSMALL; pygsti.objects.gscalc.PSMALL = 10
      DORIG = pygsti.objects.gscalc.DSMALL; pygsti.objects.gscalc.DSMALL = 10
      bulk_dPb = self.gateset.bulk_dpr("plus", evt, returnPr=False, check=True)
      pygsti.objects.gscalc.PSMALL = PORIG
      bulk_dPc = self.gateset.bulk_dpr("plus", evt, returnPr=False, check=True)
      pygsti.objects.gscalc.DSMALL = DORIG
      self.assertArraysAlmostEqual(bulk_dPb,bulk_dP_chk)
      self.assertArraysAlmostEqual(bulk_dPc,bulk_dP_chk)


      dProbs0 = self.gateset.dprobs(gatestring0)
      dProbs1 = self.gateset.dprobs(gatestring1)
      dProbs2 = self.gateset.dprobs(gatestring2)
      bulk_dProbs = self.assertNoWarnings(self.gateset.bulk_dprobs,
                                          evt, returnPr=False, check=True)
      bulk_dProbs_chk = self.assertNoWarnings(self.gateset.bulk_dprobs,
                                              evt, returnPr=True, check=True)
      self.assertArraysAlmostEqual(bulk_dProbs['plus'],bulk_dProbs_chk['plus'][0])
      self.assertArraysAlmostEqual(bulk_dProbs['plus'][0,:],dP0)
      self.assertArraysAlmostEqual(bulk_dProbs['plus'][1,:],dP1)
      self.assertArraysAlmostEqual(bulk_dProbs['plus'][2,:],dP2)
      self.assertArraysAlmostEqual(bulk_dProbs['plus'][0,:],dProbs0['plus'])
      self.assertArraysAlmostEqual(bulk_dProbs['plus'][1,:],dProbs1['plus'])
      self.assertArraysAlmostEqual(bulk_dProbs['plus'][2,:],dProbs2['plus'])

      #test with split eval tree
      evt_split = evt.copy(); evt_split.split(numSubTrees=2)
      bulk_dProbs_splt = self.assertNoWarnings(self.gateset.bulk_dprobs,
                                   evt_split, returnPr=False, check=True)
      self.assertArraysAlmostEqual(bulk_dProbs['plus'], bulk_dProbs_splt['plus'])
      self.assertArraysAlmostEqual(bulk_dProbs['minus'], bulk_dProbs_splt['minus'])


      dProbs0b = self.gateset.dprobs(gatestring0, returnPr=True)

      nGateStrings = 3; nSpamLabels = 2; nParams = self.gateset.num_params()
      probs_to_fill = np.empty( (nSpamLabels,nGateStrings), 'd')
      dprobs_to_fill = np.empty( (nSpamLabels,nGateStrings,nParams), 'd')
      dprobs_to_fillB = np.empty( (nSpamLabels,nGateStrings,nParams), 'd')
      spam_label_rows = { 'plus': 0, 'minus': 1 }
      self.assertNoWarnings(self.gateset.bulk_fill_dprobs, dprobs_to_fill, spam_label_rows, evt,
                            prMxToFill=probs_to_fill,check=True)
      self.assertArraysAlmostEqual(dprobs_to_fill[0,0,:],dP0)
      self.assertArraysAlmostEqual(dprobs_to_fill[0,1,:],dP1)
      self.assertArraysAlmostEqual(dprobs_to_fill[0,2,:],dP2)

      #without probs
      self.assertNoWarnings(self.gateset.bulk_fill_dprobs, dprobs_to_fillB, spam_label_rows, evt, check=True)
      self.assertArraysAlmostEqual(dprobs_to_fill,dprobs_to_fillB)

      dProds = self.gateset.bulk_dproduct(evt) #TODO: test output?



  def test_hessians(self):
      gatestring0 = ('Gi','Gx')
      gatestring1 = ('Gx','Gy')
      gatestring2 = ('Gx','Gy','Gy')

      evt = self.gateset.bulk_evaltree( [gatestring0,gatestring1,gatestring2] )

      hP0 = self.gateset.hpr("plus", gatestring0)
      hP1 = self.gateset.hpr("plus", gatestring1)
      hP2 = self.gateset.hpr("plus", gatestring2)
      hP0m = self.gateset.hpr("minus", gatestring0)
      hP1m = self.gateset.hpr("minus", gatestring1)
      hP2m = self.gateset.hpr("minus", gatestring2)

      hP0b,P0 = self.gateset.hpr("plus", gatestring0, returnPr=True)
      hP0b,dP0 = self.gateset.hpr("plus", gatestring0, returnDeriv=True)
      hP0mb,P0m = self.gateset.hpr("minus", gatestring0, returnPr=True)
      hP0mb,dP0m = self.gateset.hpr("minus", gatestring0, returnDeriv=True)

      bulk_hP = self.gateset.bulk_hpr("plus", evt, returnPr=False, returnDeriv=False, check=True)
      bulk_hP_m = self.gateset.bulk_hpr("minus", evt, returnPr=False, returnDeriv=False, check=True)
      bulk_hP_chk, bulk_dP, bulk_P = self.gateset.bulk_hpr("plus", evt, returnPr=True, returnDeriv=True, check=False)
      bulk_hP_m_chk, bulk_dP_m, bulk_P_m = self.gateset.bulk_hpr("minus", evt, returnPr=True, returnDeriv=True, check=False)
      self.assertArraysAlmostEqual(bulk_hP,bulk_hP_chk)
      self.assertArraysAlmostEqual(bulk_hP[0,:,:],hP0)
      self.assertArraysAlmostEqual(bulk_hP[1,:,:],hP1)
      self.assertArraysAlmostEqual(bulk_hP[2,:,:],hP2)
      self.assertArraysAlmostEqual(bulk_hP_m,bulk_hP_m_chk)
      self.assertArraysAlmostEqual(bulk_hP_m[0,:,:],hP0m)
      self.assertArraysAlmostEqual(bulk_hP_m[1,:,:],hP1m)
      self.assertArraysAlmostEqual(bulk_hP_m[2,:,:],hP2m)

      #Artificially reset the "smallness" threshold for scaling
      # to be sure to engate the scaling machinery
      PORIG = pygsti.objects.gscalc.PSMALL; pygsti.objects.gscalc.PSMALL = 10
      DORIG = pygsti.objects.gscalc.DSMALL; pygsti.objects.gscalc.DSMALL = 10
      HORIG = pygsti.objects.gscalc.HSMALL; pygsti.objects.gscalc.HSMALL = 10
      bulk_hPb = self.gateset.bulk_hpr("plus", evt, returnPr=False, returnDeriv=False, check=True)
      pygsti.objects.gscalc.PSMALL = PORIG
      bulk_hPc = self.gateset.bulk_hpr("plus", evt, returnPr=False, returnDeriv=False, check=True)
      pygsti.objects.gscalc.DSMALL = DORIG
      pygsti.objects.gscalc.HSMALL = HORIG
      self.assertArraysAlmostEqual(bulk_hPb,bulk_hP_chk)
      self.assertArraysAlmostEqual(bulk_hPc,bulk_hP_chk)


      hProbs0 = self.gateset.hprobs(gatestring0)
      hProbs1 = self.gateset.hprobs(gatestring1)
      hProbs2 = self.gateset.hprobs(gatestring2)
      bulk_hProbs = self.assertNoWarnings(self.gateset.bulk_hprobs,
                                          evt, returnPr=False, check=True)
      bulk_hProbs_chk = self.assertNoWarnings(self.gateset.bulk_hprobs,
                                              evt, returnPr=True, check=True)
      self.assertArraysAlmostEqual(bulk_hProbs['plus'],bulk_hProbs_chk['plus'][0])
      self.assertArraysAlmostEqual(bulk_hProbs['plus'][0,:,:],hP0)
      self.assertArraysAlmostEqual(bulk_hProbs['plus'][1,:,:],hP1)
      self.assertArraysAlmostEqual(bulk_hProbs['plus'][2,:,:],hP2)
      self.assertArraysAlmostEqual(bulk_hProbs['plus'][0,:,:],hProbs0['plus'])
      self.assertArraysAlmostEqual(bulk_hProbs['plus'][1,:,:],hProbs1['plus'])
      self.assertArraysAlmostEqual(bulk_hProbs['plus'][2,:,:],hProbs2['plus'])

      #test with split eval tree
      evt_split = evt.copy(); evt_split.split(maxSubTreeSize=4)
      bulk_hProbs_splt = self.assertNoWarnings(self.gateset.bulk_hprobs,
                                   evt_split, returnPr=False, check=True)
      self.assertArraysAlmostEqual(bulk_hProbs['plus'], bulk_hProbs_splt['plus'])
      self.assertArraysAlmostEqual(bulk_hProbs['minus'], bulk_hProbs_splt['minus'])


      #Vary keyword args
      hProbs0b = self.gateset.hprobs(gatestring0,returnPr=True)
      hProbs0c = self.gateset.hprobs(gatestring0,returnDeriv=True)
      hProbs0d = self.gateset.hprobs(gatestring0,returnDeriv=True,returnPr=True)
      bulk_hProbs_B = self.gateset.bulk_hprobs(evt, returnPr=True, returnDeriv=True)
      bulk_hProbs_C = self.gateset.bulk_hprobs(evt, returnDeriv=True)


      nGateStrings = 3; nSpamLabels = 2; nParams = self.gateset.num_params()
      probs_to_fill = np.empty( (nSpamLabels,nGateStrings), 'd')
      probs_to_fillB = np.empty( (nSpamLabels,nGateStrings), 'd')
      dprobs_to_fill = np.empty( (nSpamLabels,nGateStrings,nParams), 'd')
      dprobs_to_fillB = np.empty( (nSpamLabels,nGateStrings,nParams), 'd')
      hprobs_to_fill = np.empty( (nSpamLabels,nGateStrings,nParams,nParams), 'd')
      hprobs_to_fillB = np.empty( (nSpamLabels,nGateStrings,nParams,nParams), 'd')
      spam_label_rows = { 'plus': 0, 'minus': 1 }
      self.assertNoWarnings(self.gateset.bulk_fill_hprobs, hprobs_to_fill, spam_label_rows, evt,
                            prMxToFill=probs_to_fill, derivMxToFill=dprobs_to_fill, check=True)

      self.assertArraysAlmostEqual(hprobs_to_fill[0,0,:,:],hP0)
      self.assertArraysAlmostEqual(hprobs_to_fill[0,1,:,:],hP1)
      self.assertArraysAlmostEqual(hprobs_to_fill[0,2,:,:],hP2)


      #without derivative
      self.assertNoWarnings(self.gateset.bulk_fill_hprobs, hprobs_to_fillB, spam_label_rows, evt,
                            prMxToFill=probs_to_fillB, check=True) 
      self.assertArraysAlmostEqual(hprobs_to_fill,hprobs_to_fillB)
      self.assertArraysAlmostEqual(probs_to_fill,probs_to_fillB)

      #without probs
      self.assertNoWarnings(self.gateset.bulk_fill_hprobs, hprobs_to_fillB, spam_label_rows, evt,
                            derivMxToFill=dprobs_to_fillB, check=True) 
      self.assertArraysAlmostEqual(hprobs_to_fill,hprobs_to_fillB)
      self.assertArraysAlmostEqual(dprobs_to_fill,dprobs_to_fillB)

      #without either
      self.assertNoWarnings(self.gateset.bulk_fill_hprobs, hprobs_to_fillB, spam_label_rows, evt, check=True) 
      self.assertArraysAlmostEqual(hprobs_to_fill,hprobs_to_fillB)

      N = self.gateset.get_dimension()**2 #number of elements in a gate matrix
      
      hProds = self.gateset.bulk_hproduct(evt)
      hProdsB,scales = self.gateset.bulk_hproduct(evt, bScale=True)
      self.assertArraysAlmostEqual(hProds, scales[:,None,None,None,None]*hProdsB)

      hProdsFlat = self.gateset.bulk_hproduct(evt, flat=True, bScale=False)
      hProdsFlatB,S1 = self.gateset.bulk_hproduct(evt, flat=True, bScale=True)
      self.assertArraysAlmostEqual(hProdsFlat, np.repeat(S1,N)[:,None,None]*hProdsFlatB)

      hProdsC, dProdsC, prodsC = self.gateset.bulk_hproduct(evt, bReturnDProdsAndProds=True, bScale=False)
      hProdsD, dProdsD, prodsD, S2 = self.gateset.bulk_hproduct(evt, bReturnDProdsAndProds=True, bScale=True)
      self.assertArraysAlmostEqual(hProds, hProdsC)
      self.assertArraysAlmostEqual(hProds, S2[:,None,None,None,None]*hProdsD)
      self.assertArraysAlmostEqual(dProdsC, S2[:,None,None,None]*dProdsD)
      self.assertArraysAlmostEqual(prodsC, S2[:,None,None]*prodsD)

      hProdsF, dProdsF, prodsF    = self.gateset.bulk_hproduct(evt, bReturnDProdsAndProds=True, flat=True, bScale=False)
      hProdsF2, dProdsF2, prodsF2, S3 = self.gateset.bulk_hproduct(evt, bReturnDProdsAndProds=True, flat=True, bScale=True)
      self.assertArraysAlmostEqual(hProdsFlat, hProdsF)
      self.assertArraysAlmostEqual(hProdsFlat, np.repeat(S3,N)[:,None,None]*hProdsF2)
      self.assertArraysAlmostEqual(dProdsF, np.repeat(S3,N)[:,None]*dProdsF2)
      self.assertArraysAlmostEqual(prodsF, S3[:,None,None]*prodsF2)


      hcols = []
      d12cols = []
      for hprobs, dprobs12 in self.gateset.bulk_hprobs_by_column(
          spam_label_rows, evt, True, clipTo=(-1e6,1e6) ):
          hcols.append(hprobs)
          d12cols.append(dprobs12)
      all_hcols = np.concatenate( hcols, axis=3 )
      all_d12cols = np.concatenate( d12cols, axis=3 )
      dprobs12 = dprobs_to_fill[:,:,:,None] * dprobs_to_fill[:,:,None,:]
      self.assertArraysAlmostEqual(all_hcols,hprobs_to_fill)
      self.assertArraysAlmostEqual(all_d12cols,dprobs12)




  def test_tree_splitting(self):
      gatestrings = [('Gx',),
                     ('Gy',),
                     ('Gx','Gy'),
                     ('Gy','Gy'),
                     ('Gy','Gx'),
                     ('Gx','Gx','Gx'),
                     ('Gx','Gy','Gx'),
                     ('Gx','Gy','Gy'),
                     ('Gy','Gy','Gy'),
                     ('Gy','Gx','Gx') ]
      evtA = self.gateset.bulk_evaltree( gatestrings )

      evtB = self.gateset.bulk_evaltree( gatestrings )
      evtB.split(maxSubTreeSize=4)

      evtC = self.gateset.bulk_evaltree( gatestrings )
      evtC.split(numSubTrees=3)

      with self.assertRaises(ValueError):
          evtBad = self.gateset.bulk_evaltree( gatestrings )
          evtBad.split(numSubTrees=3, maxSubTreeSize=4) #can't specify both

      self.assertFalse(evtA.is_split())
      self.assertTrue(evtB.is_split())
      self.assertTrue(evtC.is_split())
      self.assertEqual(len(evtA.get_sub_trees()), 1)
      self.assertEqual(len(evtB.get_sub_trees()), 5) #empirically
      self.assertEqual(len(evtC.get_sub_trees()), 3)
      self.assertLessEqual(max([len(subTree) 
                           for subTree in evtB.get_sub_trees()]), 4)

      #print "Lenghts = ",len(evtA.get_sub_trees()),len(evtB.get_sub_trees()),len(evtC.get_sub_trees())
      #print "SubTree sizes = ",[len(subTree) for subTree in evtC.get_sub_trees()]
      
      bulk_prA = self.gateset.bulk_pr('plus',evtA)
      bulk_prB = self.gateset.bulk_pr('plus',evtB)
      bulk_prC = self.gateset.bulk_pr('plus',evtC)

      self.assertArraysAlmostEqual(bulk_prA,bulk_prB)
      self.assertArraysAlmostEqual(bulk_prA,bulk_prC)
      


  def test_failures(self):
      
      with self.assertRaises(KeyError):
          self.gateset['Non-existent-key']

      with self.assertRaises(KeyError):
          self.gateset['Non-existent-key'] = np.zeros((4,4),'d') #can't set things not in the gateset

      #with self.assertRaises(ValueError):
      #    self.gateset['Gx'] = np.zeros((4,4),'d') #can't set matrices

      #with self.assertRaises(ValueError):
      #    self.gateset.update( {'Gx': np.zeros((4,4),'d') } )

      #with self.assertRaises(ValueError):
      #    self.gateset.update( Gx=np.zeros((4,4),'d') )

      #with self.assertRaises(TypeError):
      #    self.gateset.update( 1, 2 ) #too many positional arguments...

      #with self.assertRaises(ValueError):
      #    self.gateset.setdefault('Gx',np.zeros((4,4),'d'))

      with self.assertRaises(ValueError):
          self.gateset['Gbad'] = pygsti.obj.FullyParameterizedGate(np.zeros((5,5),'d')) #wrong gate dimension
          
      
  def test_iteration(self):
      #Iterate over all gates and SPAM matrices
      #for mx in self.gateset.iterall():
      pass



      
if __name__ == "__main__":
    unittest.main(verbosity=2)
