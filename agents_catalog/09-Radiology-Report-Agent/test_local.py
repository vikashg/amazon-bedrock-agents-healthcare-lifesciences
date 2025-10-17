from deploy_strands import strands_agent_bedrock

# Test locally instead of deploying
test_payload = {"prompt": "Transthoracic echocardiogram was performed of technically limited quality. The left ventricle was normal in size and dimensions with normal LV function."}

result = strands_agent_bedrock(test_payload)
print(f"Result: {result}")