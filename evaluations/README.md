# HCLS Agent Evaluation

Provided in this folder is a data file 'hcls_trajectories.json'. This data file can be run against the [Bedrock Agent Evaluation Framework](https://github.com/aws-samples/amazon-bedrock-agent-evaluation-framework/tree/main). 

# Pre-requisites

1. Deploy the Biomarker Supervisor Agent in your AWS account by following this repository's README

2. Follow the steps for deploying the 'Bedrock Agent Evaluation Framework' found in the repository's README.md

3. Download 'hcls_trajectories.json' and place it in the data_files/ folder of the tool's repository

4. Input the relevant information in the config.py of the tool (AGENT_ID, AGENT_ALIAS_ID,DATA_FILE_PATH, and Langfuse information)

Use this data file path
```bash
DATA_FILE_PATH="data_files/hcls_trajectories.json"
```

5. Run the evaluation tool against the Biomarker Supervisor agent and the HCLS trajectories data file and see evaluation results in Langfuse