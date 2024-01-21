# MERN Application Deployment on AWS

This guide outlines the steps to deploy a MERN (MongoDB, Express.js, React, Node.js) application on AWS using various services. The deployment process is automated and orchestrated through AWS CLI, Boto3, Docker, Jenkins, and more.

## Prerequisites

Before proceeding, ensure the following:

- AWS account with necessary permissions
- Installed AWS CLI and configured with credentials
- Installed Boto3 for Python
- Basic understanding of Docker, Jenkins, and AWS services

## Architecture Overview

This deployment consists of several steps:
- Setting up AWS environment
- Containerizing the MERN application
- Version controlling with AWS CodeCommit
- Implementing Continuous Integration with Jenkins
- Defining infrastructure as code with Boto3
- Deploying backend and frontend services on EC2
- Utilizing AWS Lambda for specific tasks
- Kubernetes (EKS) deployment for scalability
- Monitoring and logging with CloudWatch
- Documentation for the entire process

## Steps to Deploy

### Step 1: Set Up AWS Environment

Follow the instructions in [this guide](https://medium.com/@mehmetodabashi/how-to-install-and-configure-aws-cli-on-windows-10-3c8decffc507) to install and configure AWS CLI with your AWS credentials.

#### b. Installing Boto3 for Python
1. Install Python from [here](https://www.python.org/downloads/).
2. Use the command `pip install boto3` to install Boto3 in Python.


### Step 2: Prepare the MERN Application

### 1. Containerize the MERN Application:
Ensure both frontend and backend components of the MERN application are containerized using Docker. Create a Dockerfile for each component.

### 2. Push Docker Images to Amazon ECR:
1. Build Docker images for both frontend and backend.
2. Create an Amazon ECR repository for each image.
3. Push the Docker images to their respective ECR repositories.


### Step 3: Version Control

1. Create a CodeCommit repository.
2. Push the MERN application source code to CodeCommit.

### Step 4: Continuous Integration with Jenkins

1. **Install and Configure Jenkins on an EC2 Instance:**
   Follow the steps in [this guide](https://devopscube.com/install-configure-jenkins-2-0/) to install and configure Jenkins on an EC2 instance.

2. **Create Jenkins Pipeline for Docker Image Building and Pushing to ECR:**
   - Go to Jenkins and navigate to "New Item".
   - Select "Pipeline" or "GitHub Project".
   - Add the GitHub project URL.
   - Configure it to build when a CodeCommit repository is updated and notify an SQS queue.
   - Select the queue and manually enter the CodeCommit URL and branches.
   - Provide the repository URL and branch.
   - For the Pipeline, choose "Pipeline script from SCM".
   - In SCM, select Git and add the repository URL.
   - Configure credentials if required.
   - Specify the branch name and save the configuration.

### Step 5: Infrastructure as Code (IaC) with Boto3

1. Define infrastructure components using Boto3.
2. Create an Auto Scaling Group (ASG) for the backend.
3. Use Boto3 to deploy EC2 instances with the Dockerized backend in the ASG.

For an example of creating an Auto Scaling Group using Boto3, refer to the file [DeployingBackendServices.py](path/to/DeployingBackendServices.py) in this repository.

### Step 7: Set Up Networking

1. **Create an Elastic Load Balancer (ELB) with a Target Group for the backend ASG:**
   - Log in to the AWS Management Console.
   - Navigate to the EC2 dashboard.
   - Click on "Load Balancers" in the navigation pane.
   - Click "Create Load Balancer".
   - Choose the appropriate load balancer type (e.g., Application Load Balancer, Network Load Balancer).
   - Configure the load balancer settings (listeners, availability zones, security settings, etc.).
   - Create a new Target Group for the load balancer, specifying target instances from the backend Auto Scaling Group (ASG).
   - Associate the target group with the load balancer.
   - Review and create the load balancer along with the target group.

2. **Configure DNS using Cloudflare:**
   - Log in to your Cloudflare account.
   - Select the website/domain you want to manage.
   - Navigate to the DNS settings or DNS management section.
   - Look for the option to add a new DNS record (often labeled as "Add Record" or "+ Add").
   - Choose the record type as "CNAME."
   - Enter the subdomain (e.g., backend.example.com) in the "Name" or "Hostname" field.
   - Enter the DNS name or endpoint of your Elastic Load Balancer (ELB) in the "Points to" or "Value" field.
   - Save the changes and allow some time for DNS propagation.
   

### Step 8: Deploying Frontend Services

1. **Deploy Dockerized frontend on EC2 instances using Boto3:**
   For an example of deploying the frontend service on EC2 instances using Boto3, refer to the file [DeployingFrontendService.py](path/to/DeployingFrontendService.py) in this repository.

### Step 9: AWS Lambda Deployment

1. **Create Lambda functions for specific tasks:**
   - Log in to the AWS Management Console.
   - Navigate to the AWS Lambda service.
   - Click on "Create function".
   - Choose the appropriate option for function creation (e.g., Author from scratch, Blueprints, etc.).
   - Configure the function settings (name, runtime, permissions, etc.).
   - Write or upload the function code for the specific task.
   - Set up triggers or event sources if required.
   - Review and create the Lambda function.

2. **Implement a Lambda function for backing up the database to S3 with timestamps:**
   - Follow the steps above to create a new Lambda function.
   - Write a Lambda function named [LambdaFunction.py](path/to/LambdaFunction.py) that performs the database backup task with timestamps and S3 storage.
   - Ensure the function includes logic to generate timestamps and store the backup in an S3 bucket.
   - Test the function to verify its functionality.

### Step 10: Kubernetes (EKS) Deployment

1. **Create an EKS cluster using eksctl or other tools:**
  - **Install eksctl on Ubuntu:**
    - Open Terminal.
    - Run the following commands to install eksctl:
      ```bash
      sudo apt-get update
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.28.5/2024-01-04/bin/linux/amd64/kubectl
      chmod +x ./kubectl
      mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
      kubectl version --client
      ```
       For more details, refer to the [ official installation guide for kubectl](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)
   - **Install eksctl on Windows:**
     - Open PowerShell or Command Prompt.
     - Run the following command to install eksctl using Chocolatey:
       ```
       choco install eksctl
       ```

   - **Create an EKS cluster with eksctl:**
     - Update the Kubernetes configuration for the EKS cluster: aws eks update-kubeconfig --name mern-abhi3 --region ap-south-1

     - Use the following command to create an EKS cluster using eksctl:
         ```sh
         eksctl create cluster --name <CLUSTER_NAME> --region <AWS_REGION> --nodegroup-name <NODEGROUP_NAME> --node-type <NODE_TYPE> --nodes <NODES_COUNT> --nodes-min <MIN_NODES> --nodes-max <MAX_NODES>
         --vpc-private-subnets=<SUBNET-ID>,<SUBNET-ID>,<SUBNET-ID>

         ```
     - Replace the placeholders with your specific cluster configuration:
        - `<CLUSTER_NAME>`: Replace with your desired EKS cluster name (e.g., mern-abhi).
        - `<AWS_REGION>`: Replace with your AWS region (e.g., us-east-1).
        - `<NODEGROUP_NAME>`: Replace with your node group name (e.g., standard-workers).
        - `<NODE_TYPE>`: Replace with the desired EC2 instance type for your nodes (e.g., t3.micro).
        - `<NODES_COUNT>`: Replace with the number of nodes for your cluster (e.g., 4).
        - `<MIN_NODES>`: Replace with the minimum number of nodes for your cluster (e.g., 2).
        - `<MAX_NODES>`: Replace with the maximum number of nodes for your cluster (e.g., 4).
        - `<SUBNET-ID>`: Replace with vpc private subnets id

2. Deploying the MERN Application:
   - Update the Kubernetes configuration for the EKS cluster:
      ```
      - aws eks update-kubeconfig --name mern-abhi3 --region ap-south-1
      ```
   - Deploy the application using the deployment YAML file:
      ```
      kubectl apply -f deploy.yml
      ```
   - Check 
      ```
      kubectl get svc mern-abhi3
      ```
3. **Install Helm on Windows using Chocolatey:**
   - Open PowerShell or Command Prompt with administrative privileges.
   - Run the following command to attempt installing Helm using Chocolatey:
     ```
     choco install kubernetes-helm
     ```
    - Check the [Chocolatey Helm package page](https://community.chocolatey.org/packages/kubernetes-helm) for updates or availability.
  
4. Setting up MicroK8s
   - Install and configure MicroK8s:
      ```
      sudo usermod -a -G microk8s $USER
      sudo chown -f -R $USER ~/.kube
      su - $USER
      microk8s status --wait-ready
      sudo usermod -a -G microk8s ubuntu
      sudo chown -R ubuntu ~/.kube
      ```
5. Install Helm
   sudo snap install helm --classic

6. Folder Structure of a Helm Chart And Deploying with Helm:
   - Folder Structure of a Helm Chart :
     - A typical Helm chart has a predefined directory structure. Understanding this structure is crucial for organizing your Kubernetes resources correctly. Below is an example of the folder structure for a Helm chart:
         ```
         chart/
            │
            ├── Chart.yaml          # A YAML file containing information about the chart
            ├── values.yaml         # The default configuration values for the chart
            ├── templates/          # A directory of templates that, when combined with values, will generate valid Kubernetes manifest files
               ├── deployment.yaml # Defines the deployment configuration
               ├── service.yaml    # Defines the service resource
               └── ...

         ```
   - Deploying the MERN Application with Helm:
      - To deploy your application with Helm:
        - Ensure your application's Helm chart follows the above folder structure.
        - Navigate to the directory where your Helm chart (chart/) is located.
        - Deploy your application using the Helm command:
            ```
            helm install mern-release ./chart
            ```
            mern-release: The name of your Helm release.
            ./chart: The path to your chart directory.
   - Checking the Status of the Release:
      ```
      helm status mern-release
      ```
      This command provides detailed information about the release, including its state, revisions, release notes, and more.
   - Deleting the Release:
      - If you need to delete the Helm release for any reason, such as to redeploy with different settings or to clean up resources, use the following command:
         ```
         helm delete mern-release
         ```
         
         This command will remove the release and all the Kubernetes resources associated with it from your cluster.

         mern-release: The name of the Helm release you wish to delete.
      
### Step 11: Monitoring and Logging


1. **Set up monitoring using CloudWatch for alarms:**
   - Log in to the AWS Management Console.
   - Navigate to the CloudWatch service.
   - Click on "Alarms" in the left-hand menu.
   - Select "Create Alarm" and choose the metric to monitor (e.g., CPU utilization, network traffic).
   - Define the threshold and conditions for the alarm trigger.
   - Configure actions (e.g., SNS notifications, Auto Scaling).
   - Review and create the CloudWatch alarm.

2. **Configure logging with CloudWatch Logs or alternative solutions:**
   - For CloudWatch Logs:
     - Go to the AWS Management Console and access the CloudWatch service.
     - Click on "Log groups" in the left-hand menu.
     - Select a log group or create a new one.
     - Configure log streams and set up log retention policies.
     - Ensure applications or services are configured to send logs to CloudWatch Logs.

   - For alternative logging solutions:
     - Choose and set up a logging service compatible with your infrastructure (e.g., ELK Stack, Splunk).
     - Install and configure necessary agents or integrations on your instances or containers.
     - Adjust logging configurations to send logs to the chosen logging service.

### Step 12: Documentation

1. **Architecture documentation:**

    #### Architecture Overview:

    Our application utilizes a Microservices-based architecture with the following components:

    - **Frontend Service:** A Dockerized React application running on EC2 instances.
    - **Backend Service:** A Dockerized Node.js application deployed via Auto Scaling Groups (ASGs).
    - **AWS Services:** Utilizing AWS CLI, Boto3, EKS for Kubernetes deployment, Lambda for serverless tasks, CloudWatch for monitoring, and Route 53 for DNS.

    #### Infrastructure Setup:

    - **AWS Environment:** Configured with VPC, subnets, security groups using Boto3.
    - **Continuous Integration/Deployment (CI/CD):** Implemented using Jenkins for Docker image building and CodeCommit for version control.
    - **Containerization:** Docker used for containerizing both frontend and backend services.
    - **EKS Cluster:** Created using eksctl for Kubernetes deployment of the MERN application.
    - **Monitoring and Logging:** CloudWatch set up for alarms and logs, monitoring metrics like CPU utilization and network traffic.

    #### Workflow:

    - Developers push code to the CodeCommit repository.
    - Jenkins triggers CI/CD jobs on new commits, building and pushing Docker images to ECR.
    - Kubernetes (EKS) deploys the MERN application using Helm charts.
    - CloudWatch monitors performance metrics and sets alarms for critical thresholds.

## Additional Notes

- This deployment process is designed for educational purposes and can be modified for production environments.
- Refer to individual sections for detailed instructions on each step.
