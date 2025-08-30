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
                echo "Jenkins workspace: ${env.WORKSPACE}"
                git url: 'https://github.com/Akshay-sudo-ux/esmini-regression.git', branch: 'main'
                sh 'ls -la ${env.WORKSPACE}'  // Check if files are available
            }
        }
        stage('Verify Workspace Content') {
            steps {
                echo "Below is the content of the workspace:"
                sh 'ls -la ${env.WORKSPACE}'  // Verify contents again inside container
            }
        }
        stage('Run Regression') {
            steps {
                echo "Running regression with config: ${params.CONFIG_FILE}"
                sh "python3 regression.py --config ${params.CONFIG_FILE}"
            }
        }
        stage('Archive Logs') {
            steps {
                archiveArtifacts artifacts: 'logs/*.log', fingerprint: true
            }
        }
    }
}
