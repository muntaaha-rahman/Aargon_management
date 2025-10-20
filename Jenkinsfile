pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = ''  // Leave empty for local builds, or add Docker Hub/registry
        IMAGE_NAME = 'aargon-management'
        REMOTE_USER = 'deployer'
        REMOTE_HOST = '10.220.220.100'
        PROJECT_PATH = '/var/www/aargon_management'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/muntaaha-rahman/Aargon_management.git',
                credentialsId: 'your-github-credentials'  // You'll set this in Jenkins
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${BUILD_NUMBER}")
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    // Run your Python tests inside Docker
                    docker.image("${IMAGE_NAME}:${BUILD_NUMBER}").inside {
                        sh 'python -m pytest tests/ -v'  // Adjust to your test command
                    }
                }
            }
        }
        
        stage('Deploy to Server') {
            steps {
                script {
                    // Stop and remove old containers
                    sshagent(['your-ssh-credentials']) {  // You'll set this in Jenkins
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
    }
    
    post {
        always {
            // Clean up Docker images
            sh 'docker system prune -f'
        }
        success {
            echo 'Deployment completed successfully!'
        }
        failure {
            echo 'Deployment failed! Check logs above.'
        }
    }
}