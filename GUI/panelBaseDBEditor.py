# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    panelBaseDBEditor: Base panel of pages in notebook of database editor
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by:     Manuel Wallner 08/03/2010
#
#------------------------------------------------------------------------------
#    (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#    http://www.energyxperts.net/
#
#    This program is free software: you can redistribute it or modify it under
#    the terms of the GNU general public license as published by the Free
#    Software Foundation (www.gnu.org).
#
#==============================================================================
import wx
from GUITools import *
from fonts import *
from displayClasses import *

[wxID_PANEL1, wxID_PANEL1BUTTON1, wxID_PANEL1BUTTON2, wxID_PANEL1LISTBOX1, 
 wxID_PANEL1STATICBOX1, wxID_PANEL1STATICBOX2, 
] = [wx.NewId() for _init_ctrls in range(6)]

TYPE_SIZE_LEFT = 9
TYPE_SIZE_TITLES = 10

VSEP = 4

class PanelBaseDBEditor(wx.Panel):

    def __init__(self, parent, frame1label, frame2label, button1label, button2label):
        self._init_ctrls(parent, frame1label, frame2label, button1label, button2label)
        self.__do_layout()

    def _init_ctrls(self, prnt, frame1label, frame2label, button1label, button2label):

        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt,
              pos=wx.DefaultPosition, size=wx.DefaultSize,
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.DefaultSize)

        fp = FontProperties()

        self.frame1 = wx.StaticBox(id=wxID_PANEL1STATICBOX1,
              label=frame1label, name='frame1', parent=self)

        self.frame1.SetForegroundColour(TITLE_COLOR)
        self.frame1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame2 = wx.StaticBox(id=wxID_PANEL1STATICBOX2,
              label=frame2label, name='frame2', parent=self)

        self.frame2.SetForegroundColour(TITLE_COLOR)
        self.frame2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.listBoxEquipment = wx.ListBox(choices=[], id=wxID_PANEL1LISTBOX1,
              name='listBoxEquipment', parent=self)

        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.frame1.SetFont(fp.getFont())
        self.frame2.SetFont(fp.getFont())
        fp.popFont()

        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_LEFT)

        self.button1 = None
        if len(button1label) > 0:
            self.button1 = wx.Button(id=wxID_PANEL1BUTTON1, label=button1label,
                  name='button1', parent=self)
            self.button1.SetMinSize((136, 22))
            self.button1.SetFont(fp.getFont())

        self.button2 = None
        if len(button2label) > 0:
            self.button2 = wx.Button(id=wxID_PANEL1BUTTON2, label=button2label,
                  name='button2', parent=self)
            self.button2.SetMinSize((136, 22))
            self.button2.SetFont(fp.getFont())

        fp.popFont()

    def __do_layout(self):

        self.sizerPage = wx.StaticBoxSizer(self.frame1, wx.HORIZONTAL)

        self.sizerGridBag = wx.GridBagSizer(hgap = 4, vgap = 4)

        self.sizerPageLeft = wx.StaticBoxSizer(self.frame2, wx.VERTICAL)
        self.sizerPageLeft.Add(self.listBoxEquipment, 1, wx.EXPAND, 0)
        if self.button1 is not None:
            self.sizerPageLeft.Add(self.button1, 0, wx.ALIGN_RIGHT | wx.TOP, 4)
        if self.button2 is not None:
            self.sizerPageLeft.Add(self.button2, 0, wx.ALIGN_RIGHT | wx.TOP, 4)

        self.sizerPageRight = wx.BoxSizer(wx.VERTICAL)
        self.sizerPageRightBottomLeft = wx.BoxSizer(wx.VERTICAL)
        self.sizerPageRightBottomRight = wx.BoxSizer(wx.VERTICAL)

        self.sizerGridBag.Add(self.sizerPageRight, pos = (0,1), flag = wx.ALIGN_CENTER, span = (1,2))
        self.sizerGridBag.Add(self.sizerPageRightBottomLeft, pos = (1,1))
        self.sizerGridBag.Add(self.sizerPageRightBottomRight, pos = (1,2))

        self.sizerPage.Add(self.sizerPageLeft, 0.5, wx.EXPAND | wx.TOP, 10)
        self.sizerPage.Add(self.sizerGridBag, 1, wx.EXPAND | wx.TOP, 10)

        self.SetSizer(self.sizerPage)
        self.Layout()

    def addControl(self, control):

        self.sizerPageRight.Add(control, 0, wx.TOP | wx.EXPAND, VSEP)

    def addControlBottomLeft(self, control):

        self.sizerPageRightBottomLeft.Add(control, 0, wx.TOP | wx.EXPAND, VSEP)

    def addControlBottomRight(self, control):

        self.sizerPageRightBottomRight.Add(control, 0, wx.TOP | wx.EXPAND, VSEP)

    def addStretchSpacer(self):

        self.sizerPageRight.AddStretchSpacer()

    def clearListBox(self):

        self.listBoxEquipment.Clear()

    def addListBoxElement(self, element):

        self.listBoxEquipment.Append(str(element))
