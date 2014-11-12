#        todo:
#         gff4file: lazy read, immediate write
# DONE     first lazy read - without writeback, will just be a read while saving
#           use id() to identify objects? probably not
#           can only replace strings in data when reference count is one
#           prevent overwriting... Structure(LazyStructure())? ... but substructures may not be...
#          last manual commit
#         search by indices: 0 : $12341 *
# DONE    search in a delayedworker?
# DENY    better method of selecting root to search from
#         search definitions before data - limit search to lists and structures that can produce a result
#         copy from search results
#          cut?
# DONE    matrix edit
# DONE    list edit: insert, remove, swap, move
#          move to top, move to bottom?
# DONE     double-click on item selects item in tree
# DONE    reference edit: clear, new
# DONE     new button shown if nullable, that nulls it
# DONE    generic list/ref edit
# DONE     new edit screen that shows the options for adding
# DENY    shelf copy paste
# DONE     intead, normal copy paste
# DONE     and, possibly a new listctrl that you can paste into and cut/copy out of... that might actually be an actual shelf.
# DENY      and maybe give it an edit control as well?
#            or give it access to the existing edit control
# DONE     warn the user that some items weren't pasted
#           turn off warning in settings
# DONE     possibly coerce all values going into a list before adding, and throwing an error if any of them fail, instead of just adding the ok items.
#          copy/paste from list edit control
# DONE     delete command in addition to cut
#          insert command (create)
#         other integer views (hex, oct, bin)
# DONE    need to pass types and allowing null to editors, and editors need to pass back value of correct type
# DONE     save/reset issue with integers and their bounds
# DONE     and of course null references being uneditable
# DONE    make struct and list subclasses from header... how to make them lazy, though? multiple inheritance/mixin?
# DONE     want to replace StructureDef and ListDef with classes... and maybe eliminate ReferenceDef and replace with something in the Structure/List
# DONE    other binary options... view as image? definitely save to file...
#         make refreshes apply to all views of a tree instead of just the one acted upon
#         flush the clipboard?
# DONE    ask to convert gff 4.1 to 4.0
# DONE    basic display of gff 3.2
#         more descriptive error messages when failing to open files
#         Tool ideas:
# DONE        Add column names to GDA files - gda column database, on add to known, trigger delete from unknown, and unknown with a check for not in known
#             Add strings from talktables to TlkStrings

import wx, wx.gizmos, sys, re, gff4
from wx.lib.wordwrap import wordwrap
from wx.lib.mixins.treemixin import VirtualTree
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.intctrl import IntCtrl
from wx.lib.dialogs import ScrolledMessageDialog
from time import sleep
import wx.lib.delayedresult as delayedresult
#import wx.py.shell as pyshell
from gff4 import *
from gff4.lazy import LazyGFF4
from gff4.datoolset_fields import *
from gff4.editorutils import *
from gff4.editpanels import EditPanel
from gff4.editsearch import SearchPanel
from erf import ERF1File, ERF2File, ERF3File
from numbers import Real, Integral
from base64 import encodestring, decodestring
from string import ascii_letters, digits
from functools import partial
from itertools import count as icount
from operator import itemgetter, attrgetter
from traceback import print_exc, format_exc
from os.path import splitext, basename, dirname
from gff32 import read_gff as read_gff32
from gff32.types import Structure as GFF32Structure
from gff32.viewer import GFFTree as GFF32Tree
from ioutils import copyio
import zlib
import fnvdb
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class DummyModel(object):
    def GetItem(self, indices):
        return None, None, None, None
    def GetChildrenCount(self, indices):
        return 0

class GFFModel(object):
    def __init__(self, header, data):
        self.header = header
        self.data = data

    def GetItem(self, indices):
        if not len(indices):
            return None, self.header, None, 1
        container = None
        field = None
        data = self.data
        count = len(data)
        for index in indices[1:]:
            container = data
            if isinstance(data, Structure):
                field = data.getfieldbyindex(index)
                data = data[field.label]
            elif isinstance(data, List):
                field = None
                data = data[index]
            else:
                raise ValueError
            
            if isinstance(data, (Structure, List)):
                count = len(data)
            else:
                count = 0
        
        return container, field, data, count

    def GetText(self, indices, column):
        container, field, data, count = self.GetItem(indices)
        if column == 0:
            if field:
                return str(field.label)
            elif indices:
                return str(indices[-1])
            else:
                return ''
        elif column == 1:
            if len(indices) == 1:
                return ' '.join(('GFF ', self.header.version, self.header.file_type, self.header.file_version, self.header.platform))
            if field:
                name = get_field_name(field.label)
                if isinstance(name, basestring):
                    return name
                else:
                    return ''
            else:
                return ''
        elif column == 2:
            def typedesc(cls, indirect):
                if cls is None:
                    if not indirect: raise ValueError
                    return '*'
                elif issubclass(cls, List):
                    if indirect: raise ValueError
                    return '['+typedesc(cls.elem_type, cls.indirect)+']'
                elif issubclass(cls, Structure):
                    return '*'+cls.fourcc if indirect else cls.fourcc
                elif issubclass(cls, Binary):
                    return '[UINT8]'
                else:
                    return '*'+cls.name if indirect else cls.name
            if field is not None:
                if data is not None:
                    return typedesc(type(data), field.indirect)
                else:
                    return typedesc(field.type, field.indirect)
            elif data is not None:
                if container is not None:
                    if container.elem_type is not None:
                        return typedesc(container.elem_type, container.indirect)
                    else:
                        return typedesc(type(data), container.indirect)
                elif len(indices) == 1:
                    return typedesc(type(data), False)
                else:
                    return typedesc(type(data), True)
            else:
                return '?'
        elif column == 3:
            return value_preview(data)
        return '%s:%s'%(indices, column)
    
    def GetChildrenCount(self, indices):
        return self.GetItem(indices)[3]

class GFFTree(VirtualTree, wx.gizmos.TreeListCtrl, ):# ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        super(GFFTree, self).__init__(*args, **kwargs)
        self._model = None
        #ListCtrlAutoWidthMixin.__init__(self)
        self.AddColumn('Index', 120)
        self.AddColumn('Label', 200)
        self.AddColumn('Type', 90)
        self.AddColumn('Value', 400)
    
    def getmodel(self):
        return self._model
    
    def setmodel(self, model):
        self._model = model
        self.RefreshItems()
    
    model = property(getmodel, setmodel)
    
    def OnGetItemText(self, index, column=0):
        return self._model.GetText(index, column)
        
    def OnGetChildrenCount(self, index):
        return self._model.GetChildrenCount(index)
    
    def GetIndicesOfItem(self, item):
        indices = ()
        while item != self.GetRootItem():
            pitem = self.GetItemParent(item)
            citem, what = self.GetFirstChild(pitem)
            i = 0
            while citem != item:
                i += 1
                citem = self.GetNextSibling(citem)
            indices = (i,) + indices
            item = pitem
        return indices
    
    def RefreshItemAncestors(self, item, itemIndex=None):
        if not itemIndex:
            itemIndex = self.GetItemByIndex(item)
        while itemIndex:
            self.RefreshItem(itemIndex)
            itemIndex = itemIndex[:-1]
    
    def SelectItemByIndices(self, indices):
        item = self.GetRootItem()
        while indices:
            self.Expand(item)
            child = self.GetFirstChild(item)[0]
            for n in xrange(indices[0]):
                child = self.GetNextSibling(child)
            indices = indices[1:]
            item = child
        self.ScrollTo(item)
        self.SelectItem(item)
        self.SetFocus()

class GFF4Editor(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(GFF4Editor, self).__init__(*args, **kwargs)
        
        self.types = map(itemgetter(1), sorted(TYPES_BY_ID.items()))
        
        self.control = GFFTree(self, style=wx.TR_ROW_LINES|wx.TR_NO_LINES|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HAS_BUTTONS|wx.TR_SINGLE) # 
        self.editor = EditPanel(self)
        self.editor.lst_panel.types = self.types
        self.editor.lst_panel.tree = self.control
        self.editor.ref_panel.types = self.types
        self.search = SearchPanel(self)
        self.search.tree = self.control
        self.shelf = ShelfPanel(self)
        
        self.treemenu = wx.Menu()
        finditem = self.treemenu.Append(wx.ID_FIND, "Search &Branch\tCTRL+F", "When searching use only this branch of the tree.")
        refreshitem = self.treemenu.Append(wx.ID_REFRESH, "&Refresh\tF5", "Refresh tree")
        copyitem = self.treemenu.Append(wx.ID_COPY, "&Copy\tCTRL+C")
        cutitem = self.treemenu.Append(wx.ID_CUT, "&Cut\tCTRL+X")
        pasteitem = self.treemenu.Append(wx.ID_PASTE, "&Paste\tCTRL+V")
        deleteitem = self.treemenu.Append(wx.ID_DELETE, "&Delete\tDelete")
        
        self.SetAcceleratorTable(wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('F'), wx.ID_FIND),
            (wx.ACCEL_NORMAL, wx.WXK_F5, wx.ID_REFRESH)
        ]))
        self.control.SetAcceleratorTable(wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('C'), wx.ID_COPY),
            (wx.ACCEL_CTRL, ord('X'), wx.ID_CUT),
            (wx.ACCEL_CTRL, ord('V'), wx.ID_PASTE),
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, wx.ID_DELETE)
        ]))
        
        sizer = wx.GridBagSizer(5, 5)
        sizer.AddGrowableCol(0, 2)
        sizer.AddGrowableCol(1, 1)
        sizer.AddGrowableCol(2, 1)
        sizer.AddGrowableRow(0, 3)
        sizer.AddGrowableRow(1, 1)
        
        sizer.Add(self.control, pos=(0,0), span=(1,2), flag=wx.EXPAND)
        
        bsizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Edit"), wx.VERTICAL)
        bsizer.Add(self.editor, 1, flag=wx.EXPAND)
        sizer.Add(bsizer, pos=(1,0), flag=wx.EXPAND)
        
        bsizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Shelf"), wx.VERTICAL)
        bsizer.Add(self.shelf, 1, flag=wx.EXPAND)
        sizer.Add(bsizer, pos=(1,1), span=(1, 2), flag=wx.EXPAND)
        
        sizer.Add(self.search, pos=(0,2), flag=wx.EXPAND)
        
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged, self.control)
        #self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeItemActivated, self.control)
        #self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnTreeItemMenu, self.control)
        self.control.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnTreeRightUp)
        self.Bind(wx.EVT_MENU, self.OnTreeItemFind, finditem)
        self.Bind(wx.EVT_MENU, self.OnTreeRefresh, refreshitem)
        self.Bind(wx.EVT_MENU, self.OnCopy, copyitem)
        self.Bind(wx.EVT_MENU, self.OnCut, cutitem)
        self.Bind(wx.EVT_MENU, self.OnPaste, pasteitem)
        self.Bind(wx.EVT_MENU, self.OnDelete, deleteitem)
    
    @property
    def model(self):
        return self.control.model
    
    @model.setter
    def model(self, model):
        if model is not None:
            self.types[:] = map(itemgetter(1), sorted(TYPES_BY_ID.items()))
            self.control.model = model
            for struct in sorted(model.header.structs, key=attrgetter('fourcc')):
                self.types.append(struct)
        else:
            model = DummyModel()
        self.search.Clear()
        self.control.Unselect()
        self.editor.Clear()
    
    def SetFocus(self):
        self.control.SetFocus()

    def OnSelectionChanged(self, evt):
        if len(self.control.Selections) != 1:
            self.editor.Clear()
            return
        self.selected_item = evt.GetItem()
        indices = self.control.GetIndicesOfItem(self.selected_item)
        container, field, data, count = self.control.model.GetItem(indices)
        def callback(key, kind, indirect, new_value=None, create_new=False):
            if create_new:
                rawkind = kind if new_value is None else new_value
                if rawkind is not None:
                    new_value = coercevalue(None, rawkind)
            if not issubclass(kind, List) or isinstance(new_value, str):
                container[key] = new_value
            item = self.control.GetItemByIndex(indices)
            self.control.RefreshItemRecursively(item, indices)
            self.control.RefreshItemAncestors(item, indices)
            if create_new or new_value is None and indirect and kind is None:
                self.control.Unselect()
                self.control.SelectItem(item)
                return None, None, False
            return container[key], kind, indirect
        if field and not isinstance(field, Header):
            self.editor.Edit(data, field.type, field.indirect,
                partial(callback, field.label, field.type, field.indirect))
        elif container:
            self.editor.Edit(data, container.elem_type, container.indirect,
                partial(callback, indices[-1], container.elem_type, container.indirect))
        else:
            self.editor.Edit(data, None, False, None)
    
    #def OnTreeItemMenu(self, evt):
    #    print evt
    #    self.context_item = evt.GetItem()
    #    self.PopupMenu(self.treemenu, evt.GetPosition())
    
    def OnTreeRightUp(self, evt):
        #from operator import sub, add
        pt = evt.GetPosition()
        self.context_item = self.control.HitTest(pt)[0]
        #pt = tuple(map(add, map(sub, self.control.GetScreenPosition(), self.GetScreenPosition()), pt))
        if self.context_item:
            self.control.SelectItem(self.context_item)
            self.PopupMenu(self.treemenu, pt)
    
    def OnTreeItemFind(self, evt):
        item = self.selected_item
        #item = self.control.GetSele
        if item:
            indices = self.control.GetIndicesOfItem(item)
            container, field, data, count = self.control.model.GetItem(indices)
            self.search.SearchFrom(data, indices)
    
    def OnTreeItemActivated(self, evt):
        indices = self.control.GetIndicesOfItem(evt.GetItem())
        container, field, data, count = self.control.model.GetItem(indices)
        self.search.SearchFrom(data, indices)
    
    def OnTreeRefresh(self, evt):
        self.control.RefreshItems()
    
    def OnCopy(self, event):
        item = self.selected_item
        if not item:
            return
        indices = self.control.GetIndicesOfItem(item)
        container, field, data, count = self.control.model.GetItem(indices)
        
        wrapper = StructCopy()
        if isinstance(data, List):
            if not len(data):
                return
            wrapper[0].extend(data)
        elif isinstance(data, Binary):
            wrapper[0].append(StructData({0: data}))
        else:
            if data is None:
                return
            wrapper[0].append(data)
        
        clipdata = GFFDataObject()
        clipdata.Struct = wrapper
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(clipdata)
        wx.TheClipboard.Close()
    
    def OnCut(self, event):
        selected_item = self.selected_item
        if not selected_item:
            return
        ctrl = self.control
        indices = ctrl.GetIndicesOfItem(selected_item)
        container, field, data, count = ctrl.model.GetItem(indices)
        
        wrapper = StructCopy()
        if isinstance(data, List):
            if not len(data):
                return
            wrapper[0].extend(data)
        elif isinstance(container, List) or field.indirect:
            if data is None:
                return
            wrapper[0].append(data)
        elif isinstance(data, Binary):
            wrapper[0].append(StructData({0: data}))
        else:
            return
            
        clipdata = GFFDataObject()
        clipdata.Struct = wrapper
        clipdata.GetDataHere()
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(clipdata)
        wx.TheClipboard.Close()
        
        if isinstance(data, List):
            del data[:]
            ctrl.RefreshItemRecursively(selected_item, indices)
            #ctrl.RefreshItemAncestors(selected_item, indices)
        elif isinstance(container, List):
            del container[indices[-1]]
            ctrl.RefreshItemRecursively(ctrl.GetItemParent(selected_item), indices[:-1])
            #ctrl.RefreshItem(indices[:-1])
            #ctrl.RefreshChildrenRecursively(ctrl.GetItemByIndex(indices[:-1]), indices[:-1])
        elif isinstance(data, Binary):
            container[container.getfieldbyindex(indices[-1]).label] = Binary()
            ctrl.RefreshItemRecursively(selected_item, indices)
        else:
            container[container.getfieldbyindex(indices[-1]).label] = None
            ctrl.RefreshItemRecursively(selected_item, indices)
            #ctrl.RefreshItemAncestors(selected_item, indices)
        ctrl.Unselect()
        ctrl.SelectItem(selected_item)
    
    def OnPaste(self, event):
        selected_item = self.selected_item
        if not selected_item:
            return
        ctrl = self.control
        
        clipdata = GFFDataObject()
        wx.TheClipboard.Open()
        if not wx.TheClipboard.GetData(clipdata):
            return
        wx.TheClipboard.Close()
        items = clipdata.Struct[0]
        if not len(items):
            return
        
        indices = ctrl.GetIndicesOfItem(selected_item)
        container, field, data, count = ctrl.model.GetItem(indices)
        ignore_errors = False
        had_error = False
        success_count = 0
        
        if isinstance(data, List) and not (data.elem_type == UINT8 and not data.indirect and isinstance(items[0], Structure) and items[0].fourcc == 'Data' and 0 in items[0]):
            coerced = []
            for item in items:
                try:
                    coerced.append(coercevalue(item, data.elem_type, data.indirect, True))
                except (ValueError, TypeError, KeyError), e:
                    had_error = True
                    if not ignore_errors:
                        with wx.MessageDialog(self, "%r\nError coercing item, paste items that are coercable?"%e, "Coercion Error", wx.YES_NO|wx.ICON_QUESTION) as dlg:
                            if dlg.ShowModal() == wx.ID_YES:
                                ignore_errors = True
                            else:
                                return
            data.extend(coerced)
            success_count = len(coerced)
            ctrl.RefreshItemRecursively(selected_item, indices)
            #ctrl.RefreshItemAncestors(selected_item, indices)
        elif isinstance(container, List):
            coerced = []
            for item in items:
                try:
                    coerced.append(coercevalue(item, container.elem_type, container.indirect, True))
                except (ValueError, TypeError, KeyError), e:
                    had_error = True
                    if not ignore_errors:
                        with wx.MessageDialog(self, "%r\nError coercing item, paste items that are coercable?"%e, "Coercion Error", wx.YES_NO|wx.ICON_QUESTION) as dlg:
                            if dlg.ShowModal() == wx.ID_YES:
                                ignore_errors = True
                            else:
                                return
            container[indices[-1]:indices[-1]] = coerced
            success_count = len(coerced)
            ctrl.RefreshItemRecursively(ctrl.GetItemParent(selected_item), indices[:-1])
            #ctrl.RefreshItem(indices[:-1])
            #ctrl.RefreshChildrenRecursively(ctrl.GetItemByIndex(indices[:-1]), indices[:-1])
        elif isinstance(container, Structure):
            if len(items) > 1:
                with wx.MessageDialog(self, "There is more than one item on the clipboard, paste the first item or cancel?", "Overflow Error", wx.OK|wx.CANCEL|wx.ICON_QUESTION) as dlg:
                    if dlg.ShowModal() != wx.ID_OK:
                        return
            try:
                # strict structure coercion here as well?
                if isinstance(items[0], Structure) and items[0].fourcc == 'Data' and 0 in items[0]:
                    container[container.getfieldbyindex(indices[-1]).label] = items[0][0]
                else:
                    container[container.getfieldbyindex(indices[-1]).label] = items[0]
                ctrl.RefreshItemRecursively(selected_item, indices)
                #ctrl.RefreshItemAncestors(selected_item, indices)
            except (ValueError, TypeError), e:
                with wx.MessageDialog(self, "Paste cancelled.", "Coercion Error", wx.OK|wx.ICON_ERROR) as dlg:
                    return
        ctrl.Unselect()
        ctrl.SelectItem(selected_item)
        
        if had_error:
            with wx.MessageDialog(self, "%d items pasted."%success_count, "Results", wx.OK|wx.ICON_INFORMATION) as dlg:
                dlg.ShowModal()
    
    def OnDelete(self, event):
        selected_item = self.selected_item
        if not selected_item:
            return
        ctrl = self.control
        indices = ctrl.GetIndicesOfItem(selected_item)
        container, field, data, count = ctrl.model.GetItem(indices)
        
        if isinstance(data, List):
            if not len(data):
                return
            del data[:]
            ctrl.RefreshItemRecursively(selected_item, indices)
        elif isinstance(container, List):
            if data is None:
                return
            del container[indices[-1]]
            ctrl.RefreshItemRecursively(ctrl.GetItemParent(selected_item), indices[:-1])
        elif field.indirect:
            if data is None:
                return
            container[container.getfieldbyindex(indices[-1]).label] = None
            ctrl.RefreshItemRecursively(selected_item, indices)
        elif isinstance(data, Binary):
            container[container.getfieldbyindex(indices[-1]).label] = Binary()
            ctrl.RefreshItemRecursively(selected_item, indices)
        else:
            return
        ctrl.Unselect()
        ctrl.SelectItem(selected_item)
    

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)
        self.CreateStatusBar()
        
        filemenu = wx.Menu()
        newwinditem = filemenu.Append(wx.ID_ANY, "New &Window\tALT+N","Open a new editor window")
        newviewitem = filemenu.Append(wx.ID_ANY, "New &View\tALT+V","Open a new editor window with the same file")
        openitem = filemenu.Append(wx.ID_OPEN, "&Open\tCTRL+O","Open a GFF File")
        self.saveasitem = saveasitem = filemenu.Append(wx.ID_SAVE, "Save &As\tCTRL+ALT+S","Save a GFF File")
        filemenu.AppendSeparator()
        exportitem = filemenu.Append(wx.ID_ANY, "&Export\tCTRL+E","Export a resource from an ERF")
        exportallitem = filemenu.Append(wx.ID_ANY, "&Export All","Export all resources from an ERF")
        filemenu.AppendSeparator()
        closeitem = filemenu.Append(wx.ID_ANY,"&Close\tCTRL+W","Close the window")
        exititem = filemenu.Append(wx.ID_EXIT,"E&xit\tCTRL+Q","Terminate the program")
        
        self.Bind(wx.EVT_MENU, self.OnNewWindow, newwinditem)
        self.Bind(wx.EVT_MENU, self.OnNewView, newviewitem)
        self.Bind(wx.EVT_MENU, self.OnOpen, openitem)
        self.Bind(wx.EVT_MENU, self.OnExport, exportitem)
        self.Bind(wx.EVT_MENU, self.OnExportAll, exportallitem)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, saveasitem)
        self.Bind(wx.EVT_MENU, self.OnClose, closeitem)
        self.Bind(wx.EVT_MENU, self.OnExit, exititem)
        
        self.settingsmenu = settingsmenu = wx.Menu()
        self.set_lazyload = settingsmenu.AppendCheckItem(wx.ID_ANY, "&Lazy Open","Read the entire file, but only parse on demand.")
        self.set_saveview = settingsmenu.AppendCheckItem(wx.ID_ANY, "&Fast Save", "Only save changed values, don't rebuild entire file.")
        self.set_savesettings = settingsmenu.AppendCheckItem(wx.ID_ANY, "Save Settings On &Exit")
        
        def store_setting(section, option, callable, event): self.config.set(section, option, str(callable()))
        def store_editor(option, callable): return partial(store_setting, 'Editor', option, callable)
        self.Bind(wx.EVT_MENU, store_editor('LazyLoad', self.set_lazyload.IsChecked), self.set_lazyload)
        self.Bind(wx.EVT_MENU, store_editor('ImmediateSave', self.set_saveview.IsChecked), self.set_saveview)
        self.Bind(wx.EVT_MENU, store_editor('SaveSettingsOnExit', self.set_savesettings.IsChecked), self.set_savesettings)
        
        settingsmenu.AppendSeparator()
        
        import_strings = settingsmenu.Append(wx.ID_ANY, "Import strings", "Load strings from text files so that they're recognized in related files (GDA, ERF)")
        export_strings = settingsmenu.Append(wx.ID_ANY, "Export strings", "Save known strings related to certain types of files to a text file")
        self.Bind(wx.EVT_MENU, self.OnImportStrings, import_strings)
        self.Bind(wx.EVT_MENU, self.OnExportStrings, export_strings)
        
        self.edit_passwords = settingsmenu.Append(wx.ID_ANY, "Edit ERF Passwords", "Open a dialog to edit ERF passwords")
        self.Bind(wx.EVT_MENU, self.OnEditPasswords, self.edit_passwords)
        
        savesetting = settingsmenu.Append(wx.ID_ANY, "&Save Settings", "Immediately save current settings")
        self.Bind(wx.EVT_MENU, self.SaveSettings, savesetting)
        
        toolmenu = wx.Menu()
#        pyshellitem = toolmenu.Append(wx.ID_ANY, "Scripting &Console","Open an interactive Python interpreter.")
        execitem = toolmenu.Append(wx.ID_ANY, "Run &Script","Run a Python script. WARNING: Be careful! Also, editor.exe does not have access to the full Python library")
        tlkdowngrade = toolmenu.Append(wx.ID_ANY, "TLK V0.5 -> V0.2 Downgrader","Downgrade the open TLK V0.5 to an uncompressed TLK V0.2")
        gdacolnames = toolmenu.Append(wx.ID_ANY, "GDA Column Namer","Add column names to the open GDA file")
        plotmenu = wx.Menu()
        toolmenu.AppendSubMenu(plotmenu, 'Plot GUIDs')
        plot2resrefs = plotmenu.Append(wx.ID_ANY, 'Plot GUIDs to Resrefs')
        plot2guids = plotmenu.Append(wx.ID_ANY, 'Plot Resrefs to GUIDs')
#        self.Bind(wx.EVT_MENU, self.OnRunConsole, pyshellitem)
        self.Bind(wx.EVT_MENU, self.OnRunScript, execitem)
        self.Bind(wx.EVT_MENU, self.OnTlkDowngrade, tlkdowngrade)
        self.Bind(wx.EVT_MENU, self.OnGDAColnames, gdacolnames)
        self.Bind(wx.EVT_MENU, self.OnPlotToResrefs, plot2resrefs)
        self.Bind(wx.EVT_MENU, self.OnPlotToGUIDs, plot2guids)
        
        helpmenu = wx.Menu()
        aboutitem = helpmenu.Append(wx.ID_ABOUT, "&About","Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutitem)

        menubar = wx.MenuBar()
        menubar.Append(filemenu,"&File")
        menubar.Append(self.settingsmenu,"&Settings")
        self.Bind(wx.EVT_MENU_OPEN, self.RefreshSettings, menubar)
        menubar.Append(toolmenu,"&Tools")
        menubar.Append(helpmenu,"&Help")
        self.SetMenuBar(menubar)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.gff4control = GFF4Editor(self)
        self.sizer.Add(self.gff4control, 1, wx.EXPAND)
        
        self.gff32control = GFF32Tree(self, style=wx.TR_HAS_BUTTONS|wx.TR_SINGLE|wx.TR_EDIT_LABELS|wx.TR_NO_LINES|wx.TR_ROW_LINES|wx.TR_FULL_ROW_HIGHLIGHT)
        # 
        self.sizer.Add(self.gff32control, 1, wx.EXPAND)
        self.gff32control.Hide()
        
        self.Sizer = self.sizer
        
        self.dirname = ''
        self.filename = ''
        self.resname = ''
        self.export_dirname = ''
        self.open_filedialog = None
        self.export_filedialog = None
        self.export_dirdialog = None
        self.import_filedialog = None
        self.fileprogress = None
        self.filetimer = None
        
        self.DropTarget = GFFDrop(self)
    
    @property
    def model(self):
        if self.gff32control.IsShown():
            return self.gff32control.model
        elif self.gff4control.IsShown():
            return self.gff4control.model
    
    @model.setter
    def model(self, model):
        if model is None:
            self.SetStatusText('')
            self.gff32control.model = None
            self.gff4control.model = None
            self.saveasitem.Enable(False)
        elif isinstance(model, GFF32Structure):
            self.SetStatusText('Loaded '+self.resname)
            self.gff32control.model = model
            self.gff4control.model = None
            self.gff4control.Hide()
            self.gff32control.Show()
            self.Layout()
            self.gff32control.SetFocus()
            self.saveasitem.Enable(False)
        else:
            self.SetStatusText('Loaded '+self.resname)
            self.gff32control.model = None
            self.gff4control.model = model
            self.gff32control.Hide()
            self.gff4control.Show()
            self.Layout()
            self.gff4control.SetFocus()
            self.saveasitem.Enable(True)
    
    @property
    def passwords(self):
        for s in self.config.get('Editor', 'ErfPasswords').split(', '):
            yield s
    
    def OnEditPasswords(self, event):
        with PasswordListEditor(self, title='Edit ERF Passwords', size=(250,400)) as dlg:
            dlg.SetStrings(self.passwords)
            dlg.ShowModal()
            if dlg.IsChanged():
                self.config.set('Editor', 'ErfPasswords', ', '.join(dlg.GetStrings()))
    
    def OnNewWindow(self, evt):
        newframe = MyFrame(None, title='GFF V4.0 Editor', size=(1000,700))
        newframe.app = self.app
        newframe.config = self.config
        newframe.config_file = self.config_file
        newframe.Show()
    
    def OnNewView(self, evt):
        newframe = MyFrame(None, title='GFF V4.0 Editor', size=(1000,700))
        newframe.app = self.app
        newframe.config = self.config
        newframe.config_file = self.config_file
        newframe.Show()
        newframe.model = self.model
    
    def OnOpenDone(self, model):
        self.model = model
    
    def OnSaveDone(self, result):
        self.CloseFileOpDialog()
        result.get()
    
    def ShowFileOpDialog(self, title, message):
        self.CloseFileOpDialog()
        self.fileprogress = wx.ProgressDialog(title, message, parent=self, style=wx.PD_ELAPSED_TIME|wx.PD_SMOOTH)
        self.filetimer = wx.Timer(self)
        self.filetimer.Start(500)
        self.Bind(wx.EVT_TIMER, self.OnFileOpTimer)
    
    def OnFileOpTimer(self, event):
        prog = self.fileprogress
        if prog is not None:
            prog.Pulse()
            prog.Refresh()

    def CloseFileOpDialog(self):
        if self.filetimer is not None:
            self.filetimer.Stop()
            self.fileprogress.Destroy()
            self.filetimer = None
            self.fileprogress = None
    
    def GetOpenFileDialog(self):
        dlg = self.open_filedialog
        if dlg is None:
            # regenerate wildcards each time, using the extension of the original file... so .csv and .yaml are automatically appended
            self.open_filedialog = dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename, "All files(*.*)|*.*|Comma-seperated values (.csv)|*.csv", wx.OPEN|wx.FD_FILE_MUST_EXIST)
        return dlg
    
    def OnOpen(self, event):
        dlg = self.GetOpenFileDialog()
        if dlg.ShowModal() == wx.ID_OK:
            self.OpenFile(dlg.Path)
    
    def OpenFile(self, filepath):
        if os.path.splitext(filepath)[1].lower() == '.csv':
            from gff4.g2da import csv2gda
            try:
                self.OnOpenDone(GFFModel(*csv2gda(filepath)))
            except:
                with wx.MessageDialog(self, format_exc(1), "Import Failed", wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
            return
        
        view = self.config.getboolean('Editor', 'ImmediateSave')
        lazy = self.config.getboolean('Editor', 'LazyLoad')
        
        self.filename = basename(filepath)
        self.dirname = dirname(filepath)
        self.model = None
        
        with open(filepath, 'rb') as f:
            sample = f.read(16)
        
        erf = None
        try:
            if ERF1File.checksample(sample):
                erf = ERF1File(filepath)
            elif ERF2File.checksample(sample):
                erf = ERF2File(filepath, self.passwords)
            elif ERF3File.checksample(sample):
                erf = ERF3File(filepath, self.passwords)
        except:
            print_exc()
            with wx.MessageDialog(self, "Not a supported file", "Parse Failure", wx.OK|wx.ICON_ERROR) as dlg:
                dlg.ShowModal()
            self.OnOpenDone(None)
            return
        
        def open_done(result):
            self.CloseFileOpDialog()
            try:
                data, header = result.get()
            except:
                #print_exc()
                self.OnOpenDone(None)
                with wx.MessageDialog(self, "Not a supported file", "Parse Failure", wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
            else:
                if header == 'gff32':
                    self.OnOpenDone(data)
                else:
                    self.OnOpenDone(GFFModel(header, data))
            
        if erf is not None:
            resnames = sorted(erf)
            with wx.SingleChoiceDialog(self, "Choose the resource to open\n%s"%erf.date.isoformat(), "Choose Resource", resnames) as dlg:
                if dlg.ShowModal() != wx.ID_OK:
                    self.OnOpenDone(None)
                    return
                self.resname = resname = resnames[dlg.GetSelection()]
            def open_gff():
                try:
                    f = erf.open(resname)
                    sample = f.read(8)
                    f.seek(0)
                    if sample[4:8] == 'V3.2':
                        buffer = StringIO()
                        copyio(buffer, f)
                        f.close()
                        buffer.seek(0)
                        return read_gff32(buffer), 'gff32'
                    elif sample[0:4] == 'GFF ' and sample[4:8] in ('V4.0', 'V4.1'):
                        try:
                            gff = LazyGFF4(f, preload=not lazy)
                        finally:
                            f.close()
                        return gff.root, gff.header
                    else:
                        raise ValueError, 'not a supported file'
                except:
                    print_exc()
                    raise
        else:
            self.resname = self.filename
            def open_gff():
                try:
                    if sample[4:8] == 'V3.2':
                        buffer = StringIO()
                        with open(filepath, 'rb') as f:
                            copyio(buffer, f)
                        buffer.seek(0)
                        return read_gff32(buffer), 'gff32'
                    elif sample[0:4] == 'GFF ' and sample[4:8] in ('V4.0', 'V4.1'):
                        with open(filepath, 'rb') as f:
                            gff = LazyGFF4(f, preload=not lazy)
                        return gff.root, gff.header
                    else:
                        raise ValueError, 'not a supported file'
                except:
                    print_exc()
                    raise
        
        self.ShowFileOpDialog("Reading GFF File", "Reading GFF File")
        delayedresult.startWorker(open_done, open_gff)
    
    def GetExportFileDialog(self, resname):
        dlg = self.export_filedialog
        if dlg is None:
            self.export_filedialog = dlg = wx.FileDialog(self, "Choose a filename", self.export_dirname or self.dirname, resname, "All files(*.*)|*.*", wx.SAVE|wx.FD_OVERWRITE_PROMPT)
        else:
            dlg.Filename = resname
            dlg.SetDirectory(self.export_dirname)
        return dlg
    
    def OnExport(self, event):
        dlg = self.GetOpenFileDialog()
        if dlg.ShowModal() != wx.ID_OK:
            return

        self.filename = dlg.GetFilename()
        self.dirname = dlg.GetDirectory()
        filepath = dlg.GetPath()
        
        with open(filepath, 'rb') as f:
            sample = f.read(16)
        
        erf = None
        try:
            if ERF1File.checksample(sample):
                erf = ERF1File(filepath)
            elif ERF2File.checksample(sample):
                erf = ERF2File(filepath, self.passwords)
            elif ERF3File.checksample(sample):
                erf = ERF3File(filepath, self.passwords)
            else:
                with wx.MessageDialog(self, "Not a supported file", "Parse Failure", wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
                return
        except:
            print_exc()
            with wx.MessageDialog(self, "Not a supported file", "Parse Failure", wx.OK|wx.ICON_ERROR) as dlg:
                dlg.ShowModal()
            return
            
        resnames = sorted(erf)
        with wx.MultiChoiceDialog(self, "Choose the resource to export\n%s"%erf.date.isoformat(), "Choose Resource", resnames) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            selections = [resnames[i] for i in dlg.GetSelections()]
            if not selections:
                return
        
        if len(selections) > 1:
            dlg = self.GetExportDirDialog()
            if dlg.ShowModal() == wx.ID_OK:
                dest_path = dlg.GetPath()
                self.export_dirname = dest_path
            else:
                return
            
            with wx.MessageDialog(self, "Would you like to overwrite existing files?", "Overwrite Files?", wx.YES_NO|wx.ICON_QUESTION) as dlg:
                rv = dlg.ShowModal()
                if rv not in (wx.ID_YES, wx.ID_NO):
                    return
                overwrite = rv == wx.ID_YES
            
            def export_files():
                try:
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    for resname in selections:
                        out_path = os.path.join(dest_path, resname)
                        out_dir = dirname(resname)
                        if out_dir:
                            out_dir = os.path.join(dest_path, out_dir)
                            if not os.path.exists(out_dir):
                                os.makedirs(out_dir)
                        if overwrite or not os.path.exists(out_path):
                            erf.export(resname, out_path)
                except:
                    print_exc()
                    raise
        
        else:
            resname = selections[0]
            dlg = self.GetExportFileDialog(resname)
            if dlg.ShowModal() == wx.ID_OK:
                dest_path = dlg.GetPath()
                self.export_dirname = dlg.GetDirectory()
            else:
                return
        
            def export_files():
                try:
                    erf.export(resname, dest_path)
                except:
                    print_exc()
                    raise
        
        def export_done(result):
            self.CloseFileOpDialog()
            try:
                result.get()
            except:
                #print_exc()
                with wx.MessageDialog(self, "Export to %s failed"%dest_path, "Export Failure", wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
            else:
                with wx.MessageDialog(self, "Export to %s succeeded"%dest_path, "Export Success", wx.OK|wx.ICON_INFORMATION) as dlg:
                    dlg.ShowModal()
        
        self.ShowFileOpDialog("Exporting File", "Exporting File")
        delayedresult.startWorker(export_done, export_files)
    
    def GetExportDirDialog(self):
        dlg = self.export_dirdialog
        if dlg is None:
            self.export_dirdialog = dlg = wx.DirDialog(self, "Choose a directory", self.export_dirname or self.dirname, wx.SAVE)
        else:
            dlg.SetPath(self.export_dirname)
        return dlg
    
    def OnExportAll(self, event):
        dlg = self.GetOpenFileDialog()
        if dlg.ShowModal() != wx.ID_OK:
            return
        
        self.filename = dlg.GetFilename()
        self.dirname = dlg.GetDirectory()
        filepath = dlg.GetPath()\
        
        with open(filepath, 'rb') as f:
            sample = f.read(16)
        
        erf = None
        try:
            if ERF1File.checksample(sample):
                erf = ERF1File(filepath)
            elif ERF2File.checksample(sample):
                erf = ERF2File(filepath, self.passwords)
            elif ERF3File.checksample(sample):
                erf = ERF3File(filepath, self.passwords)
            else:
                with wx.MessageDialog(self, "Not a supported file", "Parse Failure", wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
                return
        except:
            print_exc()
            with wx.MessageDialog(self, "Not a supported file", "Parse Failure", wx.OK|wx.ICON_ERROR) as dlg:
                dlg.ShowModal()
            return
        
        dlg = self.GetExportDirDialog()
        if dlg.ShowModal() == wx.ID_OK:
            dest_path = dlg.GetPath()
            self.export_dirname = dest_path
        else:
            return
        
        with wx.MessageDialog(self, "Would you like to overwrite existing files?", "Overwrite Files?", wx.YES_NO|wx.ICON_QUESTION) as dlg:
            rv = dlg.ShowModal()
            if rv not in (wx.ID_YES, wx.ID_NO):
                return
            overwrite = rv == wx.ID_YES
        
        def export_done(result):
            self.CloseFileOpDialog()
            try:
                result.get()
            except:
                #print_exc()
                with wx.MessageDialog(self, "Export to %s failed"%dest_path, "Export Failure", wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
            else:
                with wx.MessageDialog(self, "Export to %s succeeded"%dest_path, "Export Success", wx.OK|wx.ICON_INFORMATION) as dlg:
                    dlg.ShowModal()
        
        def export_files():
            try:
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                for resname in erf:
                    out_path = os.path.join(dest_path, resname)
                    out_dir = dirname(resname)
                    if out_dir:
                        out_dir = os.path.join(dest_path, out_dir)
                        if not os.path.exists(out_dir):
                            os.makedirs(out_dir)
                    if overwrite or not os.path.exists(out_path):
                        erf.export(resname, out_path)
            except:
                print_exc()
                raise
        
        self.ShowFileOpDialog("Exporting Files", "Exporting Files")
        delayedresult.startWorker(export_done, export_files)

    def OnSaveAs(self, event):
        quiksave = self.config.getboolean('Editor', 'ImmediateSave')
        with wx.FileDialog(self, "Choose a file", self.dirname, self.resname, "All files(*.*)|*.*|YAML (*.yaml)|*.yaml|CSV (*.csv)|*.csv", wx.SAVE|wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.Path
                save_type = dlg.GetFilterIndex()
                model = self.gff4control.model
                data = model.data
                header = model.header
                if save_type == 0:
                    self.filename = dlg.Filename
                    self.resname = dlg.Filename
                    self.dirname = dlg.Directory
                    if quiksave and not hasattr(data, 'gff'):
                        quiksave = False
                    def save_gff():
                        try:
                            with open(path, 'wb') as f:
                                if quiksave:
                                    data.gff.tofile(f)
                                else:
                                    write_gff4(f, data, header)
                        except:
                            print_exc()
                            raise
                    self.ShowFileOpDialog("Writing GFF File", "Writing GFF File")
                    delayedresult.startWorker(self.OnSaveDone, save_gff)
                elif save_type == 1:
                    import gff4.toyaml as toyaml
                    def save_gff():
                        try:
                            toyaml.save_yaml(path, data, header, True)
                        except:
                            print_exc()
                            raise
                    self.ShowFileOpDialog("Writing YAML", "Writing YAML")
                    delayedresult.startWorker(self.OnSaveDone, save_gff)
                elif save_type == 2:
                    from gff4.g2da import gda2csv
                    if not model or not header.file_type == 'G2DA' or not header.file_version == 'V0.2':
                        with wx.MessageDialog(self, "Not a V0.2 G2DA file", "File Type/Version Incorrect", wx.OK|wx.ICON_ERROR) as dlg:
                            dlg.ShowModal()
                            return
                    try:
                        gda2csv(data, path)
                    except:
                        with wx.MessageDialog(self, format_exc(1), "Save Failed", wx.OK|wx.ICON_ERROR) as dlg:
                            dlg.ShowModal()

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "GFF V4.0 Editor"
        info.Version = "1.0.0"
        info.Description = wordwrap(
            "An editor for GFF V4.0 and V4.1 files, a viewer for GFF V3.2 files,"
            " and and an extractor for ERF V1.0, V1.1, V2.0, V2.2, and V3.0 archives."
            "\nProper recognition is given to the contributors to the ERF"
            " and GFF articles DA Builder Wiki, especially Thought Process"
            " for his work reverse-engineering ERF V3.0 and supplying the"
            " list of common Bioware file extensions and for reverse-engineering"
            " the TLK V0.5 compression, and to BioWare for their"
            " documents on NWN-era ERF V1.0 and GFF V3.2 formats.",
            350, wx.ClientDC(self))
        info.WebSite = ("http://social.bioware.com/project/1936/", "BioWare Social Network project site")
        info.Developers = [ "Mephales" ]
        info.License = "Released into the public domain. Share and Enjoy."
        
        wx.AboutBox(info)  
    
    def OnClose(self, event):
        self.Close(True)
    
    def OnExit(self, event):
        self.app.ExitMainLoop()
    
    def RefreshSettings(self, event):
        if event.GetMenu() is not self.settingsmenu:
            event.Skip()
            return
        self.set_lazyload.Check(self.config.getboolean('Editor', 'LazyLoad'))
        self.set_saveview.Check(self.config.getboolean('Editor', 'ImmediateSave'))
        self.set_savesettings.Check(self.config.getboolean('Editor', 'SaveSettingsOnExit'))
    
    def SaveSettings(self, event):
        with open(self.config_file, 'w') as f:
            self.config.write(f)
    
    def GetImportFileDialog(self, message):
        dlg = self.import_filedialog
        if dlg is None:
            self.import_filedialog = dlg = wx.FileDialog(self, message, self.dirname, '', "*.*", wx.OPEN|wx.FD_FILE_MUST_EXIST|wx.FD_MULTIPLE)
        else:
            dlg.Message = message
        return dlg
    
    def OnImportStrings(self, event):
        with wx.SingleChoiceDialog(self, "Choose the type of strings to import", "Import Strings", STRING_TYPES) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            import_type = dlg.GetSelection()
        
        dlg = self.GetImportFileDialog("Choose files with %s"%STRING_TYPES[import_type])
        if dlg.ShowModal() != wx.ID_OK:
            return
        
        def worker():
            obj = [0]
            
            def strings(path):
                skip_semi = False
                with open(path) as f:
                    for s in f:
                        if not obj[0] and s.startswith(';'):
                            skip_semi = True
                            continue
                        if skip_semi and s.startswith(';'):
                            continue
                        obj[0] += 1
                        yield s.strip()
            
            try:
                if import_type == 0:
                    for path in dlg.GetPaths():
                        fnvdb.addfiles(strings(path))
                elif import_type == 1:
                    for path in dlg.GetPaths():
                        fnvdb.addtypes(strings(path))
                elif import_type == 2:
                    import gff4.gdacolnames as colnames
                    for path in dlg.GetPaths():
                        colnames.addnames(strings(path))
            except:
                print_exc()
                raise
            else:
                return obj[0]
        
        def ondone(result):
            self.CloseFileOpDialog()
            try:
                count = result.get()
                with wx.MessageDialog(self, "%d %s imported."%(count, STRING_TYPES[import_type]), "Import Finished", wx.OK|wx.ICON_INFORMATION) as dlg:
                    dlg.ShowModal()
            except:
                with wx.MessageDialog(self, format_exc(1), "Import Failed", wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
        
        self.ShowFileOpDialog("Import Strings", "Importing...")
        delayedresult.startWorker(ondone, worker)
    
    def OnExportStrings(self, event):
        with wx.SingleChoiceDialog(self, "Choose the type of strings to export", "Export Strings", STRING_TYPES) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            export_type = dlg.GetSelection()
            
        with wx.FileDialog(self, "Choose a destination", self.dirname, '', "*.*", wx.SAVE|wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            path = dlg.Path
        
        def worker():
            try:
                with open(path, 'w', 4096) as f:
                    if export_type == 0:
                        return fnvdb.dumpfiles(f)
                    elif export_type == 1:
                        return fnvdb.dumptypes(f)
                    elif export_type == 2:
                        import gff4.gdacolnames as colnames
                        return colnames.dumpnames(f)
                    else:
                        raise ValueError, ('not an option', export_type)
            except:
                print_exc()
                raise
        
        def ondone(result):
            self.CloseFileOpDialog()
            try:
                count = result.get()
                with wx.MessageDialog(self, "%d %s exported."%(count, STRING_TYPES[export_type]), "Export Finished", wx.OK|wx.ICON_INFORMATION) as dlg:
                    dlg.ShowModal()
            except:
                with wx.MessageDialog(self, format_exc(1), "Export Failed", wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
        
        self.ShowFileOpDialog("Export Strings", "Exporting...")
        delayedresult.startWorker(ondone, worker)
    
    def OnTlkDowngrade(self, event):
        import gff4.htlk
        model = self.gff4control.model
        if not model or not model.header.file_type == 'TLK ' or not model.header.file_version == 'V0.5':
            with wx.MessageDialog(self, "Not a V0.5 TLK file", "File Type/Version Incorrect", wx.OK|wx.ICON_ERROR) as dlg:
                dlg.ShowModal()
                return
        data = model.data
        model.data = DummyModel()
        
        self.ShowFileOpDialog("Converting...", "Converting TLK V0.5 to 0.2")
        
        def ondone(result):
            try:
                self.CloseFileOpDialog()
                self.OnOpenDone(GFFModel(gff4.htlk.tlkheader, result.get()))
            except:
                with wx.MessageDialog(self, format_exc(1), "Conversion Failed", wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
        
        def worker():
            try:
                return gff4.htlk.htlk2tlk(data)
            except:
                print_exc()
                raise
        
        delayedresult.startWorker(ondone, worker)
    
    def OnGDAColnames(self, event):
        import gff4.gdacolnames
        model = self.gff4control.model
        if not model or not model.header.file_type == 'G2DA' or not model.header.file_version == 'V0.2':
            with wx.MessageDialog(self, "Not a V0.2 G2DA file", "File Type/Version Incorrect", wx.OK|wx.ICON_ERROR) as dlg:
                dlg.ShowModal()
                return
        data = model.data
        header = model.header
        model.data = DummyModel()
        
        self.ShowFileOpDialog("Adding column names...", "Annotating")
        
        def ondone(result):
            try:
                self.CloseFileOpDialog()
                data, header = result.get()
                self.OnOpenDone(GFFModel(header, data))
            except:
                with wx.MessageDialog(self, format_exc(1), "Annotation Failed", wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
        
        def worker():
            try:
                return gff4.gdacolnames.annotate(data, header)
            except:
                print_exc()
                raise
        
        delayedresult.startWorker(ondone, worker)
    
    def OnPlotToGUIDs(self, event):
        import gff4.plotguids
        gff4.plotguids.convert(self.gff4control.model.data, True)
        self.gff4control.control.RefreshItems()
    
    def OnPlotToResrefs(self, event):
        import gff4.plotguids
        gff4.plotguids.convert(self.gff4control.model.data, False)
        self.gff4control.control.RefreshItems()
    
    def OnRunScript(self, event):
        with wx.FileDialog(self, "Choose a script", wildcard="Python script (*.py)|*.py", style=wx.OPEN|wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.Path
            else:
                return
        
        helper = ScriptingHelper(self)
        
        def ondone(result):
            try:
                self.CloseFileOpDialog()
                result.get()
            except:
                with ScrolledMessageDialog(self, format_exc(), caption="Error running script %s"%path, style=wx.OK|wx.ICON_ERROR) as dlg:
                    dlg.ShowModal()
        
        def worker():
            execfile(path, {'helper': helper})
        
        self.ShowFileOpDialog("Running script...", "Running Script...")
        delayedresult.startWorker(ondone, worker)
    
    #def OnRunConsole(self, event):
    #    frame = wx.Frame(self, title='Scripting Console', size=(600, 400))
    #    shell = pyshell.Shell(frame, introText='Use helper.gff4data to access and replace the currently open GFF.', locals={'helper': ScriptingHelper(self)})
    #    frame.Show()

STRING_TYPES = ['Filenames', 'File Extensions', '2DA Column Names']

class ScriptingHelper(object):
    def __init__(self, window):
        self._window = window
    
    @property
    def gff4data(self):
        model = self._window.gff4control.model
        if hasattr(model, 'data'):
            return GFF4Data(model.header, model.data)
        return None
    
    @gff4data.setter
    def gff4data(self, data):
        if isinstance(data, GFF4Data) and data.root is not None and data.header is not None:
            def later():
                self._window.OnOpenDone(GFFModel(data.header, data.root))
                self._window.StatusText = 'Updated from script'
            wx.CallAfter(later)
        elif data is None:
            self._window.gff4control.model = DummyModel()
            self._window.OnOpenDone(None)
            self._window.StatusText = 'Cleared by script'
        else:
            raise TypeError, 'gff4.GFF4Data required'

StructCopy = gff4._structtype('Copy', [Field(0, gff4._listtype(None, True), False, 0)], 4)
StructData = gff4._structtype('Data', [Field(0, gff4._listtype(UINT8), False, 0)], 4)

class ShelfPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(ShelfPanel, self).__init__(*args, **kwargs)
        
        self.lst = AutoWidthListCtrl(self, style=wx.LC_REPORT)
        self.lst.InsertColumn(0, "Type")
        self.lst.InsertColumn(1, "Value")
        
        self.items = []
        
        self.menu = wx.Menu()
        copyitem = self.menu.Append(wx.ID_COPY, "&Copy\tCTRL+C")
        cutitem = self.menu.Append(wx.ID_CUT, "Cu&t\tCTRL+X")
        pasteitem = self.menu.Append(wx.ID_PASTE, "&Paste\tCTRL+V")
        deleteitem = self.menu.Append(wx.ID_DELETE, "&Delete\tDelete")
        selectallitem = self.menu.Append(wx.ID_SELECTALL, "Select &All\tCTRL+A")
        saveitem = self.menu.Append(wx.ID_ANY, "Sa&ve As")
        loadappenditem = self.menu.Append(wx.ID_ANY, "Load (App&end)")
        loadreplaceitem = self.menu.Append(wx.ID_ANY, "L&oad (Replace)")
        
        self.SetAcceleratorTable(wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('C'), wx.ID_COPY),
            (wx.ACCEL_CTRL, ord('X'), wx.ID_CUT),
            (wx.ACCEL_CTRL, ord('V'), wx.ID_PASTE),
            (wx.ACCEL_CTRL, ord('A'), wx.ID_SELECTALL),
            #(wx.ACCEL_CTRL, ord('D'), wx.ID_PASTE), # Deselect all
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, wx.ID_DELETE)
        ]))
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.lst, 1, wx.EXPAND)
        self.SetSizer(hsizer)
        
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu, self.lst)
        self.Bind(wx.EVT_MENU, self.OnCopy, copyitem)
        self.Bind(wx.EVT_MENU, self.OnCut, cutitem)
        self.Bind(wx.EVT_MENU, self.OnPaste, pasteitem)
        self.Bind(wx.EVT_MENU, self.OnDelete, deleteitem)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, selectallitem)
        self.Bind(wx.EVT_MENU, self.OnSave, saveitem)
        self.Bind(wx.EVT_MENU, self.OnLoadAppend, loadappenditem)
        self.Bind(wx.EVT_MENU, self.OnLoadReplace, loadreplaceitem)
    
    def OnContextMenu(self, evt):
        self.PopupMenu(self.menu)
    
    def OnCopy(self, event):
        lst = self.items
        wrapper = StructCopy()
        for i in selectedIndices(self.lst):
            wrapper[0].append(lst[i])
        clipdata = GFFDataObject()
        clipdata.Struct = wrapper
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(clipdata)
        wx.TheClipboard.Close()
    
    def OnCut(self, event):
        self.Freeze()
        lst = self.items
        lstctrl = self.lst
        wrapper = StructCopy()
        i = lstctrl.GetFirstSelected()
        if i < 0:
            return
        while i >= 0:
            wrapper[0].append(lst[i])
            del lst[i]
            lstctrl.DeleteItem(i)
            i = lstctrl.GetNextSelected(i-1)
        clipdata = GFFDataObject()
        clipdata.Struct = wrapper
        clipdata.GetDataHere()
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(clipdata)
        wx.TheClipboard.Close()
        self.Thaw()
    
    def OnPaste(self, event):
        self.Freeze()
        lstctrl = self.lst
        lst = self.items
        
        clipdata = GFFDataObject()
        wx.TheClipboard.Open()
        if not wx.TheClipboard.GetData(clipdata):
            return
        wx.TheClipboard.Close()
        items = clipdata.Struct[0]
        if not len(items):
            return
        
        i = lstctrl.GetFirstSelected()
        if i < 0:
            lst.extend(items)
            for item in items:
                if item is None:
                    lstctrl.Append(('?', '?'))
                elif isinstance(item, Structure):
                    lstctrl.Append((item.fourcc, value_preview(item, 200)))
                else:
                    lstctrl.Append((type(item).__name__, value_preview(item, 200)))
        else:
            lst[i:i] = items
            for item in items:
                if item is None:
                    t, s = '?', '?'
                elif isinstance(item, Structure):
                    t, s = item.fourcc, value_preview(item, 200)
                else:
                    t, s = type(item).__name__, value_preview(item, 200)
                it = wx.ListItem()
                it.SetColumn(0)
                it.SetId(i)
                it.SetText(t)
                lstctrl.InsertItem(it)
                it = wx.ListItem()
                it.SetColumn(1)
                it.SetId(i)
                it.SetText(s)
                lstctrl.SetItem(it)
                i += 1
        self.Thaw()
    
    def OnDelete(self, event):
        self.Freeze()
        lst = self.items
        lstctrl = self.lst
        i = lstctrl.GetFirstSelected()
        while i >= 0:
            del lst[i]
            lstctrl.DeleteItem(i)
            i = lstctrl.GetNextSelected(i-1)
        self.Thaw()
    
    def OnSelectAll(self, event):
        self.Freeze()
        lstctrl = self.lst
        for i in xrange(lstctrl.ItemCount):
            lstctrl.Select(i)
        self.Thaw()
    
    def OnSave(self, event):
        with wx.FileDialog(self, "Choose a destination", wildcard="Shelf files (*.shelf)|*.shelf|All files(*.*)|*.*", style=wx.SAVE|wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                wrapper = StructCopy()
                wrapper[0].extend(self.items)
                path = dlg.Path
                with open(path, 'wb') as f:
                    write_gff4(f, wrapper)
    
    def OnLoad(self, event, clear=False):
        with wx.FileDialog(self, "Choose a file", wildcard="Shelf files (*.shelf)|*.shelf|All files(*.*)|*.*", style=wx.OPEN|wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                with open(dlg.Path, 'rb') as f:
                    wrapper, header = read_gff4(f)
                lstctrl = self.lst
                lst = self.items
                self.Freeze()
                try:
                    if clear:
                        del lst[:]
                        lstctrl.DeleteAllItems()
                    items = wrapper[0]
                    lst.extend(items)
                    for item in items:
                        if item is None:
                            lstctrl.Append(('?', '?'))
                        elif isinstance(item, Structure):
                            lstctrl.Append((item.fourcc, value_preview(item, 200)))
                        else:
                            lstctrl.Append((type(item).__name__, value_preview(item, 200)))
                finally:
                    self.Thaw()
    
    def OnLoadReplace(self, event):
        self.OnLoad(event, True)
    
    def OnLoadAppend(self, event):
        self.OnLoad(event, False)

class GFFDrop(wx.FileDropTarget):
    def __init__(self, window):
        super(GFFDrop, self).__init__()
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        window = self.window
        gff_file = filenames[0]
        window.dirname, window.filename = os.path.split(gff_file)
        window.OpenFile(gff_file)

class GFFDataObject(wx.PyDataObjectSimple):
    def __init__(self):
        super(GFFDataObject, self).__init__(wx.CustomDataFormat('application/x-gff4'))
        self.data = None
        self.struct = None

    def GetDataSize(self):
        return len(self.GetDataHere())
        
    def GetDataHere(self):
        if self.data is None:
            out = StringIO()
            write_gff4(out, self.struct)
            self.data = out.getvalue()
        return self.data  # returns a string  
    
    def GetStruct(self):
        if self.struct is None:
            if self.data:
               self.struct = read_gff4(StringIO(self.data))[0]
        return self.struct
        
    def SetData(self, data):
        self.data = data
        self.struct = None
        return True
    
    def SetStruct(self, struct):
        if not isinstance(struct, Structure):
            raise TypeError
        self.struct = struct
        # serializing immediately to prevent changes
        #self.data = None
        out = StringIO()
        write_gff4(out, self.struct)
        self.data = out.getvalue()
    
    Struct = property(GetStruct, SetStruct)

class PasswordListEditor(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(PasswordListEditor, self).__init__(*args, **kwargs)
        
        self.listedit = wx.gizmos.EditableListBox(self, wx.ID_ANY, "ERF Passwords", style=wx.gizmos.EL_ALLOW_NEW | wx.gizmos.EL_ALLOW_EDIT | wx.gizmos.EL_ALLOW_DELETE)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.ok_button = wx.Button(self, label='&OK')
        bsizer.Add(self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.ok_button)
        
        self.cancel_button = wx.Button(self, label='&Cancel')
        bsizer.Add(self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel_button)
        
        sizer.Add(self.listedit, 1, flag=wx.EXPAND)
        sizer.Add(bsizer, 0, wx.EXPAND)
        
        self.SetSizer(sizer)
        
        self.list = []
        self.saved = False
    
    def SetStrings(self, list):
        self.saved = False
        self.list = [str(s) for s in list]
        self.listedit.SetStrings(self.list)
    
    def GetStrings(self):
        return self.list
    
    def IsChanged(self):
        return self.saved
    
    def OnOk(self, event):
        self.saved = True
        self.list = self.listedit.GetStrings()
        self.Show(False)
    
    def OnCancel(self, event):
        self.Show(False)

def _process_cli():
    import ConfigParser
    config_file = 'config.ini'
    config = ConfigParser.SafeConfigParser()
    config.add_section('Editor')
    config.set('Editor', 'LazyLoad', 'True')
    config.set('Editor', 'ImmediateSave', 'True')
    config.set('Editor', 'SaveSettingsOnExit', 'True')
    config.set('Editor', 'PrintToWindow', 'False')
    config.set('Editor', 'ErfPasswords', '')
    config.read(config_file)
    
    app = wx.PySimpleApp(config.getboolean('Editor', 'PrintToWindow'))
    frame = MyFrame(None, title='GFF V4.0 Editor', size=(1000,700))
    app.SetTopWindow(frame)
    frame.app = app
    frame.config = config
    frame.config_file = config_file
    frame.Show(True)

    if len(sys.argv) > 1:
        gff_file = sys.argv[1]
        frame.dirname, frame.filename = os.path.split(gff_file)
        wx.CallAfter(frame.OpenFile, gff_file)

    app.MainLoop()
    
    if config.getboolean('Editor', 'SaveSettingsOnExit'):
        with open(config_file, 'w') as f:
            config.write(f)

if __name__ == '__main__':
    _process_cli()