# Biomarker Multi-Agent Evaluation

This folder provides resources need to evaluate a Biomarker Supervisor Agent against the [Bedrock Agent Evaluation Framework](https://github.com/aws-samples/amazon-bedrock-agent-evaluation-framework/tree/main). 

# Pre-requisites

1. Deploy the Biomarker Supervisor Agent in your AWS account by going to the multi_agent_orchestration/ folder of this repository and following instructions there

# Evaluation Steps

1. Create a SageMaker Notebook instance in your AWS account

2. Open a terminal in it and clone this repository to the SageMaker/ folder

```bash
cd SageMaker/
git clone https://github.com/aws-samples/amazon-bedrock-agents-cancer-biomarker-discovery.git
```

3. Navigate to the multi-agent-collaboration branch within the repository

```bash
cd amazon-bedrock-agents-cancer-biomarker-discovery
```
```bash
git checkout multi-agent-collaboration
```

4. Go to the evaluations folder
```bash
cd evaluations
```

5. Open the 'evaluate_biomarker_agent.ipynb' notebook and follow the steps there