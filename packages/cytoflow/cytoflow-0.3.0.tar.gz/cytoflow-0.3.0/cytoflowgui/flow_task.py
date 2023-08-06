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
Created on Feb 11, 2015

@author: brian
"""

# from traits.etsconfig.api import ETSConfig
# ETSConfig.toolkit = 'qt4'

import os.path

from traits.api import Instance, List, Bool, Str, HasStrictTraits
from pyface.tasks.api import Task, TaskLayout, PaneItem
from pyface.tasks.action.api import SMenu, SMenuBar, SToolBar, TaskAction
from pyface.api import FileDialog, OK, ImageResource, AboutDialog, information
from envisage.api import Plugin, ExtensionPoint, contributes_to
from envisage.ui.tasks.api import TaskFactory

from cytoflowgui.flow_task_pane import FlowTaskPane
from cytoflowgui.workflow_pane import WorkflowDockPane
from cytoflowgui.view_pane import ViewDockPane
from cytoflowgui.workflow import LocalWorkflow
from cytoflowgui.op_plugins import IOperationPlugin, ImportPlugin, OP_PLUGIN_EXT
from cytoflowgui.view_plugins import IViewPlugin, VIEW_PLUGIN_EXT
from cytoflowgui.notebook import JupyterNotebookWriter
import cytoflowgui.util as guiutil
import mailto

import pickle as pickle

class FlowTask(Task):
    """
    classdocs
    """
    
    id = "edu.mit.synbio.cytoflow.flow_task"
    name = "Cytometry analysis"
    
    # the main workflow instance.
    # THIS IS WHERE IT'S INSTANTIATED (note the args=() )
    model = Instance(LocalWorkflow, args = ())
        
    # the center pane
    view = Instance(FlowTaskPane)
    
    # plugin lists, to setup the interface
    op_plugins = List(IOperationPlugin)
    view_plugins = List(IViewPlugin)
    
    menu_bar = SMenuBar(SMenu(TaskAction(name='Open...',
                                         method='on_open',
                                         accelerator='Ctrl+O'),
                              TaskAction(name='Save',
                                         #image='save', 
                                         method='on_save',
                                         accelerator='Ctrl+S'),
                              TaskAction(name='Save As...',
                                         method='on_save_as',
                                         accelerator='Ctrl+e'),
                              TaskAction(name='Save Plot...',
                                         method='on_export',
                                         accelerator='Ctrl+x'),
                              TaskAction(name='Export Jupyter notebook...',
                                         method='on_notebook',
                                         accelerator='Ctrl+I'),                              
                              TaskAction(name='Preferences...',
                                         method='on_prefs',
                                         accelerator='Ctrl+P'),
                              id='File', name='&File'),
                        SMenu(TaskAction(name = 'Report a problem....',
                                         method = 'on_problem'),
                              TaskAction(name='About...',
                                         method='on_about'),
                              id="Help", name ="&Help"))
    
    tool_bars = [ SToolBar(TaskAction(method='on_new',
                                      name = "New",
                                      tooltip='New workflow',
                                      image=ImageResource('new')),
                           TaskAction(method='on_open',
                                      name = "Open",
                                      tooltip='Open a file',
                                      image=ImageResource('open')),
                           TaskAction(method='on_save',
                                      name = "Save",
                                      tooltip='Save the current file',
                                      image=ImageResource('save')),
                           TaskAction(method='on_export',
                                      name = "Save Plot",
                                      tooltip='Save the current plot',
                                      image=ImageResource('export')),
                           TaskAction(method='on_notebook',
                                      name='Notebook',
                                      tooltip="Export to an Jupyter notebook...",
                                      image=ImageResource('ipython')),
                           TaskAction(method='on_prefs',
                                      name = "Prefs",
                                      tooltip='Preferences',
                                      image=ImageResource('prefs'),
                                      enabled = False),
                           image_size = (32, 32))]
    
    # are we debugging?  ie, do we need a default setup?
    debug = Bool
    
    def activated(self):
        # add an import plugin
        import_op = ImportPlugin().get_operation()
        
        # if we're debugging, add a few data bits
        if self.debug:
            from cytoflow import Tube
                     
            import_op.conditions["Dox"] = "float"
        
            tube1 = Tube(file = "../cytoflow/tests/data/Plate01/CFP_Well_A4.fcs",
                         conditions = {"Dox" : 0.0})
        
            tube2 = Tube(file = "../cytoflow/tests/data/Plate01/RFP_Well_A3.fcs",
                         conditions = {"Dox" : 1.0})
        
            import_op.tubes = [tube1, tube2]
            
        self.model.add_operation(import_op)      
    
    def prepare_destroy(self):
        self.model = None
    
    def _default_layout_default(self):
        return TaskLayout(left = PaneItem("edu.mit.synbio.workflow_pane"),
                          right = PaneItem("edu.mit.synbio.view_traits_pane"))
     
    def create_central_pane(self):
        self.view = FlowTaskPane(model = self.model)
        return self.view
     
    def create_dock_panes(self):
        return [WorkflowDockPane(model = self.model, 
                                 plugins = self.op_plugins,
                                 task = self), 
                ViewDockPane(model = self.model,
                             plugins = self.view_plugins,
                             task = self)]
        
    def on_new(self):
        self.model.workflow = []
        
        # add an import operation
        import_op = ImportPlugin().get_operation()
        self.model.add_operation(import_op)       
        
    def on_open(self):
        """ Shows a dialog to open a file.
        """
        dialog = FileDialog(parent=self.window.control, 
                            action = 'open',
                            wildcard='*.flow')
        if dialog.open() == OK:
            self.open_file(dialog.path)
            
    def open_file(self, path):
        f = open(path, 'r')
        unpickler = pickle.Unpickler(f)
        new_workflow = unpickler.load()

        # replace the current workflow with the one we just loaded
        
        if False:
            from event_tracer import record_events 
            
            with record_events() as container:
                self.model.workflow = new_workflow
                                
            container.save_to_directory(os.getcwd()) 
        else:
            self.model.workflow = new_workflow
        
    def on_save(self):
        """ Shows a dialog to open a file.
        """
        dialog = FileDialog(parent=self.window.control,
                            action = 'save as', 
                            wildcard='*.flow')
        if dialog.open() == OK:
            self.save_file(dialog.path)
            
    def on_save_as(self):
        pass
            
    def save_file(self, path):
        # TODO - error handling
        f = open(path, 'w')
        pickler = pickle.Pickler(f, 0)  # text protocol for now
        pickler.dump(self.model.workflow)
        
    def on_export(self):
        """
        Shows a dialog to export a file
        """
        
        information(None, "This will save exactly what you see on the screen "
                          "to a file. Choose the file type via the file " 
                          "extension (ie .png, .pdf, .jpg)", "Export")
        
        dialog = FileDialog(parent = self.window.control,
                            action = 'save as')
        
        if dialog.open() == OK:
            self.view.export(dialog.path)
            
    def on_notebook(self):
        """
        Shows a dialog to export the workflow to an Jupyter notebook
        """
        
        return
    
        dialog = FileDialog(parent = self.window.control,
                            action = 'save as',
                            wildcard = '*.ipynb')
        if dialog.open() == OK:
            writer = JupyterNotebookWriter(file = dialog.path)
            writer.export(self.workflow)
   
    
    def on_prefs(self):
        pass
    
    def on_problem(self):
        
        information(None, "Your email client will now create a new message to the "
                    "developer.  Debugging logs are attached.  Please fill "
                    "out the template bug report and send -- thank you for "
                    "reporting a bug!")
        
#         import tempfile
        log = guiutil.parent_log.getvalue()
        log += self.model.get_child_log()
# 
#         logfile = tempfile.NamedTemporaryFile(delete = False)
#         logfile.write(parent_log)
#         logfile.write(child_log)
#         logfile.close()
        
        versions = ["{0} {1}".format(key, value) for key, value in self._get_package_versions().iteritems()]

        body = """
Thank you for your bug report!  Please fill out the following template.

PLATFORM (Mac, PC, Linux, other):

OPERATING SYSTEM (eg OSX 10.7, Windows 8.1):

SEVERITY (Critical? Major? Minor? Enhancement?):

DESCRIPTION:
  - What were you trying to do?
  - What happened?
  - What did you expect to happen?
  

PACKAGE VERSIONS: {0}

DEBUG LOG: {1}
""".format(versions, log)

        mailto.mailto("teague@mit.edu", 
                      subject = "Cytoflow bug report",
                      body = body)
    
    def _get_package_versions(self):
    
        import sys
        from cytoflow import __version__ as cf_version
        from fcsparser import __version__ as fcs_version
        from pandas import __version__ as pd_version
        from numpy import __version__ as np_version
        from numexpr import __version__ as nxp_version
        from bottleneck import __version__ as btl_version
        from seaborn import __version__ as sns_version
        from matplotlib import __version__ as mpl_version
        from scipy import __version__ as scipy_version
        from sklearn import __version__ as skl_version
        from pyface import __version__ as pyf_version
        from envisage import __version__ as env_version
        from traits import __version__ as trt_version
        from traitsui import __version__ as trt_ui_version
        
        return {"python" : sys.version,
                "cytoflow" : cf_version,
                "fcsparser" : fcs_version,
                "pandas" : pd_version,
                "numpy" : np_version,
                "numexpr" : nxp_version,
                "bottleneck" : btl_version,
                "seaborn" : sns_version,
                "matplotlib" : mpl_version,
                "scipy" : scipy_version,
                "scikit-learn" : skl_version,
                "pyface" : pyf_version,
                "envisage" : env_version,
                "traits" : trt_version,
                "traitsui" : trt_ui_version}
        
        
    def on_about(self):
        versions = self._get_package_versions()
        text = ["<b>Cytoflow {0}</b>".format(versions['cytoflow']),
                "<p>"]
        
        ver_text = ["{0} {1}".format(key, value) for key, value in versions.iteritems()]
        
        text.extend(ver_text)
        
        text.extend(["Icons from the <a href=http://tango.freedesktop.org>Tango Desktop Project</a>",
                "<a href=https://thenounproject.com/search/?q=setup&i=14287>Settings icon</a> by Paulo Sa Ferreira from <a href=https://thenounproject.com>The Noun Project</a>",
                "<a href=http://www.freepik.com/free-photos-vectors/background>App icon from Starline - Freepik.com</a>",
                "Cuvette image from Wikimedia Commons user <a href=http://commons.wikimedia.org/wiki/File:Hellma_Large_cone_cytometry_cell.JPG>HellmaUSA</a>"])
        
        dialog = AboutDialog(text = text,
                             parent = self.window.control,
                             title = "About",
                             image = ImageResource('cuvette'),
                             additions = text)
        dialog.open()
    
    def add_operation(self, op_id):
        # first, find the matching plugin
        plugin = next((x for x in self.op_plugins if x.id == op_id))
                
        # add the operation and the operation's default view
        self.model.add_operation(plugin.get_operation())
        
    def set_current_view(self, view_id):
        """
        called by the view pane 
        """

        if view_id == "default":
            self.model.set_current_view(self.model.selected.default_view)
        else:
            plugin = next((x for x in self.view_plugins if x.view_id == view_id))
            self.model.set_current_view(plugin.get_view())
        

        
class FlowTaskPlugin(Plugin):
    """
    An Envisage plugin wrapping FlowTask
    """

    # Extension point IDs.
    PREFERENCES       = 'envisage.preferences'
    PREFERENCES_PANES = 'envisage.ui.tasks.preferences_panes'
    TASKS             = 'envisage.ui.tasks.tasks'
    
    # these need to be declared in a Plugin instance; we pass them to h
    # the task instance thru its factory, below.
    op_plugins = ExtensionPoint(List(IOperationPlugin), OP_PLUGIN_EXT)
    view_plugins = ExtensionPoint(List(IViewPlugin), VIEW_PLUGIN_EXT)
    
    debug = Bool(False)

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'edu.mit.synbio.cytoflow'

    # The plugin's name (suitable for displaying to the user).
    name = 'Cytoflow'

    ###########################################################################
    # Protected interface.
    ###########################################################################

    @contributes_to(PREFERENCES)
    def _get_preferences(self):
        filename = os.path.join(os.path.dirname(__file__), 'preferences.ini')
        return [ 'file://' + filename ]
    
    @contributes_to(PREFERENCES_PANES)
    def _get_preferences_panes(self):
        from preferences import CytoflowPreferencesPane
        return [CytoflowPreferencesPane]

    @contributes_to(TASKS)
    def _get_tasks(self):
        return [TaskFactory(id = 'edu.mit.synbio.cytoflow.flow_task',
                            name = 'Cytometry analysis',
                            factory = lambda **x: FlowTask(application = self.application,
                                                           op_plugins = self.op_plugins,
                                                           view_plugins = self.view_plugins,
                                                           debug = self.debug,
                                                           **x))]
