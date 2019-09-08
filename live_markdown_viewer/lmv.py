"""
Live markdown viewer
"""
from argparse import ArgumentParser
from io import BytesIO

import markdown
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextBrowser
from PyQt5.QtCore import QFileSystemWatcher

class LiveMarkdownViewer:
    """Live markdown viewer"""
    def __init__(self, filename):
        """
        Constructor
        :param str filename: The file to watch
        """
        self.filename = filename

    def render_to_html_string(self):
        """
        Render the watched document to html, returning the html string
        :return: The rendered HTML of the markdown file
        """
        fake_file = BytesIO()
        markdown.markdownFromFile(input=self.filename, output=fake_file)
        fake_file.seek(0)
        return str(fake_file.read(), 'utf-8')

    def update_preview(self):
        html = self.render_to_html_string()

    def run_app(self):
        app = QApplication([])
        app.setApplicationName('Live Markdown Viewer - {filename}'.format(filename=self.filename))
        window = QMainWindow()

        viewer = QTextBrowser()
        viewer.setHtml(self.render_to_html_string())

        window.setCentralWidget(viewer)
        window.show()
        app.exec_()


def main():
    """ main """
    argparser = ArgumentParser()
    argparser.add_argument('file', type=str, help='The markdown file to view')
    # TODO use the arguments in some way
    args = argparser.parse_args()

    lmv = LiveMarkdownViewer(args.file)
    lmv.run_app()


if __name__ == '__main__':
    main()
