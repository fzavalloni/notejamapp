# Introduction 
This project is a Demo that demostrates how to deploy a small Python WebPage into Azure Web App + Sql Databases on Azure\
using Azure Devops as CI/CD.

It has 2 environments divided into 2 subscriptions (DEV/PRD):


![GitHub Logo](/images/BasicEnvironment.jpg)


The components of the solution are:
1. Azure Devops
2. Azure App Service
3. SQL Server
4. Log Analytics WorkSpace

# Getting Started

##	Installation process in your Azure Tenant

- Create 2 subscriptions called DEV and PRD.\
    https://docs.microsoft.com/en-us/azure/cost-management-billing/manage/create-subscription#:~:text=Create%20a%20subscription%20in%20the%20Azure%20portal%201,the%20form%20for%20each%20type%20of%20billing%20account.

- Create a Azure Devops Project\
    https://docs.microsoft.com/en-us/azure/devops/organizations/projects/create-project?view=azure-devops&tabs=preview-page

- Create two variable groups in the Project:
    - (variableGroupName) Pipeline ==> (variable)vmImage = ubuntu-18.04
    - (variableGroupName) SQLCredentials ==> (variables) Username and Password\
    https://docs.microsoft.com/en-us/azure/devops/pipelines/library/variable-groups?view=azure-devops&tabs=yaml

- Push the code into the Azure Devops.\
    https://docs.microsoft.com/en-us/azure/devops/user-guide/code-with-git?view=azure-devops

- Create 2 pipelines pointing to the files below:
    - azure-pipelines.yml
    - azure-shared.yml\
    https://docs.microsoft.com/en-us/azure/devops/pipelines/create-first-pipeline?view=azure-devops&tabs=java%2Ctfs-2018-2%2Cbrowser

- (optional) In the pipelines you can add an approval requirement to the PRD stage.\
    https://docs.microsoft.com/en-us/azure/devops/pipelines/release/approvals/?view=azure-devops

- In the Project Settings create 2 Service connections and make sure that each one has the Contributors role associated\
  to respective subscription.
    - DEV-NotejamApp-SPN
    - PRD-NotejamApp-SPN\
    https://azuredevopslabs.com/labs/devopsserver/azureserviceprincipal/

- Run the pipelines in the sequence below.
    - azure-shared - Either creates the SharedResources Resource Group and the SQL Server
    - azure-pipelines - Creates the App Service, Database and Log Analytics


##	Objectives

- The Application must serve variable amount of traffic. Most users are active during business hours. During big
events and conferences the traffic could be 4 times more than typically.

    - [x] In the App Service on PRD we are using a Auto Scale out policy. The App can create up to 4 instances during a
    busy time and scale back in to 1 instance.

- The Customer takes guarantee to preserve your notes up to 3 years and recover it if needed.

    - [x] The SQL Server database on PRD has long term retention enabled.

- The Customer ensures continuity in service in case of datacenter failures.
    
    - [ ] It can be done keeping the environment in only one region. In the FrontEnd can use the App Service Environment(V3).\
    Deploying 3 App Service Instances, each one on its own availability zone(datacenter) alongside with an Internal Load Balancer.
    https://docs.microsoft.com/en-us/azure/app-service/environment/zone-redundancy\
    In the Backend, we can enable Availability Zones in the SQL Database tier.\
    https://docs.microsoft.com/en-us/azure/azure-sql/database/high-availability-sla\

- The Service must be capable of being migrated to any of the regions supported by the cloud provider in case of emergency.

    - [ ] In this item we have 2 options:
    - **Offline:** We keep an offline SQL Server backup in a secondary region (GRS Storage account) and reploy the resources ad hoc via Azure Devops just replacing the region parameters and restoring the DB backup afterwards.\
    It will incur either a higher RPO (data loss) and RTO (time to recover) but it is cheaper.\
    https://docs.microsoft.com/en-us/azure/azure-sql/database/recovery-using-backups

    - **Online:** We can deploy the environment into 2 different regions and using Azure Traffic Manager(Global Load Balancer) + Application Gateway + SQL Server with Fail Over Groups. On each region we should use the Availability Zone as well.( described in the item3).\
    Better solution for RPO and RTO, but way more expensive.\
    https://docs.microsoft.com/en-us/azure/azure-sql/database/auto-failover-group-overview?tabs=azure-powershell

    ![GitHub Logo](/images/MultiRegionEnv.jpg)


- The Customer is planning to have more than 100 developers to work in this project who want to roll out multiple deployments a day without interruption / downtime.

    - [ ] It is partialy done. On DEV is possible to deploy as many environments as you want, just selecting the environment parameter when triggering the pipeline. At the moment you can select up to 10 environments, but it can be easily expandable.\
    We need also to enable more the parallel jobs in the build agents in order to have more pipelines running at the same time.\
    For PRD we would need to combine a strategy of canary deployment using Deployment slots (It was not done due the time constrains).\
    https://www.c-sharpcorner.com/blogs/doing-canary-deployments-using-azure-web-app-deployment-slots

- The Customer wants to provision separated environments to support their development process for\
development, testing and production in the near future.

    - [x] We have created 2 environments separated into stages in the pipeline

- The Customer wants to see relevant metrics and logs from the infrastructure for quality assurance and security purposes.

    - [ ] Partially done. All Resource groups has its own Log Analytics Workspace. The ARM templates does not set the Diagnostic Logging, it has to be done by hand (It was not done due the time constrains).\
    A good option to visualize metrics and logs from a unique place is throught Dashboards, however Azure has some limitations to create\ it using pipelines.\  
    So, we have a dashboard template **\dashboards\notejamapp-dev001-app-Dashboard.json** that might be imported to see metrics from Azure Monitor and Log Analytics.\
    https://devblogs.microsoft.com/devops/copy-dashboard-public-preview/\
    https://marketplace.visualstudio.com/items?itemName=EnterpriseServicesDevOpsTeam.DashBoardMigration

