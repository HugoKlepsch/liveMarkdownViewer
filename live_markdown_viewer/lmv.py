"""
Live markdown viewer
"""
from argparse import ArgumentParser
from io import BytesIO

import markdown
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser


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

        self.window.setCentralWidget(self.viewer)
        self.window.show()

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
