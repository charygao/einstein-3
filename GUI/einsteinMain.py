#!/usr/bin/env python
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
#	EINSTEIN Main 
#			
#------------------------------------------------------------------------------
#			
#	GUI Main routines
#
#==============================================================================
#
#	Version No.: 0.67
#	Created by: 	    Heiko Henning (Imsai e-soft)	February 2008
#	Revisions:          Tom Sobota                          12/03/2008
#                           Hans Schweiger                      22/03/2008
#                           Tom Sobota                          23/03/2008
#                           Hans Schweiger                      24/03/2008
#                           Hans Schweiger                      25/03/2008
#                           Tom Sobota                          26/03/2008
#                           Hans Schweiger                      02/04/2008
#                           Hans Schweiger                      03/04/2008
#                           Tom Sobota                          06/04/2008
#                           Hans Schweiger                      08/04/2008
#                           Tom Sobota                          09/04/2008
#                           Hans Schweiger                      12/04/2008
#
#       Change list:
#       12/03/2008- panel Energy added
#       13/03/2008  Changed global refs. to DB, SQL ... to references in Status
#                   Changed global refs to database params to locals
#                   Deleted all references to DataBridge
#       22/03/2008  Small changes due to changes in interface
#       23/03/2008  Added panels EA1 - EA6, EM1. Added a subtree for Yearly, Monthly and Daily
#                   statistics
#       24/03/2008  Small changes in calls to PanelBB
#       25/03/2008  Picture added in main panel
#       26/03/2008  Suppressed actions on upper level tree items
#       29/03/2008  Added panels EA2, EH1, EH2 (EH1, EH2 not yet functional)
#       02/04/2008  Small changes in event handler selectQuestionnaire
#       03/04/2008  Instance of moduleEnergy created in main
#                   Function connectToDB out of EinsteinFrame
#                   Second update: PanelHC and PanelA added
#       06/04/2008  Extracted Page 4 and all related code as an external module,so it
#                   can be called from other places
#       08/04/2008  Panels BM1-3 added (Benchmark modules)
#       09/04/2008  Extracted Page 1 to Page 9 and all related code as external modules.
#       12/04/2008  Instance of class Project created
#                   Minor changes event handlers panelQ0
#                   Function "OnEnterHeatPump" changed
#                   Function Show substituted by display added by opening EA-Panels
#                   Function Show substituted by display added by opening HP-Panel
#                   Event-handlers scroll-up "view" added
#                   Event-handlers scroll-up "user-interaction level"
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

#-----  Imports
import wx
import wx.grid
import pSQL, MySQLdb
import exceptions
import HelperClass
import BridgeClass

#--- popup frames
from status import Status #processing status of the tool
from einstein.modules.project import Project #functions for handling of PId/ANo

#--- popup frames
import DBEditFrame
import PreferencesFrame

#--- Module Panels
from panelCCheck import *
from panelA import *
from panelHC import *
from panelHP import *
from panelBB import *
from panelEnergy import *
#TS20080406 the new panels Q*
from einstein.GUI.panelQ0 import PanelQ0
from einstein.GUI.panelQ1 import PanelQ1
from einstein.GUI.panelQ2 import PanelQ2
from einstein.GUI.panelQ3 import PanelQ3
from einstein.GUI.panelQ4 import PanelQ4
from einstein.GUI.panelQ5 import PanelQ5
from einstein.GUI.panelQ6 import PanelQ6
from einstein.GUI.panelQ7 import PanelQ7
from einstein.GUI.panelQ8 import PanelQ8
from einstein.GUI.panelQ9 import PanelQ9

#TS2008-03-23 panelEA1-EA6, EM1 added
from panelEA1 import *
from panelEA2 import *
from panelEA3 import *
from panelEA4 import *
from panelEA5 import *
from panelEA6 import *
from panelEM1 import *
from panelEM2 import *
#from panelEH1 import *
#from panelEH2 import *
from panelBM1 import *
from panelBM2 import *
from panelBM3 import *


#-----  Global variables 
PList = {}      # PList stores the Parameterlist

#----- Constants
qPageSize = (800, 600) # this would be better in Status?

def connectToDB():
    
        doLog = HelperClass.LogHelper()
        conf = HelperClass.ConfigHelper()
        doLog.LogThis('Starting program')

        DBHost = conf.get('DB', 'DBHost')
        DBUser = conf.get('DB', 'DBUser')
        DBPass = conf.get('DB', 'DBPass')
        DBName = conf.get('DB', 'DBName')
        LANGUAGE = conf.get('GUI', 'LANGUAGE')
        doLog.LogThis('Reading config done')
        
        #----- Connect to the Database
        Status.SQL = MySQLdb.connect(host=DBHost, user=DBUser, passwd=DBPass, db=DBName)
        Status.DB =  pSQL.pSQL(Status.SQL, DBName)
        print "database assigned to status variable " + repr(Status.DB)
        
        doLog.LogThis('Connected to database %s @ %s' % (DBName, DBHost))


#------------------------------------------------------------------------------		
class EinsteinFrame(wx.Frame):
#------------------------------------------------------------------------------		
#   Main frame definition
#------------------------------------------------------------------------------		
    
    def __init__(self, parent, id, title):
        ############################################
        #
        # Database connexion
        #
        ############################################

        doLog = HelperClass.LogHelper()
        conf = HelperClass.ConfigHelper()
        doLog.LogThis('Starting program')

        global activeQid
        self.activeQid = 0
#        DBHost = conf.get('DB', 'DBHost')
#        DBUser = conf.get('DB', 'DBUser')
#        DBPass = conf.get('DB', 'DBPass')
#        DBName = conf.get('DB', 'DBName')
        LANGUAGE = conf.get('GUI', 'LANGUAGE')
        doLog.LogThis('Reading config done')
        
        #----- Connect to the Database
#        Status.SQL = MySQLdb.connect(host=DBHost, user=DBUser, passwd=DBPass, db=DBName)
#        Status.DB =  pSQL.pSQL(Status.SQL, DBName)
#        print "database assigned to status variable " + repr(Status.DB)
        
#        doLog.LogThis('Connected to database %s @ %s' % (DBName, DBHost))

        #----- Import the Parameterfile
        global PList
        ParamList = HelperClass.ParameterDataHelper()
        PList = ParamList.ReadParameterData()
        doLog.LogThis('Import Parameterfile done')


        ############################################
        #
        # UI generation
        #
        ############################################

        #----- Initialise the Frame
        wx.Frame.__init__(self, parent, id, title, size=(1024, 740), pos=(0,0))
        #----- add statusbar
        self.CreateStatusBar()



        #----- add menu
        self.menuBar = wx.MenuBar()
        
        self.menuFile = wx.Menu()
        self.menuView = wx.Menu()
        self.menuDatabase = wx.Menu()
        self.menuSettings = wx.Menu()        
        self.menuHelp = wx.Menu()

        self.submenuPrint = wx.Menu()
        self.submenuEditDB = wx.Menu()
                
        self.subnenuEquipments = wx.Menu()
        self.submenuUserLevel = wx.Menu()
        self.submenuClassification = wx.Menu()
        

        self.PrintFullReport = self.submenuPrint.Append(-1, "full report")
        self.PrintQuestionnaire = self.submenuPrint.Append(-1, "questionnaire")

        self.NewProject = self.menuFile.Append(-1, PList["X103"][1])
        self.OpenProject = self.menuFile.Append(-1, "&Open Project")
        self.ImportProject = self.menuFile.Append(-1, PList["X104"][1])
        self.ExportProject = self.menuFile.Append(-1, PList["X105"][1])
        self.menuFile.AppendSeparator()
        self.ImportQ = self.menuFile.Append(-1, PList["X106"][1])
        self.menuFile.AppendSeparator()
        self.Print = self.menuFile.AppendMenu(-1, "&Print", self.submenuPrint)
        self.menuFile.AppendSeparator()
        self.ExitApp = self.menuFile.Append(-1, PList["X107"][1])

        self.PresentStateQ = self.menuView.AppendRadioItem(-1, "Present state (original data)")
        self.PresentState = self.menuView.AppendRadioItem(-1, "Present state (checked data)")
        self.Alternative1 = self.menuView.AppendRadioItem(-1, "Alternative 1")
        

        self.EditDBCHP = self.subnenuEquipments.Append(-1, PList["X111"][1])
        self.EditDBHeatPump = self.subnenuEquipments.Append(-1, PList["X112"][1])
        self.EditDBChiller = self.subnenuEquipments.Append(-1, PList["X117"][1])
        self.EditDBBoiler = self.subnenuEquipments.Append(-1, PList["X115"][1])
        self.EditDBStorage = self.subnenuEquipments.Append(-1, PList["X116"][1])
        self.EditDBSolarEquip = self.subnenuEquipments.Append(-1, PList["X116"][1])

        self.EditSubDB = self.menuDatabase.AppendMenu(-1, "Equipments", self.subnenuEquipments)
        self.EditDBFuel = self.menuDatabase.Append(-1, PList["X114"][1])
        self.EditDBFluid = self.menuDatabase.Append(-1, PList["X113"][1])
        self.EditDBBenchmark = self.menuDatabase.Append(-1, PList["X108"][1])
        self.EditDBBAT = self.menuDatabase.Append(-1, "Best available technologies")
        
        self.EditDBNaceCode = self.submenuClassification.Append(-1, PList["X109"][1])
        self.EditDBUnitOperation = self.submenuClassification.Append(-1, PList["X110"][1])       
               

        self.UserSelectLevel1 = self.submenuUserLevel.AppendRadioItem(-1, PList["X120"][1])
        self.UserSelectLevel2 = self.submenuUserLevel.AppendRadioItem(-1, PList["X121"][1])
        self.UserSelectLevel3 = self.submenuUserLevel.AppendRadioItem(-1, PList["X122"][1])
        self.UserLevel = self.menuSettings.AppendMenu(-1, PList["X123"][1], self.submenuUserLevel)
        self.Classification = self.menuSettings.AppendMenu(-1, "Classification", self.submenuClassification)
        self.Preferences = self.menuSettings.Append(-1, PList["X119"][1])
        self.Language = self.menuSettings.Append(-1, "Language")

        self.HelpHelp = self.menuHelp.Append(-1, PList["X126"][1])
        self.menuHelp.AppendSeparator()
        self.HelpAbout = self.menuHelp.Append(-1, PList["X127"][1])

        self.menuBar.Append(self.menuFile, PList["X128"][1])
        self.menuBar.Append(self.menuView, "View")
        self.menuBar.Append(self.menuDatabase, "Database")
        self.menuBar.Append(self.menuSettings, PList["X130"][1])
        self.menuBar.Append(self.menuHelp, PList["X132"][1])
        
        self.SetMenuBar(self.menuBar)

        
        #----- add the widgets ...
        self.panel1=wx.Panel (self, -1)
        self.panel1.SetBackgroundColour ("white")

        #----- create splitter windows
        self.splitter = wx.SplitterWindow(self, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
        self.splitter2 = wx.SplitterWindow(self.splitter, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
        self.mainpanel = wx.Panel(self.splitter, -1)
        self.leftpanel2 = wx.Panel(self.splitter2, -1, style=wx.WANTS_CHARS) # this ist main gui panel containing qPages
        self.mainpanel.SetBackgroundColour ("white")
        self.splitter2.SetBackgroundColour (wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))

        #----- create tree control
        self.tree = wx.TreeCtrl(self.mainpanel, -1, wx.Point(0, 0), wx.Size(200, 740),
                                wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        self.qRoot = self.tree.AddRoot(PList["X001"][1])
        self.qPage0 = self.tree.AppendItem (self.qRoot, PList["X018"][1],0)
        self.qPage1 = self.tree.AppendItem (self.qPage0, PList["X010"][1],0)
        self.qPage2 = self.tree.AppendItem (self.qPage0, PList["X011"][1],0)
        self.qPage3 = self.tree.AppendItem (self.qPage0, PList["X012"][1],0)
        self.qPage4 = self.tree.AppendItem (self.qPage0, PList["X013"][1],0)
        self.qPage5 = self.tree.AppendItem (self.qPage0, PList["X014"][1],0)
        self.qPage5_1 = self.tree.AppendItem (self.qPage0, "Heat recovery",0)
        self.qPage6 = self.tree.AppendItem (self.qPage0, PList["X015"][1],0)
        self.qPage7 = self.tree.AppendItem (self.qPage0, PList["X016"][1],0)
        self.qPage8 = self.tree.AppendItem (self.qPage0, PList["X017"][1],0)
        
        self.qDataCheck = self.tree.AppendItem (self.qRoot, PList["X133"][1])
        self.qDataCheckPage1 = self.tree.AppendItem (self.qDataCheck, PList["X134"][1])
        self.qDataCheckPage2 = self.tree.AppendItem (self.qDataCheck, PList["X135"][1])
        self.qDataCheckPage3 = self.tree.AppendItem (self.qDataCheck, "Check list for visit")
        
        #
        # statistics subtree
        #
        self.qStatistics = self.tree.AppendItem (self.qRoot, PList["X136"][1])
        self.qStatisticsAnnual = self.tree.AppendItem (self.qStatistics, 'Annual data')
        self.qStatisticsMonthly = self.tree.AppendItem (self.qStatistics, 'Monthly data')
        self.qStatisticsHourly = self.tree.AppendItem (self.qStatistics, 'Hourly performance data')
        # annual statistics subtree
        self.qStatisticYPage1 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X137"][1])
        self.qStatisticYPage2 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X138"][1])
        self.qStatisticYPage3 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X139"][1])
        self.qStatisticYPage4 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X140"][1])
        self.qStatisticYPage5 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X141"][1])
        self.qStatisticYPage6 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X142"][1])
        # monthly statistics subtree
        self.qStatisticMPage1 = self.tree.AppendItem (self.qStatisticsMonthly, 'Monthly demand')
        self.qStatisticMPage2 = self.tree.AppendItem (self.qStatisticsMonthly, 'Monthly supply')
        # hourly statistics subtree
        self.qStatisticHPage1 = self.tree.AppendItem (self.qStatisticsHourly, 'Hourly demand')
        self.qStatisticHPage2 = self.tree.AppendItem (self.qStatisticsHourly, 'Hourly supply')

        
        self.qBenchmarkCheck = self.tree.AppendItem (self.qRoot, PList["X143"][1])
        self.qBenchmarkCheckPage1 = self.tree.AppendItem (self.qBenchmarkCheck, PList["X144"][1])
        self.qBenchmarkCheckPage2 = self.tree.AppendItem (self.qBenchmarkCheck, "Global energy intensity")
        self.qBenchmarkCheckPage3 = self.tree.AppendItem (self.qBenchmarkCheck, "SEC by product")
        self.qBenchmarkCheckProduct = self.tree.AppendItem (self.qBenchmarkCheckPage3, "product name")
        self.qBenchmarkCheckPage4 = self.tree.AppendItem (self.qBenchmarkCheck, "SEC by process")
        self.qBenchmarkCheckProcess = self.tree.AppendItem (self.qBenchmarkCheckPage4, "process name")
        

        self.qOptimisationProposals = self.tree.AppendItem (self.qRoot, PList["X145"][1])
        #Design
        self.qOptiProDesign = self.tree.AppendItem (self.qOptimisationProposals, PList["X146"][1])
        
        #Process optimisation
        self.qOptiProProcess = self.tree.AppendItem (self.qOptiProDesign, "Process optimisation")
        #Process optimisation interface 1
        self.qOptiProProcess1 = self.tree.AppendItem(self.qOptiProProcess, "Process optimisation interface 1")
                #Process optimisation interface 2
        self.qOptiProProcess2 = self.tree.AppendItem(self.qOptiProProcess, "Process optimisation interface 2")
            #Pinch analysis
        self.qOptiProPinch = self.tree.AppendItem(self.qOptiProDesign, "Pinch analysis")
                #Pinch interface 1
        self.qOptiProPinch1 = self.tree.AppendItem(self.qOptiProPinch, "Pinch interface 1")
                #Pinch interface 2
        self.qOptiProPinch2 = self.tree.AppendItem(self.qOptiProPinch, "Pinch interface 2")
            #HX network
        self.qOptiProHX = self.tree.AppendItem (self.qOptiProDesign, "HX network")

            #H&C Supply
        self.qHC = self.tree.AppendItem (self.qOptiProDesign, "H&C Supply")
                #H&C Storage
        self.qOptiProSupply1 = self.tree.AppendItem (self.qHC, "H&C Storage")
                #CHP
        self.qOptiProSupply2 = self.tree.AppendItem (self.qHC, "CHP")
                #Solar Thermal
        self.qOptiProSupply3 = self.tree.AppendItem (self.qHC, "Solar Thermal")
                #Heat Pumps
        self.qHP = self.tree.AppendItem (self.qHC, "Heat Pumps")
                #Biomass
        self.qOptiProSupply5 = self.tree.AppendItem (self.qHC, "Biomass")
                #Chillers
        self.qOptiProSupply6 = self.tree.AppendItem (self.qHC, "Chillers")
                #Boilers & burners
        self.qBB = self.tree.AppendItem (self.qHC, "Boilers & burners")
        
            #H&C Distribution
        self.qOptiProDistribution = self.tree.AppendItem (self.qOptiProDesign, "H&C Distribution")

        #Energy performance
        self.qOptiProEnergy = self.tree.AppendItem (self.qOptimisationProposals, "Energy performance")
            #Detailed energy flows 1
#HS2008-03-12: subdivision energy cancelled out
#        self.qOptiProEnergy1 = self.tree.AppendItem (self.qOptiProEnergy, "Detailed energy flows 1")
            #Detailed energy flows 2
#        self.qOptiProEnergy2 = self.tree.AppendItem (self.qOptiProEnergy, "Detailed energy flows 2")

        #Economic analysis
        self.qOptiProEconomic = self.tree.AppendItem (self.qOptimisationProposals, "Economic analysis")
            #Economics 1
        self.qOptiProEconomic1 = self.tree.AppendItem (self.qOptiProEconomic, "Economics 1")
            #Economics 2
        self.qOptiProEconomic2 = self.tree.AppendItem (self.qOptiProEconomic, "Economics 2")


        #Comparative analysis
        self.qOptiProComparative = self.tree.AppendItem (self.qOptimisationProposals, "Comparative analysis")
            #Comparative study � Detail Info 1
        self.qOptiProComparative1 = self.tree.AppendItem (self.qOptiProComparative, "Comparative study � Detail Info 1")
            #Comparative study � Detail Info 2
        self.qOptiProComparative2 = self.tree.AppendItem (self.qOptiProComparative, "Comparative study � Detail Info 2")
            #Comparative study � Detail Info 3
        self.qOptiProComparative3 = self.tree.AppendItem (self.qOptiProComparative, "Comparative study � Detail Info 3")


        self.qFinalReport = self.tree.AppendItem (self.qRoot, PList["X147"][1])
        self.qFinalReportPage1 = self.tree.AppendItem (self.qFinalReport, PList["X148"][1])
        self.qFinalReportPage2 = self.tree.AppendItem (self.qFinalReport, PList["X149"][1])
        self.qFinalReportPrint = self.tree.AppendItem (self.qFinalReport, PList["X150"][1])
        
        self.tree.Expand(self.qRoot)
        self.tree.Expand(self.qPage0)
        self.tree.Expand(self.qDataCheck)
        self.tree.Expand(self.qStatistics)
        self.tree.Expand(self.qBenchmarkCheck)
        self.tree.Expand(self.qOptimisationProposals)
        self.tree.Expand(self.qFinalReport)


        self.DoLayout ()

        
        
        #----- binding the EVENTS

        
        #--- binding the menu
        self.Bind(wx.EVT_MENU, self.NewQuestionnaire, self.NewProject)
        self.Bind(wx.EVT_MENU, self.OnMenuOpenProject, self.OpenProject)
        self.Bind(wx.EVT_MENU, self.OnMenuExit, self.ExitApp)

        self.Bind(wx.EVT_MENU, self.OnMenuPresentState, self.PresentState)
        self.Bind(wx.EVT_MENU, self.OnMenuPresentStateQ, self.PresentStateQ)
        self.Bind(wx.EVT_MENU, self.OnMenuAlternative1, self.Alternative1)

        self.Bind(wx.EVT_MENU, self.OnMenuEditDBBenchmark, self.EditDBBenchmark)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBNaceCode, self.EditDBNaceCode)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBUnitOperation, self.EditDBUnitOperation)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBCHP, self.EditDBCHP)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBHeatPump, self.EditDBHeatPump)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBFluid, self.EditDBFluid)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBFuel, self.EditDBFuel)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBBoiler, self.EditDBBoiler)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBSolarEquip, self.EditDBSolarEquip)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBChiller, self.EditDBChiller)     

        self.Bind(wx.EVT_MENU, self.OnMenuUserSelectLevel1, self.UserSelectLevel1)
        self.Bind(wx.EVT_MENU, self.OnMenuUserSelectLevel2, self.UserSelectLevel2)
        self.Bind(wx.EVT_MENU, self.OnMenuUserSelectLevel3, self.UserSelectLevel3)
        
        #--- binding the Tree
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged, self.tree)

        #--- bindings pageDataCheck
###HS2008-03-07        self.Bind(wx.EVT_BUTTON, self.OnButtonDataCheck, self.buttonDataCheck)        

#------------------------------------------------------------------------------		
    def DoLayout (self):
#------------------------------------------------------------------------------		
#       Layout of main frame and panels 
#------------------------------------------------------------------------------		
        
        # add other widgets
        self.help = wx.TextCtrl(self.splitter2, -1, style = wx.TE_MULTILINE|wx.TE_READONLY | wx.HSCROLL)
        
        # sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        panelsizer = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
      
        # add widgets to sizers
        panelsizer.Add(self.splitter, 1, wx.EXPAND, 0)
        sizer1.Add(self.tree, 1, wx.EXPAND)
        #sizer2.Add(self.staticBoxPage0, 1, wx.BOTTOM|wx.EXPAND|wx.ALIGN_BOTTOM, 60 )
    
        # set sizers
        self.mainpanel.SetSizer(sizer1)
        self.leftpanel2.SetSizer(sizer2)
        self.SetSizer(panelsizer)
        mainsizer.Layout()
        self.Layout()

        # set splitters
        self.splitter.SplitVertically(self.mainpanel, self.splitter2, 200)
        self.splitter2.SplitHorizontally(self.leftpanel2, self.help, -80)
        self.splitter.SetSashPosition (200)

######################################################################################        

        #----- set Panel Pages

        ####----PAGE Title
        self.pageTitle = wx.Panel(id=-1, name='pageTitle', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageTitle.Show()
        self.st1Title = wx.StaticText(id=-1,
              label='Welcome to EINSTEIN energy audit tool',
              name='st1Title', parent=self.pageTitle, pos=wx.Point(295, 30),
              size=wx.Size(222, 13), style=0)
        self.st1Title.Center(wx.HORIZONTAL)
        self.st1Title.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.Bitmap(u'zunge.jpg',wx.BITMAP_TYPE_JPEG),
                                             id=-1,#TS 2008-3-26 changed from id=wxID_PANELCCPIC1,
                                             name='staticBitmap1',
                                             parent=self.pageTitle,
                                             pos=wx.Point(220, 50),
                                             size=wx.Size(400, 500),
                                             style=0)
        
        
     
        ####----PAGE 0
        self.Page0 = PanelQ0(self.leftpanel2, self)
        self.Page0.Hide()


        ####----PAGE 1
        self.Page1 = PanelQ1(self.leftpanel2, self)
        self.Page1.Hide()


        ####----PAGE 2
        self.Page2 = PanelQ2(self.leftpanel2, self)
        self.Page2.Hide()


        ####----PAGE 3
        self.Page3 = PanelQ3(self.leftpanel2, self)
        self.Page3.Hide()

        
        ####----PAGE 4
#HS2008-04-13 None as argument added.
        self.Page4 = PanelQ4(self.leftpanel2, self, None)
        self.Page4.Hide()


        ####----PAGE 5
        self.Page5 = PanelQ5(self.leftpanel2, self)
        self.Page5.Hide()


        ####----PAGE 6 (Missing. This panel is empty)
        self.Page6 = PanelQ6(self.leftpanel2, self)
        self.Page6.Hide()


        ####----PAGE 7
        self.Page7 = PanelQ7(self.leftpanel2, self)
        self.Page7.Hide()
        


        ####----PAGE 8
        self.Page8 = PanelQ8(self.leftpanel2, self)
        self.Page8.Hide()

        ####----PAGE 9
        self.Page9 = PanelQ9(self.leftpanel2, self)
        self.Page9.Hide()




        ####----PAGE pageDataCheck
        self.pageDataCheck = wx.Panel(id=-1, name='pageDataCheck', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageDataCheck.Hide()
        ####--- End of pageDataCheck

###HS2008-03-07: Page substituted by PanelCCheck

        ####----PAGE pageDataCheckPage1
        self.pageDataCheckPage1 = PanelCC(id=-1, name='pageDataCheckPage1', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0, sql = Status.SQL, db = Status.DB) #TS 2008-03-13
        #self.pageDataCheckPage1 = PanelCC(id=-1, name='pageDataCheckPage1', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0, sql = MySql, db = DB)
        self.pageDataCheckPage1.Hide()
        ####--- End of pageDataCheckPage1



        ####----PAGE pageDataCheckPage2
        self.pageDataCheckPage2 = wx.Panel(id=-1, name='pageDataCheckPage2', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageDataCheckPage2.Hide()
        ####--- End of pageDataCheckPage2



        ####----PAGE pageStatistics
        #self.pageStatistics = wx.Panel(id=-1, name='pageStatistics', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        #self.pageStatistics.Hide()
        ####--- End of pageStatistics


        ####----PAGE pageStatisticPages

        #TS2008-03-23 changed this, added panels EA1-EA6, EM1

        #self.pageStatisticPages = wx.Panel(id=-1, name='pageStatisticPages', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        #self.pageStatisticPages.Hide()
        self.panelEA1 = PanelEA1(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA1')
        self.panelEA1.Hide()

        self.panelEA2 = PanelEA2(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA2')
        self.panelEA2.Hide()
        
        self.panelEA3 = PanelEA3(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA3')
        self.panelEA3.Hide()
        
        self.panelEA4 = PanelEA4(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA4')
        self.panelEA4.Hide()
        
        self.panelEA5 = PanelEA5(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA5')
        self.panelEA5.Hide()

        self.panelEA6 = PanelEA6(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA6')
        self.panelEA6.Hide()

        self.panelEM1 = PanelEM1(id=-1, name='pageEM1', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL)
        self.panelEM1.Hide()

        #TS2008-03-29 changed this, added panels EM2, EH1, EH2
        self.panelEM2 = PanelEM2(id=-1, name='pageEM2', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL)
        self.panelEM2.Hide()

        ####--- End of pageStatisticPages


        ####----PAGE pageBenchmarkCheck
        self.pageBenchmarkCheck = wx.Panel(id=-1, name='pageBenchmarkCheck', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageBenchmarkCheck.Hide()
        ####--- End of pageBenchmarkCheck

#HS2008-04-08 Benchmark Check
        ####--- End of pageBenchmarkCheck
        self.panelBM1 = PanelBM1(id=-1, name='panelBM1', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.panelBM1.Hide()
        self.panelBM2 = PanelBM2(id=-1, name='panelBM2', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.panelBM2.Hide()
        self.panelBM3 = PanelBM3(id=-1, name='panelBM3', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.panelBM3.Hide()

        ####----PAGE pageHeatRecoveryTargets
        #self.pageHeatRecoveryTargets = wx.Panel(id=-1, name='pageHeatRecoveryTargets', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        #self.pageHeatRecoveryTargets.Hide()
        ####--- End of pageHeatRecoveryTargets

        ####--- Page Alternatives
        self.panelA = PanelA(id=-1, name='panelA', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL)
        self.panelA.Hide()
        ####--- End op pageHeatPump

        ####--- Page H&C Supply
        self.panelHC = PanelHC(id=-1, name='panelHC', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL)
        self.panelHC.Hide()
        ####--- End op pageHeatPump

        ####--- PanelHP
        self.panelHP = PanelHP(id=-1, name='panelHP', parent=self.leftpanel2, main=self, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, sql = Status.SQL, db = Status.DB)
        self.panelHP.Hide()
        ####--- End op panelHP

        ####--- Page Boilers
        self.panelBB = PanelBB(id=-1, name='panelBB', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL)
        self.panelBB.Hide()
        ####--- End op panelHP

        ####--- Panel Energy
        self.panelEnergy = PanelEnergy(id=-1, name='panelEnergy', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL)
        self.panelEnergy.Hide()
        ####--- End op panelEnergy

        ####----PAGE pageFinalReport
        self.pageFinalReport = wx.Panel(id=-1, name='pageFinalReport', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageFinalReport.Hide()
        ####--- End of pageFinalReport


        ####----PAGE pageDataCheck
        self.pageDataCheck = wx.Panel(id=-1, name='pageDataCheck', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageDataCheck.Hide()
        ####--- End of pageDataCheck


#==============================================================================
#--- Eventhandlers Application
#==============================================================================

#------------------------------------------------------------------------------		
#--- Eventhandlers Menu
#------------------------------------------------------------------------------		

    def OnMenuOpenProject(self, event):
        self.tree.SelectItem(self.qPage0, select=True)

    def OnMenuExit(self, event):
        wx.Exit()
    
#..............................................................................		
# Scroll-up menu "VIEW"

    def OnMenuPresentStateQ(self, event):
        Status.prj.setActiveAlternative(-1)

    def OnMenuPresentState(self, event):
        Status.prj.setActiveAlternative(0)
        
    def OnMenuAlternative1(self, event):
        Status.prj.setActiveAlternative(1)

#..............................................................................		

    def OnMenuEditDBBenchmark(self, event):
        frameEditDBBenchmark = DBEditFrame.wxFrame(None, "Edit DBBenchmark", Status.DB.dbbenchmark, Status.SQL)
        frameEditDBBenchmark.Show()
    def OnMenuEditDBNaceCode(self, event):
        frameEditDBNaceCode = DBEditFrame.wxFrame(None, "Edit DBNaceCode", Status.DB.dbnacecode, Status.SQL)
        frameEditDBNaceCode.Show()
    def OnMenuEditDBUnitOperation(self, event):
        frameEditDBUnitOperation = DBEditFrame.wxFrame(None, "Edit DBUnitOperation", Status.DB.dbunitoperation, Status.SQL)
        frameEditDBUnitOperation.Show()
    def OnMenuEditDBCHP(self, event):
        frameEditDBCHP = DBEditFrame.wxFrame(None, "Edit DBCHP", Status.DB.dbchp, Status.SQL)
        frameEditDBCHP.Show()
    def OnMenuEditDBHeatPump(self, event):
        frameEditDBHeatPump = DBEditFrame.wxFrame(None, "Edit DBHeatPump", Status.DB.dbheatpump, Status.SQL)
        frameEditDBHeatPump.Show()
    def OnMenuEditDBFluid(self, event):
        frameEditDBFluid = DBEditFrame.wxFrame(None, "Edit DBFluid", Status.DB.dbfluid, Status.SQL)
        frameEditDBFluid.Show()
    def OnMenuEditDBFuel(self, event):
        frameEditDBFuel = DBEditFrame.wxFrame(None, "Edit DBFuel", Status.DB.dbfuel, Status.SQL)
        frameEditDBFuel.Show()
    def OnMenuEditDBBoiler(self, event):
        frameEditDBBoiler = DBEditFrame.wxFrame(None, "Edit DBBoiler", Status.DB.dbboiler, Status.SQL)
        frameEditDBBoiler.Show()
    def OnMenuEditDBSolarEquip(self, event):
        frameEditDBSolarEquip = DBEditFrame.wxFrame(None, "Edit DBSolarEquip", Status.DB.dbsolarequip, Status.SQL)
        frameEditDBSolarEquip.Show()
    def OnMenuEditDBChiller(self, event):
        frameEditDBChiller = DBEditFrame.wxFrame(None, "Edit DBChiller", Status.DB.dbchiller, Status.SQL)
        frameEditDBChiller.Show() 

#..............................................................................		
# Scroll-up menu "USER SELECT LEVEL 1 - 3"

    def OnMenuUserSelectLevel1(self, event):
        Status.prj.setUserInteractionLevel(1)
    def OnMenuUserSelectLevel2(self, event):
        Status.prj.setUserInteractionLevel(2)
    def OnMenuUserSelectLevel3(self, event):
        Status.prj.setUserInteractionLevel(3)

#..............................................................................		

       

    def OnMenuPreferences(self, event):
        framePreferences = PreferencesFrame.wxFrame(None)
        framePreferences.Show()
        #event.Skip()
        
#------------------------------------------------------------------------------		
#--- Eventhandlers Tree
#------------------------------------------------------------------------------		
        
    def OnTreeSelChanged(self, event):
        global qPageSize
        self.item = event.GetItem()
        select = self.tree.GetItemText(self.item)

        #if self.item:
        #    str1 = "Selected item = %s\n" % select
        #    self.help.SetValue(str1)
        print 'select='+select
        #PageTitle
        if select == "Einstein":
            self.hidePages()
            self.pageTitle.Show()
        #Page0
        elif select == PList["X018"][1]: #Edit Industry Data
            self.hidePages()
            self.Page0.Show()
            self.help.SetValue(PList["0101"][1])
            self.Page0.fillPage()
        #Page1
        elif select == PList["X010"][1]: #General data
            self.hidePages()
            self.Page1.Show()
            self.help.SetValue(PList["0101"][1])
            self.Page1.clear()
            self.Page1.fillChoiceOfNaceCode()
            self.Page1.fillPage()
        #Page2    
        elif select == PList["X011"][1]: #Energy consumption
            self.hidePages()
            self.Page2.Show()
            self.help.SetValue(PList["0102"][1])
            self.Page2.clear()
            self.Page2.fillChoiceOfDBFuelType()
            self.Page2.fillPage()
        #Page3
        elif select == PList["X012"][1]: #Processes data
            self.hidePages()
            self.Page3.Show()
            self.help.SetValue(PList["0102"][1])
            self.Page3.fillChoiceOfDBUnitOperation()
            self.Page3.fillChoiceOfPMDBFluid()
            self.Page3.fillChoiceOfSMDBFluid()
            self.Page3.clear()
            self.Page3.fillPage()
            
        #Page4
        elif select == PList["X013"][1]: #Generation of heat and cold
            self.hidePages()
            self.Page4.Show()
            self.help.SetValue(PList["0102"][1])
            self.Page4.clear()
            self.Page4.fillChoiceOfDBFuel()
            self.Page4.fillPage()
        #Page5
        elif select == PList["X014"][1]: #Distribution of heat and cold
            self.hidePages()
            self.Page5.Show()
            self.help.SetValue(PList["0102"][1])
            self.Page5.clear()
            self.Page5.fillchoiceOfEquipment()
            self.Page5.fillPage()

        #Page6 (Heat Recovery Missing)
        elif select == "Heat recovery": #Heat recovery
            self.hidePages()
            self.Page6.Show()
            self.help.SetValue(PList["Not available yet"][1])
            self.Page6.clear()
            self.Page6.fillPage()

        #Page7
        elif select == PList["X015"][1]: # Renewable energies
            self.hidePages()
            self.Page7.Show()
            self.help.SetValue(PList["0102"][1])
            self.Page7.clear()
            self.Page7.fillPage()
        #Page8
        elif select == PList["X016"][1]: #Buildings
            self.hidePages()
            self.Page8.Show()
            self.help.SetValue(PList["0102"][1])
            self.Page8.clear()
            self.Page8.fillPage()
        #Page9
        elif select == PList["X017"][1]: #Economic parameters
            self.hidePages()
            self.Page9.Show()
            self.help.SetValue(PList["0102"][1])
            self.Page9.clear()
            self.Page9.fillPage()
        #qDataCheck
        elif select == PList["X133"][1]:
            #TS 2008-3-26 No action here
            #self.hidePages()
            #self.pageDataCheck.Show()
            pass
        #qDataCheckPage1
        elif select == PList["X134"][1]:
            self.hidePages()
            self.pageDataCheckPage1.Show()        
        #qDataCheckPage2
        elif select == PList["X135"][1]:
            self.hidePages()
            self.pageDataCheckPage2.Show()
        #qStatistics
        elif select == PList["X136"][1]:
            #TS 2008-3-26 No action here
            #self.hidePages()
            #self.pageStatistics.Show()
            pass
        #qStatisticYPage1 'Primary energy - Yearly'
        elif select == PList["X137"][1]:
            self.hidePages()
            self.panelEA1.display()
#            self.panelEA1.Show()
        #qStatisticYPage2 'Final energy by fuels - Yearly'
        elif select == PList["X138"][1]:
            self.hidePages()
            self.panelEA2.Show()
        #qStatisticYPage3 'Final energy by equipment - Yearly'
        elif select == PList["X139"][1]:
            self.hidePages()
            self.panelEA3.Show()
        #qStatisticYPage4 'Process heat - Yearly'
        elif select == PList["X140"][1]:
            self.hidePages()
            self.panelEA4.Show()
        #qStatisticYPage5 'Energy intensity - Yearly'
        elif select == PList["X141"][1]:
            self.hidePages()
            self.panelEA5.Show()
        #qStatisticYPage6 'Production of CO2 - Yearly'
        elif select == PList["X142"][1]:
            self.hidePages()
            self.panelEA6.Show()
        #qStatisticMPage1 'Energy performance - Monthly'
        elif select == 'Monthly demand':
            self.hidePages()
            self.panelEM1.Show()
        #qStatisticMPage2 'Heat supply - Monthly'
        elif select == 'Monthly supply':
            self.hidePages()
            self.panelEM2.Show()
        #qStatisticHPage1 'Energy performance - Hourly'
        elif select == 'Hourly demand':
            self.hidePages()
            #self.panelEH1.Show()
        #qStatisticHPage2 'Heat supply - Hourly'
        elif select == 'Hourly supply':
            self.hidePages()
            #self.panelEH2.Show()
        #
        #
        #qBenchmarkCheck
        elif select == PList["X143"][1]:
            #TS 2008-3-26 No action here
            #self.hidePages()
            #self.pageBenchmarkCheck.Show()
            pass

#XXXHS2008-04-08
        elif select == "Global energy intensity":
            self.hidePages()
            self.panelBM1.Show()
            
        elif select == "SEC by product":
            self.hidePages()
            self.panelBM2.Show()
            
        elif select == "SEC by process":
            self.hidePages()
            self.panelBM3.Show()

        #qOptimisationProposals
        elif select == PList["X145"][1]:        #generation of alternatives
            self.hidePages()
            self.panelA.Show()

        elif select == PList["X147"][1]:
            #TS 2008-3-26 No action here
            #self.hidePages()
            #self.pageFinalReport.Show()
            pass
        #qFinalReportPage1
        elif select == PList["X148"][1]:
            self.hidePages()
            self.pageFinalReport.Show()
        #qFinalReportPage2
        elif select == PList["X149"][1]:
            self.hidePages()
            self.pageFinalReport.Show()
        #qPrintReport
        elif select == PList["X150"][1]:
            self.hidePages()
            self.pageFinalReport.Show()
        #panelHP
        elif select == "Heat Pumps":
            ret = self.OnEnterHeatPumpPage()
            if  ret == 0:
                self.hidePages()
#                self.panelHP.modHP.initPanel()
#                self.panelHP.Show()
                self.panelHP.display()
            else:
                self.showInfo("OnEnterHeatPumpPage return %s" %(ret))
###HS2008-03-07
        #pageBoilers
        elif select == "Boilers & burners":
            ###TS2008-03-11 Boiler Page activated
            self.hidePages()
            self.panelBB.modBB.initPanel()
            self.panelBB.Show()
###HS2008-03-12
        #panelEnergy
        elif select == "Energy performance":
            ###TS2008-03-11 Boiler Page activated
            self.hidePages()
            #self.panelEnergy.mod.initPanel()
            self.panelEnergy.Show()

###HS2008-04-03
        elif select == "H&C Supply":
            self.hidePages()
            self.panelHC.Show()


#------------------------------------------------------------------------------		
#--- Eventhandlers DataCheck
#------------------------------------------------------------------------------		
    def OnButtonDataCheck(self, event):
        if self.activeQid <> 0:
            #ret = self.ModBridge.FunctionOneDataCheck(Status.SQL, DB, self.activeQid)
            #self.showInfo("Return of FunctionOneDataCheck %s" %(ret))
            pass
        else:
            self.showError("Select Questionnaire first!")

#------------------------------------------------------------------------------		
#--- Eventhandlers DataCheck
#------------------------------------------------------------------------------		
    def OnEnterHeatPumpPage(self):
        if Status.PId <> 0:
            #ret = self.ModBridge.StartpanelHP(Status.SQL, DB, self.activeQid)
            #self.showInfo("Return of StartpanelHP %s" %(ret))
            return 0
        else:
            self.showError("Select project first!")
            return 1


#------------------------------------------------------------------------------		
# Auxiliary Functions
#------------------------------------------------------------------------------		
    def NewQuestionnaire(self):
        self.activeQid = 0
        self.tree.SelectItem(self.qPage1, select=True)

    def hidePages(self):
        self.pageTitle.Hide()
        self.Page0.Hide()
        self.Page1.Hide()
        self.Page2.Hide()
        self.Page3.Hide()
        self.Page4.Hide()
        self.Page5.Hide()
        #self.Page6.Hide()
        self.Page7.Hide()
        self.Page8.Hide()
        self.Page9.Hide()

        self.pageDataCheck.Hide()
        self.pageDataCheckPage1.Hide()
        self.pageDataCheckPage2.Hide()

        #self.pageStatistics.Hide()
        self.panelEA1.Hide()
        self.panelEA2.Hide()
        self.panelEA3.Hide()
        self.panelEA4.Hide()
        self.panelEA5.Hide()
        self.panelEA6.Hide()
        self.panelEM1.Hide()
        self.panelEM2.Hide()

#HS2008-04-08        
        self.pageBenchmarkCheck.Hide()
        self.panelBM1.Hide()
        self.panelBM2.Hide()
        self.panelBM3.Hide()

        #self.pageHeatRecoveryTargets.Hide()

        self.panelA.Hide()

        self.panelHC.Hide()
        self.panelHP.Hide()
        self.panelBB.Hide()
        self.panelEnergy.Hide()
        self.panelHC.Hide()

        self.pageFinalReport.Hide()

    def showError(self, message):
        dlg = wx.MessageDialog(None, message, 'Error', wx.OK)
        ret = dlg.ShowModal()
        dlg.Destroy()

    def showInfo(self, message):
        dlg = wx.MessageDialog(None, message, 'Info', wx.OK)
        ret = dlg.ShowModal()
        dlg.Destroy()

    def check(self, value):
        if value <> "" and value <> "None":
            return value
        else:
            return 'NULL'


###HS2008-04-12 no longer needed
#    def selectQuestionnaire(self):
#        id = Page0.GetID()
#        self.activeQid = Status.DB.questionnaire.Name[id]
#        Status.PId = self.activeQid
#        self.activeANo = 0
#        Status.ANo = self.activeANo
        
#        self.tree.SelectItem(self.qPage1, select=True)
        #self.tc1Page1.SetValue(self.listBoxQuestionnaresPage0.GetStringSelection())
        #self.tc1Page1.SetValue(str(self.activeQid))


                
#============================================================================== 				
#------------------------------------------------------------------------------		
#   Application start
#------------------------------------------------------------------------------		
        
if __name__ == '__main__':
    from einstein.modules.interfaces import Interfaces
    from einstein.modules.modules import Modules

    Status.PId=2 # just for testing!
    Status.ANo=0

    connectToDB()

    interf = Interfaces()       
    interf = None

    Status.mod = Modules()
    Status.prj = Project()

    app = wx.PySimpleApp()
    frame = EinsteinFrame(parent=None, id=-1, title="Einstein")
    
    frame.Show(True)
    app.MainLoop()

#==============================================================================
