# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelQ3: Process data
#
#==============================================================================
#
#	Version No.: 0.10
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger  02/05/2008
#                           Tom Sobota      04/05/2008
#                           Hans Schweiger  05/05/2008
#                           Hans Schweiger  07/05/2008
#                           Stoyan Danov    05/06/2008
#                           Tom Sobota      05/06/2008
#                           Hans Schweiger  10/06/2008
#                           Stoyan Danov    11/06/2008
#                           Hans Schweiger  12/06/2008
#                           Stoyan Danov    12/06/2008
#                           Stoyan Danov    13/06/2008
#                           Hans Schweiger  14/06/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qproduct
#       04/05/2008      Changed display format etc.
#       05/05/2008: HS  Event handlers changed
#       07/05/2008: HS  Safety features added against corrupt strings or Nones
#                       in checkboxes and fluid selectors
#                       UPHtotQ substituted by UPH
#                       UAProc substitutde by QOpProc
#       05/06/2008: SD  new classes & texts
#                   TS  adapted do_layout
#       10/06/2008: HS  introduced example TRANSPROCTYPES for static list in choice
#                       local function "check" eliminated (-> global check in GUITools)
#       11/0672008: SD  arranges tc-s,unitdict,predefined lists
#       12/06/2008: HS  some adaptation to new units.py -> to be continued
#       12/06/2008: SD  unitdict to new units.py, add fillChoice to display()
#       13/06/2008: SD  OnButtonOK changes
#       14/06/2008: HS  Clean-up
#
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	http://www.energyxperts.net/
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================
import wx
import pSQL
from status import Status
from GUITools import *
from displayClasses import *
from units import *

# constants that control the default field sizes

HEIGHT          =  27
LABELWIDTHLEFT  = 260
LABELWIDTHRIGHT = 500
DATAENTRYWIDTH  = 100
UNITSWIDTH      =  90
    
class PanelQ3(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ3', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()
        self.notebook = wx.Notebook(self, -1, style=0)

        self.page0 = wx.Panel(self.notebook)
        self.page1 = wx.Panel(self.notebook)

        self.sizer_5_staticbox = wx.StaticBox(self.page0, -1, _("Process list"))
        self.sizer_5_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_7_staticbox = wx.StaticBox(self.page0, -1, _("Processes description"))
        self.sizer_7_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_8_staticbox = wx.StaticBox(self.page0, -1, _("Schedule"))
        self.sizer_8_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_11_staticbox = wx.StaticBox(self.page1, -1,_("Waste heat (heat available for recovery)"))
        self.sizer_11_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_12_staticbox = wx.StaticBox(self.page1, -1, _("Waste heat recovery for this process"))
        self.sizer_12_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_13_staticbox = wx.StaticBox(self.page1, -1,
                                               _("Data of existing heat (or cold) supply to the process"))
        self.sizer_13_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        #
        # set default field sizes. Each data entry class has 4 configurable parameters:
        # 1. The height. This is the same for all the widgets that make the class
        # 2. The width of the label
        # 3. The width of the entry widget
        # 4. The width of the unit chooser.
        #
        f = FieldSizes(wHeight=HEIGHT,wLabel=LABELWIDTHLEFT,wData=DATAENTRYWIDTH,wUnits=UNITSWIDTH)

        #
        # left panel controls
        #

        # process list
        self.listBoxProcesses = wx.ListBox(self.page0,-1,choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxProcessesClick, self.listBoxProcesses)

        #
        # Processes description
        #
        self.tc1 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Process short name"),
                             tip=_("Give an organizational diagram of the production process \
(e.g. the flux of crude milk in chease production or the the flux of car chasis in the automobile industry)"))

        self.tc2 = ChoiceEntry(self.page0,
                               values=TRANSPROCTYPES.values(),
                               label=_("Process type"),
                               tip=_("Give a brief description of the process or the unitary operation, \
and specify if it is continuous or batch"))        

        self.tc3 = ChoiceEntry(self.page0,
                               values=[],
                               label=_("Unit operation type"),
                               tip=_("Select from predefined list"))       

        self.tc4 = ChoiceEntry(self.page0,
                               values=[],
                               label=_("Product or process medium"),
                               tip=_("The medium that is in direct contact with the treated product, \
e.g. air for drying, lye or water for washing, etc..."))           

        self.tc5 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Typical (final) temperature of the  process medium during operation"),
                              tip=_("Give the temperature of the process medium and not that of the heat supplying medium."))


        self.tc6 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Inlet temperature of the process medium (before heat recovery)"),
                              tip=_("Inlet temperature of the process medium before heat recovery"))


        self.tc7 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Start-up temperature of process medium (after breaks)"),
                              tip=_("Temperature of the process equipment before heating up \
when process start-up begins"))



        self.tc8 = FloatEntry(self.page0,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict=mergeDict(UNITS['MASS'],UNITS['VOLUME']),
                              label=_("Daily inflow of process medium"),
                              tip=_("Continuous process: Fluid flow rate times hours of circulation. \
Batch process with fluid renewal: volume times No. of lots."))


        self.tc9 = FloatEntry(self.page0,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict=UNITS['VOLUME'],
                              label=_("Volume of the process medium within the equipment or storage"),
                              tip=_("e.g. volume of liquid in a bottle for cleaning"))


        self.tc10 = FloatEntry(self.page0,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict=UNITS['POWER'],
                              label=_("Power requirement of the process in operation"),
                              tip=_("Power requierment during operation at steady state \
(thermal losses, evapoartion, endogenous chemical recations; without heating of circulating fluid)"))



        #
        # schedule
        #
##        self.tc11 = wx.TextCtrl(self.page0,-1,'')
##        self.st11 = Label(self.page0,self.tc11,_("Hours per day"),
##				  _("Hours of process operation per day (hrs/day)"))
        self.tc11 = FloatEntry(self.page0,
                              ipart=2, decimals=1, minval=0., maxval=24., value=0., 
                              unitdict={},
                              label=_("Hours of process operation per day"),
                              tip=_("For batch processes: specify the total duration of process, \
e.g. 3 batches/day x 2 hrs/batch = 6 hrs. If possible, specify daily program."))

##        self.tc12 = wx.TextCtrl(self.page0,-1,'')
##        self.st12 = Label(self.page0,self.tc12,_("Number of batches"),
##				  _("Number of batches per day"))
        self.tc12 = FloatEntry(self.page0,
                              ipart=2, decimals=1, minval=0., maxval=99., value=0.,
                              unitdict={},
                              label=_("Number of batches per day"),
                              tip=_("For batch processes: specify the total duration of process, \
e.g. 3 batches/day x 2 hrs/batch = 6 hrs. If possible, specify daily program."))

##        self.tc13 = wx.TextCtrl(self.page0,-1,'')
##        self.st13 = Label(self.page0,self.tc13,_("Duration of 1 batch"),
##                                  _("Duration of 1 batch (h)"))
        self.tc13 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TIME'],
                              label=_("Duration of 1 batch"),
                              tip=_("For batch processes: specify the total duration of process, \
e.g. 3 batches/day x 2 hrs/batch = 6 hrs. If possible, specify daily program."))

        self.tc14 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=365., value=0.,
                              unitdict={},
                              label=_("Days of process operation per year"),
                              tip=_("For batch processes: specify the total duration of process, \
e.g. 3 batches/day x 2 hrs/batch = 6 hrs. If possible, specify daily program."))


        # Right panel controls
        # make width of labels larger for this panel
        f = FieldSizes(wLabel=LABELWIDTHRIGHT)

        #
        # waste heat
        #

        self.tc15_1 = ChoiceEntry(self.page1, 
                               values=[],
                               label=_("Medium of outgoing waste heat flows"),
                               tip=_("Specify media of waste heat flows (up to 3)")) 
        self.tc15 = FloatEntry(self.page1,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Temperature of outgoing (waste) heat flows"),
                              tip=_("Temperature of the outgoing waste heat flow \
(e.g. water or hot humid air at the outlet of a drying process)"))

        self.tc15_2 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict=UNITS['SPECIFICENTHALPY'],
                              label=_("Specific enthalpy of outgoing (waste) heat flows"),
                              tip=_("Enthalpy of the outgoing waste heat flow \
(e.g. water or hot humid air at the outlet of a drying process)"))

        self.tc16 = FloatEntry(self.page1,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Final  temperature of outgoing (waste) heat flows"),
                              tip=_("Minimum temperature to which the waste heat flow can be cooled. \
If there is no limit specify 0"))

        self.tc17 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict=mergeDict(UNITS['MASS'],UNITS['VOLUME']),
                              label=_("Daily outflow of process medium"),
                              tip=_("Can be different from the incoming flow if e.g. there is evaporation \
or some chemical reaction."))

        self.tc18 = ChoiceEntry(self.page1, 
                               values=TRANSYESNO.values(),
                               label=_("Can heat be recovered from the outflowing medium?"),
                               tip=_("If NO, specify why: e.g. contamination with substances which can affect \
the heat exchanger,..."))

        # waste heat recovery

        self.tc19 = ChoiceEntry(self.page1, 
                               values=TRANSYESNO.values(),
                               label=_("Exists heat from heat  recovery for the process?"),
                               tip=_("If affirmative, give some brief description of the heat recovery system"))
        

        self.tc20 = ChoiceEntry(self.page1,
                                values=TRANSYESNO.values(),
##                               values=['list of processes...','one source'],
                               label=_("Source of waste heat"),
                               tip=_("Specify the heat source (e.g. heat lossed from process X, \
flue gases from  boiler Y, etc)"))

        self.tc21 = FloatEntry(self.page1,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Inlet temperature of the process medium  (after heat recovery)"),
                              tip=_("Inlet temperature (towards the system) of the process medium after the \
heat recovery"))
        


        # Data of existing heat ...
        
        self.tc22 = ChoiceEntry(self.page1, 
                               values=[],
                               label=_("Medium supplying heat or cold to the process (water, steam, air)"),
                               tip=_("Medium supplying heat or cold to the process (up to 3)"))


        self.tc23 = ChoiceEntry(self.page1,
                             values = ["pipe1","pipe2"],
                             label=_("Heat or cold supply to the process from distribution line / branch No."),
                             tip=_("Specify the distribution(supply) line of heat/cold feeding the process, \
using the nomenclature of the hydraulic scheme"))

        self.tc24 = FloatEntry(self.page1,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Temperature of the incoming medium supplying heat or cold to the process/heat exchanger"),
                              tip=_("Temperature of the supplying medium at heat exchangers inlet"))

        self.tc25 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=999999., value = 0.,
                              unitdict=mergeDict(UNITS['MASSFLOW'],UNITS['VOLUMEFLOW']),
                              label=_("Flow rate of the heat supply medium (close to process)"),
                              tip=_("Mass flow of the heat/cold supplyind medium"))

        self.tc26 = FloatEntry(self.page1,
                              ipart=10, decimals=2, minval=0., maxval=999999999., value=0.,
                              unitdict=UNITS['ENERGY'],
                              label=_("Annual consumption of UPH"),
                              tip=_("Only for the process"))

        self.buttonAddProcess = wx.Button(self.page0,-1,_("Add process"))
        self.buttonAddProcess.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddProcess, self.buttonAddProcess)

        self.buttonDeleteProcess = wx.Button(self.page0,-1,_("Delete process"))
        self.buttonDeleteProcess.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProcess, self.buttonDeleteProcess)

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,_("Cancel"))
        #self.buttonCancel.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        self.buttonOK = wx.Button(self,wx.ID_OK,_("OK"))
        #self.buttonOK.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)#SD before HORIZONTAL
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.StaticBoxSizer(self.sizer_13_staticbox, wx.VERTICAL)
        grid_sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_12 = wx.StaticBoxSizer(self.sizer_12_staticbox, wx.VERTICAL)
        grid_sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.StaticBoxSizer(self.sizer_11_staticbox, wx.VERTICAL)
        grid_sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.StaticBoxSizer(self.sizer_8_staticbox, wx.VERTICAL)
        grid_sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.VERTICAL)
        grid_sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_5.Add(self.listBoxProcesses, 1, wx.EXPAND, 0)
        sizer_5.Add(self.buttonAddProcess, 0, wx.ALIGN_RIGHT, 0)
        sizer_5.Add(self.buttonDeleteProcess, 0, wx.ALIGN_RIGHT, 0)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)

        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.ALIGN_CENTER_VERTICAL

        #grid_sizer_1.Add(self.st1, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc1, 0, flagText, 2) #SD before grid_sizer_1
        #grid_sizer_1.Add(self.st2, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc2, 0, flagText, 2) #SD before grid_sizer_1
        #grid_sizer_1.Add(self.st3, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc3, 0, flagText, 2) #SD before grid_sizer_1
        #grid_sizer_1.Add(self.choiceOfDBUnitOperation, 0, flagText, 2)
        grid_sizer_1.Add(self.tc4, 0, flagText, 2)
        #grid_sizer_1.Add(self.st4, 0, flagLabel, 2)
        #grid_sizer_1.Add(self.choiceOfPMDBFluid, 0, flagText, 2)
        #grid_sizer_1.Add(self.st5, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc5, 0, flagText, 2)
        #grid_sizer_1.Add(self.st6, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc6, 0, flagText, 2)
        #grid_sizer_1.Add(self.st7, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc7, 0, flagText, 2)
        #grid_sizer_1.Add(self.st8, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc8, 0, flagText, 2)
        #grid_sizer_1.Add(self.st9, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc9, 0, flagText, 2)
        #grid_sizer_1.Add(self.st10, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc10, 0, flagText, 2)

        sizer_7.Add(grid_sizer_1, 1, wx.LEFT|wx.EXPAND, 40)
        sizer_6.Add(sizer_7, 2, wx.EXPAND, 0)

        #grid_sizer_2.Add(self.st11, 0, flagLabel, 0)
        grid_sizer_2.Add(self.tc11, 0, flagText, 0)
        #grid_sizer_2.Add(self.st12, 0, flagLabel, 0)
        grid_sizer_2.Add(self.tc12, 0, flagText, 0)
        #grid_sizer_2.Add(self.st13, 0, flagLabel, 0)
        grid_sizer_2.Add(self.tc13, 0, flagText, 0)
        #grid_sizer_2.Add(self.st14, 0, flagLabel, 0)
        grid_sizer_2.Add(self.tc14, 0, flagText, 0)

        sizer_8.Add(grid_sizer_2, 1, wx.LEFT|wx.EXPAND, 40)
        sizer_6.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_6, 2, wx.EXPAND, 0)
        self.page0.SetSizer(sizer_4)
        
        #grid_sizer_3.Add(self.st15, 0, flagLabel, 0)
        grid_sizer_3.Add(self.tc15_1, 0, flagText, 0)#SD
        #grid_sizer_3.Add(self.st16, 0, flagLabel, 0)
        grid_sizer_3.Add(self.tc15, 0, flagText, 0)#SD
        #grid_sizer_3.Add(self.st17, 0, flagLabel, 0)
        grid_sizer_3.Add(self.tc15_2, 0, flagText, 0)#SD
        #grid_sizer_3.Add(self.st18, 0, flagLabel, 0)
        #grid_sizer_3.Add(self.choiceHeatRecovered, 0, flagText, 0)
        grid_sizer_3.Add(self.tc16, 0, flagText, 0)#SD
        grid_sizer_3.Add(self.tc17, 0, flagText, 0)#SD
        grid_sizer_3.Add(self.tc18, 0, flagText, 0)#SD

        sizer_11.Add(grid_sizer_3, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
        sizer_10.Add(sizer_11, 1, wx.EXPAND, 0)
        
        #grid_sizer_4.Add(self.st19, 0, flagLabel, 0)
        #grid_sizer_4.Add(self.choiceExistsHeat, 0, flagText, 0)
        #grid_sizer_4.Add(self.st20, 0, flagLabel, 0)
        #grid_sizer_4.Add(self.tc20, 0, flagText, 0)
        #grid_sizer_4.Add(self.st21, 0, flagLabel, 0)
        grid_sizer_4.Add(self.tc19, 0, flagText, 0)#SD
        grid_sizer_4.Add(self.tc20, 0, flagText, 0)#SD
        grid_sizer_4.Add(self.tc21, 0, flagText, 0)#SD

        sizer_12.Add(grid_sizer_4, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
        sizer_10.Add(sizer_12, 1, wx.EXPAND, 0)
        
        #grid_sizer_5.Add(self.st22, 0, flagLabel, 0)
        #grid_sizer_5.Add(self.choiceOfSMDBFluid, 0, flagText, 0)
        #grid_sizer_5.Add(self.st23, 0, flagLabel, 0)
        #grid_sizer_5.Add(self.tc23, 0, flagText, 0)
        #grid_sizer_5.Add(self.st24, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc22, 0, flagText, 0)#SD
        #grid_sizer_5.Add(self.st25, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc23, 0, flagText, 0)#SD
        #grid_sizer_5.Add(self.st26, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc24, 0, flagText, 0)#SD
        grid_sizer_5.Add(self.tc25, 0, flagText, 0)#SD
        grid_sizer_5.Add(self.tc26, 0, flagText, 0)#SD

        sizer_13.Add(grid_sizer_5, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
        sizer_10.Add(sizer_13, 1, wx.EXPAND, 0)
        self.page1.SetSizer(sizer_10)
        self.notebook.AddPage(self.page0, _('Process data'))
        self.notebook.AddPage(self.page1, _('Heat supply and waste heat'))
        sizer_2.Add(self.notebook, 1, wx.EXPAND, 0)
        sizer_3.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizer_3.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)
        sizer_2.Add(sizer_3, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		


    def OnButtonAddProcess(self, event):
        self.clear()

    def OnButtonDeleteProcess(self, event):
        Status.prj.deleteProcess(self.selectedProcessID)
        self.clear()
        self.fillPage()

    def OnListBoxProcessesClick(self, event):
        self.selectedProcessName = str(self.listBoxProcesses.GetStringSelection())
        processes = Status.DB.qprocessdata.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        q = processes.Process[self.selectedProcessName][0]
        self.selectedProcessID = q.QProcessData_ID

        self.tc1.SetValue(str(q.Process))
        if q.ProcType in TRANSPROCTYPES: self.tc2.SetValue(TRANSPROCTYPES[str(q.ProcType)])

        unitOpDict = Status.prj.getUnitOpDict()
        if q.DBUnitOperation_id in unitOpDict.keys():
            unitOp = unitOpDict[q.DBUnitOperation_id]
            self.tc3.SetValue(unitOp)

        fluidDict = Status.prj.getFluidDict()
        if q.ProcMedDBFluid_id in fluidDict.keys():
            fluidName = fluidDict[q.ProcMedDBFluid_id]
            self.tc4.SetValue(fluidName)

        self.tc5.SetValue(str(q.PT))
        self.tc6.SetValue(str(q.PTInFlow))
        self.tc7.SetValue(str(q.PTStartUp))
        self.tc8.SetValue(str(q.VInFlowDay))
        self.tc9.SetValue(str(q.VolProcMed))
        self.tc10.SetValue(str(q.QOpProc))
        self.tc11.SetValue(str(q.HPerDayProc))
        self.tc12.SetValue(str(q.NBatch))
        self.tc13.SetValue(str(q.HBatch))
        self.tc14.SetValue(str(q.NDaysProc))		
        self.tc15.SetValue(str(q.PTOutFlow))

        fluidDict = Status.prj.getFluidDict()        
        if q.ProcMedOut in fluidDict.keys():
            fluidName = fluidDict[q.ProcMedOut]
            self.tc15_1.SetValue(fluidName)

        self.tc15_2.SetValue(str(q.HOutFlow))
        self.tc16.SetValue(str(q.PTFinal))
        self.tc17.SetValue(str(q.VOutFlow))
        if q.HeatRecOK in TRANSYESNO: self.tc18.SetValue(TRANSYESNO[str(q.HeatRecOK)])
        if q.HeatRecExist in TRANSYESNO: self.tc19.SetValue(TRANSYESNO[str(q.HeatRecExist)])
        self.tc20.SetValue(str(q.SourceWasteHeat))	
        self.tc21.SetValue(str(q.PTInFlowRec))

        fluidDict = Status.prj.getFluidDict()        
        if q.SupplyMedDBFluid_id in fluidDict.keys():
            fluidName = fluidDict[q.SupplyMedDBFluid_id]
            self.tc22.SetValue(fluidName)

        self.tc23.SetValue(str(q.PipeDuctProc))
        self.tc24.SetValue(str(q.TSupply))
        self.tc25.SetValue(str(q.SupplyMedFlow))
        self.tc26.SetValue(str(q.UPH))

    def OnButtonCancel(self, event):
        self.clear()
        self.fillPage

    def OnButtonOK(self, event):

        if Status.PId == 0:
	    return
        processName = check(self.tc1.GetValue())
        processes = Status.DB.qprocessdata.Questionnaire_id[Status.PId].\
                    AlternativeProposalNo[Status.ANo].\
                    Process[processName]

	if processName != 'NULL' and len(processes) == 0:
            process = Status.prj.addProcessDummy()
        elif processName != 'NULL' and len(processes) == 1:
            process = processes[0]
        else:
#	    self.showError("HX name has to be a uniqe value!")
	    print "PanelQ3 (ButtonOK): Process name has to be a uniqe value!"
	    return

        unitOpDict = Status.prj.getUnitOpDict()          
        fluidDict = Status.prj.getFluidDict()
            
        tmp = {
            "Questionnaire_id":Status.PId,
            "AlternativeProposalNo":Status.ANo,
            "Process":check(self.tc1.GetValue()),
            "DBUnitOperation_id":check(findKey(unitOpDict,self.tc3.GetValue(text=True))),
            "ProcType":check(findKey(TRANSPROCTYPES,self.tc2.GetValue(text=True))),             
            "ProcMedDBFluid_id":check(findKey(fluidDict,self.tc4.GetValue(text=True))),
            "PT":check(self.tc5.GetValue()), 
            "PTInFlow":check(self.tc6.GetValue()), 
            "PTStartUp":check(self.tc7.GetValue()), 
            "VInFlowDay":check(self.tc8.GetValue()), 
            "VolProcMed":check(self.tc9.GetValue()), 
            "QOpProc":check(self.tc10.GetValue()), 
            "HPerDayProc":check(self.tc11.GetValue()), 
            "NBatch":check(self.tc12.GetValue()), 
            "HBatch":check(self.tc13.GetValue()), 
            "NDaysProc":check(self.tc14.GetValue()),
            "ProcMedOut":check(findKey(fluidDict,self.tc15_1.GetValue(text=True))),
            "PTOutFlow":check(self.tc15.GetValue()),
            "HOutFlow":check(self.tc15_2.GetValue()),
            "PTFinal":check(self.tc16.GetValue()), 
            "VOutFlow":check(self.tc17.GetValue()), 
            "HeatRecOK":check(findKey(TRANSYESNO,self.tc18.entry.GetStringSelection())),
            "HeatRecExist":check(findKey(TRANSYESNO,self.tc19.entry.GetStringSelection())),
            "SourceWasteHeat":check(findKey(TRANSYESNO,self.tc20.entry.GetStringSelection())), 	
            "PTInFlowRec":check(self.tc21.GetValue()), 
            "SupplyMedDBFluid_id":check(findKey(fluidDict,self.tc22.entry.GetStringSelection())),
            "PipeDuctProc":check(self.tc23.GetValue(text=True)), 
            "TSupply":check(self.tc24.GetValue()), 
            "SupplyMedFlow":check(self.tc25.GetValue()), 
            "UPH":check(self.tc26.GetValue()) 
        }
        process.update(tmp)               

        Status.SQL.commit()
        self.fillPage()

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

    def display(self):
        self.fillChoiceOfDBUnitOperation()
        self.fillChoiceOfPMDBFluid()
        self.fillChoiceOfODBFluid()
        self.fillChoiceOfSMDBFluid()
        self.clear()
        self.fillPage()
        self.Show()


    def fillChoiceOfDBUnitOperation(self):
        unitOpDict = Status.prj.getUnitOpDict()
        unitOpNames = unitOpDict.values()
        self.tc3.entry.Clear()
        for name in unitOpNames:
            self.tc3.entry.Append(name) 

            
    def fillChoiceOfPMDBFluid(self):
        fluidDict = Status.prj.getFluidDict()
        fluidNames = fluidDict.values()
        self.tc4.entry.Clear()
        for name in fluidNames:
            self.tc4.entry.Append(name)

    def fillChoiceOfODBFluid(self):
        fluidDict = Status.prj.getFluidDict()
        fluidNames = fluidDict.values()
        self.tc15_1.entry.Clear()
        for name in fluidNames:
            self.tc15_1.entry.Append(name)

    def fillChoiceOfSMDBFluid(self):
        fluidDict = Status.prj.getFluidDict()
        fluidNames = fluidDict.values()
        self.tc22.entry.Clear()
        for name in fluidNames:
            self.tc22.entry.Append(name)

    def fillPage(self):
        self.listBoxProcesses.Clear()
        processList = Status.prj.getProcessList("Process")
        for n in processList:
            self.listBoxProcesses.Append (str(n))

    def clear(self):
        self.tc1.SetValue('')
        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc6.SetValue('')
        self.tc7.SetValue('')
        self.tc8.SetValue('')
        self.tc9.SetValue('')
        self.tc10.SetValue('')
        self.tc11.SetValue('')
        self.tc12.SetValue('')
        self.tc13.SetValue('')
        self.tc14.SetValue('')
        self.tc15.SetValue('')
        self.tc15_1.SetValue('')
        self.tc15_2.SetValue('')
        self.tc16.SetValue('')
        self.tc17.SetValue('')
        self.tc18.SetValue('')
        self.tc19.SetValue('')
        self.tc20.SetValue('')
        self.tc21.SetValue('')
        self.tc22.SetValue('')
        self.tc23.SetValue('')
        self.tc24.SetValue('')
        self.tc25.SetValue('')
        self.tc26.SetValue('')        

if __name__ == '__main__':
    import pSQL
    import MySQLdb
    class Main(object):
	def __init__(self,qid):
	    self.activeQid = qid

    DBName = 'einstein'
    Status.SQL = MySQLdb.connect(host='localhost', user='root', passwd='tom.tom', db=DBName)
    Status.DB =  pSQL.pSQL(Status.SQL, DBName)

    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelQ3")
    main = Main(1)
    panel = PanelQ3(frame, main)

    frame.Show(True)
    app.MainLoop()
        
