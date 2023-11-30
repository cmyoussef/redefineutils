import sys
from PySide2 import QtWidgets
from git import Repo
import subprocess
from urllib.parse import quote


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
        # self.token_input.setText('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')
        self.token_input.setText('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')


        self.pull_button = QtWidgets.QPushButton('Pull')
        self.pull_button.clicked.connect(self.git_pull)

        self.push_button = QtWidgets.QPushButton('Push')
        self.push_button.clicked.connect(self.git_push)

        self.repo_path_label = QtWidgets.QLabel('Local Repository Path:')
        self.repo_path_input = QtWidgets.QLineEdit()
        self.repo_path_input.setText('/hosts/mtlws1546/user_data/mahy/git/stash/nuke-sd/src/nukesd')
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

        try:
            # Encodes username and token to ensure they are URL safe
            encoded_username = quote(username, safe='')
            encoded_token = quote(token, safe='')
            
            # Forming the git pull command with the encoded credentials
            pull_command = f"git pull https://{encoded_username}:{encoded_token}@{repo_url.split('https://')[1]}"
            
            result = subprocess.run(pull_command, shell=True, cwd=local_repo_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                QtWidgets.QMessageBox.information(self, "Success", "Successfully pulled the latest updates.")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", result.stderr)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))



    def git_push(self):
        repo_url = self.repo_url_input.text()
        username = self.username_input.text()
        token = self.token_input.text()
        local_repo_path = self.repo_path_input.text()
        commit_message = "Auto commit message"

        try:
            repo = Repo(local_repo_path)

            # Stage all changes
            repo.git.add('--all')

            # Commit changes
            repo.git.commit('-m', commit_message)

            # URL-encode the token and username
            encoded_username = quote(username, safe='')
            encoded_token = quote(token, safe='')

            # Form the git URL including the token and username
            git_url_with_token = f"https://{encoded_username}:{encoded_token}@{repo_url.split('https://')[1]}"

            # Check if 'origin' remote exists, else create
            if 'origin' in [remote.name for remote in repo.remotes]:
                remote = repo.remote('origin')
                remote.set_url(git_url_with_token)
            else:
                remote = repo.create_remote('origin', git_url_with_token)

            # Push changes
            remote.push()

            QtWidgets.QMessageBox.information(self, "Success", "Successfully pushed to the repository.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = GitUI()
    ex.show()
    sys.exit(app.exec_())

"""
bob-world -t python3.9;
python /hosts/mtlws1546/user_data/mahy/git/stash/redefineutils/git/token_pull.py
"""

