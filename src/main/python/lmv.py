"""
Live markdown viewer
"""
from argparse import ArgumentParser
from io import BytesIO
import logging
from time import sleep

from fbs_runtime.application_context.PyQt5 import ApplicationContext
import markdown
from markdown.extensions import (abbr, admonition, attr_list, codehilite, def_list, extra, fenced_code, footnotes,
                                 legacy_attrs, legacy_em, meta, nl2br, sane_lists, smarty, tables, toc, wikilinks)
from PyQt5.QtWidgets import QMainWindow, QTextBrowser
from PyQt5.QtCore import QFileSystemWatcher, QFileInfo


class LiveMarkdownViewer:
    """Live markdown viewer"""
    def __init__(self, filename, app, logger):
        """
        Constructor
        :param str filename: The file to watch
        """
        self.logger = logger

        self.filename = filename
        app.setApplicationName('Live Markdown Viewer - {filename}'.format(filename=self.filename))

        self.window = QMainWindow()

        self.logger.debug('Creating viewer component')
        self.viewer = QTextBrowser()
        self.update_viewer()

        self.logger.debug('Creating file watcher')
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.filename)
        self.watcher.fileChanged.connect(self._file_change_handler)

        self.window.setCentralWidget(self.viewer)
        self.window.show()

    def _file_change_handler(self, path):
        """
        https://stackoverflow.com/a/30076119
        Some text editors delete and re-write the file when they save. When the file is deleted, Qt will stop
        watching it. To get around this, we can wait a short time to see if the file returns.
        :param str path: The path of the changed file.
        """
        self.logger.debug('File changed (%s)', path)
        file_info = QFileInfo(path)

        time_slept = 0.0
        sleep_for = 0.1

        # Sleep up to 1 second while waiting for the file to be re-created
        while not file_info.exists() and time_slept < 1.0:
            self.logger.debug('File deleted... waiting (%s)', path)
            time_slept += sleep_for
            sleep(sleep_for)

        if file_info.exists():
            self.logger.debug('File exists (%s)', path)
            self.watcher.addPath(path)

            self.update_viewer()
        else:
            # File deleted ?
            self.logger.debug('File deleted, not re-adding watcher (%s)', path)

    def render_to_html_string(self):
        """
        Render the watched document to html, returning the html string
        :return: The rendered HTML of the markdown file
        """
        self.logger.debug('Rendering markdown (%s)', self.filename)
        fake_file = BytesIO()
        markdown.markdownFromFile(input=self.filename,
                                  output=fake_file,
                                  extensions=[abbr.AbbrExtension(), admonition.AdmonitionExtension(),
                                              attr_list.AttrListExtension(), codehilite.CodeHiliteExtension(),
                                              def_list.DefListExtension(), extra.ExtraExtension(),
                                              fenced_code.FencedCodeExtension(), footnotes.FootnoteExtension(),
                                              legacy_attrs.LegacyAttrExtension(), legacy_em.LegacyEmExtension(),
                                              meta.MetaExtension(), nl2br.Nl2BrExtension(),
                                              sane_lists.SaneListExtension(), smarty.SmartyExtension(),
                                              tables.TableExtension(), toc.TocExtension(),
                                              wikilinks.WikiLinkExtension()])
        fake_file.seek(0)
        return str(fake_file.read(), 'utf-8')

    def update_viewer(self):
        """Update the viewer"""
        self.logger.debug('Updating viewer')
        html = self.render_to_html_string()

        self.viewer.setHtml(html)


def main():
    """ main """
    argparser = ArgumentParser()
    argparser.add_argument('file', type=str, help='The markdown file to view')
    argparser.add_argument('-v', '--verbose', action='store_true', help='Verbose logging')
    # TODO use the arguments in some way
    args = argparser.parse_args()
    logger = logging.getLogger("Live markdown viewer")
    logger.setLevel(level=logging.DEBUG if args.verbose else logging.INFO)
    logger.addHandler(logging.StreamHandler())

    logger.debug('Initializing Qt')
    app_ctx = ApplicationContext()

    logger.debug('Initializing lmv')
    _lmv = LiveMarkdownViewer(args.file, app_ctx.app, logger)

    logger.debug('Opening window')
    exit_code = app_ctx.app.exec_()
    exit(exit_code)


if __name__ == '__main__':
    main()
