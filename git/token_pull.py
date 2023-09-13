import sys
from PySide2 import QtWidgets
from git import Repo


class GitUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout()

        self.repo_url_label = QtWidgets.QLabel('Repository URL:')
        self.repo_url_input = QtWidgets.QLineEdit()
        self.repo_url_input.setText(r'https://github.com/cmyoussef/nukesd.git')

        self.username_label = QtWidgets.QLabel('Username:')
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setText('cmyoussef')

        self.token_label = QtWidgets.QLabel('Personal Access Token:')
        self.token_input = QtWidgets.QLineEdit()
        self.token_input.setText('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')

        self.pull_button = QtWidgets.QPushButton('Pull')
        self.pull_button.clicked.connect(self.git_pull)

        self.push_button = QtWidgets.QPushButton('Push')
        self.push_button.clicked.connect(self.git_push)

        self.repo_path_label = QtWidgets.QLabel('Local Repository Path:')
        self.repo_path_input = QtWidgets.QLineEdit()
        self.repo_path_button = QtWidgets.QPushButton('<')
        self.repo_path_button.clicked.connect(self.load_directory)

        self.layout.addWidget(self.repo_path_label)
        self.layout.addWidget(self.repo_path_input)
        self.layout.addWidget(self.repo_path_button)

        self.layout.addWidget(self.repo_url_label)
        self.layout.addWidget(self.repo_url_input)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.token_label)
        self.layout.addWidget(self.token_input)
        self.layout.addWidget(self.pull_button)
        self.layout.addWidget(self.push_button)

        self.setLayout(self.layout)

    def load_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a directory')
        if directory:
            self.repo_path_input.setText(directory)

    def git_pull(self):
        repo_url = self.repo_url_input.text()
        username = self.username_input.text()
        token = self.token_input.text()
        local_repo_path = self.repo_path_input.text()

        full_repo_url = f"https://{username}@{repo_url.split('https://')[1]}"

        repo = Repo.clone_from(full_repo_url, local_repo_path, env={'GIT_ASKPASS': token})
        repo.git.pull()

    def git_push(self):
        repo_url = self.repo_url_input.text()
        username = self.username_input.text()
        token = self.token_input.text()
        local_repo_path = self.repo_path_input.text()

        full_repo_url = f"https://{username}@{repo_url.split('https://')[1]}"

        repo = Repo(local_repo_path)
        remote = repo.create_remote('origin', full_repo_url)
        repo.git.push(env={'GIT_ASKPASS': token})


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = GitUI()
    ex.show()
    sys.exit(app.exec_())
