#!/bin/bash

cd ${BASE_DIR} && python -m pylint --rcfile .pylintrc live_markdown_viewer
