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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load rasmover class from file rasmover
    from rasmover import rasmover
    return rasmover(iface)
