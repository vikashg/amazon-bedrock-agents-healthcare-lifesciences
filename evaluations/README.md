# Biomarker Multi-Agent Evaluation

Provided in this folder is a data file 'hcls_trajectories.json'. This data file can be run against the [Bedrock Agent Evaluation Framework](https://github.com/aws-samples/amazon-bedrock-agent-evaluation-framework/tree/main). 

# Pre-requisites

1. Deploy the Biomarker Supervisor Agent in your AWS account by going to the multi_agent_orchestration/ folder of this repository and following instructions there

2. Follow steps for cloning the 'Bedrock Agent Evaluation Framework' found in the the [README.md](https://github.com/aws-samples/amazon-bedrock-agent-evaluation-framework/tree/main?tab=readme-ov-file#amazon-bedrock-agent-evaluation) 

# Evaluation Steps

1. Familiarize yourself with the 'Bring Your Own Agent' option in Bedrock Agent Evaluation Framework [README](https://github.com/aws-samples/amazon-bedrock-agent-evaluation-framework/tree/main?tab=readme-ov-file#option-1-bring-your-own-agent-to-evaluate)

2. Download the 'hcls_trajectories.json' file from this folder and place it in the data_files/ folder of the tool's repository

3. Input the relevant information specific to the Biomarker Agent and data file in the config.py of the tool (AGENT_ID, AGENT_ALIAS_ID, DATA_FILE_PATH, and Langfuse information)

Use this data file path
```bash
DATA_FILE_PATH="data_files/hcls_trajectories.json"
```

4. Run the evaluation tool against the Biomarker Supervisor agent with the trajectories data file and see evaluation results in Langfuse!