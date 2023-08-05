"""Subclass of ImportProject, which is generated by wxFormBuilder."""

import wx
import wxx
import app
import os
import model


# Implementing ImportProject
class ImportProjectDialog(app.ImportProject):
    """
    This dialog allows to import a project
    into the workspace.
    """
    @wxx.SetInfo(__doc__)
    def __init__(self, parent, workspace):
        """Initialize dialog"""
        super(ImportProjectDialog, self).__init__(parent)
        self.workspace = workspace

    def CppImport(self, dlg=None):
        """Do the work of importing C++ files"""
        wx.MessageBox("The C++ import is not already implemented", "Error",
            wx.OK | wx.CENTER | wx.ICON_ERROR, self)
        return False

    def PythonImport(self, dlg=None):
        """Do the work of importing python files"""
        #create the project
        kwargs = {
            'parent': self.workspace, 'name': self.project_name, 'language': 'python',
            'dir': self.dir,
            'note': 'project imported from {self.origin_dir}'.format(self=self)}
        project = model.Project(**kwargs)
        return project.update_from_sources(dir=self.origin_dir, progress=dlg)

    def Validate(self):
        """Validate dialog"""
        # first of all, get the base dir
        self.origin_dir = self.m_dirPicker2.Path
        if not os.access(self.origin_dir, os.R_OK):
            wx.MessageBox("The path {self.origin_dir} is not readable".format(self=self), "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, self)
            return False
        (head, self.project_name) = os.path.split(self.origin_dir)
        if len(self.project_name) == 0:
            wx.MessageBox("The path {self.dir} is invalid".format(self=self), "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, self)
            return False
        self.dir = os.path.join(self.workspace._dir, self.project_name)
        #Operate throgh the import target
        self.option = self.m_choicebook4.GetSelection()
        return True

    def DoImport(self, dlg=None):
        """This call is expected to come after EndDialog(wx.ID_OK)"""
        if self.option == 0:
            return self.PythonImport(dlg)
        else:
            return self.CppImport(dlg)

    def OnCancel(self, event):
        """cancel event handler"""
        self.EndModal(wx.ID_CANCEL)

    def OnOK(self, event):
        """Handle OnOk"""
        if self.Validate():
            self.EndModal(wx.ID_OK)


