# -*- coding: UTF-8 -*-

import sublime
import sublime_plugin
import os
import re
import time
import threading
import plantuml_connection

from debug_tools import getLogger
log = getLogger(1, __package__)

try:
    from .diagram import setup, process
except ValueError:
    from diagram import setup, process

try:
    all_views_active
except NameError:
    all_views_active = {}


def process_diagram_image(view):
    all_views_active[view.id()] = view
    view.set_status(view.file_name(), "Generating diagrams from '%s'..." % view.file_name())

    try:
        if not process(view):
            sublime.error_message("No diagrams found, nothing to process.")
    except plantuml_connection.PlantUMLSyntaxError as error:
        # TODO show syntax error use mdpop
        sublime.error_message("Syntax error on diagram: %s",
            re.findall(r'X-PlantUML-Diagram-Description:((?:.|\n)*?)X-Powered-By', str(error)))
    finally:
        view.erase_status(view.file_name())


class DisplayDiagramsContinuallyEventListener(sublime_plugin.ViewEventListener):
    def on_modified_async(self):
        if self.view.id() not in all_views_active:
            return
        process_diagram_image(self.view)


class DisplayDiagrams(sublime_plugin.TextCommand):
    def run(self, edit):
        process_diagram_image(self.view)

    def isEnabled(self):
        return True


if sublime.version()[0] == '2':
    setup()
else:
    def plugin_loaded():
        """Sublime Text 3 callback to do after-loading initialization"""
        try:
            setup()
        except Exception as error:
            print("Unable to load diagram plugin, check console for details.\n\n%s" % error)
            raise