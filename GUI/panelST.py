#Boa:FramePanel:PanelST
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
#	Panel SOLAR THERMAL
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Panel for heat pump design assistant
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	    25/06/2008
#                           (based on PanelHP and PanelBB)
#	Revised by:         
#
#       Changes to previous version:
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

import wx
import wx.grid
#from einstein.modules.heatPump.moduleHP import *
from einstein.GUI.status import Status
import einstein.modules.matPanel as Mp
from einstein.GUI.panelQ4 import PanelQ4
from einstein.GUI.dialogOK import *

from einstein.modules.interfaces import *
from einstein.modules.modules import *
from einstein.modules.constants import *
from numpy import *
from einstein.GUI.addEquipment_popup import * #TS 20080405 changed

[wxID_PANEL, wxID_PANELBUTTONADD, 
 wxID_PANELBUTTONBACK, wxID_PANELBUTTONCANCEL, 
 wxID_PANELBUTTONFWD, wxID_PANELBUTTONOK, 
 wxID_PANELCBCONFIG1, wxID_PANELCHOICECONFIG2, 
 wxID_PANELGRIDPAGEST, wxID_PANELCALCULATE, 
 wxID_PANEL10, wxID_PANEL11, 
 wxID_PANEL12, wxID_PANEL1, 
 wxID_PANELCONFIG, wxID_PANELCONFIG1, 
 wxID_PANELCONFIG2, wxID_PANELCONFIG3, 
 wxID_PANELCONFIG4, wxID_PANELCONFIG5, 
 wxID_PANELCONFIG6, wxID_PANELCONFIG7, 
 wxID_PANELATICBOX1, wxID_PANELTCCONFIG3, 
 wxID_PANELTCCONFIG4, wxID_PANELTCCONFIG5, 
 wxID_PANELTCCONFIG6, wxID_PANELTCCONFIG7, 
 wxID_PANELTCINFO1, wxID_PANELTCINFO2,
 wxID_PANELFIG
] = [wx.NewId() for _init_ctrls in range(31)]

#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem

MAXROWS = 1
COLNO = 6

TYPELIST = STTYPES


#------------------------------------------------------------------------------		
#HS2008-03-22: 
#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		
    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.plot(Status.int.GData['ST Plot'][0],
                      Status.int.GData['ST Plot'][1],
                      'go-', label='QD', linewidth=2)
    self.subplot.plot(Status.int.GData['ST Plot'][0],
                      Status.int.GData['ST Plot'][2],
                      'rs',  label='QA')
    self.subplot.plot(Status.int.GData['ST Plot'][0],
                      Status.int.GData['ST Plot'][3],
                      'go-', label='QD_mod', linewidth=2)
    self.subplot.plot(Status.int.GData['ST Plot'][0],
                      Status.int.GData['ST Plot'][4],
                      'rs',  label='QA_mod')
    self.subplot.axis([0, 100, 0, 3e+7])
    self.subplot.legend()


#------------------------------------------------------------------------------		
class PanelST(wx.Panel):
#------------------------------------------------------------------------------		
#   Panel of the heat pump design assistant
#------------------------------------------------------------------------------		

#    def __init__(self, parent, main, id, pos, size, style, name):
    def __init__(self, parent, main, id, name):

        print "PanelST (__init__)"
        self.prnt = parent
        self.main = main
          
        self._init_ctrls(parent)
#        self.__do_layout()

	self.keys = ['ST Table']
        self.mod = Status.mod.moduleST

#   graphic: Cumulative heat demand by hours
        labels_column = 1
        ignoredrows = []
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : self.keys[0],                # key for Interface
                   'title'       : _('Some title'),           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelFig, wx.Panel, drawFigure, paramList)
        del dummy

        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.grid.CreateGrid(MAXROWS, COLNO)

        self.grid.EnableGridLines(True)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.SetDefaultRowSize(24)
        self.grid.SetDefaultColSize(100)
        self.grid.SetRowLabelSize(30)
        self.grid.SetColSize(0,150)
        self.grid.SetColSize(1,150)
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _("Collector model"))
        self.grid.SetColLabelValue(1, _("Collector type"))
        self.grid.SetColLabelValue(2, _("c0"))
        self.grid.SetColLabelValue(3, _("c1"))
        self.grid.SetColLabelValue(4, _("c2"))
        self.grid.SetColLabelValue(5, _("K(50�)"))
        #
        # copy values from dictionary to grid
        #
        for r in range(MAXROWS):
            self.grid.SetRowAttr(r, attr)
            for c in range(COLNO):
                self.grid.SetCellValue(r, c, "")
                if c <= labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid.SetGridCursor(0, 0)
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL, name='PanelST', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
#        self.SetClientSize(wx.Size(792, 618))

#------------------------------------------------------------------------------		
#       Displays of status
#------------------------------------------------------------------------------		

#..............................................................................
# Figure to be plotted

        self.staticBox1 = wx.StaticBox(id=-1,
              label=_('Temperature dependent heat demand with and without solar system'),
              name='staticBox1', parent=self, pos=wx.Point(450, 130),
              size=wx.Size(340, 260), style=0)

        self.panelFig = wx.Panel(id=wxID_PANELFIG, name='panelFigure', parent=self,
              pos=wx.Point(460, 160), size=wx.Size(320, 220),
              style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)

#..............................................................................
# Grid for display of existing heat pumps

        self.boxTable = wx.StaticBox(id=-1,
              label=_('Solar collector'),
              name='boxTable', parent=self, pos=wx.Point(10, 10),
              size=wx.Size(780, 100), style=0)

        self.grid = wx.grid.Grid(id=wxID_PANELGRIDPAGEST,
              name='gridpageST', parent=self, pos=wx.Point(20, 40),
              size=wx.Size(760, 60), style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageSTGridCellLeftDclick, id=wxID_PANELGRIDPAGEST)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageSTGridCellRightClick, id=wxID_PANELGRIDPAGEST)

#------------------------------------------------------------------------------		
#       Action buttons and text entry
#------------------------------------------------------------------------------		

# Button "run design assistant"
        self.calculate = wx.Button(id=wxID_PANELCALCULATE,
              label=_('run design assistant'), name='ST_Calculate', parent=self,
              pos=wx.Point(230, 130), size=wx.Size(200, 24), style=0)

        self.calculate.Bind(wx.EVT_BUTTON, self.OnCalculateButton,
              id=wxID_PANELCALCULATE)

# Button "add heat pump"
        self.selectCol = wx.Button(id=-1,
              label=_('choose solar collector'), name='selectCol',
              parent=self, pos=wx.Point(10, 130), size=wx.Size(200, 24),
              style=0)
        self.selectCol.Bind(wx.EVT_BUTTON, self.OnSelectColButton,
              id=-1)

#------------------------------------------------------------------------------		
#       System parameters
#------------------------------------------------------------------------------		
        self.boxSystem = wx.StaticBox(id=-1,
              label=_('Solar thermal system parameters'),
              name='boxSystem', parent=self, pos=wx.Point(10, 170),
              size=wx.Size(420, 120), style=0)

        self.stSys1 = wx.StaticText(id=-1,
              label=_('Installed capacity [kW]'),
              name='stSys1', parent=self, pos=wx.Point(20, 200),
              style=0)

        self.tcSys1 = wx.TextCtrl(id=-1, name='tcConfig3',
              parent=self, pos=wx.Point(300, 200), size=wx.Size(120, 20),
              style=wx.TE_PROCESS_ENTER, value="")

        self.tcSys1.Bind(wx.EVT_KILL_FOCUS, self.OnTcSysTextEnter,
              id=-1)


        self.stSys2 = wx.StaticText(id=-1,
              label=_('Efficiency of distribution [-]'),
              name='stSys2', parent=self, pos=wx.Point(20, 230),
              style=0)

        self.tcSys2 = wx.TextCtrl(id=-1, name='tcSys2',
              parent=self, pos=wx.Point(300, 230), size=wx.Size(120, 20),
              style=wx.TE_PROCESS_ENTER, value="")

        self.tcSys2.Bind(wx.EVT_KILL_FOCUS, self.OnTcSysTextEnter,
              id=-1)
        

        self.stSys3 = wx.StaticText(id=-1,
              label=_('Solar buffer storage volume [m3]'),
              name='stSys3', parent=self, pos=wx.Point(20, 260),
              style=0)

        self.tcSys3 = wx.TextCtrl(id=-1, name='tcSys3',
              parent=self, pos=wx.Point(300, 260), size=wx.Size(120, 20),
              style=wx.TE_PROCESS_ENTER, value="")

        self.tcSys3.Bind(wx.EVT_KILL_FOCUS, self.OnTcSysTextEnter,
              id=-1)
        

#------------------------------------------------------------------------------		
#       Configuration design assistant
#------------------------------------------------------------------------------		

        self.boxDA = wx.StaticBox(id=-1,
              label=_('Configuration of design assistant'),
              name='boxDA', parent=self, pos=wx.Point(10, 330),
              size=wx.Size(420, 120), style=0)

#..............................................................................
# 1. Solar fraction

        self.stConfig1 = wx.StaticText(id=-1,
              label=_('Desired solar fraction [-]'),
              name='stConfig1', parent=self, pos=wx.Point(20, 360),
              style=0)

        self.tcConfig1 = wx.TextCtrl(id=-1, name='tcConfig1',
              parent=self, pos=wx.Point(300, 360), size=wx.Size(120, 20),
              style=wx.TE_PROCESS_ENTER, value="")

        self.tcConfig1.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig1TextEnter,
              id=-1)

#        self.tc1 = FloatEntry(self,
#                              ipart=4, decimals=2, minval=0., maxval=1., value=0.5,
#                              unitdict='FRACTION',
#                              label=_("Desired solar fraction"),
#                              tip=_("Reasonable values should be between 0 and 80 %"))
#..............................................................................
# 2. Solar collector type 

        self.stConfig2 = wx.StaticText(id=-1, label=_('Solar collector type'),
              name='stConfig2', parent=self, pos=wx.Point(40, 390),
              style=0)

        self.choiceConfig2 = wx.Choice(choices=TYPELIST, id=-1, name='choice', parent=self,
              pos=wx.Point(300, 390), size=wx.Size(120, 20), style=0)

        self.choiceConfig2.Bind(wx.EVT_CHOICE, self.OnChoiceConfig2Choice,
              id=-1)

#..............................................................................
# 3. Minimum operating hours

        self.stConfig3 = wx.StaticText(id=-1,
              label=_('Minimum annual energy yield [kWh/kW.a]'),
              name='stConfig3', parent=self, pos=wx.Point(40, 420),
              style=0)

        self.tcConfig3 = wx.TextCtrl(id=-1, name='tcConfig3',
              parent=self, pos=wx.Point(300, 420), size=wx.Size(120, 20),
              style=wx.TE_PROCESS_ENTER, value="")

        self.tcConfig3.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig3TextEnter,
              id=-1)


#------------------------------------------------------------------------------		
#       Display field at the right
#------------------------------------------------------------------------------		


        self.stInfo1 = wx.StaticText(id=-1,
              label=_('Latitude of the site'), name='stInfo1',
              parent=self, pos=wx.Point(460, 400), style=0)

        self.stInfo1val = wx.StaticText(id=-1,
              label="-", name='stInfo1',
              parent=self, pos=wx.Point(700, 400), style=0)


        self.stInfo2 = wx.StaticText(id=-1,
              label=_('Total available surface area [m2]'), name='stInfo2',
              parent=self, pos=wx.Point(460, 420), style=0)

        self.stInfo2val = wx.StaticText(id=-1,
              label="-", name='stInfo1',
              parent=self, pos=wx.Point(700, 420), style=0)


        self.stInfo3 = wx.StaticText(id=-1,
              label=_('Total gross solar surface area [m2]'), name='stInfo3',
              parent=self, pos=wx.Point(460, 440), style=0)

        self.stInfo3val = wx.StaticText(id=-1,
              label="-", name='stInfo1',
              parent=self, pos=wx.Point(700, 440), style=0)


        self.stInfo4 = wx.StaticText(id=-1,
              label=_('Solar fraction [%]'), name='stInfo4',
              parent=self, pos=wx.Point(460, 470), style=0)

        self.stInfo4val = wx.StaticText(id=-1,
              label="", name='stInfo4val',
              parent=self, pos=wx.Point(700, 470), style=0)


        self.stInfo5 = wx.StaticText(id=-1,
              label=_('Annual energy yield [kWh/m2.a]'), name='stInfo5',
              parent=self, pos=wx.Point(460, 490), style=0)

        self.stInfo5val = wx.StaticText(id=-1,
              label="", name='stInfo4val',
              parent=self, pos=wx.Point(700, 490), style=0)


        self.stInfo6 = wx.StaticText(id=-1,
              label=_('Average operating temperature (coll.) [\xb0C]'), name='stInfo6',
              parent=self, pos=wx.Point(460, 510), style=0)

        self.stInfo6val = wx.StaticText(id=-1,
              label="---", name='stInfo6val',
              parent=self, pos=wx.Point(700, 510), style=0)


#------------------------------------------------------------------------------		
#       Default action buttons: FWD / BACK / OK / Cancel
#------------------------------------------------------------------------------		

        self.buttonOk = wx.Button(id=wx.ID_OK, label=_('OK'),
              name='buttonOk', parent=self, pos=wx.Point(528, 560),
              size=wx.Size(75, 20), style=0)

        self.buttonCancel = wx.Button(id=wx.ID_CANCEL, label=_('Cancel'),
              name='buttonCancel', parent=self, pos=wx.Point(616,
              560), size=wx.Size(75, 20), style=0)

        self.buttonFwd = wx.Button(id=wxID_PANELBUTTONFWD,
              label='>>>', name='buttonFwd', parent=self,
              pos=wx.Point(704, 560), size=wx.Size(75, 20), style=0)

        self.buttonFwd.Bind(wx.EVT_BUTTON,
              self.OnButtonFwdButton,
              id=wxID_PANELBUTTONFWD)

        self.buttonBack = wx.Button(id=wxID_PANELBUTTONBACK,
              label='<<<', name='buttonBack', parent=self,
              pos=wx.Point(440, 560), size=wx.Size(75, 20), style=0)

        self.buttonBack.Bind(wx.EVT_BUTTON,
              self.OnButtonBackButton,
              id=wxID_PANELBUTTONBACK)

    def __do_layout(self):
        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.ALIGN_CENTER_VERTICAL

        # panel 0, right part, distribution
#        sizer_DA = wx.StaticBoxSizer(self.boxDA, wx.VERTICAL)
#        sizer_DA.Add(self.tc1, 0, flagText, 2)
        
 #------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   function activated on each entry into the panel from the tree
#------------------------------------------------------------------------------		

        self.mod.initPanel()        # prepares data for plotting

#..............................................................................
# update of equipment table

        try:
            data = Status.int.GData[self.keys[0]]
            (rows,cols) = data.shape
        except:
            rows = 0
            cols = COLNO
            
        for r in range(rows):
            for c in range(cols):
                try:
                    self.grid.SetCellValue(r, c, data[r][c])
                except:
                    pass

        for r in range(rows,MAXROWS):
            for c in range(cols):
                self.grid.SetCellValue(r, c, "")

#..............................................................................
# update of system and design assistant parameters

        self.config = Status.int.GData["ST Config"]

        #config0..2: DA parameters
        self.tcConfig1.SetValue(str(self.config[0]))
        self.choiceConfig2.SetSelection(self.config[1])
        self.tcConfig3.SetValue(str(self.config[2]))
        
        #config3..5: system parameters
        self.tcSys1.SetValue(str(self.config[3]))
        self.tcSys2.SetValue(str(self.config[4]))
        self.tcSys3.SetValue(str(self.config[5]))
        
#..............................................................................
# update of info-values

        self.info = Status.int.GData["ST Info"]
        
        self.stInfo1val.SetLabel(str(self.info[0]))
        self.stInfo2val.SetLabel(str(self.info[1]))
        self.stInfo3val.SetLabel(str(self.info[2]))
        self.stInfo4val.SetLabel(str(self.info[3]))
        self.stInfo5val.SetLabel(str(self.info[4]))
        self.stInfo6val.SetLabel(str(self.info[5]))

#..............................................................................
# and finally draw the figure

#        self.panelFig.draw()
        self.Show()
        
#==============================================================================
#   Event handlers
#==============================================================================

#------------------------------------------------------------------------------		
    def OnCalculateButton(self, event):
#------------------------------------------------------------------------------		
#   Button "Run Design Assistant" pressed
#------------------------------------------------------------------------------		

#..............................................................................
# Step 1 design assistant: gets a preselected list of possible heat pumps

        (mode,STList) = self.mod.designAssistant1()
        
#..............................................................................
# In interactive mode open DB Edidor Heat pump and select manually

        if (mode == "MANUAL"):
            self.dbe = DBEditFrame(self,
                            _('Select collector from preselected list'), # title for the dialogs
			    _('dbheatpump'),              # database table
			    0,                         # column to be returned
			    False,
                            preselection = STList)      # database table can be edited in DBEditFrame?
            if self.dbe.ShowModal() == wx.ID_OK:
                STId = self.dbe.theId
            else:
                STId = -1
                print "PanelST: no ST selected after DA1 -> check whether this works"

        elif (mode == "AUTOMATIC"):
            STId = STList[0]    #in automatic mode just take first in the list

        elif (mode == "CANCEL"):
            STId = -1 #make designAssistant2 to understand that
        else:
            print _("PanelST (DesignAssistant-Button): erroneous panel mode: "),mode

#..............................................................................
# Step 2 design assistant: add selected equipment to the list and update display
        
        self.mod.designAssistant2(STId)
        self.display()

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnSelectColButton(self, event):
#------------------------------------------------------------------------------		
#   adds an equipment to the list
#------------------------------------------------------------------------------		

	self.equipe = self.mod.addEquipmentDummy() 

        pu1 =  AddEquipment(self,                      # pointer to this panel
                            self.mod,                  # pointer to the associated module
                            _('Select solar collector'), # title for the dialogs
                            _('dbheatpump'),              # database table
                            0,                         # column to be returned
                            False)                     # database table can be edited in DBEditFrame?

        if pu1.ShowModal() == wx.ID_OK:
            print 'PanelST (Select solar collector): Select collector accepted. Id='+str(pu1.theId)
        else:
            self.mod.deleteEquipment(None)

        self.display()

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnGridPageSTGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
#       edits the selected equipment
#------------------------------------------------------------------------------		

        rowNo = event.GetRow() #number of the selected boiler should be detected depending on the selected row
        EqId = self.mod.getEqId(rowNo)
	dialog = ManualAddDialog(self, EqId)

        if (dialog.ShowModal() ==wx.ID_OK):
            print _("PanelST (OnGridLeftDclick) - OK")

        self.display()

#------------------------------------------------------------------------------		
    def OnGridPageSTGridCellRightClick(self, event):
#------------------------------------------------------------------------------		
#   right double click
#   --> for the moment only DELETE foreseen !!!
#------------------------------------------------------------------------------		

        rowNo = event.GetRow() #number of the selected boiler should be detected depending on the selected row

        ret = "delete"

#..............................................................................
# "delete" selected:

        if (ret=="delete"):
            pu2 =  DialogOK(self,_("delete equipment"),_("do you really want to eliminate the solar system ?"))
            if pu2.ShowModal() == wx.ID_OK:
                self.mod.deleteEquipment(rowNo)
                self.display()
                
        elif (ret == "edit"):
            OnGridPageBBGridCellLeftDclick(self,event)
        
#------------------------------------------------------------------------------		
#   Event handlers: parameter change in design assistant
#------------------------------------------------------------------------------		

    def OnTcConfig1TextEnter(self, event):
        self.config[0] = self.cbConfig1.GetValue()
        print _("new config[%s] value: ")%0,self.config[0]
        Status.int.GData["ST Config"] = self.config
        self.mod.setUserDefinedParamST()

    def OnChoiceConfig2Choice(self, event):
        self.config[1] = self.choiceConfig2.GetSelection()
        print _("new config[%s] value: ")%1,self.config[1]
        Status.int.GData["ST Config"] = self.config
        self.mod.setUserDefinedParamST()

    def OnTcConfig3TextEnter(self, event):
        print _("new config[%s] value: ")%2,self.config[2]
        self.config[2] = self.tcConfig3.GetValue()
        Status.int.GData["ST Config"] = self.config
        self.mod.setUserDefinedParamST()

    def OnTcSysTextEnter(self, event):
        self.config[3] = self.tcSys1.GetValue()
        self.config[4] = self.tcSys2.GetValue()
        self.config[5] = self.tcSys3.GetValue()
        print _("new config[%s] value: ")%3,self.config[3]
        print _("new config[%s] value: ")%4,self.config[4]
        print _("new config[%s] value: ")%5,self.config[5]
        Status.int.GData["ST Config"] = self.config
        self.mod.setUserDefinedParamST()

#------------------------------------------------------------------------------		
#   Default event handlers: FWD / BACK / OK / Cancel - Buttons
#------------------------------------------------------------------------------		

    def OnButtonBackButton(self, event):
        self.Hide
        self.main.tree.SelectItem(self.main.qHC, select=True)
        event.Skip()

    def OnButtonFwdButton(self, event):
        self.Hide
        self.main.tree.SelectItem(self.main.qHP, select=True)
        event.Skip()

    def OnButtonOkButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)
        event.Skip()

    def OnButtonCancelButton(self, event):
        print _("Button exitModuleCancel: CANCEL Option not yet foreseen")

#============================================================================== 				

        
