#!/bin/bash
# Extract Jenkins API token from built Docker image

set -e

IMAGE_NAME="${1:-laser-ci-jenkins}"

echo "Extracting API token from Docker image: $IMAGE_NAME"
echo

# Create a temporary container to extract the token
CONTAINER_ID=$(docker create "$IMAGE_NAME" /bin/true)

# Extract the token file
if docker cp "$CONTAINER_ID:/var/jenkins_home/api-token.txt" /tmp/jenkins-token.txt 2>/dev/null; then
    API_TOKEN=$(cat /tmp/jenkins-token.txt)
    rm /tmp/jenkins-token.txt

    echo "=================================================="
    echo "  Jenkins API Token from Docker Image"
    echo "=================================================="
    echo "Image: $IMAGE_NAME"
    echo "Token: $API_TOKEN"
    echo
    echo "Add to GitLab CI/CD variables:"
    echo "JENKINS_API_TOKEN: \"$API_TOKEN\""
    echo "=================================================="
else
    echo "❌ Could not extract API token from image"
    echo "Make sure the image was built with token generation"
    exit 1
fi

# Clean up
docker rm "$CONTAINER_ID" >/dev/null

echo
echo "✅ Token extracted successfully!"
