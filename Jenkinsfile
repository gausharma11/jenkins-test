pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION="us-east-1"
        AWS_CREDS=credentials('aws-jenkins-creds')
    }
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
                python -m venv "tempenv"
                call tempenv/Scripts/activate.bat
                python -V
                pip3 -V
                python test.py
                ping pypi.python.org
                python -m pip install pytest pylint coverage boto3
                python -m pylint cfn-templates/src/index.py
                deactivate
                '''
            }
        }    
        stage('AWS Configure'){
            steps{
                bat '''echo "installing the aws cli & boto3------------------------->>"
                msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
                pip install -r requirements.txt
                echo "dependency completed--------------->>"
                '''            
            }                        
        }
        stage('AWS Deploy'){
            steps{
                bat '''echo "AWS Deploy--------->>"
                aws --version
                aws ec2 describe-instances
                echo ${CFN-Template-Action}
                if ${CFN-Template-Action}=="create" (aws cloudformation validate-template --template-body file://cfn-templates/cfn-template.yaml)
                '''          
            }                        
        }
    }
}

