#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Copyright (c) 2014+ Raphaël Seban <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

# lib imports

from tkinter import ttk

import tkRAD

from tkRAD.core import tools



class GameScrollView (tkRAD.RADXMLFrame):
    r"""
        Scrollable viewport widget component;
    """

    def _get_scroll_step (self, step=None):
        r"""
            ensures a non-zero scrolling step;
        """

        return max(1, abs(tools.ensure_int(step)))

    # end def



    def _update_scrollregion (self):

        self.viewport.configure(scrollregion=self.viewport.bbox("all"))

    # end def



    def init_widget (self, **kw):
        r"""
            widget main inits;
        """

        # XML source code

        _xml = """
            <tkwidget>
                <canvas
                    id="CanvasViewport"
                    bd="0"
                    layout="grid"
                    layout_options="row=0, column=0"
                    resizable="yes"
                />
                <ttkscrollbar
                    connect="CanvasViewport"
                    orient="vertical"
                    layout="grid"
                    layout_options="row=0, column=1"
                    resizable="height"
                />
                <ttkscrollbar
                    connect="CanvasViewport"
                    orient="horizontal"
                    layout="grid"
                    layout_options="row=1, column=0"
                    resizable="width"
                />
            </tkwidget>
        """

        # build GUI

        _frame = tkRAD.RADXMLFrame(self)        # because of subclasses!

        _frame.xml_build(tools.choose_str(kw.get("xml"), _xml))

        _frame.pack(expand=1, fill="both")

        # get viewport canvas object

        self.viewport = _frame.get_object_by_id("CanvasViewport")

        # set viewport's widget container

        self.viewport.container = ttk.Frame(self.viewport)

        # add container to canvas

        self.viewport.container_id = self.viewport.create_window(

            0, 0,

            anchor="nw",

            window=self.viewport.container,
        )

        # connect events

        self.events.connect_dict(
            {
                "MouseWheelScrollDown": self.slot_mouse_scrolldown,

                "MouseWheelScrollUp": self.slot_mouse_scrollup,
            }
        )

        # bind tkevents

        self.viewport.bind("<Configure>", self.slot_viewport_changed)

        self.viewport.container.bind(

            "<Configure>", self.slot_container_changed
        )

    # end def



    def slot_container_changed (self, tkevent=None, *args, **kw):
        r"""
            viewport's frame container has changed (size, ...);
        """

        # inits

        self._update_scrollregion()

    # end def



    def slot_mouse_scrolldown (self, tkevent=None, *args, **kw):
        r"""
            mouse events scroll down;
        """

        _step = self._get_scroll_step(kw.get("step"))

        self.viewport.yview_scroll(_step, "units")

    # end def



    def slot_mouse_scrollup (self, tkevent=None, *args, **kw):
        r"""
            mouse events scroll up;
        """

        _step = self._get_scroll_step(kw.get("step"))

        self.viewport.yview_scroll(-_step, "units")

    # end def



    def slot_viewport_changed (self, tkevent=None, *args, **kw):
        r"""
            viewport canvas has changed (size, others...);
        """

        # inits

        self._update_scrollregion()

    # end def


# end class
