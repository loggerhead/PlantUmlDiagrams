#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from __future__ import absolute_import

import sublime
from .plantuml import PlantUMLProcessor
from debug_tools import getLogger
from threading import Thread

import sys

log = getLogger(__name__)
INITIALIZED = False

AVAILABLE_PROCESSORS = [PlantUMLProcessor]
ACTIVE_UML_PROCESSORS = []


def setup():
    global INITIALIZED
    sublime_settings = sublime.load_settings("PlantUmlDiagrams.sublime-settings")

    log._debug_level = 1 + sublime_settings.get('check_on_startup', 0)
    _load_preprocessor(sublime_settings)

    INITIALIZED = True
    log(4, "Processors: %s", ACTIVE_UML_PROCESSORS)


def _load_preprocessor(sublime_settings):
    global ACTIVE_UML_PROCESSORS
    ACTIVE_UML_PROCESSORS = []

    def load_preprocessor():
        try:
            log(4, "Loading plantuml_processor class: %s", plantuml_processor)
            proc = plantuml_processor()
            proc.CHARSET = sublime_settings.get('charset', None)
            proc.CHECK_ON_STARTUP = sublime_settings.get('check_on_startup', 1)
            proc.NEW_FILE = sublime_settings.get('new_file', True)
            proc.OUTPUT_FORMAT = sublime_settings.get('output_format', 'png')
            proc.load()

            ACTIVE_UML_PROCESSORS.append(proc)
            log(4, "Loaded plantuml_processor: %s", proc)
            return True
        except Exception as error:
            log(1, "Unable to load plantuml_processor: %s, %s", plantuml_processor, error)
        return False

    for plantuml_processor in AVAILABLE_PROCESSORS:
        if load_preprocessor():
            break

    if not ACTIVE_UML_PROCESSORS:
        log(1, 'PlantUMLDiagrams: ERROR, no working processors found!' )


def process(view):
    diagrams = []

    for plantuml_processor in ACTIVE_UML_PROCESSORS:
        log(4, "plantuml_processor %s", plantuml_processor)
        text_blocks = []
        for text_block in plantuml_processor.extract_blocks(view):
            text_blocks.append(view.substr(text_block))
        if text_blocks:
            diagrams.append((plantuml_processor, text_blocks))

    if not diagrams:
        return False

    sourceFile = view.file_name()
    t = Thread(target=render_and_view, args=(view, sourceFile, diagrams))
    t.daemon = True
    t.start()
    return True


def render_and_view(view, sourceFile, diagrams):
    # log(1, "Rendering %s", diagrams)
    sequence = [0]
    diagram_files = []

    for plantuml_processor, text_blocks in diagrams:
        diagram_files.extend(plantuml_processor.process(sourceFile, text_blocks, sequence))
        sequence[0] += 1

    if diagram_files:
        names = [d.name for d in diagram_files if d]
        for diagram_file in diagram_files:
            sublime.active_window().open_file(diagram_file.name)
            sublime.active_window().focus_view(view)
    else:
        sublime.error_message("No diagrams generated...")
