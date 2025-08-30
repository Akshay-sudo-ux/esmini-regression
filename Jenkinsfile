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
                // Add debugging echo to ensure we print the contents of the workspace
                script {
                    echo "Below is the content of the workspace:"
                }
                sh '''
                    # Debugging step to list files in the mounted workspace
                    echo "Listing the contents of /workspace inside the Docker container:"
                    ls -la /workspace

                    # Now run the regression.py script with the given config file
                    echo "Running regression.py with config file ${CONFIG_FILE}"
                    python3 /workspace/regression.py --config /workspace/${CONFIG_FILE}
                '''
            }
        }
        stage('Archive Logs') {
            steps {
                archiveArtifacts artifacts: 'logs/*.log', fingerprint: true
            }
        }
    }
}
