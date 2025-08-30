pipeline {
    agent {
        docker {
            image 'esmini-regression:latest'
            args '-v /tmp/logs:/workspace/logs -v ${WORKSPACE}:/workspace'  // Mounting the Jenkins workspace to /workspace inside the container
        }
    }
    parameters {
        string(name: 'CONFIG_FILE', defaultValue: 'configs/regression_highway.json', description: 'Regression config file')
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Akshay-sudo-ux/esmini-regression.git', branch: 'main'
            }
        }
        stage('Run Regression') {
            steps {
                // Running the regression with the correct config file path inside the container
                sh "python3 /workspace/regression.py --config /workspace/${CONFIG_FILE}"
            }
        }
        stage('Archive Logs') {
            steps {
                archiveArtifacts artifacts: 'logs/*.log', fingerprint: true
            }
        }
    }
}
