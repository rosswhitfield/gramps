#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2000-2003  Donald N. Allingham
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

#-------------------------------------------------------------------------
#
# GTK/Gnome modules
#
#-------------------------------------------------------------------------
import gobject
import gtk.glade
import const
from gettext import gettext as _

column_names = [
    _('Name'),
    _('ID') ,
    _('Gender'),
    _('Birth Date'),
    _('Birth Place'),
    _('Death Date'),
    _('Death Place'),
    ]

class ColumnOrder:

    def __init__(self,arglist,callback):
        self.glade = gtk.glade.XML(const.gladeFile,"columns","gramps")
        self.top = self.glade.get_widget('columns')
        self.tree = self.glade.get_widget('list')
        self.arglist = arglist
        self.callback = callback

        self.model = gtk.ListStore(gobject.TYPE_BOOLEAN,
                                   gobject.TYPE_STRING,
                                   gobject.TYPE_INT)
        
        self.tree.set_model(self.model)

        checkbox = gtk.CellRendererToggle()
        checkbox.connect('toggled', self.toggled, self.model)
        renderer = gtk.CellRendererText()
        
        column_n = gtk.TreeViewColumn(_('Display'), checkbox, active=0)
        column_n.set_min_width(50)
        self.tree.append_column(column_n)

        column_n = gtk.TreeViewColumn(_('Column Name'),  renderer, text=1)
        column_n.set_min_width(225)
        self.tree.append_column(column_n)

        self.glade.get_widget('okbutton').connect('clicked',self.ok_clicked)
        self.glade.get_widget('cancelbutton').connect('clicked',self.cancel_clicked)

        for item in self.arglist:
            iter = self.model.append()
            self.model.set(iter,0,item[0],1,column_names[item[1]],2,item[1])

    def ok_clicked(self,obj):
        newlist = []
        for i in range(0,len(self.arglist)):
            iter = self.model.get_iter((int(i),))
            newlist.append((self.model.get_value(iter,0),
                            self.model.get_value(iter,2)))
        self.callback(newlist)
        self.top.destroy()

    def cancel_clicked(self,obj):
        self.top.destroy()

    def toggled(self, cell, path, model):
        iter = model.get_iter((int(path),))
        value = model.get_value(iter,0)
        value = not value
        model.set(iter,0,value)
