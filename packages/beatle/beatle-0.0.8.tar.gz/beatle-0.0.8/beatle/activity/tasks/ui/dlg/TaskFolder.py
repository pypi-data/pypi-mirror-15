"""Subclass of NewFolder, which is generated by wxFormBuilder."""

import wx
import wxx
import app.resources as rc
from activity.tasks.ui import ui


# Implementing NewFolder
class TaskFolderDialog(ui.NewFolder):
    """
    This dialog allows to setup the task folder name.
    Folders are organizative items for classify the
    tasks.
    """
    @wxx.SetInfo(__doc__)
    def __init__(self, parent, container):
        """Initialization"""
        super(TaskFolderDialog, self).__init__(parent)
        self._container = container
        self.original = ""
        self.m_textCtrl2.SetFocus()
        self.m_sdbSizer2OK.SetDefault()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(rc.GetBitmap("folder"))
        self.SetIcon(icon)

    def Validate(self):
        """Process OnOk event"""
        self._name = self.m_textCtrl2.GetValue().strip()
        if len(self._name) == 0:
            wx.MessageBox("Task folder name must be non empty", "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, self)
            return False
        self._note = self.m_richText3.GetValue()
        return True

    def CopyAttributes(self, folder):
        """Transfer attributes to folder"""
        folder._name = self._name
        folder.note = self._note

    def SetAttributes(self, folder):
        """Transfer attributes from existing constructor"""
        self._container = folder.parent
        self._name = folder._name
        self.original = folder._name
        self._note = folder.note
        self.m_textCtrl2.SetValue(self._name)
        self.m_richText3.SetValue(self._note)
        self.SetTitle("Edit task folder")

    def get_kwargs(self):
        """return arguments suitable for object instance"""
        return {'parent': self._container, 'name': self._name,
            'note': self._note}

    def OnOK(self, event):
        """On Ok"""
        if self.Validate():
            self.EndModal(wx.ID_OK)





