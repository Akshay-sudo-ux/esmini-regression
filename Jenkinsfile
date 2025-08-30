pipeline {
    agent none  // Don't specify an agent here
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
                script {
                    def configFile = params.CONFIG_FILE
                    sh """
                        docker run -t -d -u 1000:1000 -v /tmp/logs:/workspace/logs -w /var/jenkins_home/workspace/esmini-regression \
                        --volumes-from ${env.DOCKER_CONTAINER_ID} \
                        esmini-regression:latest --config ${configFile}
                    """
                }
            }
        }
        stage('Archive Logs') {
            steps {
                archiveArtifacts artifacts: 'logs/*.log', fingerprint: true
            }
        }
    }
}

