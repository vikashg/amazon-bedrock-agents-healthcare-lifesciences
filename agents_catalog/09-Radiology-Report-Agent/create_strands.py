from strands import Agent, tool
import argparse
import json
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel
import os

@tool
def download_guidance_document(anatomical_structure):
    """
    he function downloads the appropriate documents from the S3 bucket
    for validating the report. The documents are downloaded to the local
    directory where the lambda function is running. 
    """
    print(f"🔧 TOOL CALLED: download_guidance_document with structure: {anatomical_structure}")
    logger.info("Downloading guidance document")
    s3 = boto3.client('s3')
    bucket_name = "radiologyreport-validator"
    response = s3.list_objects_v2(Bucket = bucket_name)
    files = [obj['Key'] for obj in response['Contents']]
    s3_resource = boto3.resource('s3')
    download_dir = '/tmp'
    
    logger.info("Anatomical structure: ", anatomical_structure)
    res_files =[]
    for _file in files:
        if anatomical_structure.title() in _file and _file.endswith(".pdf"):
            logger.info(_file)
            response = s3.get_object(Bucket = bucket_name, Key = _file)
            # download the file object from S3 to local using boto3
            # Get the basename of the file
            basename = os.path.basename(_file)
            s3_resource.Bucket(bucket_name).download_file(_file, 
                            os.path.join(download_dir, basename))
            res_files.append(basename)
            logger.info("Downloaded guidance document")
            # Here are the downloaded files 
            logger.info(os.listdir(download_dir))
    
    if len(res_files) > 0:
        print(f"✅ TOOL RESULT: SUCCESS - Downloaded {len(res_files)} files")
        return 'SUCCESS'
    else:
        print(f"✅ TOOL RESULT: FAILURE - No files found")
        return 'FAILURE'
            

@tool
def run_validator(text):
    print(f"🔧 TOOL CALLED: run_validator with text: {text[:100]}...")
    validation_document_dir = '/tmp'
    validation_documents = os.listdir(validation_document_dir)
    if len(validation_documents) == 0:
        return "No validation documents found. Please upload the validation documents to the S3 bucket."    
    elif len(validation_documents) > 0:

        prompt_postpend = "Does the above radiology report adheres to the ACR guidelines mentioned in the document? \
        Is it detailed enough to provide a diagnosis? \
        Is the report missing any key anatomical structures? \
        Does the report meet the \
        quality standards of the ACR guidelines? Please provide a terse actionable feedback and do not try to summarize the report itself. ?"
        prompt = prompt_postpend + " " + text

        val_doc = os.path.join(validation_document_dir,validation_documents[0])
        print("Validation document: ", val_doc)
        with open(val_doc, 'rb') as file:
            pdf_bytes = file.read()
        messages =[
        {
        "role": "user",
        "content": [
        {
            "document": {
                "format": "pdf",
                "name": "DocumentPDFmessages",
                "source": {
                    "bytes":  pdf_bytes
                }
            }
        },
        {"text": prompt        }
        ]
        }
        ]
        inf_params = {"maxTokens": 200, "topP": 0.1, "temperature": 0.3}
        model_response = bedrock_agent_client.converse(modelId=MODEL_ID, messages=messages, inferenceConfig=inf_params)
        response_text = model_response['output']['message']['content'][0]['text']
        print("***************Tested***************")
        print(f"✅ TOOL RESULT: {response_text}")
        return response_text

@tool
def check_radiology_report(text):
    """Check radiology report for anatomical structures and diagnostic adequacy."""
    print(f"🔧 TOOL CALLED: check_radiology_report with text: {text[:100]}...")
    prompt = f"Does this radiology report contain proper anatomical structures? Is it detailed enough for diagnosis? Provide terse actionable feedback.\n\nReport: {text}"
    from strands_tools import use_llm
    result = use_llm(prompt, max_tokens=200, temperature=0.1)
    print(f"✅ TOOL RESULT: {result}")
    return result
        
    
@tool
def identify_anatomical_structures(report):
    """Identify anatomical structures in the radiology report using LLM."""
    print(f"🔧 TOOL CALLED: identify_anatomical_structures with report: {report[:100]}...")
    from strands_tools import use_llm
    
    result = use_llm(
        f"Extract anatomical structures from this radiology report. Return only from this list: Brain, Spine, Chest, Abdomen, Pelvis, Extremities, Transthoracic, Echocardiography\n\nReport: {report}\n\nReturn only the matching structures, comma-separated:",
        max_tokens=50,
        temperature=0.1
    )
    print(f"✅ TOOL RESULT: {result}")
    return result


model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
model = BedrockModel(
    model_id=model_id,
)

system_prompt = "You are a Radiology Report Validator, helping junior radiologist \
                    write reports in adherence to the ACR guidance criterion. Does the radiology report adheres to the ACR guidelines mentioned in the document? \
                    Is it detailed enough to provide a diagnosis? \
                    Is the report missing any key anatomical structures? \
                    Does the report meet the \
                    quality standards of the ACR guidelines? Please provide a terse actionable feedback and do not try to summarize the report itself. ?"


agent = Agent(
    model=model,
    tools=[identify_anatomical_structures, check_radiology_report, run_validator, download_guidance_document],
    system_prompt=system_prompt,
)

def strands_agent_bedrock(payload):
    """Process user input through Strands agent with tool usage logging."""
    user_input = payload.get("prompt")
    print(f"🚀 AGENT INPUT: {user_input}")
    print(f"🤖 AVAILABLE TOOLS: identify_anatomical_structures, check_radiology_report, run_validator, download_guidance_document")
    
    response = agent(user_input)
    result = response.message['content'][0]['text']
    print(f"🏁 FINAL RESPONSE: {result}")
    return result

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("payload", type=str)
    # args = parser.parse_args()
    # print(args.payload)
    test_query = "Transthoracic echocardiogram was performed of technically limited quality. \
    The left ventricle was normal in size and dimensions with normal LV function. Ejection fraction \
    was 50% to 55%. Concentric hypertrophy noted with interventricular septum measuring 1.6 cm, \
    posterior wall measuring 1.2 cm. Left atrium is enlarged, measuring 4.42 cm. \
    Right-sided chambers are normal in size and dimensions. Aortic root has normal diameter. \
    Mitral and tricuspid valve reveals annular calcification. Fibrocalcific valve leaflets noted \
    with adequate excursion. Similar findings noted on the aortic valve as well with \
    significantly adequate excursion of valve leaflets. Atrial and ventricular septum are intact.\
    Pericardium is intact without any effusion. No obvious intracardiac mass or thrombi noted. \
    Doppler study reveals mild-to-moderate mitral regurgitation. Severe aortic stenosis with peak \
    velocity of 2.76 with calculated ejection fraction 50% to 55% with severe aortic stenosis. There is also mitral stenosis."

    test = '{"prompt": "' + test_query + '"}'
    response = strands_agent_bedrock(json.loads(test))
    