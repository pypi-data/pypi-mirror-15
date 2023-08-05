"""Subclass of EditDecorators, which is generated by wxFormBuilder."""

import wx
import wxx
from activity.models.ui import ui as ui
import app.resources as rc
import model
from PyDecorator import PyDecoratorDialog


# Implementing EditDecorators
class EditDecoratorsDialog(ui.EditDecorators):
    """
    This dialog allows to edit the decorators applied
    to some method
    """
    @wxx.SetInfo(__doc__)
    def __init__(self, parent, container):
        """Initialize dialog"""
        super(EditDecoratorsDialog, self).__init__(parent)
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(rc.GetBitmap("decorator"))
        self.SetIcon(icon)
        self._container = container
        sz = self.m_listCtrl6.GetClientSize()
        self.m_listCtrl6.InsertColumn(0, "decorators", wx.LIST_FORMAT_LEFT, sz.x - 48)
        # iterate through the decorators and insert them
        self._count = 0
        self._map = {}
        for deco in container[model.py.Decorator]:
            self.m_listCtrl6.InsertStringItem(self._count, deco._name)
            self.m_listCtrl6.SetItemData(self._count, self._count)
            self._map[self._count] = deco
            self._count = self._count + 1

    def Validate(self):
        """Validate dialog"""
        # Transform al decorators in new decorators
        for k in self._map:
            v = self._map[k]
            if type(v) is not tuple:
                name = v._name
                call = v._call
                self._map[k] = (name, call)
        return True

    # Handlers for EditDecorators events.
    def OnSelectDecorator(self, event):
        """Handles the selection of a decorator in the report"""
        self.m_bpButton65.Enable(True)
        self.m_bpButton66.Enable(True)
        n = self.m_listCtrl6.GetFirstSelected()
        if n > 0:
            self.m_bpButton67.Enable(True)
        if n + 1 < self.m_listCtrl6.GetItemCount():
            self.m_bpButton68.Enable(True)

    def OnUnselectDecorator(self, event):
        """Handles decorator unselection"""
        self.m_bpButton65.Enable(False)
        self.m_bpButton66.Enable(False)
        self.m_bpButton67.Enable(False)
        self.m_bpButton68.Enable(False)

    def OnDecoratorUp(self, event):
        """Handles the addition of a new decorator"""
        n = self.m_listCtrl6.GetFirstSelected()
        if n == wx.NOT_FOUND:
            return
        k = self.m_listCtrl6.GetItemData(n)
        name = self.m_listCtrl6.GetItemText(n)
        self.m_listCtrl6.DeleteItem(n)
        n = n - 1
        self.m_listCtrl6.InsertStringItem(n, name)
        self.m_listCtrl6.SetItemData(n, k)
        self.m_listCtrl6.Select(n)

    def OnDecoratorDown(self, event):
        """Handles the addition of a new decorator"""
        n = self.m_listCtrl6.GetFirstSelected()
        if n == wx.NOT_FOUND:
            return
        n = self.m_listCtrl6.GetFirstSelected()
        if n == wx.NOT_FOUND:
            return
        k = self.m_listCtrl6.GetItemData(n)
        name = self.m_listCtrl6.GetItemText(n)
        self.m_listCtrl6.DeleteItem(n)
        n = n + 1
        self.m_listCtrl6.InsertStringItem(n, name)
        self.m_listCtrl6.SetItemData(n, k)
        self.m_listCtrl6.Select(n)

    def OnAddDecorator(self, event):
        """Handles the addition of a new decorator"""
        dialog = PyDecoratorDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            # se anhade el nuevo decorador
            n = self.m_listCtrl6.GetItemCount()
            name = dialog._name
            call = dialog._call
            self.m_listCtrl6.InsertStringItem(n, name)
            self.m_listCtrl6.SetItemData(n, self._count)
            self._map[self._count] = (name, call)
            self.m_listCtrl6.Select(self._count)
            self._count = self._count + 1

    def OnEditDecorator(self, event):
        """Handles the edition of a decorator"""
        # get selected index
        n = self.m_listCtrl6.GetFirstSelected()
        if n == wx.NOT_FOUND:
            return
        # get key
        k = self.m_listCtrl6.GetItemData(n)
        # get object
        obj = self._map[k]
        # edit decorator
        dialog = PyDecoratorDialog(self, self._container)
        dialog.SetAttributes(obj)
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog._name
            call = dialog._call
            # update the element
            self.m_listCtrl6.SetItemText(n, name)
            # replace entry
            self._map[k] = (name, call)

    def OnDeleteDecorator(self, event):
        """Handles the removal of a decorator"""
        # TODO: Implement OnDeleteDecorator
        n = self.m_listCtrl6.GetFirstSelected()
        if n == wx.NOT_FOUND:
            return
        # get key
        k = self.m_listCtrl6.GetItemData(n)
        # simply remove element and index
        self.m_listCtrl6.DeleteItem(n)
        del self._map[k]
        self._count = self._count - 1

    def OnCancel(self, event):
        """Cancels the dialog"""
        self.EndModal(wx.ID_CANCEL)

    def OnOK(self, event):
        """Validates and accepts the dialog"""
        if self.Validate():
            self.EndModal(wx.ID_OK)

    def get_kwargs(self):
        """Create the new decorators"""
        #remove previous decorators
        olds = self._container(model.py.Decorator)
        for old in olds:
            old.Delete()
        #create news
        kwargs = {'parent': self._container}
        for k in self._map:
            v = self._map[k]
            kwargs['name'] = v[0]
            kwargs['call'] = v[1]
            model.py.Decorator(**kwargs)
        return None


