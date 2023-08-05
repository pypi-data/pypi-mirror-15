"""Subclass of NewEnum, which is generated by wxFormBuilder."""

import re
import wx
import wxx
from activity.models.ui import ui as ui
import app.resources as rc


# Implementing NewEnum
class EnumDialog(ui.NewEnum):
    """
    This dialog allows the edition of enum type.
    If this enum is inside class or struct, you can also
    specify his visibility.
    """
    @wxx.SetInfo(__doc__)
    def __init__(self, parent, container):
        """Initialize dialog"""
        super(EnumDialog, self).__init__(parent)
        self._container = container
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(rc.GetBitmap("enum"))
        sz = self.m_listCtrl5.GetClientSize()
        w = sz.x // 2 - 4
        self.m_listCtrl5.InsertColumn(0, "items", wx.LIST_FORMAT_LEFT, w)
        self.m_listCtrl5.InsertColumn(1, "values", wx.LIST_FORMAT_LEFT, w)
        if container.inner_class:
            self.m_staticText8.Enable(True)
            self.m_choice2.Enable(True)
        self.SetIcon(icon)

    def SetAttributes(self, obj):
        """Transfer attributes to dialog"""
        self.SetTitle("Edit enum")
        # reset button states
        self.m_bpButton14.Enable(False)
        self.m_bpButton12.Enable(False)
        self.m_bpButton13.Enable(False)
        #remove old elements if any
        self.m_listCtrl5.DeleteAllItems()
        #set name
        self.m_textCtrl55.SetValue(obj._name)
        #set access
        iSel = self.m_choice2.FindString(obj._access)
        self.m_choice2.SetSelection(iSel)
        #insert new elements
        for pair in obj._items:
            self.m_listCtrl5.Append(pair)
        #set note
        self.m_richText3.SetValue(obj.note)
        self.SetTitle("Edit enum")

    def get_kwargs(self):
        """return arguments suitable for object instance"""
        return {'parent': self._container, 'name': self._name,
                'access': self._access, 'items': self._items,
                'note': self._note}

    def CopyAttributes(self, enum):
        """Copy attributes to method"""
        enum._name = self._name
        enum._access = self._access
        enum._items = self._items
        enum.note = self._note

    def Validate(self):
        """Check about validity"""
        self._name = self.m_textCtrl55.GetValue().strip()
        if len(self._name) == 0:
            wx.MessageBox("enum name must be not empty", "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, self)
            return False
        if re.match("^[A-Za-z_][0-9A-Za-z_]*$", self._name) is None:
            wx.MessageBox("enum name contains invalid characters", "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, self)
            return False
        #get the list of values
        self._items = [
            (
                self.m_listCtrl5.GetItemText(i, 0),
                self.m_listCtrl5.GetItemText(i, 1)
            ) for i in range(0, self.m_listCtrl5.GetItemCount())]
        iSel = self.m_choice2.GetCurrentSelection()
        self._access = self.m_choice2.GetString(iSel)
        self._note = self.m_richText3.GetValue()
        return True

    # Handlers for NewEnum events.
    def OnAddEnumItem(self, event):
        """Implement OnAddEnumItem"""
        from dlg import EnumItemDialog
        d = EnumItemDialog(self)
        if d.ShowModal() == wx.ID_OK:
            self.m_listCtrl5.Append((d._label, d._value))

    def OnSelectEnumItem(self, event):
        """Handles enum item selection"""
        # When an enum item is selected, we enable delete it
        self.m_bpButton14.Enable(True)
        # if this item is not the first, enable move up
        self.m_bpButton12.Enable(event.GetIndex() > 0)
        # if this item is not the last, enable move down
        self.m_bpButton13.Enable(event.GetIndex() + 1 < self.m_listCtrl5.GetItemCount())

    def OnDeselectEnumItem(self):
        """Handle enum item unselect"""
        self.m_bpButton14.Enable(False)
        self.m_bpButton12.Enable(False)
        self.m_bpButton13.Enable(False)

    def OnEditEnumItem(self, event):
        """Handles enum item edition"""
        i = event.GetIndex()
        label = self.m_listCtrl5.GetItemText(i, 0)
        value = self.m_listCtrl5.GetItemText(i, 1)
        from dlg import EnumItemDialog
        d = EnumItemDialog(self, (label, value))
        if d.ShowModal() == wx.ID_OK:
            item = wx.ListItem()
            item.SetId(i)
            item.SetMask(wx.LIST_MASK_TEXT)
            item.SetText(d._label)
            item.SetColumn(0)
            self.m_listCtrl5.SetItem(item)
            item.SetMask(wx.LIST_MASK_TEXT)
            item.SetText(d._value)
            item.SetColumn(1)
            self.m_listCtrl5.SetItem(item)

    def OnEnumItemUp(self, event):
        """Implement OnEnumItemUp"""
        i = self.m_listCtrl5.GetFirstSelected()
        label = self.m_listCtrl5.GetItemText(i, 0)
        value = self.m_listCtrl5.GetItemText(i, 1)
        self.m_listCtrl5.DeleteItem(i)
        i = i - 1
        self.m_listCtrl5.InsertStringItem(i, label)
        self.m_listCtrl5.SetStringItem(i, 1, value)
        self.m_listCtrl5.Select(i)

    def OnEnumItemDown(self, event):
        """Implement OnEnumItemDown"""
        i = self.m_listCtrl5.GetFirstSelected()
        label = self.m_listCtrl5.GetItemText(i, 0)
        value = self.m_listCtrl5.GetItemText(i, 1)
        self.m_listCtrl5.DeleteItem(i)
        i = i + 1
        self.m_listCtrl5.InsertStringItem(i, label)
        self.m_listCtrl5.SetStringItem(i, 1, value)
        self.m_listCtrl5.Select(i)

    def OnRemoveEnumItem(self, event):
        """Implement OnRemoveEnumItem"""
        i = self.m_listCtrl5.GetFirstSelected()
        self.m_listCtrl5.DeleteItem(i)

    def OnCancel(self, event):
        """Cancel dialog"""
        self.EndModal(wx.ID_CANCEL)

    def OnOK(self, event):
        """Implement OnOK"""
        if self.Validate():
            self.EndModal(wx.ID_OK)


