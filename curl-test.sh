#!/bin/bash

# config
URL="http://localhost:5000/api/timeline_post"

# 1. Generate random details for the test post
RANDOM_NUM=$RANDOM
TEST_NAME="User_$RANDOM_NUM"
TEST_EMAIL="user_$RANDOM_NUM@mlh.io"
TEST_CONTENT="Automated test entry post number $RANDOM_NUM"

echo "=== STARTING TIMELINE API TEST ==="

# 2. Test POST Endpoint (Matches the exact styling from the images using -d flags)
echo "Sending POST request..."
POST_RESPONSE=$(curl -s -X POST "$URL" \
  -d "name=$TEST_NAME" \
  -d "email=$TEST_EMAIL" \
  -d "content=$TEST_CONTENT")

echo "POST Response:"
echo "$POST_RESPONSE"

# Extract the database assigned ID for cleanup using pattern matching
POST_ID=$(echo "$POST_RESPONSE" | grep -o '"id":[0-9]*' | sed 's/"id"://')

if [ -z "$POST_ID" ]; then
    echo "Failure: Could not parse database ID from the POST response."
    exit 1
fi

# 3. Test GET Endpoint (Verifies the freshly inserted record is present in the feed)
echo "Sending GET request to verify insertion..."
GET_RESPONSE=$(curl -s "$URL")

echo "GET Response:"
echo "$GET_RESPONSE"

# Check if our unique random user exists in the returned payload
if echo "$GET_RESPONSE" | grep -q "$TEST_NAME"; then
    echo "Success: The newly created timeline post was found in the GET payload."
else
    echo "Failure: The timeline post was not found in the GET payload."
    exit 1
fi

# 4. BONUS: Clean up the database by hitting the DELETE endpoint
echo "Sending DELETE request for teardown..."
DELETE_RESPONSE=$(curl -s -X DELETE "$URL/$POST_ID")

echo "DELETE Response:"
echo "$DELETE_RESPONSE"

