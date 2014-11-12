import wx, wx.gizmos, sys
from wx.lib.mixins.treemixin import VirtualTree
from wx.lib.mixins.listctrl import TextEditMixin, ColumnSorterMixin
from time import sleep
import wx.lib.delayedresult as delayedresult
from gff4 import *
from gff4.lazy import LazyGFF4
from gff4.datoolset_fields import *
from gff4.editorutils import *
from functools import partial
from traceback import print_exc
from ioutils import copyio
import zlib
try:
    from win32com.shell import shell
except ImportError:
    shell = None
from ConfigParser import RawConfigParser
try: from cStringIO import StringIO
except ImportError: from StringIO import StringIO

try:
    _resdir = os.path.dirname(__file__)
except NameError:
    import sys
    _resdir = os.path.dirname(sys.argv[0])

VERSION_DAO = 1
VERSION_DA2 = 2

with open(os.path.join(_resdir, 'StatPropertyNames.txt')) as f:
    _attribute_names = [line.strip().split(',') for line in f]
with open(os.path.join(_resdir, 'StatPropertyNames2.txt')) as f:
    _attribute_names_da2 = [line.strip().split(',') for line in f]
with open(os.path.join(_resdir, 'ResRefNames.txt')) as f:
    _resrefnames = dict(line.strip().decode('utf-8').split(None, 1) for line in f)
with open(os.path.join(_resdir, 'ResRefNames2.txt')) as f:
    _resrefnames_da2 = dict(line.strip().decode('utf-8').split(None, 1) for line in f)

def strnumcmp(a, b):
    m, n = len(a), len(b)
    i, j = 0, 0
    while i < m and j < n:
        if a[i].isdigit() and b[j].isdigit():
            q, r = i+1, j+1
            while q < m and a[q].isdigit():
                q += 1
            while r < n and b[r].isdigit():
                r += 1
            z = cmp(int(a[i:q]), int(b[j:r]))
            if z != 0:
                return z
            i, j = q, r
        else:
            z = cmp(a[i], b[j])
            if z != 0:
                return z
            i, j = i+1, j+1
    return 0

class SaveModel(object):
    def __init__(self, *args, **kwargs):
        super(SaveModel, self).__init__(*args, **kwargs)
        df = shell.SHGetDesktopFolder()
        pidl = df.ParseDisplayName(0, None, "::{450d8fba-ad25-11d0-98a8-0800361b1103}")[1]
        mydocs = shell.SHGetPathFromIDList(pidl)
        self.base = os.path.join(mydocs, 'Bioware', 'Dragon Age')

    def GetItem(self, indices):
        text = 'root'
        path = os.path.join(self.base, 'Characters')
        children = filter(lambda x: x[0] != '.', os.listdir(path))
        
        for i, index in enumerate(indices):
            text = children[index]
            if i == 0:
                path = os.path.join(path, text, 'Saves')
                children = sorted(filter(lambda x: x[0] != '.', os.listdir(path)), strnumcmp)
            else:
                path = os.path.join(path, text)
                children = ()
        
        return text, path, children

    def GetText(self, indices, column):
        text, path, children = self.GetItem(indices)
        if not column:
            return text
        
        if len(indices) == 2:
            files = filter(lambda x: x.endswith('.das.met'), os.listdir(path))
            if len(files):
                file = os.path.join(path, files[0])
                header, data = open_gff(file)
                info = data[16800+column-1]
                if column == 2:
                    return '%d:%02d:%02d'%(info/3600, (info/60)%60, info%60)
                if column == 4:
                    return ('Invalid', 'Warrior', 'Mage', 'Rogue', None, None, None, None, None, None, None, None, None, None, None, None, None, 'Dog')[info]
                elif column == 5:
                    return ('Invalid', 'Male', 'Female', 'Other')[info]
                elif column == 6:
                    return ('Invalid', '?Dwarf', 'Elf', 'Human')[info]
                elif column == 7:
                    return ('Invalid', 'Dalish Elf', 'Dwarf Commoner', 'City Elf', 'Magi', 'Human Noble', 'Dwarf Noble')[info]
                else:
                    return str(info)
        
        return ''

    def GetChildrenCount(self, indices):
        return len(self.GetItem(indices)[2])
    
    def GetSaveFile(self, character, save):
        if not character or not save:
            return None
        path = os.path.join(self.base, 'Characters', character, 'Saves', save)
        files = filter(lambda x: x.endswith('.das'), os.listdir(path))
        if len(files):
            return os.path.join(path, files[0])
        else:
            return None
    
    def GetLastPlayedGame(self):
        data = RawConfigParser()
        with open(os.path.join(self.base, 'Settings', 'DragonAge.ini'), 'r') as f:
            data.readfp(f)
        return data.get('GameOptions', 'LastPlayedGame')

class SaveSelectTree(VirtualTree, wx.gizmos.TreeListCtrl):
    def __init__(self, *args, **kwargs):
        super(SaveSelectTree, self).__init__(*args, **kwargs)
        self.AddColumn('Name', 120)
        self.AddColumn('Area', 180)
        self.AddColumn('Played', width=70)
        self.AddColumn('Level', width=50)
        self.AddColumn('Class', width=50)
        self.AddColumn('Gender', width=50)
        self.AddColumn('Race', width=50)
        self.AddColumn('Background', width=100)
    
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
    

class SaveSelectDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        if 'model' in kwargs:
            model = kwargs.pop('model')
        else:
            model = None
        super(SaveSelectDialog, self).__init__(*args, **kwargs)
        
        self.control = SaveSelectTree(self)
        if model is not None:
            self.control.model = model
        self.buttons = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        self.ok_button = None
        for button in self.buttons.GetChildren():
            window = button.GetWindow()
            if window is not None and window.GetId() == wx.ID_OK:
                self.ok_button = window
                break
        if self.ok_button is not None:
            self.ok_button.SetDefault()
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)
        self.sizer.Add(self.buttons, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.control)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self.control)
    
    def OnSelChanged(self, event):
        if self.ok_button is not None:
            if len(get_tree_text_path(self.control, event.GetItem())) != 3:
                self.ok_button.Disable()
            else:
                self.ok_button.Enable()
    
    def OnActivate(self, event):
        if len(get_tree_text_path(self.control, event.GetItem())) == 3:
            self.EndModal(wx.ID_OK)
        else:
            event.Skip()

class InventoryPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(InventoryPanel, self).__init__(*args, **kwargs)
        self.sizer = wx.FlexGridSizer(0, 3)
        text_flag = wx.TOP|wx.LEFT|wx.RIGHT|wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL
        item_flag = wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP
        
        self.sizer.Add(wx.StaticText(self, label="Money"), border=5, flag=text_flag)
        
        self.money = wx.SpinCtrl(self, max=999999999)
        self.sizer.Add(self.money, border=5, flag=item_flag)
        
        self.maxmoney = wx.Button(self, label='Max')
        self.sizer.Add(self.maxmoney, border=5, flag=item_flag)
        
        self.sizer.Add(wx.StaticText(self, label="Max Items"), border=5, flag=text_flag)
        
        self.capacity = wx.SpinCtrl(self, max=999999999)
        self.sizer.Add(self.capacity, border=5, flag=item_flag)
        
        self.maxcapacity = wx.Button(self, label='Max')
        self.sizer.Add(self.maxcapacity, border=5, flag=item_flag)
        
        self.SetSizer(self.sizer)
        
        self.Bind(wx.EVT_BUTTON, lambda e: self.money.SetValue(self.money.GetMax()), self.maxmoney)
        self.Bind(wx.EVT_BUTTON, lambda e: self.capacity.SetValue(self.capacity.GetMax()), self.maxcapacity)
    
    def save(self):
        changed = False
        value = INT32(self.money.GetValue())
        if self.data[SAVEGAME_MONEY] != value:
            self.data[SAVEGAME_MONEY] = value
            changed = True
        value = INT32(self.capacity.GetValue())
        if self.data[SAVEGAME_MAX_ITEMS] != value:
            self.data[SAVEGAME_MAX_ITEMS] = value
            changed = True
        return changed
    
    def load(self, data, root, game_version=VERSION_DAO):
        self.data = data
        self.money.SetValue(data[SAVEGAME_MONEY])
        self.capacity.SetValue(data[SAVEGAME_MAX_ITEMS])

class ItemList(wx.ListCtrl, TextEditMixin, ColumnSorterMixin):
    def __init__(self, *args, **kwargs):
        kwargs['style'] = wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES
        wx.ListCtrl.__init__(self, *args, **kwargs)
        
        self.changed = False
        
        self.InsertColumn(0, "ResRef", wx.LIST_FORMAT_CENTRE, 200)
        self.InsertColumn(1, "Name", wx.LIST_FORMAT_CENTRE, 200)
        self.InsertColumn(2, "Count", wx.LIST_FORMAT_CENTRE, 50)
        self.InsertColumn(3, "Infinite", wx.LIST_FORMAT_CENTRE, 50)
        self.InsertColumn(4, "Plot", wx.LIST_FORMAT_CENTRE, 50)
        self.InsertColumn(5, "16238", wx.LIST_FORMAT_CENTRE, 50)
        
        TextEditMixin.__init__(self)
        
        self.itemDataMap = []
        self.itemIndexMap = []
        
        ColumnSorterMixin.__init__(self, 6)
        
        self.context_menu = wx.Menu()
        dupeitem = self.context_menu.Append(wx.ID_ANY, 'Duplicate')
        moveitem = self.context_menu.Append(wx.ID_ANY, 'Move Item', 'Move selected items to a different inventory')
        
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit)
        self.Bind(wx.EVT_CONTEXT_MENU, lambda event: self.PopupMenu(self.context_menu))
        self.Bind(wx.EVT_MENU, self.OnDupeItem, dupeitem)
        self.Bind(wx.EVT_MENU, self.OnMoveItem, moveitem)
    
    def OnDupeItem(self, event):
        for index in selectedIndices(self):
            index = self.itemIndexMap[index]
            
            # not a deep clone, but doesn't need to be
            row = self.data[index]
            cop = type(row)(row)
            self.wdbe[SAVEGAME_WORLDDB_LASTID] += 1
            cop[OBJECT_ID] = self.wdbe[SAVEGAME_WORLDDB_LASTID]
            
            self.AppendItem(cop)
            self.changed = True
    
    def AppendItem(self, item):
        if self.data:
            item[POSITION] = item[POSITION]._replace(a=self.data[-1][POSITION].a+1)
        else:
            item[POSITION] = item[POSITION]._replace(a=0.)
        index = len(self.data)
        self.itemIndexMap.append(index)
        self.itemDataMap.append(self.GetRowText(item))
        self.data.append(item)
        self.SetItemCount(len(self.data))
        self.RefreshItem(index)
        self.changed = True
    
    def OnMoveItem(self, event):
        names = sorted(k for k, v in self.inventories.iteritems() if v != self and v.data != self.data)
        
        with wx.SingleChoiceDialog(self, "Choose destination inventory", "Choose Inventory", names) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            item_list = self.inventories[names[dlg.GetSelection()]]
        
        visible = self.GetFirstSelected()
        while visible >= 0:
            index = self.itemIndexMap[visible]
            row = self.data[index]
            self.DeleteItem(visible) 
            del self.itemDataMap[index]
            del self.itemIndexMap[visible]
            for i, n in enumerate(self.itemIndexMap):
                if n > index:
                    self.itemIndexMap[i] = n - 1
            del self.data[index]
            item_list.AppendItem(row)
            visible = self.GetFirstSelected()
            self.changed = True
    
    def save(self):
        return self.changed
    
    def load(self, data, root, game_version=VERSION_DAO):
        self.DeleteAllItems()
        del self.itemDataMap[:]
        del self.itemIndexMap[:]
        
        self.data = data
        self.root = root
        
        self.resrefnames = _resrefnames if game_version == 1 else _resrefnames_da2
        
        self.wdbe = filter(lambda x: x[SAVEGAME_WORLDDB_IDGROUP] == 0, self.root[SAVEGAME_WORLDDATABASE])[0]
        
        self.itemDataMap = [self.GetRowText(row) for row in self.data]
        self.itemIndexMap = range(len(self.data))
        self.SetItemCount(len(data))
        self.changed = False
    
    def reset(self):
        self.DeleteAllItems()
        self.itemDataMap = []
        self.itemIndexMap = []
        self.data = None
        self.root = None
        self.changed = False
    
    def OnGetItemText(self, index, column):
        index = self.itemIndexMap[index]
        row = self.data[index]
        if not column:
            return row[TEMPLATERESREF].strip('\0')
        elif column == 1:
            return self.resrefnames.get(row[TEMPLATERESREF].strip('\0'), '')
        elif column == 2:
            return row[ITEM_STACKSIZE]
        elif column == 3:
            return row[SAVEGAME_ITEM_INFINITE]
        elif column == 4:
            return row[SAVEGAME_OBJECT_PLOT]
        elif column == 5:
            return row.get(16238, '')
    
    def GetRowText(self, row):
        resref = row[TEMPLATERESREF].strip('\0')
        return [
            resref,
            self.resrefnames.get(resref, ''),
            row[ITEM_STACKSIZE],
            row[SAVEGAME_ITEM_INFINITE],
            row[SAVEGAME_OBJECT_PLOT],
            row.get(16238, ''),
        ]
    
    def SetVirtualData(self, index, column, s):
        index = self.itemIndexMap[index]
        row = self.data[index]
        
        if column == 2:
            row[ITEM_STACKSIZE] = s
            self.itemDataMap[index][2] = row[ITEM_STACKSIZE]
        elif column == 3:
            row[SAVEGAME_ITEM_INFINITE] = s
            self.itemDataMap[index][3] = row[SAVEGAME_ITEM_INFINITE]
        self.changed = True
    
    def OnBeginEdit(self, event):
        index, column = event.GetIndex(), event.GetColumn()
        if column not in (2, 3):
            event.Veto()
    
    def SortItems(self,sorter=cmp):
        items = list(range(len(self.data)))
        items.sort(sorter)
        self.itemIndexMap = items
        self.Refresh()

    def GetListCtrl(self):
        return self

class CreatureStatsList(wx.ListCtrl, TextEditMixin):
    def __init__(self, *args, **kwargs):
        kwargs['style'] = wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES
        wx.ListCtrl.__init__(self, *args, **kwargs)
        
        self.changed = False
        
        self.InsertColumn(0, "Id", wx.LIST_FORMAT_CENTRE, 25)
        self.InsertColumn(1, "Name", wx.LIST_FORMAT_CENTRE, 180)
        self.InsertColumn(2, "Base", wx.LIST_FORMAT_CENTRE)
        self.InsertColumn(3, "Modifier", wx.LIST_FORMAT_CENTRE)
        self.InsertColumn(4, "Current", wx.LIST_FORMAT_CENTRE)
        self.InsertColumn(5, "Regen", wx.LIST_FORMAT_CENTRE)
        self.InsertColumn(6, "Combat Regen", wx.LIST_FORMAT_CENTRE)
        
        TextEditMixin.__init__(self)
        
        self.context_menu = wx.Menu()
        addpropitem = self.context_menu.Append(wx.ID_ANY, 'Add Known Attribute')
        
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit)
        self.Bind(wx.EVT_CONTEXT_MENU, lambda event: self.PopupMenu(self.context_menu))
        self.Bind(wx.EVT_MENU, self.OnAddProperty, addpropitem)
    
    def save(self):
        return self.changed
    
    def load(self, data, root, game_version=VERSION_DAO):
        self.data = data
        self.root = root
        self.SetItemCount(len(data))
        if game_version == 1:
            self._attribute_names = _attribute_names
        else:
            self._attribute_names = _attribute_names_da2
        self.changed = False
    
    def OnGetItemText(self, index, column):
        if column != 1:
            data = self.data[index]
            id = self._column2id[column]
            if id in data:
                return str(data[id])
        else:
            data = self.data[index]
            id = data[SAVEGAME_STATPROPERTY_INDEX]
            if 0 < id and id <= len(self._attribute_names):
                name = self._attribute_names[id-1][0]
                if name is not None:
                    return name
        return ''
    
    def SetVirtualData(self, index, column, s):
        data = self.data[index]
        id = self._column2id[column]
        if id in data:
            data[id] = type(data[id])(s)
        self.changed = True
    
    def OnBeginEdit(self, event):
        index, column = event.GetIndex(), event.GetColumn()
        if column <= 1:
            event.Veto()
        else:
            data = self.data[index]
            id = self._column2id[column]
            if id not in data:
                event.Veto()
    
    _column2id = [
        SAVEGAME_STATPROPERTY_INDEX, 
        None, 
        SAVEGAME_STATPROPERTY_BASE, 
        SAVEGAME_STATPROPERTY_MODIFIER, 
        SAVEGAME_STATPROPERTY_CURRENT, 
        SAVEGAME_STATPROPERTY_REGEN, 
        SAVEGAME_STATPROPERTY_COMREGEN]
    
    def OnAddProperty(self, event):
        existing = set(attr[SAVEGAME_STATPROPERTY_INDEX] - 1 for attr in self.data)
        properties = sorted(attr[0] for i, attr in enumerate(self._attribute_names) if i not in existing)
        
        with wx.SingleChoiceDialog(self, "Choose a standard attribute", "Choose Attribute", properties) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            propname = properties[dlg.GetSelection()]
        
        for i, attr in enumerate(self._attribute_names):
            if attr[0] == propname:
                cls = self.root.header.find(attr[1])
                item = cls()
                item[SAVEGAME_STATPROPERTY_INDEX] = i + 1
                index = len(self.data)
                self.data.append(item)
                self.SetItemCount(len(self.data))
                self.RefreshItem(index)
                break
        self.changed = True

class PartyPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(PartyPanel, self).__init__(*args, **kwargs)
        
    def load(self, data, root, game_version=VERSION_DAO):
        self.data = data
        
        resrefnames = _resrefnames if game_version == 1 else _resrefnames_da2
        
        self.ids2name = {}
        for crl1 in (data[SAVEGAME_PARTYPOOLMEMBERS] or ()):
            name = crl1[SAVEGAME_OBJECT_NAME].s
            if not name:
                resref = name = crl1[3].strip('\0')
                name = resrefnames.get(resref, resref)
            else:
                name = name.strip('\0')
            self.ids2name[crl1[OBJECT_ID]] = name
        
        text_flag = wx.TOP|wx.LEFT|wx.RIGHT|wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL
        item_flag = wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP
        
        self.sizer = wx.FlexGridSizer(0, 4)
        self.approval = {}
        self.buttons = {}
        
        for aprv in (data[SAVEGAME_PARTY_APPROVAL_LIST] or ()):
            id = aprv[SAVEGAME_PARTY_APPROVAL_ID]
            level = aprv[SAVEGAME_PARTY_APPROVAL_LEVEL]
            name = self.ids2name.get(id, 'Unknown%d'%id)
            
            self.sizer.Add(wx.StaticText(self, label="%s's Approval"%name), border=5, flag=text_flag)
            
            self.approval[id] = wx.SpinCtrl(self, max=100, min=-100, initial=level)
            self.sizer.Add(self.approval[id], border=5, flag=item_flag)
            
            maxbutton = wx.Button(self, label='Max')
            self.buttons[maxbutton] = self.approval[id]
            self.sizer.Add(maxbutton, border=5, flag=item_flag)
            self.Bind(wx.EVT_BUTTON, self.OnMaxSpin, maxbutton)
            
            minbutton = wx.Button(self, label='Min')
            self.buttons[minbutton] = self.approval[id]
            self.sizer.Add(minbutton, border=5, flag=item_flag)
            self.Bind(wx.EVT_BUTTON, self.OnMinSpin, minbutton)
            
        self.SetSizer(self.sizer)
    
    def OnMaxSpin(self, event):
        spin = self.buttons[event.GetEventObject()]
        spin.SetValue(spin.GetMax())
    
    def OnMinSpin(self, event):
        spin = self.buttons[event.GetEventObject()]
        spin.SetValue(spin.GetMin())
    
    def save(self):
        changed = False
        for aprv in self.data[SAVEGAME_PARTY_APPROVAL_LIST]:
            id = aprv[SAVEGAME_PARTY_APPROVAL_ID]
            spin = self.approval[id]
            value = INT32(spin.GetValue())
            if aprv[SAVEGAME_PARTY_APPROVAL_LEVEL] != value:
                aprv[SAVEGAME_PARTY_APPROVAL_LEVEL] = value
                changed = True
        return changed

class AreaInventoryPanel(wx.Panel):
    _choices = [
        'Placeables',
        'Stores',
        'Creature\'s Equipment',
        'Creature\'s Backpack',
        'Creature\'s Plot Items',
    ]
    
    def __init__(self, *args, **kwargs):
        super(AreaInventoryPanel, self).__init__(*args, **kwargs)
        self.arealist = wx.ListCtrl(self, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.arealist.InsertColumn(0, "Name", wx.LIST_FORMAT_LEFT, 150)
        self.arealist.InsertColumn(1, "Resref", wx.LIST_FORMAT_LEFT, 150)
        self.types = wx.ComboBox(self, choices=self._choices, style=wx.CB_READONLY)
        self.containers = wx.ListCtrl(self, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.containers.InsertColumn(0, "#", wx.LIST_FORMAT_RIGHT, 25)
        self.containers.InsertColumn(1, "Name", wx.LIST_FORMAT_LEFT, 150)
        self.containers.InsertColumn(2, "Resref", wx.LIST_FORMAT_LEFT, 150)
        self.show_empty = wx.CheckBox(self, label="Show empty containers")
        self.itemlist = ItemList(self)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.arealist, 1, wx.EXPAND)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(self.types, 0, wx.EXPAND)
        sizer2.Add(self.containers, 1, wx.EXPAND)
        sizer2.Add(self.show_empty, 0, wx.EXPAND)
        sizer.Add(sizer2, 1, wx.EXPAND)
        sizer.Add(self.itemlist, 3, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.arealist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnAreaSelect)
        self.types.Bind(wx.EVT_COMBOBOX, self.OnTypeSelect)
        self.containers.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnContainerSelect)
        self.show_empty.Bind(wx.EVT_CHECKBOX, self.OnShowEmpty)
        
        self.areacont = None
        self.area = None
        self.container = None
        self.area_changed = False
        self.changed = False
    
    @property
    def inventories(self):
        return self.itemlist.inventories
    
    @inventories.setter
    def inventories(self, value):
        self.itemlist.inventories = value
    
    def save(self):
        if self.itemlist.save():
            self.area_changed = True
        if self.area_changed:
            if self.areacont:
                arec, areg = self.areacont
                temp = StringIO()
                areg.tofile(temp)
                temp.seek(0)
                data = temp.read()
                arec[16022] = len(data)
                data = Binary(zlib.compress(data))
                arec[16021] = data
            self.changed = True
        return self.changed
    
    def load(self, data, root, game_version=VERSION_DAO):
        self.arealist.DeleteAllItems()
        self.containers.DeleteAllItems()
        self.itemlist.reset()
        self.data = data
        self.root = root
        self.game_version = game_version
        list = self.arealist
        for area in data:
            resref = area[TAG].strip('\0')
            name = (_resrefnames if game_version == 1 else _resrefnames_da2).get(resref)
            list.Append([name, resref])
        
        self.area = None
        self.areacont = None
        self.container = None
        self.area_changed = False
        self.changed = False
    
    def OnAreaSelect(self, event):
        self.save()
        
        tag = self.arealist.GetItem(event.Index, 1).Text
        area = self.data[event.Index]
        assert area[TAG].strip('\0') == tag
        
        if area.fourcc == 'AREC':
            g = LazyGFF4(StringIO(zlib.decompress(area[16021])))
            self.areacont = (area, g)
            self.area = g.root[16023]
        else:
            self.area = area
        
        self.area_changed = False
        self.RefreshContainerList()
    
    def OnTypeSelect(self, event):
        self.RefreshContainerList()
    
    def OnShowEmpty(self, event):
        self.RefreshContainerList()
    
    def OnContainerSelect(self, event):
        if self.itemlist.save():
            self.area_changed = True
        
        self.itemlist.load(self.shown_containers[event.Index], self.root, self.game_version)
    
    def RefreshContainerList(self):
        self.containers.DeleteAllItems()
        self.itemlist.reset()
        
        area = self.area
        type = self.types.GetValue()
        if not area or not type:
            return
        
        show_all = self.show_empty.IsChecked()
        list = self.containers
        
        resrefnames = _resrefnames if self.game_version == 1 else _resrefnames_da2
        shown_containers = []
        
        if type == 'Stores':
            def generator():
                for c in area[SAVEGAME_AREA_STORES]:
                    yield c[TEMPLATERESREF], c[SAVEGAME_STORE_ITEMLIST]
        elif type == 'Placeables':
            def generator():
                for c in area[SAVEGAME_AREA_PLACEABLES]:
                    yield c[TEMPLATERESREF], c[SAVEGAME_ITEMS]
        elif type == 'Creature\'s Equipment':
            def generator():
                for c in area[SAVEGAME_AREA_CREATURES]:
                    yield c[TEMPLATERESREF], c[SAVEGAME_EQUIPMENT_ITEMS]
        elif type == 'Creature\'s Backpack':
            def generator():
                for c in area[SAVEGAME_AREA_CREATURES]:
                    yield c[TEMPLATERESREF], c[SAVEGAME_BACKPACK]
        elif type == 'Creature\'s Plot Items':
            def generator():
                for c in area[SAVEGAME_AREA_CREATURES]:
                    yield c[TEMPLATERESREF], c[SAVEGAME_PLOTITEMS]
        
        # ALSO: player character/party pool member equipment/backpack/plotitems
        
        for resref, items in generator():
            itemcount = len(items)
            if show_all or itemcount:
                resref = resref.strip('\0')
                name = resrefnames.get(resref, resref)
                list.Append([itemcount, name, resref])
                shown_containers.append(items)
        
        self.shown_containers = shown_containers
    
class SavegameNotebook(wx.Treebook):
    def __init__(self, *args, **kwargs):
        super(SavegameNotebook, self).__init__(*args, **kwargs)
        self.AddPage(None, "No Data")
        self.savables = []
    
    def save(self):
        changed = False
        for savable in self.savables:
            changed |= savable.save()
        return changed
    
    def load(self, data, root, game_version=VERSION_DAO):
        #print game_version
        self.DeleteAllPages()
        del self.savables[:]
        
        self.data = data
        
        self.inventory = InventoryPanel(self)
        self.inventory.load(data[SAVEGAME_PARTYLIST], root, game_version)
        self.savables.append(self.inventory)
        self.AddPage(self.inventory, "Inventory")
        
        inventories = dict()
        
        self.backpack = ItemList(self)
        self.backpack.load(data[SAVEGAME_PARTYLIST][SAVEGAME_BACKPACK], root, game_version)
        self.savables.append(self.backpack)
        self.AddSubPage(self.backpack, "Backpack")
        inventories["Backpack"] = self.backpack
        self.backpack.inventories = inventories
        
        self.plotitems = ItemList(self)
        self.plotitems.load(data[SAVEGAME_PARTYLIST][SAVEGAME_PLOTITEMS], root, game_version)
        self.savables.append(self.plotitems)
        self.AddSubPage(self.plotitems, "Plot Items")
        inventories["Plot Items"] = self.plotitems
        self.plotitems.inventories = inventories
        
        if 32000 in data[SAVEGAME_PARTYLIST]:
            self.party_store = ItemList(self)
            self.party_store.load(data[SAVEGAME_PARTYLIST][32000][SAVEGAME_STORE_ITEMLIST], root, game_version)
            self.savables.append(self.party_store)
            self.AddSubPage(self.party_store, "Party Storage")
            inventories["Party Storage"] = self.party_store
            self.party_store.inventories = inventories
        
        for area in data[SAVEGAME_AREALIST]:
            if area[TAG] == 'gwb201ar_sp_repaired\0':
                placename = 'gwb201ip_party_chest\0'
                suffix = " (Warden's Keep)"
            elif area[TAG] == 'vgk210ar_throne_room\0':
                placename = 'vgk210ip_party_chest\0'
                suffix = " (Awakening)"
            else:
                continue
            for placeable in area[SAVEGAME_AREA_PLACEABLES]:
                if placeable[TEMPLATERESREF] == placename:
                    party_store = ItemList(self)
                    party_store.load(placeable[SAVEGAME_ITEMS], root, game_version)
                    self.savables.append(party_store)
                    placename = (_resrefnames if game_version == 1 else _resrefnames_da2)[placename.strip('\0')]+suffix
                    self.AddSubPage(party_store, placename)
                    inventories[placename] = party_store
                    party_store.inventories = inventories
                    break
        
        self.party = PartyPanel(self)
        self.party.load(data[SAVEGAME_PARTYLIST], root, game_version)
        self.savables.append(self.party)
        self.AddPage(self.party, "Party")
        
        crp1 = data[SAVEGAME_PLAYERCHAR][SAVEGAME_PLAYERCHAR_CHAR]
        char_data = crp1[SAVEGAME_CREATURE_STATS][SAVEGAME_STATLIST]
        character = CreatureStatsList(self)
        character.load(char_data, root, game_version)
        self.savables.append(character)
        self.characters = [character]
        self.AddSubPage(character, crp1[SAVEGAME_OBJECT_NAME].s.strip('\0'))
        
        for crl1 in (data[SAVEGAME_PARTYLIST][SAVEGAME_PARTYPOOLMEMBERS] or ()):
            char_data = crl1[SAVEGAME_CREATURE_STATS][SAVEGAME_STATLIST]
            character = CreatureStatsList(self)
            character.load(char_data, root, game_version)
            self.savables.append(character)
            self.characters.append(character)
            self.AddSubPage(character, self.party.ids2name[crl1[OBJECT_ID]])
        
        self.AddPage(wx.Panel(self), "Areas")
        self.area_items = AreaInventoryPanel(self)
        self.area_items.load(data[SAVEGAME_AREALIST], root, game_version)
        self.area_items.inventories = inventories
        self.savables.append(self.area_items)
        self.AddSubPage(self.area_items, "Items")

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)
        self.control = SavegameNotebook(self, wx.ID_ANY)
        self.CreateStatusBar()
        
        self.filename = ''
        self.dirname = ''
        self.gff_file = ''
        if shell:
            self.savemodel = SaveModel()
        else:
            self.savemodel = None
        self.character = ''
        self.save = ''
        
        filemenu = wx.Menu()
        if shell:
            openitem = filemenu.Append(wx.ID_OPEN, "&Open","Open a savegame")
            lastitem = filemenu.Append(wx.ID_ANY, "Open &Last Played","Open the last played savegame")
        manualitem = filemenu.Append(wx.ID_ANY, "Open &File\tCTRL+O","Open a savegame by manually locating it")
        saveitem = filemenu.Append(wx.ID_SAVE, "&Save\tCTRL+S","Save the savegame")
        filemenu.AppendSeparator()
        exititem = filemenu.Append(wx.ID_EXIT,"E&xit\tCTRL+Q","Terminate the program")
        
        helpmenu = wx.Menu()
        aboutitem = helpmenu.Append(wx.ID_ABOUT, "&About","Information about this program")

        menubar = wx.MenuBar()
        menubar.Append(filemenu,"&File")
        menubar.Append(helpmenu,"&Help")
        self.SetMenuBar(menubar)
        
        if shell:
            self.Bind(wx.EVT_MENU, self.OnOpen, openitem)
            self.Bind(wx.EVT_MENU, self.OnOpenLast, lastitem)
        self.Bind(wx.EVT_MENU, self.OnOpenFile, manualitem)
        self.Bind(wx.EVT_MENU, self.OnSave, saveitem)
        self.Bind(wx.EVT_MENU, self.OnExit, exititem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutitem)
    
    def OnOpen(self, event):
        dlg = SaveSelectDialog(self, title="Choose a savegame", size=(480, 480), model=self.savemodel)
        if dlg.ShowModal() == wx.ID_OK:
            path = get_tree_text_path(dlg.control)
            self.character, self.save = path[1:]
            self.gff_file = self.savemodel.GetSaveFile(self.character, self.save)
            self.ShowFileOpDialog("Reading Savegame", "Reading Savegame")
            delayedresult.startWorker(self.OnOpenDone, open_gff, wargs=[self.gff_file])
        dlg.Destroy()
    
    def OnOpenLast(self, event):
        self.gff_file = self.savemodel.GetLastPlayedGame()
        path = os.path.split(self.gff_file)[0]
        path, self.save = os.path.split(path)
        path = os.path.split(path)[0]
        path, self.character = os.path.split(path)
        self.ShowFileOpDialog("Reading Savegame", "Reading Savegame")
        delayedresult.startWorker(self.OnOpenDone, open_gff, wargs=[self.gff_file])
    
    def OnOpenFile(self, event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename, "Dragon Age Savegames (*.das)|*.das", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.gff_file = os.path.join(self.dirname, self.filename)
            self.character = ''
            self.save = ''
            self.ShowFileOpDialog("Reading Savegame", "Reading Savegame")
            delayedresult.startWorker(self.OnOpenDone, open_gff, wargs=[self.gff_file])
        dlg.Destroy()
    
    def OnSave(self, event):
        self.control.save()
        if self.gff_file:
            gff_file = self.gff_file
        else:
            gff_file = self.savemodel.GetSaveFile(self.character, self.save)
        if gff_file:
            if not os.path.exists(gff_file+'.orig'):
                os.rename(gff_file, gff_file+'.orig')
            else:
                bak_file = gff_file+'.bak'
                if os.path.exists(bak_file):
                    os.unlink(bak_file)
                os.rename(gff_file, bak_file)
            self.ShowFileOpDialog("Saving Savegame", "Saving Savegame")
            delayedresult.startWorker(self.OnSaveDone, save_gff, wargs=[gff_file, self.header, self.data])
    
    def ShowFileOpDialog(self, title, message):
        self.fileprogress = wx.ProgressDialog(title, message, parent=self, style=wx.PD_ELAPSED_TIME)
        self.filetimer = wx.Timer(self)
        self.filetimer.Start(500)
        self.Bind(wx.EVT_TIMER, self.OnFileOpTimer)
    
    def OnFileOpTimer(self, event):
        self.fileprogress.Pulse()
        self.fileprogress.Refresh()

    def CloseFileOpDialog(self):
        self.filetimer.Stop()
        self.fileprogress.Destroy()
    
    def OnOpenDone(self, result):
        self.CloseFileOpDialog()
        self.header, self.data = result.get()
        self.control.load(self.data, self.data, self.header.version == 'V4.0')
    
    def OnSaveDone(self, result):
        self.CloseFileOpDialog()
        try:
            result.get()
        except Exception, ex:
            print_exc()

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small savegame editor for Dragon Age: Origins, by Mephales", "About Dragon Age: Origins Savegame Editor", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
  
    def OnExit(self, event):
        self.app.ExitMainLoop()

def open_gff(gff_file):
    with open(gff_file, 'rb') as f:
        gff = LazyGFF4(f)
    return gff

def save_gff(gff_file, header, data):
    with open(gff_file, 'wb') as f:
        data.gff.tofile(f)

def get_tree_text_path(tree, item=None):
    if item is None: item = tree.GetSelection()
    path = []
    while item.IsOk():
        path[0:0] = [tree.GetItemText(item)]
        item = tree.GetItemParent(item)
    return path

if __name__ == '__main__':
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = MyFrame(None, title='Dragon Age: Origins Savegame Editor', size=(800,600))
    frame.app = app
    frame.Show(True)
    app.MainLoop()