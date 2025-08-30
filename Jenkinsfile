pipeline {
    agent {
        docker {
            image 'esmini-regression:latest'
            args '-v /tmp/logs:/workspace/logs'
        }
    }
    parameters {
        string(name: 'CONFIG_FILE', defaultValue: 'configs/regression_highway.json', description: 'Regression config file')
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/<your-username>/esmini-regressions.git', branch: 'main'
            }
        }
        stage('Run Regression') {
            steps {
                sh "python3 regression.py --config ${CONFIG_FILE}"
            }
        }
        stage('Archive Logs') {
            steps {
                archiveArtifacts artifacts: 'logs/*.log', fingerprint: true
            }
        }
    }
}

