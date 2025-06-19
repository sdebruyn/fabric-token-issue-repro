# Fabric notebook token issues

Tokens retrieved from notebookutils in Fabric notebooks do not work for SQL or DWH when the notebook is run in the context of a service principal (SP).

## Setup

This repo contains the Fabric items and can be linked to a Fabric Workspace.

1. Create a service principal, give it access to the Workspace (I gave full admin)
1. Install Fabric CLI
1. Fill in credentials in test_run.sh
1. Use test_run.sh to copy Data Pipeline so that it is owned by SP (optional)
1. Start a test run of the Notebook as the SP

## Relevant files

* `test_run.sh`: Script to run the test Notebook as a service principal.
* `test_local.sh`: Same as what the notebook does, but using `azure-identity` to get a token for the service principal.

## Findings

Anytime the Notebook executes in the context of the SP, the notebookutils return a token which is not authorized to access SQL Endpoint or DWH.

This is not a problem when the Notebook runs in the context of a user.

| Scenario | JWT aud | JWT scp | Result |
| --- | --- | --- | --- |
| Run Notebook as user in Fabric UI | https://analysis.windows.net/powerbi/api | user_impersonation | ✅ |
| Run Notebook from scheduled Data Pipeline owned by user | https://analysis.windows.net/powerbi/api | user_impersonation | ✅ |
| Run Notebook from scheduled Data Pipeline owned by SP | https://analysis.windows.net/powerbi/api | Dataset.ReadWrite.All Lakehouse.ReadWrite.All MLExperiment.ReadWrite.All MLModel.ReadWrite.All Notebook.ReadWrite.All SparkJobDefinition.ReadWrite.All Workspace.ReadWrite.All | Could not login because the authentication failed. (18456) |
| Run Notebook through API as SP | https://analysis.windows.net/powerbi/api | Dataset.ReadWrite.All Lakehouse.ReadWrite.All MLExperiment.ReadWrite.All MLModel.ReadWrite.All Notebook.ReadWrite.All SparkJobDefinition.ReadWrite.All Workspace.ReadWrite.All | Could not login because the authentication failed. (18456) |
| Run Notebook through API as user | https://analysis.windows.net/powerbi/api | user_impersonation | ✅ |
| Same code but get token for SP with azure-identity | https://analysis.windows.net/powerbi/api | not present | ✅ |
