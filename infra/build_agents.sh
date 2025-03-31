#!/bin/bash

# Debug: Print current location and S3 bucket
echo "Current directory: $(pwd)"
echo "S3 Bucket: ${S3_BUCKET}"

# Process agent templates from agents_catalog
cd agents_catalog || exit
echo "Processing agent templates..."

# Array of agent directories and their templates
AGENT_TEMPLATES=(
    "1-Biomarker-database-analyst/Biomarker-database-analyst.yaml"
    "2-Clinical-evidence-researcher/Clinical-evidence-researcher.yaml"
    "3-Medical-imaging-expert/Medical-imaging-expert.yaml"
    "4-Statistician/Statistician.yaml"
    "5-Biological-pathways-analyst/Biological-pathways-analyst.yaml"
)

# Process each agent template
for agent_path in "${AGENT_TEMPLATES[@]}"; do
    if [ -f "${agent_path}" ]; then
        echo "Found agent file: ${agent_path}"
        agent_name=$(basename "${agent_path}" .yaml)
        echo "Packaging agent: ${agent_name}"
        aws cloudformation package \
            --template-file "${agent_path}" \
            --s3-bucket "${S3_BUCKET}" \
            --output-template-file "../packaged_${agent_name}.yaml"
        
        # Copy to S3 immediately after packaging
        aws s3 cp "../packaged_${agent_name}.yaml" "s3://${S3_BUCKET}/packaged_${agent_name}.yaml"
    fi
done
cd ..

# Process Supervisor agent template
cd multi_agent_collaboration/cancer_biomarker_discovery || exit
echo "Processing supervisor agent template..."
if [ -f "supervisor_agent.yaml" ]; then
    echo "Packaging supervisor agent"
    aws cloudformation package \
        --template-file supervisor_agent.yaml \
        --s3-bucket "${S3_BUCKET}" \
        --output-template-file "../../packaged_supervisor_agent.yaml"
    
    # Copy to S3 immediately after packaging
    aws s3 cp "../../packaged_supervisor_agent.yaml" "s3://${S3_BUCKET}/packaged_supervisor_agent.yaml"
fi
cd ../..

# Process agent build template
echo "Processing agent build template..."
if [ -f "infra/agent_build.yaml" ]; then
    echo "Packaging agent build template"
    aws cloudformation package \
        --template-file infra/agent_build.yaml \
        --s3-bucket "${S3_BUCKET}" \
        --output-template-file "infra/packaged_agent_build.yaml"
    
    # Copy to S3
    aws s3 cp "infra/packaged_agent_build.yaml" "s3://${S3_BUCKET}/packaged_agent_build.yaml"
fi

# Process streamlit app
if [ -d "streamlitapp" ] && [ -f "streamlitapp/streamlit_build.yaml" ]; then
    echo "Processing streamlit app..."
    cd streamlitapp || exit
    aws cloudformation package \
        --template-file streamlit_build.yaml \
        --s3-bucket "${S3_BUCKET}" \
        --output-template-file "../packaged_streamlit_build.yaml"
    
    # Copy to S3
    aws s3 cp "../packaged_streamlit_build.yaml" "s3://${S3_BUCKET}/packaged_streamlit_build.yaml"
    cd ..
fi

echo "All templates packaged and uploaded to S3"
