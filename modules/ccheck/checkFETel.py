# -*- coding: cp1252 -*-
#============================================================================== 				
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	CCheck (Consistency Check)
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Functions for consistency checking of data
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Claudia Vannoni 	17/04/2008
#                           
#       Changes in last update:
#       
#
#	
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	www.energyxperts.net / info@energyxperts.net
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#============================================================================== 				

EPSILON = 1.e-3     # required accuracy for function "isequal"
INFINITE = 1.e99    # numerical value assigned to "infinite"

DEBUG = False
TEST = True
TESTCASE = 3

from math import *
from ccheckFunctions import *

#------------------------------------------------------------------------------
class CheckFETel():
#------------------------------------------------------------------------------
#   Carries out consistency checking for process k
#------------------------------------------------------------------------------

    def __init__(self):     #function that is called at the beginning when object is created

# assign a variable to all intermediate values needed
        
        self.ElectricityNet = CCPar("ElectricityNet") 
        self.ElectricityNet1 = CCPar("ElectricityNet1")
        self.FECel1 = CCPar("FECel1")
        self.FECel2 = CCPar("FECel2")
        self.FECel = CCPar("FECel")
        self.FEOel1 = CCPar("FEOel1")
        self.FEOel = CCPar("FEOel")
        self.FETel1 = CCPar("FETel1")
        self.FETel2 = CCPar("FETel2")
        self.FETel = CCPar("FETel")
        
        if TEST:
            self.importTestData()
        else:
#            self.importData()
            pass

    def importTestData(self):  #later on should import data from SQL. now simply sets to some value

# Old Step 0: Assign all a priori known values to variables.
#   -> here manually. in tool values substituted by import from SQL

        if TESTCASE == 2:       #original test case Kla - first version of FECel
            self.ElectricityGen = CCPar(" ElectricityGen")
            self.ElectricityGen.val = 50
            self.ElectricityGen.sqerr = 0.01

            self.ElectricitySales = CCPar("ElectricitySales")
            self.ElectricitySales.val = 15
            self.ElectricitySales.sqerr = 0.01
            
            self.ElectricityTotYear = CCPar("ElectricityTotYear")
            self.ElectricityTotYear.val = 400
            self.ElectricityTotYear.sqerr = 0.01

            #self.ElProd electricty required per product, has to be defined as vector

            self.ElectricityMotors = CCPar("ElectricityMotors")
            self.ElectricityMotors.val = 2
            self.ElectricityMotors.sqerr = 0.02

            self.ElectricityChem = CCPar("ElectricityChem")
            self.ElectricityChem.val = 0.5
            self.ElectricityChem.sqerr = 0.02

            self.ElectricityLight = CCPar("ElectricityLight")
            self.ElectricityLight.val = 2.5
            self.ElectricityLight.sqerr = 0.0201

            self.ElectricityRef = CCPar("ElectricityRef")
            self.ElectricityRef.val = 100
            self.ElectricityRef.sqerr = 0.015

            self.ElectricityAC = CCPar("ElectricityAC")
            self.ElectricityAC.val = 130
            self.ElectricityAC.sqerr = 0.001

            self.ElectricityThOther = CCPar("ElectricityThOther")
            self.ElectricityThOther.val = 200
            self.ElectricityThOther.sqerr = 0.05

        elif TESTCASE == 3:       #Test case for overall algoritm
            self.ElectricityGen = CCPar(" ElectricityGen")
            self.ElectricityGen.val = 0.0
            self.ElectricityGen.sqerr = 0.0

            self.ElectricitySales = CCPar("ElectricitySales")
            self.ElectricitySales.val = 0.0
            self.ElectricitySales.sqerr = 0.0
            
            self.ElectricityTotYear = CCPar("ElectricityTotYear")
            self.ElectricityTotYear.val = 5000
            self.ElectricityTotYear.sqerr = 0.001

            #self.ElProd electricty required per product, has to be defined as vector

            self.ElectricityMotors = CCPar("ElectricityMotors")
            self.ElectricityMotors.val = None
            self.ElectricityMotors.sqerr = INFINITE

            self.ElectricityChem = CCPar("ElectricityChem")
            self.ElectricityChem.val = 0.0
            self.ElectricityChem.sqerr = 0.0

            self.ElectricityLight = CCPar("ElectricityLight")
            self.ElectricityLight.val = None
            self.ElectricityLight.sqerr = INFINITE

            self.ElectricityRef = CCPar("ElectricityRef")
            self.ElectricityRef.val = 0.0
            self.ElectricityRef.sqerr = 0.0

            self.ElectricityAC = CCPar("ElectricityAC")
            self.ElectricityAC.val = None
            self.ElectricityAC.sqerr = INFINITE

            self.ElectricityThOther = CCPar("ElectricityThOther")
            self.ElectricityThOther.val = None
            self.ElectricityThOther.sqerr = INFINITE

        else:
            print "CheckFETel: WARNING - don't have input data for this test case no. ",TESTCASE

        if DEBUG:
            self.showAllFETel()

    def showAllFETel(self):
        print "====================="
        self.ElectricityNet.show()
        self.ElectricityNet1.show()
        self.ElectricityGen.show()
        self.ElectricitySales.show()
        self.ElectricityTotYear.show()
        #self.ElProd.show()
        self.FECel1.show()
        self.FECel2.show()
        self.FECel.show()
        self.ElectricityMotors.show()
        self.ElectricityChem.show()
        self.ElectricityLight.show()
        self.ElectricityRef.show()
        self.ElectricityAC.show()
        self.ElectricityThOther.show()
        self.FEOel1.show()
        self.FEOel.show()
        self.FETel1.show()
        self.FETel2.show()
        self.FETel.show()
                  
                
        print "====================="
    
    def check(self):     #function that is called at the beginning when object is created
        for n in range(3):

            if DEBUG in ["ALL"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

            if DEBUG in ["ALL"]:
                print "Step 1: calculating from left to right (CALC)"
            
            self.ElectricityNet1 = calcDiff("ElectricityNet1",self.ElectricityGen,self.ElectricitySales)
            self.FECel1 = calcSum("FECel1",self.ElectricityNet,self.ElectricityTotYear)
            #self.FECel2 = calcRowSum(name,row,m)self.ElProd
            self.FEOel1 = calcSum3("FEOel1",self.ElectricityMotors,self.ElectricityChem,self.ElectricityLight)
            self.FETel1 = calcDiff("FETel1",self.FECel,self.FEOel)
            self.FETel2 = calcSum3("FETel2",self.ElectricityRef,self.ElectricityAC,self.ElectricityThOther)

                      
            if DEBUG in ["ALL"]:
                self.showAllFETel()

# Step 2: Cross check the variables

                print "Step 2: cross checking"

            ccheck1(self.ElectricityNet,self.ElectricityNet1)
#            ccheck2(self.FECel,self.FECel1,self.FECel2)
            ccheck1(self.FECel,self.FECel1)
            ccheck1(self.FEOel,self.FEOel1)
            ccheck2(self.FETel,self.FETel1,self.FETel2)
                          

            if DEBUG in ["ALL"]:
                self.showAllFETel()

# Step 3: Adjust the variables (inverse of calculation routines)

                print "Step 3: calculating from right to left (ADJUST)"

            adjustSum3(self.FETel2,self.ElectricityRef,self.ElectricityAC,self.ElectricityThOther)
            adjustDiff(self.FETel1,self.FECel,self.FEOel)
            adjustSum3(self.FEOel1,self.ElectricityMotors,self.ElectricityChem,self.ElectricityLight)
            #adjRowSum(name,y,row,m) self.FECel2
            adjustSum(self.FECel1,self.ElectricityNet,self.ElectricityTotYear)
            adjustDiff(self.ElectricityNet1,self.ElectricityGen,self.ElectricitySales)

                        
            if DEBUG in ["ALL"]:
                self.showAllFETel()

# Step 4: Adjust the variables (inverse of calculation routines)

                print "Step 3: calculating from right to left (ADJUST)"


            ccheck1(self.ElectricityNet,self.ElectricityNet1)
    #            ccheck2(self.FECel,self.FECel1,self.FECel2)
            ccheck1(self.FECel,self.FECel1)
            ccheck1(self.FEOel,self.FEOel1)
            ccheck2(self.FETel,self.FETel1,self.FETel2)
                          
            if DEBUG in ["ALL"]:
                self.showAllFETel()
        

# End of the cycle. Last print in DEBUG mode


        if DEBUG in ["ALL","BASIC"]:
            self.showAllFETel()


#==============================================================================

if __name__ == "__main__":
    
    ccFETel = CheckFETel()       # creates an instance of class CCheck
    ccFETel.check()
    
#==============================================================================
