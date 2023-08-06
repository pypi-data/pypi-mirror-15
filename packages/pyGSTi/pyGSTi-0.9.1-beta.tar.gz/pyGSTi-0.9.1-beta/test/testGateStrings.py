import unittest
import copy
import pygsti
import numpy as np


class GateStringTestCase(unittest.TestCase):

    def setUp(self):
        #Set GateSet objects to "strict" mode for testing
        pygsti.objects.GateSet._strict = True


class TestGateStringMethods(GateStringTestCase):
    def test_simple(self):
        #The workhorse function is pygsti.construction.create_gatestring_list, which executes its positional arguments within a nested
        # loop given by iterable keyword arguments.  That's a mouthful, so let's look at a few examples:
        As = [('a1',),('a2',)]
        Bs = [('b1',), ('b2',)]

        def rep2(x):
            return x+x

        def asserter(x):
            assert(False)

        def samestr(x):
            return "Gx" #to test string processing

        def sametup(x):
            return "Gx" #to test string processing


        list0 = pygsti.construction.create_gatestring_list("")
        list1 = pygsti.construction.create_gatestring_list("a", a=As)
        list2 = pygsti.construction.create_gatestring_list("a+b", a=As, b=Bs, order=['a','b'])
        list3 = pygsti.construction.create_gatestring_list("a+b", a=As, b=Bs, order=['b','a'])
        list4 = pygsti.construction.create_gatestring_list("R(a)+c", a=As, c=[('c',)], R=rep2, order=['a','c'])
        list5 = pygsti.construction.create_gatestring_list("Ast(a)", a=As, Ast=asserter)
        list6 = pygsti.construction.create_gatestring_list("SS(a)", a=As, SS=samestr)
        list7 = pygsti.construction.gatestring_list(list1)

        self.assertEqual(list0, pygsti.construction.gatestring_list([ () ] )) #special case: get the empty gate string
        self.assertEqual(list1, pygsti.construction.gatestring_list(As))
        self.assertEqual(list2, pygsti.construction.gatestring_list([('a1','b1'),('a1','b2'),('a2','b1'),('a2','b2')]))
        self.assertEqual(list3, pygsti.construction.gatestring_list([('a1','b1'),('a2','b1'),('a1','b2'),('a2','b2')]))
        self.assertEqual(list4, pygsti.construction.gatestring_list([('a1','a1','c'),('a2','a2','c')]))
        self.assertEqual(list5, []) # failed assertions cause item to be skipped
        self.assertEqual(list6, pygsti.construction.gatestring_list([('Gx',), ('Gx',)])) #strs => parser => GateStrings
        self.assertEqual(list7, list1)
        
        with self.assertRaises(ValueError):
            pygsti.construction.gatestring_list( [ {'foo': "Bar"} ] ) #cannot convert dicts to GateStrings...
            

    def test_truncate_methods(self):
        self.assertEqual( pygsti.construction.repeat_and_truncate(('A','B','C'),5), ('A','B','C','A','B'))
        self.assertEqual( pygsti.construction.repeat_with_max_length(('A','B','C'),5), ('A','B','C'))
        self.assertEqual( pygsti.construction.repeat_count_with_max_length(('A','B','C'),5), 1)

    def test_fiducials_germs(self):
        fids  = pygsti.construction.gatestring_list( [ ('Gf0',), ('Gf1',)    ] )
        germs = pygsti.construction.gatestring_list( [ ('G0',), ('G1a','G1b')] )

        gateStrings1 = pygsti.construction.create_gatestring_list("f0+germ*e+f1", f0=fids, f1=fids,
                                                                  germ=germs, e=2, order=["germ","f0","f1"])
        expected1 = ["Gf0(G0)^2Gf0",
                     "Gf0(G0)^2Gf1",
                     "Gf1(G0)^2Gf0",
                     "Gf1(G0)^2Gf1",
                     "Gf0(G1aG1b)^2Gf0",
                     "Gf0(G1aG1b)^2Gf1",
                     "Gf1(G1aG1b)^2Gf0",
                     "Gf1(G1aG1b)^2Gf1" ]
        self.assertEqual( map(str,gateStrings1), expected1 )

        
        gateStrings2 = pygsti.construction.create_gatestring_list("f0+T(germ,N)+f1", f0=fids, f1=fids,
                                                                  germ=germs, N=3, T=pygsti.construction.repeat_and_truncate,
                                                                  order=["germ","f0","f1"])
        expected2 = ["Gf0G0G0G0Gf0",
                     "Gf0G0G0G0Gf1",
                     "Gf1G0G0G0Gf0",
                     "Gf1G0G0G0Gf1",
                     "Gf0G1aG1bG1aGf0",
                     "Gf0G1aG1bG1aGf1",
                     "Gf1G1aG1bG1aGf0",
                     "Gf1G1aG1bG1aGf1" ]
        self.assertEqual( map(str,gateStrings2), expected2 )
        

        gateStrings3 = pygsti.construction.create_gatestring_list("f0+T(germ,N)+f1", f0=fids, f1=fids,
                                                                  germ=germs, N=3, 
                                                                  T=pygsti.construction.repeat_with_max_length,
                                                                  order=["germ","f0","f1"])
        expected3 = [ "Gf0(G0)^3Gf0",
                      "Gf0(G0)^3Gf1",
                      "Gf1(G0)^3Gf0",
                      "Gf1(G0)^3Gf1",
                      "Gf0(G1aG1b)Gf0",
                      "Gf0(G1aG1b)Gf1",
                      "Gf1(G1aG1b)Gf0",
                      "Gf1(G1aG1b)Gf1" ] 
        self.assertEqual( map(str,gateStrings3), expected3 )

    def test_string_compression(self):
        gs = pygsti.objects.GateString(None, stringRepresentation="Gx^100")
        comp_gs = pygsti.objects.gatestring.CompressedGateString.compress_gate_label_tuple(tuple(gs))
        exp_gs = pygsti.objects.gatestring.CompressedGateString.expand_gate_label_tuple(comp_gs)
        self.assertEqual(tuple(gs), exp_gs)

    def test_repeat(self):
        gs = pygsti.objects.GateString( ('Gx','Gx','Gy') )
        
        gs2 = pygsti.construction.repeat(gs, 2)
        self.assertEqual( gs2, pygsti.obj.GateString( ('Gx','Gx','Gy','Gx','Gx','Gy') ))

        gs3 = pygsti.construction.repeat_with_max_length(gs, 7)
        self.assertEqual( gs3, pygsti.obj.GateString( ('Gx','Gx','Gy','Gx','Gx','Gy') ))

        gs4 = pygsti.construction.repeat_and_truncate(gs, 4)
        self.assertEqual( gs4, pygsti.obj.GateString( ('Gx','Gx','Gy','Gx') ))

        gs5 = pygsti.construction.repeat_remainder_for_truncation(gs, 4)
        self.assertEqual( gs5, pygsti.obj.GateString( ('Gx',) ))

    def test_simplify(self):
        s = "{}Gx^1Gy{}Gz^1"
        self.assertEqual( pygsti.construction.simplify_str(s), "GxGyGz" )

        s = "{}Gx^1(Gy)^2{}Gz^1"
        self.assertEqual( pygsti.construction.simplify_str(s), "Gx(Gy)^2Gz" )

        s = "{}{}^1{}"
        self.assertEqual( pygsti.construction.simplify_str(s), "{}" )


    def test_lists(self):
        expected_allStrs = set( pygsti.construction.gatestring_list( 
                [(),('Gx',),('Gy',),('Gx','Gx'),('Gx','Gy'),('Gy','Gx'),('Gy','Gy')] ))
        allStrs = pygsti.construction.list_all_gatestrings( ('Gx','Gy'), 0,2 )
        self.assertEqual( set(allStrs), expected_allStrs)

        allStrs = list(pygsti.construction.gen_all_gatestrings( ('Gx','Gy'), 0,2 ))
        #self.assertEqual( set(allStrs), set([(),('Gx',),('Gy',),('Gx','Gx'),('Gx','Gy'),('Gy','Gx'),('Gy','Gy')]))
        #self.assertEqual( set(allStrs), set([(),('Gx',),('Gy',),('Gx','Gy'),('Gy','Gx')]))

        randStrs = pygsti.construction.list_random_gatestrings_onelen( ('Gx','Gy','Gz'), 2, 3)
        self.assertEqual( len(randStrs), 3 )
        self.assertTrue( all( [len(s)==2 for s in randStrs] ) )

        partialStrs = pygsti.construction.list_partial_strings( ('G1','G2','G3') )
        self.assertEqual( partialStrs, [ (), ('G1',), ('G1','G2'), ('G1','G2','G3') ] )


    def test_python_string_conversion(self):
        gs = pygsti.obj.GateString(None, stringRepresentation="Gx^3Gy^2GxGz")

        pystr = gs.to_pythonstr( ('Gx','Gy','Gz') )
        self.assertEqual( pystr, "AAABBAC" )
        
        gs2_tup = pygsti.obj.GateString.from_pythonstr( pystr, ('Gx','Gy','Gz') )
        self.assertEqual( gs2_tup, tuple(gs) )

    def test_std_lists(self):
        gateLabels = ['Gx','Gy']
        strs = pygsti.construction.gatestring_list( [('Gx',),('Gy',),('Gx','Gx')] )
        germs = pygsti.construction.gatestring_list( [('Gx','Gy'),('Gy','Gy')] )

        # LSGST
        maxLens = [0,1,2]
        lsgstLists = pygsti.construction.make_lsgst_lists(
            gateLabels, strs, strs, germs, maxLens, fidPairs=None,
            truncScheme="whole germ powers")

        lsgstLists2 = pygsti.construction.make_lsgst_lists(
            gateLabels, strs, strs, germs, maxLens, fidPairs=None,
            truncScheme="truncated germ powers")

        lsgstLists3 = pygsti.construction.make_lsgst_lists(
            gateLabels, strs, strs, germs, maxLens, fidPairs=None,
            truncScheme="length as exponent")

        maxLens = [1,2]
        lsgstLists4 = pygsti.construction.make_lsgst_lists(
            gateLabels, strs, strs, germs, maxLens, fidPairs=None,
            truncScheme="whole germ powers", nest=False)

        lsgstExpList = pygsti.construction.make_lsgst_experiment_list(
            gateLabels, strs, strs, germs, maxLens, fidPairs=None,
            truncScheme="whole germ powers")

        with self.assertRaises(ValueError):
            pygsti.construction.make_lsgst_lists(
                gateLabels, strs, strs, germs, maxLens, fidPairs=None,
                truncScheme="foobar")


        

        # ELGST
        maxLens = [0,1,2]
        elgstLists = pygsti.construction.make_elgst_lists(
            gateLabels, germs, maxLens, truncScheme="whole germ powers")

        maxLens = [1,2]
        elgstLists2 = pygsti.construction.make_elgst_lists(
            gateLabels, germs, maxLens, truncScheme="whole germ powers",
            nest=False)        

        elgstExpLists = pygsti.construction.make_elgst_experiment_list(
            gateLabels, germs, maxLens, truncScheme="whole germ powers")

        with self.assertRaises(ValueError):
            pygsti.construction.make_elgst_lists(
                gateLabels, germs, maxLens, truncScheme="foobar")



        #TODO: check values here

    def test_gatestring_object(self):
        s1 = pygsti.obj.GateString( ('Gx','Gx'), "Gx^2" )
        s2 = pygsti.obj.GateString( s1, "Gx^2" )
        s3 = s1 + s2
        s4 = s1**3
        s5 = s4
        s6 = copy.copy(s1)
        s7 = copy.deepcopy(s1)

        self.assertEqual( s1, ('Gx','Gx') )
        self.assertEqual( s2, ('Gx','Gx') )
        self.assertEqual( s3, ('Gx','Gx','Gx','Gx') )
        self.assertEqual( s4, ('Gx','Gx','Gx','Gx','Gx','Gx') )
        self.assertEqual( s5, s4 )
        self.assertEqual( s1, s6 )
        self.assertEqual( s1, s7 )
        
        b1 = s1 < s2
        b2 = s1 > s2

        with self.assertRaises(ValueError):
            s1[0] = 'Gx' #cannot set items - like a tuple they're read-only
        with self.assertRaises(ValueError):
            bad = s1 + ("Gx",) #can't add non-GateString to gatestring
        with self.assertRaises(ValueError):
            pygsti.obj.GateString( ('Gx','Gx'), "GxGy" ) #mismatch 
        with self.assertRaises(ValueError):
            pygsti.obj.GateString( None )

        w1 = pygsti.obj.WeightedGateString( ('Gx','Gy'), "GxGy", weight=0.5)
        w2 = pygsti.obj.WeightedGateString( ('Gy',), "Gy", weight=0.5)
        w3 = w1 + w2
        w4 = w2**2
        w5 = s1 + w2
        w6 = w2 + s1
        w7 = copy.copy(w1)

        with self.assertRaises(ValueError):
            w1 + ('Gx',) #can only add to other GateStrings
        with self.assertRaises(ValueError):
            ('Gx',) + w1 #can only add to other GateStrings

        w1_str = str(w1)
        w1_repr = repr(w1)
        x = w1[0]
        x2 = w1[0:2]
        
        self.assertEqual( w1, ('Gx','Gy') ); self.assertEqual(w1.weight, 0.5)
        self.assertEqual( w2, ('Gy',) ); self.assertEqual(w2.weight, 0.5)
        self.assertEqual( w3, ('Gx','Gy','Gy') ); self.assertEqual(w3.weight, 1.0)
        self.assertEqual( w4, ('Gy','Gy') ); self.assertEqual(w4.weight, 0.5)
        self.assertEqual( w5, ('Gx','Gx','Gy') ); self.assertEqual(w5.weight, 0.5)
        self.assertEqual( w6, ('Gy','Gx','Gx') ); self.assertEqual(w6.weight, 0.5)
        self.assertEqual( x, 'Gx' )
        self.assertEqual( x2, ('Gx','Gy') )
        self.assertEqual( w1, w7)

        c1 = pygsti.objects.gatestring.CompressedGateString(s1)
        s1_expanded = c1.expand()
        self.assertEqual(s1,s1_expanded)

        with self.assertRaises(ValueError):
            pygsti.objects.gatestring.CompressedGateString( ('Gx',) ) #can only create from GateStrings
        
        

        
        
if __name__ == "__main__":
    unittest.main(verbosity=2)
