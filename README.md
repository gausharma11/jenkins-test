# jenkins-test

Author: Gaurav Sharma


In this readme file you will create a simple CI/CD pipeline using Jenkins deployed on the EC2 Windows host pn AWS in order to push/publish the lambda written in the python and the push /publish AWS resources mentioned in the cfn-templates.yaml file on the AWS Console.


## Prerequisites

You will need the following to complete pre-requisite:

- An AWS account //sign up and sign in the AWS Console.
- python
- git
- java 8 or 11
- jenkins
- awscliv2

on the host in which the windows EC2 instance in our case.

Please see the section of the installation of the following softwares/packages needs to be installed:

refer the section "Preparing Jenkins"


## Forking the Repository

You will have to push changes to Github in order to trigger the CI/CD pipeline. Therefore, before
going any further in this tutorial, **fork this repository** and work on your own fork from now on.

## Preparing Jenkins

You will need a Jenkins instance for this tutorial. Perform the following steps to deploy Jenkins
inside your AWS account:

### Create an IAM User for Jenkins

1. In the AWS IAM create a user in order to use the programmatic access & awscli.
2. Assign the AmazonEC2FullAccess & AWSCloudFormationFullAccess Policy under the permission tab.
3. Get the AccessKeyId & SecretAccessKeyId for the configuration purpose in the AWS Credentials store using plugin- https://plugins.jenkins.io/aws-credentials/ 

### Create an EC2 Instance

1. In the EC2 console click **Launch Instance**.
2. Select an **Windows** AMI.
3. Leave **t2.micro** selected and click **Next: Configure Instance Details**.
4. Under **Network**, choose any VPC with a public subnet. The **default VPC** will work fine here,
too.
5. Under **Subnet**, choose any public subnet.
6. Under **Auto-assign Public IP** choose **Enabled**.
7. Under **IAM role** choose the **Jenkins** role you created before.
8. Click **Next: Add Storage**.
9. Click **Next: Add Tags**.
10. Create a tag with the key "Name" and the value "Jenkins" and click **Next: Configure Security Group**.
11. Name the security group "Jenkins" and allow **RDP access** as well as access to **TCP port
3389, jenkins host port -8080** from your WAN IP address.
12. Click **Review and Launch**.
13. Click **Launch**.
14. Choose an existing or create a new keypair, then click **Launch Instances**.

### Download the dependency softwares on jenkins EC2.

1. RDP into the instance you created in the previous step.
3. download the java 8 or java 11 for the Windows x64 Installer from -https://www.oracle.com/in/java/technologies/javase/jdk11-archive-downloads.html
4. download the git for windows & install - https://git-scm.com/download/win 
5. downlaod the python or python3 from - https://www.python.org/downloads/windows/
6. download the awscliv2 from the command prompt & install- msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
7. Set the system path for the - Python, Java, git, awscliv2.
8. download the windows LTS jenkins from the installer- https://www.jenkins.io/download/
9. install the jenkins installer and configure based on this link- https://www.jenkins.io/doc/book/installing/windows/ or in the section- "Run the Jenkins Setup Wizard"
 


### Run the Jenkins Setup Wizard

1. Browse `http://<instance_ip>:8080`.
2. Under **Administrator password** enter the output of "C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword" on the Jenkins instance.
3. Click **Continue**.
4. Click **Install suggested plugins** and let the installation finish.
5. Click **Continue as admin**.
6. Click **Start using Jenkins**.
7. Install the custom plugin for storing the AWS credentials- https://plugins.jenkins.io/aws-credentials/


## Creating the Pipeline

We will now create the Jenkins pipeline. Perform the following steps on the Jenkins UI:

1. Click **New Item** to create a new Jenkins job.
2. Under **Enter an item name** type "sample-pipeline".
3. Choose **Pipeline** as the job type and click **OK**.
4. Under **Pipeline -> Definition** choose **Pipeline script from SCM**.
5. Under **SCM** choose **Git**.
6. Under **Repository URL** paste the of your (forked) repository or the repo you created by your own.
7. Leave the rest at the default and click **Save**.

You should now have a pipeline configured. When executing the pipeline, Jenkins will clone the Git
repository, look for a file named `Jenkinsfile` at its root and execute the instructions in it.


### Looking at the Pipeline

Let's take a look at the pipeline that is already in the repository. Open the file called
`Jenkinsfile` file in a text editor 

We can see that the entire pipeline is inside a top-level directive called `pipeline`.

Then we have a line saying `agent any` - this is required for declarative pipelines, but we are not
going to touch it in this tutorial. can be used for the docker images or any specific agent for the particular stage.

Next we have the `environment` directive. This section allows us to configure global variables
which will be available (for both reading and writing) in any of the pipeline's stages. This is
useful for configuring global settings.

Next we have two user paramter with type choice- create,update,delete,none
Based on the choice the two paramters evaluate the actions on the aws cloudformation template in order to create, update, delete the stacks respectively, none indicates no action on respective stack.

Next we have the stage "scm checkout with git" comes from the plugin jenkins pipeline which does the checkout of the code repo.

Next we have the stage "Testing Python Code" which does the things:
1. creates the virtual env with dependecies installed like- pylint, pytest, coverage in order to do syntax, PEP8 linting , test the python test cases(defined in the tests dir in the repo) & finally provide a coverage report.
2. After the testing done provides the coverage report in the build logs and deactivate the virtual env created.
3. Virtual env helps make a isolated env with the version of dependency installed separate from the host.


Next we have two stages: 
1.  AWS Validate & Deploy Compute Product: This stage basically check the choice parameter provided at the time of the build with paramter & do the cloudfromation stack creation, update & delete. The compute template written in the cfn-templates dir with the name cfn-template.yaml

First it validate the cloudformation template i.e. yaml is well formed or not, if no provide the error message and if yes does the required action.

2.  AWS Validate & Deploy lambda Product:This stage basically check the choice parameter provided at the time of the build with paramter & do the cloudfromation stack creation, update & delete. The lambda template written in the cfn-templates dir with the name cfn-lambda-template.yaml

First it validate the cloudformation template i.e. yaml is well formed or not, if no provide the error message and if yes does the required action.
secondly it will package the cfn template for lambda along with the python code written inside the src dir file name "index.py" and upload it to the s3 bucket created.
At last it deploy the lambda cfn template along with the python aws lambda to the AWS account.

So, now that we understand the structure of our pipeline, let's run it.

### Running the Pipeline

1. From the top-level view on the Jenkins UI, click on the pipeline created.
2. On the menu to the left, click **Build Now with paramters**.
3. Select the respective actions and hit build.

This will trigger a run. You should see a new run (or "build") under the **Build History** view on
on the left side. To see the logs from the build, click the build number.

**Note**
Please Evaluate the things and implement as per your need, there are few things which are limitation to me & can be enhanced in other ways.
Like - Hardware compatibilty & Cost budget.


