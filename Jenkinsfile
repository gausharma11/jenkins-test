pipeline {
    agent any
    parameters {
        choice(name: 'CFNTemplateAction', choices: ['update', 'create', 'delete', 'none'], description: 'Pick something')
        choice(name: 'CFNLambdaTemplateAction', choices: ['update', 'create', 'delete', 'none'], description: 'Pick something')
    }
    environment {
        AWS_DEFAULT_REGION="us-east-1"
        AWS_CREDS1=credentials('aws-jenkins-creds')
    }
    stages {
        stage('Testing Python Code') {
            steps {
                bat '''echo \'installing dependencies-------------------->>\'
                echo "creating virtual env-->"
                python -m venv "tempenv"
                echo "activating Virtual env"
                call tempenv/Scripts/activate.bat
                echo "virtual env activated"
                python -V
                pip3 -V
                echo "installing dependencies in the virtual env------->"
                python -m pip install pytest pylint coverage boto3
                echo "depedncies installed-------->"
                echo "checking the linting of the python file/code using the pylint---->"
                python -m pylint cfn-templates/src/index.py
                echo "checking the unit cases of the python file/code using the pytest--->"
                python -m pytest tests/test_index.py
                echo "Coverage of the code using the coverage---->"
                coverage report
                echo "deactivating the virtual env"
                deactivate
                '''
            }
        }
        stage('AWS Validate & Deploy Compute Product'){
            steps{
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
        stage('AWS Validate & Deploy Lambda Product'){
            steps{
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

