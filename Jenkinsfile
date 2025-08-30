pipeline {
    agent any
    
    parameters {
        string(name: 'CONFIG_FILE', defaultValue: 'configs/regression_highway.json', description: 'Regression config file')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Akshay-sudo-ux/esmini-regression', branch: 'main'
            }
        }

        stage('Run Regression') {
            steps {
                script {
                    def configFile = params.CONFIG_FILE
                    sh """
                        docker run -t -d -u 1000:1000 -v /tmp/logs:/workspace/logs -w /var/jenkins_home/workspace/esmini-regression \
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
