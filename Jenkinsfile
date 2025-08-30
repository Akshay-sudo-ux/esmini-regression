pipeline {
    agent none  // No global agent, we'll specify in the stages
    
    parameters {
        string(name: 'CONFIG_FILE', defaultValue: 'configs/regression_highway.json', description: 'Regression config file')
    }
    
    stages {
        stage('Checkout') {
            agent any  // Use any available agent for this stage
            steps {
                git url: 'https://github.com/Akshay-sudo-ux/esmini-regression', branch: 'main'
            }
        }
        
        stage('Run Regression') {
            agent any  // Use any available agent for this stage
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
            agent any  // Use any available agent for this stage
            steps {
                archiveArtifacts artifacts: 'logs/*.log', fingerprint: true
            }
        }
    }
}
