"""Subclass of GenerateSources, which is generated by wxFormBuilder."""

import wx
import wxx
import app

from activity.models.ui import ui as ui
from ctx import theContext as context


# Implementing GenerateSources
class GenerateSourcesDialog(ui.GenerateSources):
    """
    This method exports the project model to language files.
    The files may be written only if they have changes or may
    be forced to be regenerated by using the checkbox
    'overwrite all'
    """
    @wxx.SetInfo(__doc__)
    def __init__(self, parent, project):
        """"Initialization"""
        super(GenerateSourcesDialog, self).__init__(parent)
        self.project = project
        self.m_author.SetValue(project._author)
        #setup report
        sz = self.m_report.GetClientSize()
        self.m_report.ClearAll()
        sz.x -= 5
        self.m_report.InsertColumn(0, "Operation", wx.LIST_FORMAT_LEFT, sz.x)

    # Handlers for GenerateSources events.
    def OnGenerate(self, event):
        """When the Generate button is pressed"""
        force = self.m_overwrite.GetValue()
        context.App().SaveProject(self.project)
        self.project.ExportCodeFiles(force, self)

    def AppendReportLine(self, line, style=wx.OK):
        """Append a information line on report"""
        self.m_report.InsertStringItem(0, line)
        self.Refresh()
        self.Update()



