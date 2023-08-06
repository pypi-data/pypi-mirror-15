#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""AdventureDocs

Choose Your Own Adventure style software
documentation from markdown.

Use markdown files to represent a section of instructions,
and options to skip to a section, or just go to the next
section.

Load a directory of markdown files, which also includes a
file named ORDER which specifies the default order of the
markdown files. The ORDER enables us to have a "next
section" link per section (while you can still present
options to jump to other sections).

Usage:
    adocs <source> [<destination>]

"""

import os
import glob
import docopt
import markdown
import pkgutil

from adventuredocs import plugins
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


class Section(object):
    """"

    Attributes:
        index (int): --
        name (str): --
        path (str): --
        soup (BeautifulSoup): --

    """

    def __init__(self, index, name, path, soup):
        self.index = index
        self.name = name
        self.path = path
        self.soup = soup

    @property
    def contents(self):
        return self.soup.prettify()

    @classmethod
    def from_file(cls, section_index, path_to_markdown_file):
        """Create a section object by reading
        in a markdown file from path!

        Arguments:
            section_index (int):
            path_to_markdown_file (str): --

        Returns:
            Section

        """

        with open(path_to_markdown_file) as f:
            # markdown module strictly only
            # supports UTF-8
            file_contents = unicode(f.read(), 'utf-8')

        html = markdown.markdown(file_contents)
        section_soup = BeautifulSoup(html, "html.parser")

        # get the file name without the extension
        __, section_file_name = os.path.split(path_to_markdown_file)
        section_name, __ = os.path.splitext(section_file_name)

        return cls(index=section_index,
                   path=path_to_markdown_file,
                   soup=section_soup,
                   name=section_name)


class AdventureDoc(object):
    """A directory of markdown files, with an ORDER file.

    """

    SECTION_CHOICE_KEYWORD = "NEXT_SECTION:"
    TEMPLATE = pkgutil.get_data("adventuredocs", "layout.html")

    def __init__(self, sections):
        self.sections = sections

    def build(self):

        for section_soup in self.sections:
            section_soup = self.use_plugins(section_soup)

        # Use collected sections with jinja
        return (Environment().from_string(self.TEMPLATE)
                .render(title=u'AdventureDocs',
                        sections=self.sections)).encode('UTF-8')

    @staticmethod
    def get_sections(directory):
        """Collect the files specified in the
        ORDER file, returning a list of
        dictionary representations of each file.

        Returns:
            list[Section]: list of sections which

        """

        with open(os.path.join(directory, "ORDER")) as f:
            order_file_lines = f.readlines()

        ordered_section_file_paths = []

        for line_from_order_file in order_file_lines:
            section_path = os.path.join(directory, line_from_order_file)
            ordered_section_file_paths.append(section_path.strip())

        sections = []

        for i, section_file_path in enumerate(ordered_section_file_paths):
            sections.append(Section.from_file(i, section_file_path))

        return sections

    # NOTE: this currently actually changes the section's
    # beautiful soup but should make copy instead!
    def use_plugins(self, section):

        for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
            module_name = "adventuredocs.plugins." + module_name
            plugin = __import__(module_name, fromlist=["change_soup"])
            change_soup_function = getattr(plugin, "change_soup")
            plugin.change_soup(self, section)

        return section

    @classmethod
    def from_directory(cls, directory):
        ordered_sections = cls.get_sections(directory)

        return AdventureDoc(ordered_sections)


def main():
    arguments = docopt.docopt(__doc__)
    source_directory = arguments["<source>"]
    adoc = AdventureDoc.from_directory(source_directory)

    destination = arguments["<destination>"] or "adocs-output.html"

    with open(destination, 'w') as f:
        f.write(adoc.build())
