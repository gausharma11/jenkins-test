pipeline {
    agent any
    stages {
        stage('checkout') {
            steps {
                echo 'checking out code------------------>>'
                checkout([$class: 'GitSCM', branches: [[name: '*/feature1']], extensions: [], userRemoteConfigs: [[credentialsId: 'f9e370eb-38f7-4bad-8a21-7dd8349f152c', url: 'https://github.com/gausharma11/jenkins-test.git']]])
            }
        }
        stage('install dependencies') {
            steps {
                echo 'installing dependencies-------------------->>'
            }
        }
    }
}
