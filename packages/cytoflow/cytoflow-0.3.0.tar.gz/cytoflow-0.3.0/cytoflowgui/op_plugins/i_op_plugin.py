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
Created on Mar 15, 2015

@author: brian
"""
from traits.api import Interface, Str, HasTraits, Instance, Property, List
from traitsui.api import Group, Item
from cytoflowgui.workflow import WorkflowItem
from cytoflowgui.color_text_editor import ColorTextEditor

OP_PLUGIN_EXT = 'edu.mit.synbio.cytoflow.op_plugins'

class IOperationPlugin(Interface):
    """
    Attributes
    ----------
    
    id : Str
        The Envisage ID used to refer to this plugin
        
    operation_id : Str
        Same as the "id" attribute of the IOperation this plugin wraps.
        
    short_name : Str
        The operation's "short" name - for menus and toolbar tool tips
        
    menu_group : Str
        If we were to put this op in a menu, what submenu to use?
        Not currently used.
    """
    
    operation_id = Str
    short_name = Str
    menu_group = Str

    def get_operation(self):
        """
        Return an instance of the IOperation that this plugin wraps, along
        with the factory for the handler
        """

    def get_icon(self):
        """
        
        """

class PluginOpMixin(HasTraits):
    pass

shared_op_traits = Group(Item('context.warning',
                              label = 'Warning',
                              resizable = True,
                              visible_when = 'context.warning',
                              editor = ColorTextEditor(foreground_color = "#000000",
                                                       background_color = "#ffff99")),
                         Item('context.error',
                               label = 'Error',
                               resizable = True,
                               visible_when = 'context.error',
                               editor = ColorTextEditor(foreground_color = "#000000",
                                                        background_color = "#ff9191")))

        
class OpHandlerMixin(HasTraits):
    """
    This used to hold properties for dynamically updated metadata lists ....
    but now those are updated elsewhere.  Keep this around in case a mixin
    becomes useful again.
    """
    
    pass
