"""Subclass of ContextItems, which is generated by wxFormBuilder."""

import copy
import wx
import wxx

from activity.models.ui import ui as ui
import model.decorator
import app.resources as rc


# Implementing ContextItems
class ContextItems(ui.ContextItems):
    """
    Dialog for editing context definitions. Context elements have two functions.

        - May act as macros controlled by the 'enabled' checkbox:

            We can control the inclusion of the definition inserted in the definition box.

        - May act as macro context labeling:

            We can prefix and sufix both the element declaration and the element definition
            with the code inserted in the corresponding boxes.

    These functionalities can be conbined by defining macros used on the context labeling.
    """
    @wxx.SetInfo(__doc__)
    def __init__(self, parent, project):
        """Initialize dialog"""
        super(ContextItems, self).__init__(parent)
        if not hasattr(project, '_contexts'):
            project._contexts = []
        self._contexts = copy.deepcopy(project._contexts)
        count = 0
        for item in self._contexts:
            self.m_listBox1.Insert(item._name, count, item)
        self._selected = None
        self._selectedIndex = None
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(rc.GetBitmap("context"))
        self.SetIcon(icon)


    def OnSelectItem(self, event):
        """Handles context item selection"""
        obj = self.m_listBox1.GetClientData(event.GetSelection())
        self._selectedIndex = event.GetSelection()
        self._selected = obj
        # replace al info in the editors
        self.m_textCtrl40.SetValue(obj.name)
        self.m_checkBox64.SetValue(obj._enable)
        self.m_richText15.SetValue(obj._define)
        self.m_richText11.SetValue(obj._prefix_declaration)
        self.m_richText13.SetValue(obj._sufix_declaration)
        self.m_richText12.SetValue(obj._prefix_implementation)
        self.m_richText14.SetValue(obj._sufix_implementation)
        self.m_richText1.SetValue(obj.note)
        self.m_button31.Enable(True)

    def OnChangeName(self, event):
        """Handle change context name event"""
        txt = self.m_textCtrl40.GetValue()
        if self._selected is not None:
            self._selected._name = txt
        if self._selectedIndex is not None:
            self.m_listBox1.SetString(self._selectedIndex, txt)
        event.Skip()

    def OnEnabledChanged(self, event):
        """Handle on enable change"""
        if self._selected is not None:
            self._selected._enable = self.m_checkBox64.GetValue()
        event.Skip()

    def OnChangeDefinition(self, event):
        """Handle change context name event"""
        txt = self.m_richText15.GetValue()
        if self._selected is not None:
            self._selected._define = txt
        event.Skip()

    def OnChangeDeclarationPrefix(self, event):
        """Handle change context declaration prefix event"""
        txt = self.m_richText11.GetValue()
        if self._selected is not None:
            self._selected._prefix_declaration = txt
        event.Skip()

    def OnChangeDeclarationSufix(self, event):
        """Handle change context declaration sufix event"""
        txt = self.m_richText13.GetValue()
        if self._selected is not None:
            self._selected._sufix_declaration = txt
        event.Skip()

    def OnChangeImplementationPrefix(self, event):
        """Handle change context implementation prefix event"""
        txt = self.m_richText12.GetValue()
        if self._selected is not None:
            self._selected._prefix_implementation = txt
        event.Skip()

    def OnChangeImplementationSufix(self, event):
        """Handle change context implementation sufix event"""
        txt = self.m_richText14.GetValue()
        if self._selected is not None:
            self._selected._sufix_implementation = txt
        event.Skip()

    def OnChangeNote(self, event):
        """Handle change context name event"""
        txt = self.m_richText1.GetValue()
        if self._selected is not None:
            self._selected.note = txt
        event.Skip()

    def OnAddNewContext(self, event):
        """Handle add new context button event"""
        count = self.m_listBox1.GetCount()
        name = self.m_textCtrl40.GetValue()
        if self._selected is not None or len(name) == 0:
            name = 'new context'
            self._selected = None
            self._selectedIndex = None
            self.m_textCtrl40.SetValue(name)
            self.m_checkBox64.SetValue(True)
            self.m_richText11.SetValue('')
            self.m_richText12.SetValue('')
            self.m_richText13.SetValue('')
            self.m_richText14.SetValue('')
            self.m_richText15.SetValue('')
            self.m_richText1.SetValue('')
        item = model.decorator.ContextItem(
            name=name,
            define=self.m_richText15.GetValue(),
            enable=self.m_checkBox64.GetValue(),
            prefix_declaration=self.m_richText11.GetValue(),
            sufix_declaration=self.m_richText13.GetValue(),
            prefix_implementation=self.m_richText12.GetValue(),
            sufix_implementation=self.m_richText14.GetValue(),
            note=self.m_richText1.GetValue()
            )
        self._contexts.append(item)
        self.m_listBox1.Insert(item._name, count, item)
        self._selected = item
        self._selectedIndex = count
        self.m_listBox1.Select(self._selectedIndex)
        self.m_button31.Enable(False)

    def OnRemoveContext(self, event):
        """Handle remove context"""
        self._contexts.remove(self._selected)
        self.m_listBox1.Delete(self._selectedIndex)
        self._selected = None
        self._selectedIndex = None
        self.m_textCtrl40.SetValue('')
        self.m_checkBox64.SetValue(True)
        self.m_richText11.SetValue('')
        self.m_richText12.SetValue('')
        self.m_richText13.SetValue('')
        self.m_richText14.SetValue('')
        self.m_richText15.SetValue('')
        self.m_richText1.SetValue('')
        self.m_button31.Enable(False)

    def Validate(self):
        """Checks validation"""
        return True

    # Handlers for ContextItems events.
    def OnOk(self, event):
        """Implements Ok"""
        if self.Validate():
            self.EndModal(wx.ID_OK)

    def CopyAttributes(self, project):
        """Transfer attributes to project"""
        project._contexts = self._contexts

