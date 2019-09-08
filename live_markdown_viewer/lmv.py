"""
Live markdown viewer
"""
from argparse import ArgumentParser

import markdown


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
        return markdown.markdownFromFile(input=self.filename)


def main():
    """ main """
    argparser = ArgumentParser()
    argparser.add_argument('file', type=str, help='The markdown file to view')
    # TODO use the arguments in some way
    args = argparser.parse_args()

    lmv = LiveMarkdownViewer(args.file)
    print(lmv.render_to_html_string())


if __name__ == '__main__':
    main()
