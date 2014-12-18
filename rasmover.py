# -*- coding: utf-8 -*-
"""
/***************************************************************************
 rasmover
                                 A QGIS plugin
 rasmover
                              -------------------
        begin                : 2014-03-24
        copyright            : (C) 2014 by geodrinx
        email                : geodrinx@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from rasmoverdialog import rasmoverDialog
import os.path
import math
import sys, itertools, os, glob, subprocess, zipfile, zlib, tempfile
import platform
import string 
import subprocess

try:
  from osgeo import gdal
  from sys import platform as _platform
except ImportError:
  import gdal


rb=QgsRubberBand(iface.mapCanvas(),QGis.Point )
rl=QgsRubberBand(iface.mapCanvas(),QGis.Line )
premuto= False
linea=False
point0=iface.mapCanvas().getCoordinateTransform().toMapCoordinates(0, 0)
point1=iface.mapCanvas().getCoordinateTransform().toMapCoordinates(0, 0)
class rasmover:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'rasmover_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = rasmoverDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/rasmover/icon.png"),
            u"rasmover", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&rasmover", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&rasmover", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):

       
        tool = PointTool(self.iface.mapCanvas())
        self.iface.mapCanvas().setMapTool(tool)  
    
       
  
class PointTool(QgsMapTool):  

        
        def __init__(self, canvas):
        
            QgsMapTool.__init__(self, canvas)
            self.canvas = canvas    

        def canvasPressEvent(self, event):
            x = event.pos().x()
            y = event.pos().y()
            global rb ,premuto ,point0
            if not premuto: 
              premuto=True
              rb=QgsRubberBand(iface.mapCanvas(),QGis.Point )
              rb.setColor ( Qt.red )
              point0 = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
              rb.addPoint(point0)  
  
        def canvasMoveEvent(self, event):
              x = event.pos().x()
              y = event.pos().y()        
              global premuto,point0,point1,linea,rl
              if premuto:
               if not linea:              
                rl.setColor ( Qt.red )
                poin1 = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
                rl.addPoint(point0)  
                rl.addPoint(point1)
                linea=True
               else:
                if linea: 
                  point1 = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
                  rl.reset(QGis.Line)
                  rl.addPoint(point0)  
                  rl.addPoint(point1)
                  
                  
      
        def canvasReleaseEvent(self, event):
            global premuto,linea,rb,rl,point1,point0
            angle = math.atan2(point1.x() - point0.x(), point1.y() - point0.y())
            angle = math.degrees(angle)if angle>0 else (math.degrees(angle) + 180)+180
            premuto=False
            linea=False
            actual_crs = self.canvas.mapRenderer().destinationCrs()
            crsDest = QgsCoordinateReferenceSystem(4326)  # WGS 84 / UTM zone 33N
            xform = QgsCoordinateTransform(actual_crs, crsDest)
            pt1 = xform.transform(point0)

            dbName = os.getenv("HOME")+'/.qgis2/python/plugins/rasmover/temp/coords'

            dx = point1.x() - point0.x()
            dy = point1.y() - point0.y()

            line = ""
            
            f2 = open(dbName+'.csv', 'w')

            f2.write("dx,dy\n")            

            line = ("%lf")      %( dx )
            line = ("%s,%lf\n") %( line, dy )
            
            f2.write(line)
            f2.close()


            out_folder = os.getenv("HOME")+'/.qgis2/python/plugins/rasmover/temp'
            if _platform == "win32":
               out_folder = out_folder.replace("\\","/")

#            print("%s\n") %(out_folder)

            listaRaster = out_folder + '/lista.txt'
            
            f5   = open( listaRaster, 'w' )

            toglimi = 0
                
            for iLayer in range(self.canvas.layerCount()):
                 layer = self.canvas.layer(iLayer)
                 
                 if layer.type() == layer.RasterLayer:
                      if (layer.name() == "moved"):
                         toglimi = layer.id()                        
                      else:           
                         fileIMAGE = str(layer.source())                  
                         scrivimi = ("%s\n") %(fileIMAGE)
                         f5.write( scrivimi )                                          

            if (toglimi != 0):
                 QgsMapLayerRegistry.instance().removeMapLayer(toglimi)
                 #print("HO TOLTO %s\n") %("moved")                 

            f5.close()
                 
            fileVRT = ("%s") %(out_folder + '/original.vrt')
            
            subprocess.call([ "gdalbuildvrt", fileVRT, "-input_file_list", listaRaster ])            
            if _platform == "win32":
               fileVRT = fileVRT.replace("/","\\")
                        
            f1   = open(fileVRT, 'r')

            f2   = open(out_folder + '/moved.vrt', 'w')
                        
            for line in f1:
               stringa = line

               if(string.find(stringa,"<GeoTransform>") <> -1):
                  words1 = stringa.replace(">-","> -");
                  words2 = words1.replace(",-",", -");
                  words3 = words2.split();
			  
#                  print("%s") %( words[1].replace(",","") )
#                  print("%s") %( words[4].replace(",","") )

                  coordX = words3[1].replace(",","")
                  coordY = words3[4].replace(",","")  
                  
                  X = float( coordX ) + dx
                  Y = float( coordY ) + dy                                 

                  stringazza = "  <GeoTransform>"
                  stringazza = ("%s %lf, ") %( stringazza, X )
                  stringazza = ("%s %s") %( stringazza, words3[2] )
                  stringazza = ("%s %s") %( stringazza, words3[3] )
                  stringazza = ("%s %lf,") %( stringazza, Y )
                  stringazza = ("%s %s ") %( stringazza, words3[5] )
                  stringazza = ("%s %s ") %( stringazza, words3[6] )                                                      
                  f2.write(stringazza)
                  
                  
               else:  
                  f2.write(stringa)


            f2.close()
            f1.close() 

            rl.reset()
            rb.reset()  

            fileName = out_folder + '/moved.vrt'
            fileInfo = QFileInfo(fileName)
            baseName = fileInfo.baseName()
            rlayer = QgsRasterLayer(fileName, baseName)
            if not rlayer.isValid():
              print "Layer failed to load!"
              
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)              
            


        def activate(self):
            pass
    
        def deactivate(self):
            pass
    
        def isZoomTool(self):
            return False
    
        def isTransient(self):
            return False
    
        def isEditTool(self):
            return True    
