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
#    parseExcel.py : provides functionality to parse Excel Questionnaires
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by:     Andr� Rattinger 29/03/2010
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

from parseSpreadsheet import parseSpreadsheet
import MySQLdb
import pSQL
from win32com.client import Dispatch
from SpreadsheetDictionary import SpreadsheetDict as SD
import wx
import time


class parseExcel(parseSpreadsheet):
    def __init__(self,filepath,mysql_username,mysql_password):
        parseSpreadsheet.__init__(self, filepath)
        self.__filepath=filepath
        self.__username = mysql_username
        self.__password = mysql_password
    
    
    
    
    def __tupleToList(self,tuple):
        data = []
        for elem in tuple:
            data.append(elem.GetValue())
        return data
    
    def __openExcelDispatch(self,filepath):
        xlApp = Dispatch("Excel.Application")
        xlWb = xlApp.Workbooks.Open(filepath)
        return xlApp, xlWb
    
    def __closeExcelDispatch(self,xlWb,xlApp):
        xlWb.Close(SaveChanges=0)
        xlApp.Quit()
    
    def __splitExcelColumns(self,nr_of_elements, columns, parsed_list,dict,Questionnaire_id,createDictionary,db_table):
        """
        Splits columns of the excel import and inserts them into the Database
        nr_of_elements: Number of Columns that should be inserted into the database (count from left)
        columns: Existing Columns 
        parsed_list: Parsed list from the Excel Worksheet
        dict: additional Dictionary that should be included
        createDictionary: Function that creates the Database Dictionary from the input list
        db_table: pSQL Database Table
        Example Usage: 
        splitExcelColumns(4, 6, QFuel, Questionnaire_ID, createQFuelDictionary,md.qfuel)
        """
        list = []
        for i in xrange(nr_of_elements):
            for j in xrange(0+i,len(parsed_list),columns):
                list.append(parsed_list[j])
            Dict = createDictionary(list,self.__md)
            if Questionnaire_id != "":
                Dict['Questionnaire_id']= Questionnaire_id
            Dict.update(dict)
            db_table.insert(Dict)
            list = []
    
    def __getExcelLists(self, sheetnames, xlWb): 
        lists = []
        if len(sheetnames)!=11:
            return parseSpreadsheet.parseError("wrong number of Sheets"), []
        try:
            sht = xlWb.Worksheets(sheetnames[0])
            Q1=self.__tupleToList(sht.Range("Q1_GeneralData"))    
            Q1+=self.__tupleToList(sht.Range("Q1_StatisticalData"))
            Q1+=self.__tupleToList(sht.Range("Q1_Operation"))
            QProduct =self.__tupleToList(sht.Range("Q1_Products"))
        except:
            return parseSpreadsheet.parseError(sheetnames[0]), []
        
        try:
            sht = xlWb.Worksheets(sheetnames[1])
            Q1+=self.__tupleToList(sht.Range("Q1_Percent"))
            QProduct+=self.__tupleToList(sht.Range("Q2_Products"))
            
            Q2 = self.__tupleToList(sht.Range("Q2_EnergyConsumption"))
            Q2 += self.__tupleToList(sht.Range("Q2_ElectricityConsumption"))
            Q2 += self.__tupleToList(sht.Range("Q2_EnergyConsumptionProduct"))
            QFuel = self.__tupleToList(sht.Range("Q2_EnergyConsumption"))
        except:
            return parseSpreadsheet.parseError(sheetnames[1]), []
        
        try:
            sht = xlWb.Worksheets(sheetnames[2])
            Q3 = self.__tupleToList(sht.Range("Q3_ProcessData"))
            Q3 += self.__tupleToList(sht.Range("Q3_WasteHeat"))
            Q3 += self.__tupleToList(sht.Range("Q3_Schedule")) 
            Q3 += self.__tupleToList(sht.Range("Q3_DataOfExistingHCSupply")) 
        except:
            return parseSpreadsheet.parseError(sheetnames[2]), []
            
        try:    
            sht= xlWb.Worksheets(sheetnames[3])
            Q3+= self.__tupleToList(sht.Range("Q3_ScheduleTolerance"))
            Q3+= self.__tupleToList(sht.Range("Q3_OperationCycle"))
        except:
            return parseSpreadsheet.parseError(sheetnames[3]), []
            
        try:    
            sht = xlWb.Worksheets(sheetnames[8])
            QRenewables = self.__tupleToList(sht.Range("Q7_Interest"))
            QRenewables += self.__tupleToList(sht.Range("Q7_REReason"))
            QRenewables += self.__tupleToList(sht.Range("Q7_Others"))
            QRenewables += self.__tupleToList(sht.Range("Q7_Latitude"))
            QRenewables += self.__tupleToList(sht.Range("Q7_Biomass"))
            
            QSurf = self.__tupleToList(sht.Range("Q7_Area"))
            QSurf += self.__tupleToList(sht.Range("Q7_Roof"))
        except:
            return parseSpreadsheet.parseError(sheetnames[8]), []
          
        try:    
            sht = xlWb.Worksheets(sheetnames[3])
            QProfiles = []
            QProcNames = self.__tupleToList(sht.Range("Q3A_ProcessName"))
            
            for i in xrange(3):
                QProfil = self.__tupleToList(sht.Range("Q3A_Profiles_"+ str(i+1)))
                QProfil.append(QProcNames[i*3])
                QProfiles.append(QProfil)
        
            QIntervals  = self.__tupleToList(sht.Range("Q3A_StartTime_1"))
            QIntervals += self.__tupleToList(sht.Range("Q3A_StartTime_2"))
            QIntervals += self.__tupleToList(sht.Range("Q3A_StartTime_3"))
            QIntervals += self.__tupleToList(sht.Range("Q3A_EndTime_1"))
            QIntervals += self.__tupleToList(sht.Range("Q3A_EndTime_2"))
            QIntervals += self.__tupleToList(sht.Range("Q3A_EndTime_3"))
        except:
            return parseSpreadsheet.parseError(sheetnames[3]), []
        
        try:
            sht = xlWb.Worksheets(sheetnames[10])
            Q9Questionnaire=[]
            for i in xrange(3):
                Q9Questionnaire+=self.__tupleToList(sht.Range("Q9_"+str(i+1)))
        except:
            return parseSpreadsheet.parseError(sheetnames[10]), []
            
        lists.append(Q1)
        lists.append(Q2)
        lists.append(QProduct)
        lists.append(QFuel)
        lists.append(Q3)
        lists.append(QRenewables)
        lists.append(QSurf)
        lists.append(QProfiles)
        lists.append(QIntervals)
        lists.append(Q9Questionnaire)
        print lists
        return "", lists

    
    def parse(self):
        
        Q1 = Q2 = QProduct = QFuel = Q3 = QRenewables = QSurf = QProfiles = QIntervals = Q9Questionnaire = []
        try:
            self.__xlApp, self.__xlWb = self.__openExcelDispatch(self.__filepath)
            __sheets = self.__xlWb.Sheets
            self.__sheetnames = []
            for i in xrange(0,__sheets.count):
                if __sheets[i].Name[0] == 'Q':
                    self.__sheetnames.append(__sheets[i].Name)
            self.__md = self.__connectToDB()
            
        except:
            self.__closeExcelDispatch(self.__xlWb, self.__xlApp)
            return parseSpreadsheet.parseError("Consistency")
            
        try:
            __handle, lists = self.__getExcelLists(self.__sheetnames, self.__xlWb)
        except:
            try:
                time.sleep(3)
                self.__xlApp, self.__xlWb = openExcelDispatch()
                __handle, lists = self.__getExcelLists(self.__sheetnames, self.__xlWb)
            except:
                try:
                    time.sleep(3)
                    self.__xlApp, self.__xlWb = openExcelDispatch()
                    __handle, lists = self.__getExcelLists(self.__sheetnames, self.__xlWb)
                except:
                    self.__closeExcelDispatch(self.__xlWb, self.__xlApp)
                    return parseSpreadsheet.parseError("Consistency")
                
        try:
            Q1, Q2, QProduct, QFuel, Q3, QRenewables, QSurf, QProfiles, QIntervals, Q9Questionnaire = lists
        except:
            self.__closeExcelDispatch(self.__xlWb, self.__xlApp)
            return __handle
        __handle = self.__writeToDB(Q1, Q2, QProduct, QFuel, Q3, QRenewables, QSurf, QProfiles, QIntervals, Q9Questionnaire)
        self.__closeExcelDispatch(self.__xlWb, self.__xlApp)
        return __handle
        

        
    def __connectToDB(self):
        conn = MySQLdb.connect("localhost", self.__username, self.__password, db="einstein")
        md = pSQL.pSQL(conn, "einstein")
        return md
    

    

        
        

    
    
    


