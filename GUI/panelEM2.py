#Boa:Frame:PanelEM1
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEM2- GUI component for: Heat supply - Monthly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	28/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#
#       Changes to previous version:
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

import wx

from status import Status
from einstein.modules.energyStats.moduleEM2 import *
import einstein.modules.matPanel as Mp
from einstein.GUI.graphics import drawStackedBarPlot

[wxID_PANELEM2, wxID_PANELEM2BTNBACK, wxID_PANELEM2BTNFORWARD, 
 wxID_PANELEM2BTNOK, wxID_PANELEM2GRID1, wxID_PANELEM2PANELGRAPHMPHS, 
] = [wx.NewId() for _init_ctrls in range(6)]

#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem


class PanelEM2(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        keys = ['EM2'] 
        self.mod = ModuleEM2(keys)

        labels_column = 0

        # remaps drawing methods to the wx widgets.
        #
        # single grid: Monthly process heat demand
        #
        paramList={'labels'      : labels_column,                 # labels column
                   'data'        : 4,                             # data column for this graph
                   'key'         : keys[0],                       # key for Interface
                   'title'       : 'Monthly process heat supply', # title of the graph
                   'ylabel'      : 'UPH (MWh)',                   # y axis label
                   'backcolor'   : GRAPH_BACKGROUND_COLOR,        # graph background color
                   'tickfontsize': 8,                             # tick label fontsize
                   'ignoredrows' : [0,12]}                        # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphMPHS,wx.Panel,drawStackedBarPlot,paramList)

        #
        # additional widgets setup
        #
        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # set grid properties
        # warning: this grid has a variable nr. of cols
        # so the 1st.row has the column headings
        data = Interfaces.GData[keys[0]]
        (rows,cols) = data.shape
        self.grid1.CreateGrid(max(rows,20), cols)

        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.EnableEditing(False)
        headings = data[0] # extract the array of headings
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        for col in range(len(headings)):
            self.grid1.SetColSize(col,115)
            self.grid1.SetColLabelValue(col, headings[col])
        self.grid1.SetColSize(0,120)
        #
        # copy values from dictionary to grid
        # ignore the 1st. row, the column headings, which has been already
        # processed
        for r in range(rows-1):
            self.grid1.SetRowAttr(r, attr)
            for c in range(cols):
                self.grid1.SetCellValue(r, c, data[r+1][c])
                if c == labels_column:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid1.SetGridCursor(0, 0)


    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEM2, name=u'PanelEM2', parent=prnt,
              pos=wx.Point(6, 0), size=wx.Size(800, 600), style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEM2GRID1, name='grid1',
              parent=self, pos=wx.Point(40, 48), size=wx.Size(700, 168),
              style=0)

        self.panelGraphMPHS = wx.Panel(id=wxID_PANELEM2PANELGRAPHMPHS,
              name=u'panelGraphMPHS', parent=self, pos=wx.Point(40, 240),
              size=wx.Size(700, 272), style=wx.TAB_TRAVERSAL)
        self.panelGraphMPHS.SetBackgroundColour(wx.Colour(77, 77, 77))

        self.btnBack = wx.Button(id=wx.ID_BACKWARD, label=u'<<<',
              name=u'btnBack', parent=self, pos=wx.Point(160, 520),
              size=wx.Size(104, 32), style=0)
        self.btnBack.Bind(wx.EVT_BUTTON, self.OnBtnBackButton,
              id=wxID_PANELEM2BTNBACK)

        self.btnOK = wx.Button(id=wx.ID_OK, label=u'OK', name=u'btnOK',
              parent=self, pos=wx.Point(272, 520), size=wx.Size(104, 32),
              style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_PANELEM2BTNOK)

        self.btnForward = wx.Button(id=wx.ID_FORWARD, label=u'>>>',
              name=u'btnForward', parent=self, pos=wx.Point(384, 520),
              size=wx.Size(96, 32), style=0)
        self.btnForward.Bind(wx.EVT_BUTTON, self.OnBtnForwardButton,
              id=wxID_PANELEM2BTNFORWARD)


    def OnBtnOKButton(self, event):
        event.Skip()

    def OnBtnBackButton(self, event):
        event.Skip()

    def OnButton1Button(self, event):
        event.Skip()

    def OnBtnForwardButton(self, event):
        event.Skip()