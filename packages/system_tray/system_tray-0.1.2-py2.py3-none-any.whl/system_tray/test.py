from __future__ import print_function
from __future__ import absolute_import

from timstools import ignored
import queue
import _thread as thread
import os
import time
import logging
from functools import partial
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gdk, GLib

def named_partial(func, *args, **kwargs):
        # attribute error because there is no
        # __name__ method found when using functools.partial,this resolves that
        name = func.__name__
        function = partial(func, *args, **kwargs)
        function.__name__ = name
        return function
class FormBuilder:
    # Returns values as one would expects, an interface for easier unpacking and len methods on results
    # Used by custom form and toolbar

    # First of all recognizes the need (or my lack of knowlegde on unpacking)
    # So if it is a single row will use that way to unpack, otherwise another
    # way for multilple row items

    # Encompasses two different build methods

    # The coloum is always returned (so that multiple items in rows can be
    # grided)

    def __init__(self, form):
        self.form = form

    def __iter__(self):
        for h, item in enumerate(self.form):
            if not isinstance(item[0], tuple):        # Single Row
                try:                                    # first way
                    # not sure why its not unpacking item properly.. have to
                    # put it in a list wf
                    for text, icon, command in ([item]):
                        yield(h, 0, text, icon, command)
                except ValueError as err:               # second way
                    for funct, text, dict_name, where, config in ([item]):
                        yield(h, 0, funct, text, dict_name, where, config)
            elif isinstance(item[0], tuple):  # Multi
                for j, *sub_items in enumerate(item):  # going over sub items
                    try:  # first way
                        for text, icon, command in sub_items:
                            yield(h, j, text, icon, command)
                    except ValueError as e:  # second way
                        if not 'too many' in str(e):
                            raise e
                        for funct, text, dict_name, where, config in sub_items:
                            yield(h, j, funct, text, dict_name, where, config)

class SystemTray():
    def __init__(self,
                 icon_file=None,
                 tooltip=None,
                 menu_options=None,
                 windows_lib='win32',
                 linux_lib='gtk',
                 gui_lib='tkinter',
                 error_on_no_icon=True,
                 consumer=None,
                 app=None
                 ):
        self.icon_file = icon_file
        self.tooltip = tooltip
        self.menu_options = menu_options
        self.error_on_no_icon = error_on_no_icon    # TBD this is fucking wtf
        self.consumer = consumer
        self.app = app
        
        self.start()
        
        self.tray_queue = queue.Queue()
        self._tray_consumer()
        self._setup_tray()
        
    def start(self):
        '''set variables here'''
        
    def _setup_tray(self):
        def _start_tray():
            try:
                aind = appindicator.Indicator.new(
                    'tim',
                    self.icon_file,
                    appindicator.IndicatorCategory.APPLICATION_STATUS)
                aind.set_status(appindicator.IndicatorStatus.ACTIVE)
                gtkmenu = gtk.Menu()
                if hasattr(self, 'shutdown'):
                    quitter = ('Quit', None, lambda e: self.shutdown()),
                    self.menu_options += quitter

                gtk_menu_items = []
                self.menu_options = FormBuilder(self.menu_options)
                for row, col, text, icon, command in self.menu_options: 
                    item = gtk.MenuItem(text)
                    gtk_menu_items.append(item)
                
                for item in gtk_menu_items:
                    gtkmenu.append(item)
                
                aind.set_menu(gtkmenu)
                
                for item in gtk_menu_items:
                    item.show()

                for item, options in zip(gtk_menu_items, self.menu_options):
                    self._connect_item(item, options[-1])
                # gtk.main()
                # Gdk.threads_leave()
            except TypeError:
                pass
        _start_tray()
        gtk.main()
        Gdk.threads_leave()
        # thread.start_new_thread(_start_tray, ())

    def _connect_item(self, item, command):
        def func(menu_item):
            self.tray_queue.put(named_partial(command, menu_item))
        item.connect('activate', func)
    
    def _tray_consumer(self):
        def threaded_consumer(): 
            if callable(self.consumer):
                while 1:
                    try:
                        data = self.tray_queue.get(block=True)
                    except queue.Empty:
                        pass
                    else:
                        thread.start_new_thread(self.consumer, (data,))
            else:
                while 1:
                    try:
                        data = self.tray_queue.get(block=True)
                    except queue.Empty:
                        pass
                    else:
                        thread.start_new_thread(data, (),)
                time.sleep(0.01)
        thread.start_new_thread(threaded_consumer, ())


if __name__ == '__main__':
    import platform
    
    def setup_logger(log_file):
        '''One function call to set up logging with some nice logs about the machine'''
        
        logging.basicConfig(filename=log_file,
                            filemode='w',
                            level=logging.DEBUG,
                            format='%(asctime)s:%(levelname)s: %(message)s')    # one run

    setup_logger('system_tray.log')

    ICON_FILE = os.path.join(os.getcwd(), 'mario.ico')      # on windows doesn't ahve to be with getcwd(), but on linux yes...
    TOOLTIP = 'testing_tooltip'
    
    def dodo():
        time.sleep(5)
        print('done')
    MENU_OPTIONS = (('ass', None, lambda menu_item: print(menu_item)),
                    ('do', None, lambda menu_item: print(menu_item)),
                    ('aa', None, lambda menu_item: dodo()))

    def consumer(callback):
        print('custom consumer', callback)
        callback()

    sys_tray = SystemTray(
        ICON_FILE,
        TOOLTIP,
        menu_options=MENU_OPTIONS,
        consumer=consumer,
        error_on_no_icon=True)


    while True:
        pass

# References
# Taskbar Https://bbs.archlinux.org/viewtopic.php?id=121303
# http://standards.freedesktop.org/systemtray-spec/systemtray-spec-0.2.html
# http://www.perlmonks.org/?node_id=626617
# Gdk.threads_enter()
# GLib.threads_init()
# Gdk.threads_init()
# Gdk.threads_enter()

