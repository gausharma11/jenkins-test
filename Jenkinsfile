pipeline {
    agent any
    parameters {
        choice(name: 'CFNTemplateAction', choices: ['update', 'create', 'delete', 'none'], description: 'Pick something')
        choice(name: 'CFNLambdaTemplateAction', choices: ['update', 'create', 'delete', 'none'], description: 'Pick something')
    }
    environment {
        AWS_DEFAULT_REGION="us-east-1"
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
                python -m pip install pytest pylint coverage boto3
                python -m pylint cfn-templates/src/index.py
                python -m pytest tests/test_index.py
                coverage report
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
        stage('AWS Deploy Compute Product'){
            steps{
                withCredentials([<object of type com.cloudbees.jenkins.plugins.awscredentials.AmazonWebServicesCredentialsBinding>]) {
                    echo "Choice: ${params.CFNTemplateAction}"
                    bat '''echo "AWS Deploy--------->>"
                    aws --version
                    SET action=%CFNTemplateAction%
                    echo "validating  template------------------------------->>"
                    aws cloudformation validate-template --template-body file://cfn-templates/cfn-template.yaml
                    echo "template validated--------------------------------->>"
                    if %action%==create (aws cloudformation create-stack --stack-name mycompute --template-body file://cfn-templates/cfn-template.yaml --capabilities CAPABILITY_NAMED_IAM)
                    if %action%==update (aws cloudformation update-stack --stack-name mycompute --template-body file://cfn-templates/cfn-template.yaml --capabilities CAPABILITY_NAMED_IAM)
                    if %action%==delete (aws cloudformation delete-stack --stack-name mycompute)
                    '''
                }
            }
        }
        stage('AWS Deploy Lambda Product'){
            steps{
                withCredentials([<object of type com.cloudbees.jenkins.plugins.awscredentials.AmazonWebServicesCredentialsBinding>]) {
                    echo "Choice: ${params.CFNLambdaTemplateAction}"
                    bat '''echo "AWS Deploy--------->>"
                    aws --version
                    SET action=%CFNLambdaTemplateAction%
                    echo "validating  template------------------------------->>"
                    aws cloudformation validate-template --template-body file://cfn-templates/cfn-lambda-template.yaml
                    echo "template validated--------------------------------->>"
                    if %action%==create (aws s3api create-bucket --bucket demo-gaurav-lambdajenk --region us-east-1)
                    if %action%==create (aws cloudformation package --template-file cfn-templates/cfn-lambda-template.yaml --s3-bucket demo-gaurav-lambdajenk --output-template-file packaged-cfn-lambda-template.yaml)
                    if %action%==create (aws cloudformation deploy --template-file packaged-cfn-lambda-template.yaml --stack-name mylambdastack --capabilities CAPABILITY_NAMED_IAM)
                     
                    if %action%==update (aws cloudformation package --template-file cfn-templates/cfn-lambda-template.yaml --s3-bucket demo-gaurav-lambdajenk --output-template-file packaged-cfn-lambda-template.yaml)
                    if %action%==update (aws cloudformation deploy --template-file packaged-cfn-lambda-template.yaml --stack-name mylambdastack --capabilities CAPABILITY_NAMED_IAM)
                    
                    if %action%==delete (aws cloudformation delete-stack --stack-name mylambdastack)
                    if %action%==delete (aws s3 rm s3://demo-gaurav-lambdajenk --recursive)
                    if %action%==delete (aws s3api delete-bucket --bucket demo-gaurav-lambdajenk --region us-east-1)               
                    '''
                }    
            }
        }
    }
}

