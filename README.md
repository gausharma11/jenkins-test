# jenkins-test

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

## Preparing Jenkins

You will need a Jenkins instance for this tutorial. Perform the following steps to deploy Jenkins
inside your AWS account:

### Create an IAM Role for Jenkins

1. In the [IAM roles view][6] click **Create role**.
2. Choose **EC2** and click **Next: Permissions**.
3. Check the **AmazonECS_FullAccess** and the **AmazonEC2ContainerRegistryPowerUser** policies and
click **Next: Review**.
4. Under **Role name** type "Jenkins" and click **Create role**.

### Create an EC2 Instance

1. In the [EC2 console][7] click **Launch Instance**.
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
11. Name the security group "Jenkins" and allow **SSH access** as well as access to **TCP port
8080** from your WAN IP address.
12. Click **Review and Launch**.
13. Click **Launch**.
14. Choose an existing SSH key or create a new one, then click **Launch Instances**.

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
2. Under **Administrator password** enter the output of `sudo cat /var/lib/jenkins/secrets/initialAdminPassword` on the Jenkins instance.
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
6. Under **Repository URL** paste the [HTTPS URL][9] of your (forked) repository or the repo you created by your own.
7. Leave the rest at the default and click **Save**.

You should now have a pipeline configured. When executing the pipeline, Jenkins will clone the Git
repository, look for a file named `Jenkinsfile` at its root and execute the instructions in it.


### Looking at the Pipeline

Let's take a look at the pipeline that is already in the repository. Open the file called
`Jenkinsfile` file in a text editor (preferably one [which][12] [supports][13] the Jenkinsfile
syntax).

We can see that the entire pipeline is inside a top-level directive called `pipeline`.

Then we have a line saying `agent any` - this is required for declarative pipelines, but we are not
going to touch it in this tutorial. If you are still curious about what the agent directive does,
you can read about it [here][15].

Next we have the `environment` directive. This section allows us to configure global variables
which will be available (for both reading and writing) in any of the pipeline's stages. This is
useful for configuring global settings.

Lastly, we have a `stage`. You can have as many stages as you want in a pipeline. A stage is a
major section of the pipeline and it contains the actual "work" which the pipeline does. This work
is defined in `steps`. A step can execute a shell script, push an artifact somewhere, send an email
or a Slack message to someone and do lots of other stuff. We can see that at the moment our
pipeline doesn't do much, just prints something to the console using an `echo` step.

> **NOTE:** There is [an entire list][16] of step types which can be used in Jenknis pipelines,
> however in this tutorial we will keep things simple and use mostly the `sh` step, which executes
> a shell script.

So, now that we understand the structure of our pipeline, let's run it.

### Running the Pipeline

1. From the top-level view on the Jenkins UI, click on the pipeline's name ("sample-pipeline").
2. On the menu to the left, click **Build Now**.

This will trigger a run. You should see a new run (or "build") under the **Build History** view on
on the left side. To see the logs from the build, click the build number (`#1` if this is your
first build) and the click **Console Output**.

If all went well, after some Git-related output you should see that the pipeline ran the only stage
we currently have, which should simply print `This is a sample stage`.

Great. Now let's make the pipeline do some real stuff.

### Adding a CI Stage

Let's add a simple CI step to our pipeline. We want to build a Docker image from our app and push
it to ECR so that we can later deploy containers from it.

Let's populate the `docker_repo_uri` environment variable with the full URI of the ECR repository
you created previously. It shall be similar to the following:

    pipeline {
        ...

        environment {
            region = "us-east-1"
            docker_repo_uri = "xxxxxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com/sample-app"
            task_def_arn = ""
            cluster = ""
            exec_role_arn = ""
        }

        ...
    }

Now, replace the "Example" stage with the following:

    stage('Build') {
        steps {
            // Get SHA1 of current commit
            script {
                commit_id = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
            }
            // Build the Docker image
            sh "docker build -t ${docker_repo_uri}:${commit_id} ."
            // Get Docker login credentials for ECR
            sh "aws ecr get-login --no-include-email --region ${region} | sh"
            // Push Docker image
            sh "docker push ${docker_repo_uri}:${commit_id}"
            // Clean up
            sh "docker rmi -f ${docker_repo_uri}:${commit_id}"
        }
    }

Notice that we have two types of steps here: `script` and `sh`. `script` steps allow us to run a
Groovy code snippet inside our declarative pipeline. We need this because we want to capture the
SHA1 of the current commit and assign it to a variable, which we can then use to uniquely tag the
Docker image we are building. `sh` steps are simply shell commands.

So now our pipeline should build a Docker image, push it to ECR and clean up the leftover image so
that we don't accumulate garbage on Jenkins.

In order to update the pipeline, we must commit and push our changes to Github. So, when you are
done editing, do the following:

1. Commit your changes by running `git commit -am "Add CI step to pipeline"`.
2. Push your changes to Github by running `git push origin`.

Now, re-run the pipeline on Jenkins and examine its output. If all goes well, the pipeline will
build a Docker image, push it to ECR and clean up the local image on Jenkins. Verify this by
looking at the [Repositories][14] section of the ECS console. Your repository should now have an
image in it.

### Adding a CD Stage

Now that we have a pipeline which automatically generates Docker images for us, let's add another
stage that will deploy new images to our deployment environment (Fargate).

In your editor, open the `taskdef.json` file. This file defines how to deploy our app to Fargate.
It already contains everything we need except one thing: the Docker image to use for the
deployment. As you can see, at the moment the `image` key contains a placeholder - `{{image}}`.
This placeholder is **invalid** if you just try to submit it as-is to Fargate, and must be edited
first. However, we can't simply hardcode a specific Docker image here, because we want our pipeline
to every time deploy **the image we just built** to the environment. So, we will override this
field with the correct value in our new stage.

Before adding the stage, populate the following variables in your `environment`:

`task_def_arn` - should contain the ARN of the task definition Fargate has already created for
you, **without the revision number** (`:1` etc.).

> **Note:** You can look for this ARN under the [Task Definitions view][18] on the ECS console, or
> by running `aws ecs list-task-definitions | grep first-run-task-definition`.

`cluster` - should contain the name of the Fargate cluster you created before.

`exec_role_arn` - should contain the ARN of the **ecsTaskExecutionRole** role which was created
automatically for you when you created the cluster.

> **Note:** In case you don't have such a role, you can create it using [these instructions][17].

So, after these changes, your `environment` should look similar to the following:

    environment {
        region = "us-east-1"
        docker_repo_uri = "xxxxxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com/sample-app"
        task_def_arn = "arn:aws:ecs:us-east-1:xxxxxxxxxxxx:task-definition/first-run-task-definition"
        cluster = "default"
        exec_role_arn = "arn:aws:iam::xxxxxxxxxxxx:role/ecsTaskExecutionRole"
    }

Now, add the following stage right after the existing "Build" stage:

    stage('Deploy') {
        steps {
            // Override image field in taskdef file
            sh "sed -i 's|{{image}}|${docker_repo_uri}:${commit_id}|' taskdef.json"
            // Create a new task definition revision
            sh "aws ecs register-task-definition --execution-role-arn ${exec_role_arn} --cli-input-json file://taskdef.json --region ${region}"
            // Update service on Fargate
            sh "aws ecs update-service --cluster ${cluster} --service sample-app-service --task-definition ${task_def_arn} --region ${region}"
        }
    }

The first step in this stage overrides the `image` field in taskdef.json with the name of the image
that has been created in the CI stage.

> **Note:** We use `|` as a delimiter in `sed` because `${docker_repo_uri}` contains a slash, which
> creates escaping problems in this case.

The second step registers a new task definition revision which references the new image we already
have in ECR.

The last step instructs Fargate to update the app on the cluster, which will cause a new container
to be launched from the image we just pushed to ECR, replacing the old one.

> **Note:** When calling `update-service` you may specify a specific **task definition revision**
> by including the revision number in the provided ARN (for example `:3`). When not doing so,
> Fargate simply uses the most recent revision, which is fine in our case.

So, we should now be ready to test our CD stage. Commit your changes, push them to Github and run
the pipeline. If all goes well, an update should be triggered on Fargate, which will deploy our
app instead of the sample app we deployed using the Getting Started wizard. Verify this by browsing
the DNS name of the load balancer again. If you still see the sample app, the deployment might
still be in progress. You can follow it on the service's [Deployments][19] tab.

## Testing the Pipeline

Up to now, all we did was set up a CI/CD pipeline which will build and deploy code changes
automatically. Now, we will verify it actually does so by making a very simple code change.

Open `app.go` in your editor and change `version = "1.0"` on line 11 to `version = "1.1"`. Push
the change to Github and run the pipeline. If all goes well, after a short time you should see the
"Version" field change when refreshing your browser.

> **Note:** Deploying a new version could take a few minutes, mainly because the default
> [Deregistration Delay][20] is 5 minutes. You may reduce this timer to speed up deployments, or
> manually kill the old tasks.

## Cleaning Up

When you are done experimenting and would like to delete the environment, perform the following:

1. Terminate the Jenkins instance and delete its IAM role, security group and SSH key.
2. On the [Clusters view][21] of the ECS console, choose your cluster, click **Delete Cluster** and
then **Delete**. This will delete everything Fargate has created for you including the VPC and the
load balancer.
3. In the [Task Definitions view][18], click **first-run-task-definition**, check all of the
revisions in the list, then click **Actions -> Deregister** and then **Deregister**.
4. In the [Repositories view][14], check the repository you created, then click **Delete
repository** and then **Delete**.
