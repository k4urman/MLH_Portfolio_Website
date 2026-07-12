#!/bin/bash

BASE_URL="http://127.0.0.1:5000"

RANDOM_NUMBER=$RANDOM
NAME="test user $RANDOM_NUMBER"
EMAIL="test-$RANDOM_NUMBER@example.com"
CONTENT="test post from curl $RANDOM_NUMBER"

echo "Initiating the creation process for a brand new timeline post..."
echo "name: $NAME"
echo "email: $EMAIL"
echo "content: $CONTENT"

POST_RESPONSE=$(curl -s -X POST "$BASE_URL/api/timeline_post" \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")

echo "Received the following response data from the POST endpoint:"
echo "$POST_RESPONSE"

POST_ID=$(echo "$POST_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

echo "Querying the GET endpoint to verify that the newly created timeline post successfully appears in the records..."
GET_RESPONSE=$(curl -s "$BASE_URL/api/timeline_post")

echo "Received the following response data from the GET endpoint:"
echo "$GET_RESPONSE"

if echo "$GET_RESPONSE" | grep -q "$CONTENT"; then
  echo "Validation success: The created timeline post content matches and was successfully found in the timeline records!"
else
  echo "Critical error execution halted: The timeline post content could not be located in the response from the server."
  exit 1
fi

echo "Sending a request to purge and permanently delete the temporary test timeline post from the system..."
curl -s -X DELETE "$BASE_URL/api/timeline_post/$POST_ID"
echo ""

echo "All testing phases have finished executing successfully."
