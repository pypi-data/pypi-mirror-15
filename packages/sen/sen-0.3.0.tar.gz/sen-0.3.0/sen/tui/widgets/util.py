import logging
import threading

import urwid

from sen.docker_backend import RootImage
from sen.tui.widgets.list.util import get_map


logger = logging.getLogger(__name__)


class AdHocAttrMap(urwid.AttrMap):
    """
    Ad-hoc attr map change

    taken from https://github.com/pazz/alot/
    """
    def __init__(self, w, maps, init_map='normal'):
        self.maps = maps
        urwid.AttrMap.__init__(self, w, maps[init_map])
        if isinstance(w, urwid.Text):
            self.attrs = [x[0] for x in self.original_widget.get_text()[1]]

    def set_map(self, attrstring):
        attr_map = {None: self.maps[attrstring]}

        # for urwid.Text only: do hovering for all markups in the widget
        if isinstance(self.original_widget, urwid.Text):
            if attrstring == "normal":
                for a in self.attrs:
                    attr_map[self.maps["focus"]] = a
            elif attrstring == "focus":
                for a in self.attrs:
                    attr_map[a] = self.maps["focus"]
        self.set_attr_map(attr_map)


def get_basic_image_markup(docker_image):
    if isinstance(docker_image, RootImage):
        return [str(docker_image)]

    text_markup = [docker_image.short_id]

    if docker_image.names:
        text_markup.append(" ")
        text_markup.append(("main_list_lg", docker_image.names[0].to_str()))

    text_markup.append(" ")
    text_markup.append(("main_list_ddg", docker_image.container_command))

    return text_markup


def get_container_status_markup(docker_container):
    if docker_container.running:
        attr_map = get_map("main_list_green")
    elif docker_container.exited_well:
        attr_map = get_map("main_list_orange")
    elif docker_container.status_created:
        attr_map = get_map("main_list_yellow")
    else:
        attr_map = get_map("main_list_red")
    return docker_container.status, attr_map


def get_basic_container_markup(docker_container):
    text_markup = [docker_container.short_id, " "]

    markup, attr = get_container_status_markup(docker_container)
    text_markup.append((attr["normal"], markup))

    if docker_container.names:
        text_markup.append(" ")
        text_markup.append(("main_list_lg", docker_container.names[0]))

    return text_markup


class ColorTextMixin:
    @property
    def text(self):
        return self.original_widget.text

    @text.setter
    def text(self, value):
        self.original_widget.set_text(value)

    def keypress(self, size, key):
        """ get rid of tback: `AttributeError: 'Text' object has no attribute 'keypress'` """
        return key


class ColorText(ColorTextMixin, urwid.AttrMap):
    def __init__(self, text, color):
        super().__init__(urwid.Text(text, align="left", wrap="clip"), color)


class SelectableText(ColorTextMixin, AdHocAttrMap):
    def __init__(self, text, maps=None):
        maps = maps or get_map()
        super().__init__(urwid.Text(text, align="left", wrap="clip"), maps)


class ThreadSafeFrame(urwid.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_lock = threading.Lock()

    def set_body(self, body):
        with self.update_lock:
            return super().set_body(body=body)

    def set_footer(self, footer):
        with self.update_lock:
            return super().set_footer(footer=footer)

    def set_header(self, header):
        with self.update_lock:
            return super().set_header(header=header)

    def render(self, size, focus=False):
        with self.update_lock:
            return super().render(size=size, focus=focus)


class UnselectableListBox(urwid.ListBox):
    _selectable = False
