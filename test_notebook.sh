#!/usr/bin/env sh

# Auth as SP
fab auth login -u "TODO" -p "TODO" --tenant "TODO"

# Copy the pipeline so that is owned by the SP - you can now schedule/trigger this in the scheduling UI
fab cp TokenRepro.Workspace/pl_run_notebook_owned_by_user.DataPipeline TokenRepro.Workspace/pl_run_notebook_owned_by_sp.DataPipeline

# Also test directly
fab job start TokenRepro.Workspace/test_sql_token.Notebook
