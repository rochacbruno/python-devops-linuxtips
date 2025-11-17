pipeline {
    agent any
    environment {
        PATH = "$HOME/.local/bin:$PATH"
        UV_UNMANAGED_INSTALL = "$HOME/.local/bin"
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

        stage('Matrix build') {
            matrix {
                axes {
                    axis {
                        name 'PYTHON_VERSION'
                        values '3.13', '3.14'
                    }
                }

                stages {
                    stage('Load inner pipeline') {
                        steps {
                            dir('/var/jenkins_home/project') {
                                script {
                                    echo "Running with Python ${PYTHON_VERSION}"
                                    load 'Jenkinsfile'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

