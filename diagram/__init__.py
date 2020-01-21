#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from __future__ import absolute_import

import sublime
from .plantuml import PlantUMLProcessor
from debug_tools import getLogger
from threading import Thread

import sys

log = getLogger(__name__)

AVAILABLE_PROCESSORS = [PlantUMLProcessor]
ACTIVE_UML_PROCESSORS = []


def setup():
    log._debug_level = 1
    sublime_settings = sublime.load_settings("PlantUmlDiagrams.sublime-settings")
    _load_preprocessor(sublime_settings)


def _load_preprocessor(sublime_settings):
    global ACTIVE_UML_PROCESSORS
    ACTIVE_UML_PROCESSORS = []

    def load_preprocessor(plantuml_processor):
        try:
            log(4, "Loading plantuml_processor class: %s", plantuml_processor)
            proc = plantuml_processor()
            proc.OUTPUT_FORMAT = sublime_settings.get('output_format', 'png')
            proc.load()

            ACTIVE_UML_PROCESSORS.append(proc)
            log(4, "Loaded plantuml_processor: %s", proc)
            return True
        except Exception as error:
            log(1, "Unable to load plantuml_processor: %s, %s", plantuml_processor, error)
        return False

    for plantuml_processor in AVAILABLE_PROCESSORS:
        if load_preprocessor(plantuml_processor):
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


def render_and_view(source_view, sourceFile, diagrams):
    sequence = [0]
    diagram_files = []

    for plantuml_processor, text_blocks in diagrams:
        source_view.set_status(str(source_view.id()), "Generating diagrams from '%s'..." % sourceFile)
        diagram_file = plantuml_processor.process(sourceFile, text_blocks, sequence)
        source_view.erase_status(str(source_view.id()))
        diagram_files.extend(diagram_file)
        sequence[0] += 1

    if diagram_files:
        diagram_files = list(filter(lambda x: x, diagram_files))
        names = [d.name for d in diagram_files if d]
        for diagram_file in diagram_files:
            render_view = sublime.active_window().open_file(diagram_file.name)
            sublime.active_window().focus_view(source_view)
    else:
        sublime.error_message("No diagrams generated...")
