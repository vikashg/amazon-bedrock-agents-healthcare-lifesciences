#!/bin/bash

# Process Subagent templates
cd agents
for agent_file in *.yaml; do
  if [ -f "${agent_file}" ]; then
    echo "Found agent file: ${agent_file}"
    agent_name=$(basename "${agent_file}" .yaml)
    echo "Packaging agent: ${agent_name}"
    aws cloudformation package \
      --template-file "${agent_file}" \
      --s3-bucket ${S3_BUCKET} \
      --output-template-file "../packaged_${agent_name}.yaml"
  fi
done
cd ..

# Process Supervisor agent template
cd "Supervisor agent"
if [ -f "supervisor_agent.yaml" ]; then
  echo "Packaging supervisor agent"
  aws cloudformation package \
    --template-file supervisor_agent.yaml \
    --s3-bucket ${S3_BUCKET} \
    --output-template-file "../packaged_supervisor_agent.yaml"
fi
cd ..

# Process agent build template
if [ -f "agent_build.yaml" ]; then
  echo "Packaging agent build template"
  aws cloudformation package \
    --template-file agent_build.yaml \
    --s3-bucket ${S3_BUCKET} \
    --output-template-file "packaged_agent_build.yaml"
fi

# Process streamlit app
if [ -d "streamlitapp" ]; then
  cd streamlitapp
  if [ -f "streamlit_build.yaml" ]; then
    echo "Packaging streamlit app"
    aws cloudformation package \
      --template-file streamlit_build.yaml \
      --s3-bucket ${S3_BUCKET} \
      --output-template-file "../packaged_streamlit_build.yaml"
  fi
  cd ..
fi

# Copy packaged templates to S3
for packaged_file in packaged_*.yaml; do
  if [ -f "${packaged_file}" ]; then
    echo "Copying ${packaged_file} to S3"
    aws s3 cp "${packaged_file}" "s3://${S3_BUCKET}/${packaged_file}"
  fi
done

echo "All templates packaged and uploaded to S3"