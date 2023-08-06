#!/usr/bin/env python2.7

# (c) Massachusetts Institute of Technology 2015-2016
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Created on Feb 24, 2015

@author: brian
"""

from traits.api import provides, Callable, Dict
from traitsui.api import View, Item, VGroup, Controller, EnumEditor
from envisage.api import Plugin, contributes_to
from pyface.api import ImageResource

import numpy as np
import scipy.stats

from cytoflow import BarChartView, geom_mean

from cytoflowgui.subset_editor import SubsetEditor
from cytoflowgui.color_text_editor import ColorTextEditor
from cytoflowgui.clearable_enum_editor import ClearableEnumEditor
from cytoflowgui.view_plugins.i_view_plugin \
    import IViewPlugin, VIEW_PLUGIN_EXT, ViewHandlerMixin, PluginViewMixin
    
class BarChartHandler(Controller, ViewHandlerMixin):
    """
    docs
    """
    
    summary_functions = Dict({np.mean : "Mean",
                             # TODO - add count and proportion
                             geom_mean : "Geom.Mean",
                             len : "Count"})
    
    spread_functions = Dict({np.std : "Std.Dev.",
                             scipy.stats.sem : "S.E.M"
                       # TODO - add 95% CI
                       })
    
    def default_traits_view(self):
        return View(VGroup(
                    VGroup(Item('name'),
                           Item('channel',
                                editor=EnumEditor(name='context.channels'),
                                label = "Channel"),
                           Item('by',
                                editor=EnumEditor(name='context.conditions'),
                                label = "Variable"),
                           Item('function',
                                editor = EnumEditor(name='handler.summary_functions'),
                                label = "Summary\nFunction"),
                          # TODO - waiting on seaborn v0.6
#                      Item('object.orientation')
#                       Item('object.error_bars',
#                            editor = EnumEditor(values = {None : "",
#                                                          "data" : "Data",
#                                                          "summary" : "Summary"}),
#                            label = "Error bars?"),
#                       Item('object.error_function',
#                            editor = EnumEditor(name='handler.spread_functions'),
#                            label = "Error bar\nfunction",
#                            visible_when = 'object.error_bars is not None'),
#                       Item('object.error_var',
#                            editor = EnumEditor(name = 'handler.conditions'),
#                            label = "Error bar\nVariable",
#                            visible_when = 'object.error_bars == "summary"'),
                           Item('xfacet',
                                editor=ClearableEnumEditor(name='context.conditions'),
                                label = "Horizontal\nFacet"),
                           Item('yfacet',
                                editor=ClearableEnumEditor(name='context.conditions'),
                                label = "Vertical\nFacet"),
                           Item('huefacet',
                                editor=ClearableEnumEditor(name='context.conditions'),
                                label="Color\nFacet"),
                             label = "Bar Chart",
                             show_border = False),
                    VGroup(Item('subset',
                                show_label = False,
                                editor = SubsetEditor(conditions_types = "context.conditions_types",
                                                      conditions_values = "context.conditions_values")),
                           label = "Subset",
                           show_border = False,
                           show_labels = False),
                    Item('warning',
                         resizable = True,
                         visible_when = 'warning',
                         editor = ColorTextEditor(foreground_color = "#000000",
                                                 background_color = "#ffff99")),
                    Item('error',
                         resizable = True,
                         visible_when = 'error',
                         editor = ColorTextEditor(foreground_color = "#000000",
                                                  background_color = "#ff9191"))))
    
class BarChartPluginView(BarChartView, PluginViewMixin):
    handler_factory = Callable(BarChartHandler)

@provides(IViewPlugin)
class BarChartPlugin(Plugin):
    """
    classdocs
    """

    id = 'edu.mit.synbio.cytoflowgui.view.barchart'
    view_id = 'edu.mit.synbio.cytoflow.view.barchart'
    short_name = "Bar Chart"
    
    def get_view(self):
        return BarChartPluginView()

    def get_icon(self):
        return ImageResource('bar_chart')

    @contributes_to(VIEW_PLUGIN_EXT)
    def get_plugin(self):
        return self