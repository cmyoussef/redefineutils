#!/usr/bin/env python3

import filecmp
import json
import os
from shutil import copy2

from PySide2 import QtWidgets, QtCore


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Directory Sync Tool'
        self.source_dir = ''
        self.target_dir = ''
        self.config_path = os.path.expanduser('~/.sync_config.json')

        self.layout = QtWidgets.QVBoxLayout()

        source_layout = QtWidgets.QHBoxLayout()
        source_label = QtWidgets.QLabel('Source:')
        self.source_dir_line = QtWidgets.QLineEdit()
        self.source_dir_button = QtWidgets.QPushButton('<')
        self.source_dir_button.clicked.connect(self.load_source_directory)
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_dir_line)
        source_layout.addWidget(self.source_dir_button)
        self.layout.addLayout(source_layout)

        target_layout = QtWidgets.QHBoxLayout()
        target_label = QtWidgets.QLabel('Target:')
        self.target_dir_line = QtWidgets.QLineEdit()
        self.target_dir_button = QtWidgets.QPushButton('<')
        self.target_dir_button.clicked.connect(self.load_target_directory)
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.target_dir_line)
        target_layout.addWidget(self.target_dir_button)
        self.layout.addLayout(target_layout)

        self.ext_filter_line = QtWidgets.QLineEdit('py,json')  # default filter for .py and .json files
        self.layout.addWidget(self.ext_filter_line)

        self.match_button = QtWidgets.QPushButton('Find Matching Files')
        self.match_button.clicked.connect(self.populate_tree)
        self.layout.addWidget(self.match_button)

        self.file_tree = QtWidgets.QTreeWidget()
        self.file_tree.setHeaderLabels(['File', 'Discard'])  # Two columns, one for file path, one for checkbox
        self.layout.addWidget(self.file_tree)

        self.sync_button = QtWidgets.QPushButton('Synchronize Directories')
        self.sync_button.clicked.connect(self.sync_directories)

        self.setLayout(self.layout)
        self.layout.addWidget(self.sync_button)  # Sync button moved to the end

        self.load_config()

    def load_source_directory(self):
        self.source_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        self.source_dir_line.setText(self.source_dir)

    def load_target_directory(self):
        self.target_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Target Directory')
        self.target_dir_line.setText(self.target_dir)

    def populate_tree(self):
        self.file_tree.clear()
        ext_filter = self.ext_filter_line.text().split(',')

        for root, dirs, files in os.walk(self.source_dir):
            for filename in files:
                if filename.split('.')[-1] in ext_filter:  # only add files with the correct extension
                    relative_path = os.path.relpath(os.path.join(root, filename), self.source_dir)
                    target_file = os.path.join(self.target_dir, relative_path)
                    if os.path.isfile(target_file):
                        item = QtWidgets.QTreeWidgetItem(self.file_tree)
                        item.setText(0, relative_path)  # File path in first column
                        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                        item.setCheckState(1, QtCore.Qt.Unchecked)  # Checkbox in second column

                        if filecmp.cmp(os.path.join(root, filename), target_file, shallow=False):
                            item.setBackground(0,
                                               QtCore.Qt.green)  # set background color to green if files are identical

    def sync_directories(self):
        for index in range(self.file_tree.topLevelItemCount()):
            item = self.file_tree.topLevelItem(index)
            if item.checkState(1) != QtCore.Qt.Checked:  # Skip file if checkbox is checked (file is to be discarded)
                relative_path = item.text(0)
                source_file = os.path.join(self.source_dir, relative_path)
                target_file = os.path.join(self.target_dir, relative_path)
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                copy2(source_file, target_file)

        self.save_config()

    def save_config(self):
        config = {
            'source_dir': self.source_dir,
            'target_dir': self.target_dir,
            'ignored_files': [self.file_tree.topLevelItem(index).text(0) for index in
                              range(self.file_tree.topLevelItemCount()) if
                              self.file_tree.topLevelItem(index).checkState(1) == QtCore.Qt.Checked],
            # Checkbox in second column
            'ext_filter': self.ext_filter_line.text()
        }
        with open(self.config_path, 'w') as config_file:
            json.dump(config, config_file)

    def load_config(self):
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as config_file:
                config = json.load(config_file)
                self.source_dir = config['source_dir']
                self.target_dir = config['target_dir']
                self.ext_filter_line.setText(config['ext_filter'])
                self.source_dir_line.setText(self.source_dir)
                self.target_dir_line.setText(self.target_dir)
                self.populate_tree()
                for index in range(self.file_tree.topLevelItemCount()):
                    item = self.file_tree.topLevelItem(index)
                    if item.text(0) in config['ignored_files']:
                        item.setCheckState(1, QtCore.Qt.Checked)  # Checkbox in second column
                    else:
                        item.setCheckState(1, QtCore.Qt.Unchecked)  # Checkbox in second column


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ex = App()
    ex.show()
    app.exec_()
