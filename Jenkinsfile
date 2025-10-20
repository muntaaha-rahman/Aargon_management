pipeline {
    agent any
    
    environment {
        REMOTE_USER = 'deployer'
        REMOTE_HOST = '10.220.220.100'
        PROJECT_PATH = '/var/www/aargon_management'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/muntaaha-rahman/Aargon_management.git',
                credentialsId: 'your-github-credentials'
            }
        }
        
        stage('Deploy to Server') {
            steps {
                sshagent(['your-ssh-credentials']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} '
                            cd ${PROJECT_PATH}
                            docker-compose down
                            git pull origin main
                            docker-compose up -d --build
                            docker system prune -f
                        '
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo 'Deployment completed successfully!'
        }
        failure {
            echo 'Deployment failed! Check logs above.'
        }
    }
}