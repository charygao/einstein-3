# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleBB (Boilers and Burners)
#			
#------------------------------------------------------------------------------
#			
#	Module for calculation of boilers
#
#==============================================================================
#
#	Version No.: 0.18
#	Created by: 	    Hans Schweiger	11/03/2008
#	Last revised by:    Tom Sobota          15/03/2008
#                           Enrico Facci /
#                           Hans Schweiger      24/03/2008
#                           Tom Sobota           1/04/2008
#                           Hans Schweiger      03/04/2008
#                           Enrico Facci        09/04/2008
#                           Stoyan Danov        16/04/2008
#                           Enrico Facci        24/04/2008
#                           Enrico Facci        05/05/2008
#                           Hans Schweiger      06/05/2008
#                           Enrico Facci        07/05/2008
#                           Enrico Facci        13/05/2008
#                           Hans Schweiger      15/04/2008
#                           Enrico Facci        26/05/2008
#                           Enrico Facci        06/06/2008
#                           Hans Schweiger      02/07/2008
#                           Hans Schweiger      03/07/2008
#
#       Changes to previous version:
#       2008-3-15 Added graphics functionality
#       2008-03-24  Incorporated "calculateEnergyFlows" from Enrico Facci
#                   - adapted __init__ and plots similar to moduleHP
#       1/04/2008   Adapted to new graphics interfase using numpy
#       03/04/2008  Link to modules via Modules
#       09/04/2008  addEquipmentDummy, setEquipmentFromDB
#       16/04/2008  setEquipmentFromDB: aranged & tested (it was indented incorrectly), 
#                   3 functions copied from moduleHP: getEqId,deleteEquipment,deleteFromCascade ->
#                   -> In order to activate deleteEquipment: screenEquipments should be arranged before
#                   (BBList in alalogy with HPList), see moduleHP
#       24/04/2008  functions added: designAssistant,automDeleteBoiler, designBB80, designBB140, designBBmaxTemp
#                   findmaxTemp. screenEquipments arranged in analogy with moduleHP.
#                   (HS: some clean-up of non-used functions and old comments)
#       05/05/2008  functions added: sortBoiler, redundancy, selectBB. Changes in designAssistant and designBB.
#       06/05/2008  Changes marked with ###HS in the text:
#                   - elimination of table cgenerationhc (now is in qgenerationhc)
#                   Status.int no longer used. substituted by Status.int
#                   Functions __init__, initPanel, updatePanel and
#                   screenEquipments modified in symmetry with moduleHP
#                   Function "setEquipmentFromDB" modified
#                   Bug corrections:    status.xxx -> Status.xxx
#                                       k=o -> k=0 (sortBoiler)
#                                       Status.ints -> Status.int (sortBoiler)
#                                       cascade[k].equipeType -> cascade[k]["equipeType"] (sortBoiler)
#                                       cascade[k].equipeID -> cascade[k]["equipeID"] (sortBoiler)
#                                       self.equipment -> self.equipments (sortBoiler)
#       07/05/2008  sortBoiler modified and tested.
#       12/05/2008  function added: findBiggerBB. some changes in designAssistant, selectBB, designBB80 and calculateEnergyFlows.
#       16/05/2008  some small notes marked with ###HS2008-05-16
#                   (by the way eliminated some old comments that are no longer useful)
#                   => changes in updatePanel
#                   => "userDefinedPars"-Functions copied from HP (not working yet)
#       26/05/2008 some changes in functions sortBoiler, designAssistant, redundancy                   
#       06/06/2008 implemented function updatePannel. Some small changes in designAsssistant
#       27/06/2008: HS small bug-fixes: - equipment screening moved from __init__ to initPanel.
#                                       - PowerSumMaxtemp -> PowerSumTmax
#                   Security feature: where's no table uheatpump, one is created
#       02/07/2008: HS Calulation of FETFuel_j,FETel_j and HPerYearEq added to
#                       calculateEnergyFlows
#       03/07/2008ff: HS  Call to updatePanel eliminated in initPanel
#                       change in setting of cascadeIndex in screenEquipments
#                       some bug-fixing and clean-up
#                       boiler efficiency set as fraction of 1
#                       introduction of several security items and bug-fixes
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

from sys import *
from math import *
from numpy import *
import copy

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP
from einstein.modules.constants import *
from einstein.modules.messageLogger import *

#============================================================================== 
#============================================================================== 
class ModuleBB(object):
#============================================================================== 
#============================================================================== 

    BBList = []
    
    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel

        self.DB = Status.DB
        self.sql = Status.SQL

        self.neweqs = 0 #new equips added
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

        if Status.int.cascadeUpdateLevel < 0:
            Status.int.initCascadeArrays(0)
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------

#............................................................................................
# get list of equipments and boilers in the system
# and update the energetic calculation up to the level needed for representation

        (BBList,BBTableDataList) = self.screenEquipments()

        if Status.int.cascadeUpdateLevel < self.cascadeIndex:
            Status.mod.moduleEnergy.runSimulation(self.cascadeIndex)

#............................................................................................
# 1. List of equipments

        matrix = []
        for row in BBTableDataList:
            matrix.append(row)

        data = array(matrix)

        Status.int.setGraphicsData('BB Table',data)
#............................................................................................
# 2. Preparing data
        self.findmaxTemp(Status.int.QD_T)
        print "maximum temperature",self.maxTemp
        PowerSum80=0
        PowerSum140=0
        PowerSumTmax=0

        if self.maxTemp > 80:
            if self.maxTemp>160: # the minimum temperature difference is now setted at 20�C but could even be a parameter
                for i in BBList:
                    bbs = Status.DB.qgenerationhc.QGenerationHC_ID[i["equipeID"]]
                    if len(bbs) > 0:
                        bb = bbs[0]
                        if bb.TMaxSupply > 80 and bb.TMaxSupply <= 140:
                            PowerSum140 += i["equipePnom"]
                        if bb.TMaxSupply > 140:
                            PowerSumTmax += i["equipePnom"]
            else :
                for i in BBList:
                    bbs = Status.DB.qgenerationhc.QGenerationHC_ID[i["equipeID"]]
#                    bbs = self.equipments.QGenerationHC_ID[i["equipeID"]]  #HS2008-07-03: changed. gave some strange SQL error
                    if len(bbs) > 0:
                        bb = bbs[0]
                        if bb.TMaxSupply > 80:
                            PowerSumTmax += i["equipePnom"]
                            
            for i in BBList:
                bbs = Status.DB.qgenerationhc.QGenerationHC_ID[i["equipeID"]]
                if len(bbs) > 0:
                    bb = bbs[0]
                    if bb.TMaxSupply <=80:
                        PowerSum80 += i["equipePnom"]
        else:
            for i in BBList:
               PowerSumTmax += i["equipePnom"] 

        if len(BBList)==0:
            index=max(len(self.equipments),1)     #HS2008-07-06. bug-fix. assures that index >= 0
                                                  #even if there's NO equipment at all !!!
        else:
            bbs = Status.DB.qgenerationhc.QGenerationHC_ID[BBList[0]["equipeID"]]
            if len(bbs) > 0:
                bb = bbs[0]
                index = bb.CascadeIndex

        QD80C = Status.int.QD_Tt_mod[index-1][int(80/Status.TemperatureInterval+0.5)]
        QD80C.sort(reverse=True)

        if self.maxTemp>160: # the minimum temperature difference is now setted at 20�C but could even be a parameter
            QD140C=Status.int.QD_Tt_mod[index-1][int(140/Status.TemperatureInterval)]
            QD140C.sort(reverse=True)
        else:
            QD140C=[]
            for i in range(len(QD80C)):
                QD140C.append(0)

        iT_maxTemp = int(self.maxTemp/Status.TemperatureInterval)
        QDmaxTemp=Status.int.QD_Tt_mod[index-1][iT_maxTemp]
        QDmaxTemp.sort(reverse=True)

#............................................................................................
# 2. XY Plot
        TimeIntervals=[]
        for it in range(Status.Nt+1):
            TimeIntervals.append(1.0*(it+1))

        try:

            if self.maxTemp>160:
                
                Status.int.setGraphicsData('BB Plot',[TimeIntervals,
                                                            QD80C,
                                                            QD140C,
                                                            QDmaxTemp])
            elif self.maxTemp>80:
                Status.int.setGraphicsData('BB Plot',[TimeIntervals,
                                                            QD80C,
                                                            QD140C,
                                                            QDmaxTemp])
            else:
                Status.int.setGraphicsData('BB Plot',[TimeIntervals,
                                                            QD80C])
        except:
            logDebug("ModuleBB (updatePanel): problems sending data for BB Plot")

#............................................................................................
# 3. Configuration design assistant

        config = self.getUserDefinedPars()
        Status.int.setGraphicsData('BB Config',config)
        
#............................................................................................
# 4. additional information (Info field right side of panel)

        info = []
        info.append(10)  #first value to be displayed
        
        info.append(max(0,(QD80C[0]-PowerSum80)))  #power for T-level
        
        if self.maxTemp>160:
            info.append(max(0,(QD140C[0]-QD80C[0]-PowerSum140)))  #power for T-level
            info.append(max(0,(QDmaxTemp[0]-QD140C[0]-PowerSumTmax)))  #power for T-level
        else:
            info.append(0)
            if self.maxTemp>80:
                info.append(max(0,(QDmaxTemp[0]-QD80C[0]-PowerSumTmax)))  #power for T-level
            else:
                info.append(0)


        Status.int.setGraphicsData('BB Info',info)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def getUserDefinedPars(self):
#------------------------------------------------------------------------------
#   gets the user defined data from UHeatPump and stores it to interfaces to be shown in HP panel
#------------------------------------------------------------------------------

        urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

        if len(urows) == 0:
            print 'getUserDefinedParamBB: Status.PId =', Status.PId, 'Status.ANo =', Status.ANo, 'not defined'
            print 'Error: confusion in PId and ANo'
            dummy = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo} 
            Status.DB.uheatpump.insert(dummy)

            maintainExisting = True
            config = [False,10,True,"Natural Gas",100,500,85]            
            Status.int.setGraphicsData('BB Config',config)

            self.setUserDefinedPars()

        else:
            u = urows[0]
            config = [u.BBMaintain,
                      u.BBSafety,
                      u.BBRedundancy,
                      u.BBFuelType,
                      u.BBHOp,
                      u.BBPmin,
                      u.BBEff]
            print "ModuleBB (getUserDefinedPars): config = ",config
        return config

#------------------------------------------------------------------------------
    def setUserDefinedPars(self):
#------------------------------------------------------------------------------

        config = Status.int.GData['BB Config']

        urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
        
        if len(urows)==0:
            print "ModuleBB(setUserDefinedParamHP): corrupt data base - no entry for uheatpump under current ANo"
            dummy = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo} 
            Status.DB.uheatpump.insert(dummy)
            urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
            
        u = urows[0]

#        row.MaintainExisting = UDList[0] # to add in UHeatPump
        u.BBMaintain = config[0]
        u.BBSafety = config[1]
        u.BBRedundancy = config[2]
        u.BBFuelType = config[3]
        u.BBHOp = config[4]
        u.BBPmin = config[5]
        u.BBEff = config[6]

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def screenEquipments(self,setIndex = True):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#------------------------------------------------------------------------------

        self.equipments = Status.prj.getEquipments()
        Status.int.getEquipmentCascade()
        self.NEquipe = len(self.equipments)

        self.BBList = []
        maxIndex = self.NEquipe
        index = 0
        for row in Status.int.cascade:
            index += 1
            if getEquipmentClass(row["equipeType"]) == "BB":
                self.BBList.append(row)
                maxIndex = index

        if setIndex == True:
            self.cascadeIndex = maxIndex

        BBTableDataList = []
        for row in Status.int.EquipTableDataList:
            if getEquipmentClass(row[3]) == "BB":
                BBTableDataList.append(row)

        #screen list and substitute None with "not available"
        for i in range(len(BBTableDataList)):
            for j in range(len(BBTableDataList[i])):
                if BBTableDataList[i][j] == None:
                    BBTableDataList[i][j] = 'not available'        

        return (self.BBList,BBTableDataList)
        

        
#------------------------------------------------------------------------------
    def getEqId(self,rowNo):
#------------------------------------------------------------------------------
#   gets the EqId from the rowNo in the BBList
#------------------------------------------------------------------------------

        BBId = self.BBList[rowNo]["equipeID"]
        return BBId

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def deleteEquipment(self,rowNo,automatic=False):
#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------

        if automatic == False:
            if rowNo == None:   #indicates to delete last added equipment dummy
                BBid = self.dummyEqId
            else:
            #--> delete BB from the equipment list under current alternative #from C&QGenerationHC under ANo
                BBid = self.getEqId(rowNo)
                print "Module BB (delete): id to be deleted = ",BBid
        else:
            BBid= rowNo
            print "Module BB (delete automaticly): id to be deleted = ",BBid
        
        Status.prj.deleteEquipment(BBid)
        self.screenEquipments()

#------------------------------------------------------------------------------
    def addEquipmentDummy(self):
#------------------------------------------------------------------------------
#       adds a new dummy equipment to the equipment list and returns the
#       position in the cascade 
#------------------------------------------------------------------------------

        self.equipe = Status.prj.addEquipmentDummy()
        self.dummyEqId = self.equipe.QGenerationHC_ID

        self.neweqs += 1 #No of last equip added
        NewEquipmentName = "New boiler %s"%(self.neweqs)

        equipeData = {"Equipment":NewEquipmentName,"EquipType":"Boiler (specify subtype)"}
        self.equipe.update(equipeData)
        Status.SQL.commit()

        self.screenEquipments()
        self.cascadeIndex = self.NEquipe
        
        return(self.equipe)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def setEquipmentFromDB(self,equipe,modelID):
#------------------------------------------------------------------------------
#   takes an equipment from the data base and stores it under a given Id in
#   the equipment data base
#------------------------------------------------------------------------------

        model = self.DB.dbboiler.DBBoiler_ID[modelID][0]

        if model.BBPnom != None: equipe.update({"HCGPnom":model.BBPnom})
        
        if model.BBEfficiency != None:
            if model.BBEfficiency > 1.3 and model.BBEfficiency < 130.0:
                logTrack("ModuleBB: Efficiency data should be stored internally as fractions of 1")
                eff = model.BBEfficiency/100.0
                model.update({"BBEfficiency":eff})
            else:
                eff = model.BBEfficiency
            equipe.update({"HCGTEfficiency":eff})
            
        if model.BoilerTemp != None: equipe.update({"TMaxSupply":model.BoilerTemp})
        if model.BoilerManufacturer != None: equipe.update({"Manufact":model.BoilerManufacturer})
        if model.BoilerModel != None: equipe.update({"Model":model.BoilerModel})
        equipe.update({"EquipType":getEquipmentType("BB",model.BoilerType)})
        equipe.update({"NumEquipUnits":1})
        if model.BoilerType != None: equipe.update({"EquipTypeFromDB":model.BoilerType})
        if model.DBBoiler_ID != None: equipe.update({"EquipIDFromDB":model.DBBoiler_ID})
        Status.SQL.commit()

        self.calculateEnergyFlows(equipe,self.cascadeIndex)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,cascadeIndex):
#------------------------------------------------------------------------------
#   calculates the energy flows in the equipment identified by "cascadeIndex"
#------------------------------------------------------------------------------

        if Status.int.cascadeUpdateLevel < (cascadeIndex - 1):
            logDebug("ModuleBB (calculateEnergyFlows): cannot calulate without previously updating the previous levels")
            Status.mod.moduleEnergy.runSimulation(last=(cascadeIndex-1))
            Status.int.extendCascadeArrays(cascadeIndex)

        if cascadeIndex > 0 and cascadeIndex <= Status.NEquipe:
            logTrack("ModuleBB (calculateEnergyFlows): starting (cascade no: %s)"%cascadeIndex)
        else:
            logError("ModuleBB (calculateEnergyFlows): cannot simulate index %s: out of cascade [%s]"%\
                     (cascadeIndex,Status.NEquipe))
            return
#..............................................................................
# get equipment data from equipment list in SQL

        BBModel = equipe.Model
        BBType = equipe.EquipType
        PNom = equipe.HCGPnom
        COPh_nom = equipe.HCGTEfficiency
        TMax = equipe.TMaxSupply
        EquipmentNo = equipe.EqNo

        if PNom is None:
            PNom = 0.0
            logWarning("ModuleBB (calculateEnergyFlows): No nominal power specified for equipe no. %s"%\
                 (EquipmentNo))

        if TMax is None:
            TMax = INFINITE
            logDebug("ModuleBB (calculateEnergyFlows): no Tmax specified for equipe no. %s"%EquipmentNo)
  
        logTrack("ModuleBB (calculateEnergyFlows): Model = %s Type = %s PNom = %s"%\
                 (BBModel,BBType,PNom))

#..............................................................................
# get demand data for CascadeIndex/EquipmentNo from Interfaces
# and create arrays for storing heat flow in equipment

        QD_Tt = copy.deepcopy(Status.int.QD_Tt_mod[cascadeIndex-1])
        QA_Tt = copy.deepcopy(Status.int.QA_Tt_mod[cascadeIndex-1])
        
        USHj_Tt = Status.int.createQ_Tt()
        USHj_T = Status.int.createQ_T()

        
        QHXj_Tt = Status.int.createQ_Tt()
        QHXj_T = Status.int.createQ_T()

#..............................................................................
# Start hourly loop

        USHj = 0
        QHXj = 0
        HPerYear = 0
        QD = 0

        for it in range(Status.Nt):

#..............................................................................
# Calculate heat delivered by the given equipment for each time interval

            for iT in range (Status.NT+2):
                QHXj_Tt[iT][it] = 0     #for the moment no waste heat considered
                
                if TMax >= Status.int.T[iT] :   #TMax is the max operating temperature of the boiler 
                    USHj_Tt[iT][it] = min(QD_Tt[iT][it],PNom*Status.TimeStep)     #from low to high T
                    
                else:
                    if (iT > 0):
                        USHj_Tt[iT][it] = USHj_Tt[iT-1][it]     #no additional heat supply at high temp.
                    else:
                        USHj_Tt[iT][it] = 0
                        
                QD_Tt[iT][it]= QD_Tt[iT][it]- USHj_Tt[iT][it]
                
            USHj += USHj_Tt[Status.NT+1][it]
            if USHj_Tt[Status.NT+1][it]>0:
                HPerYear += Status.TimeStep

            QD += QD_Tt[Status.NT+1][it]

#..............................................................................
# End of year reached. Store results in interfaces
       
# remaining heat demand and availability for next equipment in cascade
        Status.int.QD_Tt_mod[cascadeIndex] = QD_Tt
        Status.int.QD_T_mod[cascadeIndex] = Status.int.calcQ_T(QD_Tt)
        Status.int.QA_Tt_mod[cascadeIndex] = QA_Tt
        Status.int.QA_T_mod[cascadeIndex] = Status.int.calcQ_T(QA_Tt)

# heat delivered by present equipment

        Status.int.USHj_Tt[cascadeIndex-1] = USHj_Tt
        Status.int.USHj_T[cascadeIndex-1] = Status.int.calcQ_T(USHj_Tt)
        Status.int.USHj_t[cascadeIndex-1] = copy.deepcopy(USHj_Tt[Status.NT+1])

# waste heat absorbed by present equipment

        Status.int.QHXj_Tt[cascadeIndex-1] = QHXj_Tt
        Status.int.QHXj_T[cascadeIndex-1] = Status.int.calcQ_T(QHXj_Tt)
        Status.int.QHXj_t[cascadeIndex-1] = copy.deepcopy(QHXj_Tt[Status.NT+1])

        logTrack("ModuleBB (calculateEnergyFlows): Total energy supplied by equipment %s MWh"%(USHj*Status.EXTRAPOLATE_TO_YEAR))
        logTrack("ModuleBB (calculateEnergyFlows): Total waste heat input  %s MWh"%(QHXj*Status.EXTRAPOLATE_TO_YEAR))

        Status.int.cascadeUpdateLevel = cascadeIndex

#........................................................................
# Global results (annual energy flows)

        Status.int.USHj[cascadeIndex-1] = USHj*Status.EXTRAPOLATE_TO_YEAR

        if COPh_nom > 0:
            FETFuel_j = USHj*Status.EXTRAPOLATE_TO_YEAR/COPh_nom
            print "ModuelBB (cEF): converting USH [%s] to FET [%s]"%\
                  (USHj*Status.EXTRAPOLATE_TO_YEAR,FETFuel_j*Status.EXTRAPOLATE_TO_YEAR)
        else:
            FETFuel_j = 0.0
            showWarning("Strange boiler with COP = 0.0")

        FETel_j = 0.0
        
        Status.int.FETFuel_j[cascadeIndex-1] = FETFuel_j
        Status.int.FETel_j[cascadeIndex-1] = FETel_j
        Status.int.HPerYearEq[cascadeIndex-1] = HPerYear*Status.EXTRAPOLATE_TO_YEAR
        
        logMessage("Boiler: eq.no.:%s energy flows [MWh] USH: %s FETFuel: %s FETel: %s QD: %s HPerYear: %s "%\
                   (equipe.EqNo,\
                    USHj*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
                    FETFuel_j*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
                    FETel_j*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
                    QD*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
                    HPerYear*Status.EXTRAPOLATE_TO_YEAR/1000.0))
        return USHj    


#==============================================================================

 
#------------------------------------------------------------------------------
    def sortBoiler (self): 
#------------------------------------------------------------------------------
#   moove all the boilers to the end of the cascade.
#  sorts boilers by temperature and by efficiency
#------------------------------------------------------------------------------
#first bring all your boilers in a listing for easier access

        boilerList = []
        for i in range(len(Status.int.cascade)):
            entry = Status.int.cascade[i]
            a=getEquipmentClass(entry["equipeType"])
            if a=="BB":
                eqID = entry["equipeID"]
                equipe = Status.DB.qgenerationhc.QGenerationHC_ID[eqID][0]
                efficiency = equipe.HCGTEfficiency
                temperature = equipe.TMaxSupply
                boilerList.append({"equipeID":eqID,"efficiency":efficiency,"temperature":temperature})

#then reorganise boilerList by efficiencies (maybe there are more intelligent ways to do this, but here's one ...:
# if you want the most efficient on top [n-1] instead on bottom [0], just change the sign of the comparison from > to <

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if boilerList[j]["efficiency"] > boilerList[i]["efficiency"]:
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi
                    
#then reorganise boilerList by temperature levels:
#   first level:

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if boilerList[i]["temperature"] <= 80 and boilerList[j]["temperature"]>80:
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi

#   second level:

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if 80 < boilerList[i]["temperature"] <= 140 and (boilerList[j]["temperature"]<=80 or boilerList[j]["temperature"]>140):
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi

#   second level:

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if  boilerList[i]["temperature"] > 140 and  boilerList[j]["temperature"]<=140:
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi


#then move consecutively to the bottom of the cascade (move the one last, which you finally want to have at the bottom

        for i in range(len(boilerList)):
            eqID = boilerList[i]["equipeID"]
            equipe = Status.DB.qgenerationhc.QGenerationHC_ID[eqID][0]
            cascadeIndex = equipe.CascadeIndex
            if cascadeIndex < Status.int.NEquipe:
                Status.mod.moduleHC.cascadeMoveToBottom(cascadeIndex)

#find the position in the cascade of the first and last boiler of each T level
        a=0
        b=0
        for i in range(len(boilerList)):
            if  boilerList[i]["temperature"] > 80 :
                a+=1
            if  boilerList[i]["temperature"] > 140 :
                b+=1

        self.firstBB = len(Status.int.cascade)-len(boilerList)
        
        self.firstBB140 = len(Status.int.cascade)-a
        if self.maxTemp >140:
            self.firstBBmaxTemp = len(Status.int.cascade)-b
        else:
            self.firstBBmaxTemp =len(Status.int.cascade)-a
        lastBB = len(Status.int.cascade)-1
            
    
#------------------------------------------------------------------------------
    def automDeleteBoiler (self,minEfficencyAccepted=0.80):  #0.80 is a default value for minimum of efficiency
#------------------------------------------------------------------------------
# delete unefficient boiler
#------------------------------------------------------------------------------
        print"entered 'automDeleteBoiler' function" 
        self.screenEquipments()
        automatic=True
        for i in range (len (self.BBList)):
            print "controlling equipe", self.BBList[i]['equipeID']
            eff= Status.DB.qgenerationhc.QGenerationHC_ID[self.BBList[i]['equipeID']][0]['HCGTEfficiency']
            print "efficiency of the boiler number '%s'is:'%s'"%(i,eff)
            print "min efficiency accepted:",minEfficencyAccepted
            if eff < minEfficencyAccepted:
#                 add the fuel criterion: if not biomass,biofuels?,gas methane ->delete ???
                print "Module BB (): id to be deleted = ",self.BBList[i]['equipeID']
                self.deleteEquipment(self.BBList[i]['equipeID'],automatic)# The row number should be passed. is this right? 
                
#------------------------------------------------------------------------------
    def sortDemand(self,T):
#------------------------------------------------------------------------------
#       for each temperature sort the heat demand by power from max to min (the output is a monotonous descending function for each temperature level)
#       function to be implemented
#------------------------------------------------------------------------------
        return QDh_descending

#------------------------------------------------------------------------------
    def findmaxTemp(self,QDa):
#------------------------------------------------------------------------------
#       find the maximum temperature level of the heat demand
#       QDa is the annual heat demand by temperature
#------------------------------------------------------------------------------
        maxTemp=0
        for i in range(Status.NT+1):
            if i>0:
                if QDa[i]>QDa[i-1]:
                    self.maxTemp=Status.TemperatureInterval*(i+1) #temperatureInterval is defined in status.py
        print "maxtemp=", self.maxTemp


#------------------------------------------------------------------------------
    def redundancy(self):
#------------------------------------------------------------------------------
#       when redundancy is required provides suitable boilers.
#       N.B. the possibility of retriveing deleted boilers is not implemented yet.
#       N.B. The possibility that a boiler with nominal power > than biggerBB is in the list has to be considered.
#------------------------------------------------------------------------------      
        print "dimensioning reduntant boilers"
        self.maxPow80=0
        self.maxPow140=0
        self.maxPowTmax=0
        for k in range(len(Status.int.cascade)):

#HS2008-07-05: here some abbreviations
            equipeID = Status.int.cascade[k]["equipeID"]
            
            if getEquipmentClass(Status.int.cascade[k]["equipeType"]) == "BB":
                equipe = Status.DB.qgenerationhc.QGenerationHC_ID[equipeID][0]
                Pnom = Status.int.cascade[k]["equipePnom"]
                if equipe['TMaxSupply'] <=90 and \
                   Pnom > self.maxPow80:     # TMaxSupply to be sostituted with tthe operating temperature
                    self.maxPow80 = Pnom
                elif 90 < equipe['TMaxSupply'] <= 150 and \
                     Pnom > self.maxPow140:
                    self.maxPow140 = Pnom
                elif Pnom > self.maxPowTmax:
                    self.maxPowTmax = Pnom
                    
        if self.maxPow80>0:
            modelID =self.selectBB(self.maxPow80,80)
            equipe = self.addEquipmentDummy()
            self.setEquipmentFromDB(equipe,modelID)
        if self.maxPow140>0 and self.maxTemp>140:
            modelID =self.selectBB(self.maxPow140,140)
            equipe = self.addEquipmentDummy()
            self.setEquipmentFromDB(equipe,modelID)
        modelID =self.selectBB(self.maxPowTmax,self.maxTemp)
        equipe = self.addEquipmentDummy()
        self.setEquipmentFromDB(equipe,modelID)
        


#------------------------------------------------------------------------------
    def findBiggerBB(self):
#------------------------------------------------------------------------------
# finds the maximum power of the boiler in the DB (for each temperature level)
#------------------------------------------------------------------------------
        sqlQuery="BoilerTemp >='%s' ORDER BY BBPnom DESC" %(self.maxTemp)
        search= Status.DB.dbboiler.sql_select(sqlQuery)
        self.biggermaxTemp=search[0].BBPnom
        sqlQuery="140<=BoilerTemp <170 ORDER BY BBPnom DESC"
        search= Status.DB.dbboiler.sql_select(sqlQuery)
        self.bigger140=search[0].BBPnom
        sqlQuery="80<=BoilerTemp <120 ORDER BY BBPnom DESC"
        search= Status.DB.dbboiler.sql_select(sqlQuery)
        self.bigger80=search[0].BBPnom

#------------------------------------------------------------------------------
    def selectBB(self,Pow,Top):
#------------------------------------------------------------------------------
#  the query should consider the fuel too but at the moment the fuel column doesn't exist in mySQL.
#  we could give the possibility to choose the boiler to the user (in the interactive mode) in a 'selected' list. In this version we take the first  
#  element of the list
#------------------------------------------------------------------------------
        print "entered selectBB module"
        sqlQuery="BoilerTemp >= '%s'AND BBPnom >= '%s' ORDER BY BBPnom ASC" %(Top,Pow)       
        selected = Status.DB.dbboiler.sql_select(sqlQuery)
        for i in range(len(selected)):
            for j in range(i,len(selected)):
                if selected[j].BoilerTemp < selected[i].BoilerTemp:
                    bi = selected[i]
                    bj = selected[j]
                    selected[i] = bj
                    selected[j] = bi

        
        modelID =selected[0].DBBoiler_ID
        print "selectBB: the requested power is:", Pow 
        print "selectBB: the selected boiler ID is:", modelID
#        print "selectBB: the list of boiler is:"
#        print selected
        return modelID
        


            
#------------------------------------------------------------------------------
    def designBB80(self):
#------------------------------------------------------------------------------
#    def designBB80(self,...):
# design a boiler sistem at 80�C
#------------------------------------------------------------------------------
        added=0
        if Status.int.QD_T_mod[self.firstBB][int(80/Status.TemperatureInterval)] >= 0.1*Status.int.QD_T_mod[self.firstBB][int(self.maxTemp/Status.TemperatureInterval)]: #we design boiler at this temperature level only if the demand is bigger than the 10% of the total demand
            print "point AA reached"
            if self.QDh80[0]*self.securityMargin >= self.minPow:
                print "point AB reached"
                if self.QDh80[0]*self.securityMargin>=2*self.minPow:
                    print "point AC reached"
                    if self.QDh80[0]*self.securityMargin < self.QDh80[self.minOpTime]*1.3 \
                       or (self.QDh80[0]*self.securityMargin - self.QDh80[self.minOpTime]) < self.minPow:
                        print "point A reached"
                        modelID = self.selectBB((self.QDh80[0]*self.securityMargin),80)  #select the right bb from the database.                        
#HS line not valid code                        selectBB((QDh_descending[0]*securityMargin),...)  #select the right bb from the database.
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
#HS: elif requires a condition !!!                    elif:
                    else:
                        if self.QDh80[self.minOpTime]>self.bigger80:
                            for i in range (int(self.QDh80[self.minOpTime]/self.bigger80)):
                                print "point B reached"
                                modelID =self.selectBB(self.bigger80,80)
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)
                            added += int(self.QDh80[self.minOpTime]/self.bigger80)*self.bigger80
                        else:
                            print "point C reached"
                            modelID =self.selectBB(self.QDh80[self.minOpTime],80) #aggiungere condizione sul rendimento
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)
                            added += self.DB.dbboiler.DBBoiler_ID[modelID][0].BBPnom
                        print "power of the last bb group added"
                        print added
                        if self.QDh80[0]*self.securityMargin - added >= 2*self.minPow:
                            if self.QDh80[0]*self.securityMargin - added >= self.bigger80:
                                for i in range (int((self.QDh80[0]*self.securityMargin - added)/self.bigger80)):
                                    print "point D reached"
                                    modelID =self.selectBB(self.bigger80,80)
                                    equipe = self.addEquipmentDummy()
                                    self.setEquipmentFromDB(equipe,modelID)
                                print "point E reached"
                                added += int((self.QDh80[0]*self.securityMargin - added)/self.bigger80)*self.bigger80
                                modelID =self.selectBB((self.QDh80[0]*self.securityMargin - added),80)
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)
                            else:
                                print "point F reached"
                                modelID=self.selectBB(((self.QDh80[0]*self.securityMargin - added)/2),80)  #sempre aggiungere anche il criterio di efficienza
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                        else:
#HS: elif requires a condition !!!                        elif:
                            print "point G reached"
                            self.selectBB((self.QDh80[0]*self.securityMargin - added),80)
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                else:
#HS: elif requires a condition !!!                elif:
                    print "point H reached"
                    self.selectBB(self.QDh80[0]*self.securityMargin,80)
                    equipe = self.addEquipmentDummy()
                    self.setEquipmentFromDB(equipe,self.modelID)   #assign model from DB to current equipment in equipment list

        print "point i reached"
        self.sortBoiler()                
                        

                    

#------------------------------------------------------------------------------
    def designBB140(self):
#HS input list has to be defined !!!!    def designBB140(self,...):
#------------------------------------------------------------------------------
# design a boiler sistem at 140�C
#------------------------------------------------------------------------------
        added=0
        if Status.int.QD_T_mod[self.firstBB140][int(140/Status.TemperatureInterval)] >= 0.1*Status.int.QD_T_mod[self.firstBB][int(self.maxTemp/Status.TemperatureInterval)]:
            print"point A1 reached"
            if self.QDh140[0]*self.securityMargin >= self.minPow:
                print "point A2 reached"
                if self.QDh140[0]*self.securityMargin>=2*self.minPow:
                    print "point A3 reached"
                    if self.QDh140[0]*self.securityMargin < self.QDh140[self.minOpTime]*1.3 or \
                    self.QDh140[0]*self.securityMargin -self.QDh140[self.minOpTime]<self.minPow:
                        print "point A4 reached"
                    
#HS TAKE CARE !!!! methods of the same class have to be called with the "self." before
#                   has probably to be corrected throughout the code ... !!!!
#                        selectBB((QDh_descending[0]*securityMargin)) # ,...)  #select the right bb from the database.
                        modelID=self.selectBB((self.QDh140[0]*self.securityMargin),140) # ,...)  #select the right bb from the database.
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

                    else:
#HS: elif requires a condition !!!                    elif:
                        if self.QDh140[self.minOpTime]>self.bigger140:
                            for i in range (int(self.QDh140[self.minOpTime]/self.bigger140)):
                                print "point B1 reached"
                                modelID =self.selectBB(self.bigger140,140)
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)
                            added += int(self.QDh140[self.minOpTime]/self.bigger140)*self.bigger140
                        else:
                            print "point C1 reached"
                            modelID =self.selectBB(self.QDh140[self.minOpTime],140)  #  select the base load boiler from DB
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                            added += self.DB.dbboiler.DBBoiler_ID[modelID][0].BBPnom
                        print "power of the last bb group added"
                        print added
                      
                        if self.QDh140[0]*self.securityMargin - added>= 2*self.minPow:
                            if self.QDh80[0]*self.securityMargin - added >= self.bigger80:
                                for i in range (int((self.QDh140[0]*self.securityMargin - added)/self.bigger140)):
                                    print "point D1 reached"
                                    modelID =self.selectBB(self.bigger140,140)
                                    equipe = self.addEquipmentDummy()
                                    self.setEquipmentFromDB(equipe,modelID)
                                print "point E1 reached"
                                added += int((self.QDh140[0]*self.securityMargin - added)/self.bigger140)*self.bigger140
                                modelID =self.selectBB((self.QDh140[0]*self.securityMargin - added),140)
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)
                            else:
                                print "point F1 reached"
                                modelID=self.selectBB(((self.QDh140[0]*self.securityMargin - added)/2),140)  #sempre aggiungere anche il criterio di efficienza
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                                self.setEquipmentFromDB(equipe,modelID)
                            
                        else:
                            print "point G1 reached"
                            self.selectBB((self.QDh140[0]*self.securityMargin - added),140)
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

                else:
                    print "point H1 reached"
                    self.selectBB(self.QDh140[0]*self.securityMargin,140)
                    equipe = self.addEquipmentDummy()
                    self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

        print "point i1 reached"
        self.sortBoiler()
#------------------------------------------------------------------------------
    def designBBmaxTemp(self): #HS .........,maxTemp...):
#------------------------------------------------------------------------------
# design a boiler sistem at the maximum temperature of the heat demand
#------------------------------------------------------------------------------
        added=0
        if self.QDhmaxTemp[0]*self.securityMargin>=2*self.minPow:
            if self.QDhmaxTemp[0]*self.securityMargin < self.QDhmaxTemp[self.minOpTime]*1.3 \
               or (self.QDhmaxTemp[0]*self.securityMargin - self.QDhmaxTemp[self.minOpTime]) < self.minPow:
                modelID = self.selectBB((self.QDhmaxTemp[0]*self.securityMargin),self.maxTemp) #HS....,...)  #select the right bb from the database.
                equipe = self.addEquipmentDummy()
                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

            else:
                if self.QDhmaxTemp[self.minOpTime]>self.biggermaxTemp:
                    for i in range (int(self.QDhmaxTemp[self.minOpTime]/self.biggermaxTemp)):
                        modelID =self.selectmaxTemp(self.biggermaxTemp,self.maxTemp)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)
                    added += int(self.QDhmaxTemp[self.minOpTime]/self.biggermaxTemp)*self.biggermaxTemp
                else:
                    modelID =self.selectBB(self.QDhmaxTemp[self.minOpTime],self.maxTemp)
                    equipe = self.addEquipmentDummy()
                    self.setEquipmentFromDB(equipe,modelID)
                    added += self.DB.dbboiler.DBBoiler_ID[modelID][0].BBPnom


                if self.QDhmaxTemp[0]*self.securityMargin - added >= 2*self.minPow:
                    if self.QDhmaxTemp[0]*self.securityMargin - added >= self.biggermaxTemp:
                        for i in range (int((self.QDhmaxTemp[0]*self.securityMargin - added)/self.biggermaxTemp)):
                            modelID =self.selectBB(self.biggermaxTemp,self.maxTemp)
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)
                        added += int((self.QDhmaxTemp[0]*self.securityMargin - added)/self.biggermaxTemp)*self.biggermaxTemp
                        modelID =self.selectBB((self.QDhmaxTemp[0]*self.securityMargin - added),self.maxTemp)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)
                    else:
                        modelID=self.selectBB(((self.QDhmaxTemp[0]*self.securityMargin - added)/2),maxTemp)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)

                   
                else:
                    modelID=self.selectBB((self.QDhmaxTemp[0]*self.securityMargin - added),self.maxTemp)
                    equipe = self.addEquipmentDummy()
                    self.setEquipmentFromDB(equipe,modelID)

        else:
            modelID=self.selectBB(self.QDhmaxTemp[0]*self.securityMargin,self.maxTemp)
            equipe = self.addEquipmentDummy()
            self.setEquipmentFromDB(equipe,modelID)


        self.sortBoiler()
    
#------------------------------------------------------------------------------
    def designAssistant(self):
#------------------------------------------------------------------------------
#   auto-design of boiler cascade
#------------------------------------------------------------------------------

#............................................................................................
# getting configuration parameters of DA

        DATable = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(DATable) > 0:
            DA = DATable[0]
        else:
            logTrack("ModuleBB (design assistant): WARNING - no DA configuration parameters available")
            return

        if DA.BBRedundancy == True:
            pass
        
        self.securityMargin=1.2      #  N.B. securityMargin should be choosen by the user!!! At the moment is setted to 1.2############
        self.minPow =100             #  N.B. minPow should be an imput from the boiler window!!! At the moment is setted to 100kW
        self.minOpTime=100          #  N.B. minOpTime should be an imput from the boiler window!!! At the moment is setted to 100 hours:for testing Nt is 168 corresponding to 1 week.

#        self.screenEquipments()
#HS 2008-07-06: this should not be necessary. should be updated

        self.automDeleteBoiler()   # delete unefficient boiler

#............................................................................................
# first do some sorting ...

#        self.findmaxTemp(Status.int.QD_T)
#HS2008-07-06: CHECK CHECK CHECK -> should this not be the REAL demand seen by the boiler cascade ???
        self.findmaxTemp(Status.int.QD_T_mod[self.cascadeIndex-1])
        
        self.findBiggerBB()       
        self.sortBoiler()     # sort boilers by temperature (ascending) and by efficiency (descending)
                                

#............................................................................................
# after shifting, the equipment cascade has to be updated, as the modified demand is used
# in the following

        if Status.int.cascadeUpdateLevel < self.NEquipe:
            Status.mod.moduleEnergy.runSimulation()
            
#............................................................................................
# low temperature boiler look-up
        exBP=0       #   power of the boiler in the cascade operating at 80�C

        for row in Status.int.cascade:
            bbs = Status.DB.qgenerationhc.QGenerationHC_ID[row["equipeID"]]
            if len(bbs) > 0:
                equipTry= bbs[0]
                if getEquipmentClass(row["equipeType"]) == "BB" and equipTry.TMaxSupply <=80:
                    exBP += row['equipePnom']

        logTrack("ModuleBB: power of the boilers at 80�C present in the cascade at the moment %s"%exBP)

        if self.firstBB < 0 or self.firstBB > self.NEquipe-1:
            logDebug("MoudleBB (DA): error in no. of firstBB: %s (NEquipe = %s)"%(self.firstBB,self.NEquipe))
            
        iT80 = int(80/Status.TemperatureInterval + 0.5)
#        zz=int(80/Status.TemperatureInterval)
#HS2008-07-06: zz substituted by iT80. is more self-understanding

        QDmax = maxInList(Status.int.QD_Tt_mod[self.firstBB][iT80])
#        yy= maxInList(Status.int.QD_Tt_mod[self.firstBB][iT80])
#HS2008-07-06. idem yy -> QDmax

        b=max((QDmax  - exBP),0)
        b1= max(((QDmax  * self.securityMargin) - exBP),0) #   minimum power of the new boilers at 80�C
        c=[]
        for it in range (Status.Nt):
            c.append ( min (b, Status.int.QD_Tt_mod[self.firstBB][iT80][it]))

        self.QDh80=c  # demand to be supplied by new boilers at 80�C

        self.QDh80.sort(reverse=True)
        if self.QDh80[0]>0:
            self.designBB80()

#............................................................................................
# 140 �C boilers
            
        if self.maxTemp>160:   # N.B. The difference between temperature levels is now setted in 20�C but in the future could be a parameter.      
                        
            exBP=0       #   power of the boiler in the cascade operating at 140�C
            for row in Status.int.cascade:
                bbs = Status.DB.qgenerationhc.QGenerationHC_ID[row["equipeID"]]
                if len(bbs) > 0:
                    equipTry= bbs[0]
                    if getEquipmentClass(row["equipeType"]) == "BB" and 90 <= equipTry.TMaxSupply <=140:
                        exBP += row['equipePnom']

            iT140 =int(140/Status.TemperatureInterval + 0.5)
            QDmax = maxInList(Status.int.QD_Tt_mod [self.firstBB140][iT140])
            b=max((QDmax  - exBP),0) #   minimum power of the new boilers at 140�C
            c=[]
            for it in range (Status.Nt):
                c.append ( min (b, Status.int.QD_Tt_mod[self.firstBB140][iT140][it]))

            self.QDh140=c  # demand to be supplied by new boilers at 140�C
            self.QDh140.sort(reverse=True)

            if self.QDh140[0]>0:
                self.designBB140()
        
#............................................................................................
# maxTemp boilers


        exBP=0       #   power of the boiler in the cascade operating at maxTemp
        for row in Status.int.cascade:
            bbs = Status.DB.qgenerationhc.QGenerationHC_ID[row["equipeID"]]
            if len(bbs) > 0:
                equipTry= bbs[0]

            if getEquipmentClass(row["equipeType"]) == "BB":
                exBP += row['equipePnom']

        cI= len(Status.int.QD_Tt_mod)+1
        
        iTmax =int(self.maxTemp/Status.TemperatureInterval + 0.5)
        QDmax = maxInList(Status.int.QD_Tt_mod [self.firstBBmaxTemp][iTmax])
        b=max((QDmax  - exBP),0) #   minimum power of the new boilers at maxTemp�C
        c=[]
        for it in range (Status.Nt):
            c.append ( min (b, Status.int.QD_Tt_mod[self.firstBBmaxTemp][iTmax][it]))

        self.QDhmaxTemp=c  # demand to be supplied by new boilers at maxTemp�C

        self.QDhmaxTemp.sort(reverse=True)
        if self.QDhmaxTemp[0]>0:
            self.designBBmaxTemp()

        off= False
        if off== False:
            self.redundancy()
        
#        self.updatePanel()    #updatePanel should be called only from the Panel !!!
    
#==============================================================================


if __name__ == "__main__":
    print "Testing ModuleBB"
    import einstein.GUI.pSQL as pSQL, MySQLdb
    from einstein.modules.interfaces import *
    from einstein.modules.energy.moduleEnergy import *    

    stat = Status("testModuleBB")

    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    
    Status.PId = 2
    Status.ANo = 0

    interf = Interfaces()

    Status.int = Interfaces()
    
    keys = ["BB Table","BB Plot","BB UserDef"]
    mod = ModuleBB(keys)
    equipe = mod.addEquipmentDummy()
    mod.calculateEnergyFlows(equipe,mod.cascadeIndex)
                    

#    mod.designAssistant1()
#    mod.designAssistant2(12)
