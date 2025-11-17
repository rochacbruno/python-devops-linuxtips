pipeline {
    agent any
    environment {
        PATH = "$HOME/.local/bin:$PATH"
        UV_UNMANAGED_INSTALL = "$HOME/.local/bin"
        PYTHON_VERSION = "3.13"
    }

    stages {

        stage('Setup') {
            steps {
                sh '''
                    mkdir -p $HOME/.local/bin
                    curl -LsSf https://astral.sh/uv/install.sh | sh
                    uv run --isolated python --version
                    uv --version
                '''
            }
        }

        stage('Load inner pipeline') {
            steps {
                dir('/var/jenkins_home/project') {
                    script {
                        load 'Jenkinsfile'
                    }
                }
            }
        }
    }
}
