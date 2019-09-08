"""
Live markdown viewer
"""
from argparse import ArgumentParser
from io import BytesIO
from time import sleep

import markdown
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser
from PyQt5.QtCore import QFileSystemWatcher, QFileInfo


class LiveMarkdownViewer(QApplication):
    """Live markdown viewer"""
    def __init__(self, filename):
        """
        Constructor
        :param str filename: The file to watch
        """
        super().__init__([])

        self.filename = filename
        self.setApplicationName('Live Markdown Viewer - {filename}'.format(filename=self.filename))

        self.window = QMainWindow()

        self.viewer = QTextBrowser()
        self.update_viewer()

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
        file_info = QFileInfo(path)

        time_slept = 0.0
        sleep_for = 0.1

        # Sleep up to 1 second while waiting for the file to be re-created
        while not file_info.exists() and time_slept < 1.0:
            time_slept += sleep_for
            sleep(sleep_for)

        if file_info.exists():
            self.watcher.addPath(path)

            self.update_viewer()
        else:
            # File deleted ?
            pass

    def render_to_html_string(self):
        """
        Render the watched document to html, returning the html string
        :return: The rendered HTML of the markdown file
        """
        fake_file = BytesIO()
        markdown.markdownFromFile(input=self.filename, output=fake_file)
        fake_file.seek(0)
        return str(fake_file.read(), 'utf-8')

    def update_viewer(self):
        """Update the viewer"""
        html = self.render_to_html_string()
        self.viewer.setHtml(html)


def main():
    """ main """
    argparser = ArgumentParser()
    argparser.add_argument('file', type=str, help='The markdown file to view')
    # TODO use the arguments in some way
    args = argparser.parse_args()

    lmv = LiveMarkdownViewer(args.file)
    lmv.exec()


if __name__ == '__main__':
    main()
