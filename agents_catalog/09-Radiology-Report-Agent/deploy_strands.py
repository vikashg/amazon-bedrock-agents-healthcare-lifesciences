from strands import Agent, tool
from strands_tools import calculator # Import the calculator tool
import argparse
import json
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel

app = BedrockAgentCoreApp()

from create_strands import download_guidance_document, run_validator, \
    check_radiology_report, identify_anatomical_structures
    

model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"

model = BedrockModel(model_id=model_id)
system_prompt = "You are a Radiology Report Validator, helping junior radiologist \
                    write reports in adherence to the ACR guidance criterion. Does the radiology report adheres to the ACR guidelines mentioned in the document? \
                    Is it detailed enough to provide a diagnosis? \
                    Is the report missing any key anatomical structures? \
                    Does the report meet the \
                    quality standards of the ACR guidelines? Please provide a terse actionable feedback and do not try to summarize the report itself. ?"


agent = Agent(
    model = model,
    tools =[download_guidance_document, run_validator, check_radiology_report, \
        identify_anatomical_structures],
    system_prompt = system_prompt
)

@app.entrypoint
def strands_agent_bedrock(payload):
    """Process user input through Strands agent with tool usage logging."""
    user_input = payload.get("prompt")
    print(f"🚀 AGENT INPUT: {user_input}")
    print(f"🤖 AVAILABLE TOOLS: download_guidance_document, run_validator, check_radiology_report, identify_anatomical_structures")
    
    response = agent(user_input)
    result = response.message['content'][0]['text']
    print(f"🏁 FINAL RESPONSE: {result}")
    return result

if __name__ == '__main__':
    app.run()