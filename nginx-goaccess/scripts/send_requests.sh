#!/bin/bash

REQUEST_URL="http://localhost:81/v1/chat/completions"

MODEL_NAME="qwen/qwen3-vl-4b"

# Number of requests (default: 10)
NUM_REQUESTS=${1:-10}

# Array of random questions
QUESTIONS=(
    "Hello! What is Python?"
    "Explain machine learning in simple terms"
    "What are the benefits of Docker containers?"
    "How does HTTP work?"
    "What is the difference between REST and GraphQL?"
    "Explain what is artificial intelligence"
    "What are microservices?"
    "How do databases work?"
    "What is cloud computing?"
    "Explain version control with Git"
    "What is the purpose of load balancers?"
    "How does encryption work?"
    "What are APIs and how are they used?"
    "Explain the concept of DevOps"
    "What is the difference between SQL and NoSQL?"
)

echo "Sending $NUM_REQUESTS requests to $REQUEST_URL"

for i in $(seq 1 $NUM_REQUESTS); do
    # Get random question
    RANDOM_INDEX=$((RANDOM % ${#QUESTIONS[@]}))
    QUESTION="${QUESTIONS[$RANDOM_INDEX]}"
    
    echo "Request $i: $QUESTION"
    
    curl -X POST $REQUEST_URL \
      -H "Content-Type: application/json" \
      -d "{
        \"model\": \"$MODEL_NAME\",
        \"messages\": [
          {\"role\": \"user\", \"content\": \"$QUESTION\"}
        ],
        \"temperature\": 0.7,
        \"max_tokens\": 1000
      }" \
      --silent --output /dev/null
    
    # Small delay between requests
    sleep 0.5
done

echo "Completed $NUM_REQUESTS requests"
