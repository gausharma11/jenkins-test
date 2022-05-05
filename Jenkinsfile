pipeline {
    agent any
    stages {
        stage('checkout') {
            steps {
                echo 'checking out code------------------>>'
                checkout changelog: false, poll: false, scm: [$class: 'GitSCM', branches: [[name: '*/feature1']], extensions: [], userRemoteConfigs: [[credentialsId: 'f9e370eb-38f7-4bad-8a21-7dd8349f152c', url: 'https://github.com/gausharma11/jenkins-test.git']]]
            }
        }
        stage('install dependencies') {
            steps {
                bat '''echo \'installing dependencies-------------------->>\'
                SET PATH="C:\\\\Users\\\\Gaurav Sharma\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python38"
                mkdir "Gaurav"
                python -m venv "Gaurav/tempenv"
                call Gaurav/tempenv/Scripts/activate.bat
                python -V
                pip3 -V
                python test.py'''     
            }
        }
    }
}

