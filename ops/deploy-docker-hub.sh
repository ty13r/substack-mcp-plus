#!/bin/bash
set -e

# Validate environment variables
if [ -z "$DOCKERHUB_USERNAME" ]; then
  echo "Error: DOCKERHUB_USERNAME is not set"
  exit 1
fi

if [ -z "$DOCKERHUB_TOKEN" ]; then
  echo "Error: DOCKERHUB_TOKEN is not set"
  exit 1
fi

export REGISTRY_NAMESPACE="marcomoauro"

echo "Logging in to Docker Hub..."
echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

# Set repository name
REPO="${REGISTRY_NAMESPACE}/substack-mcp"

# Initialize tags array
TAGS=()

# Always add SHA tag
SHA=$(git rev-parse --short HEAD)
TAGS+=("$REPO:$SHA")

# Check if we're on a tag
if [[ "$GITHUB_REF" == refs/tags/* ]]; then
  VERSION=${GITHUB_REF#refs/tags/}
  TAGS+=("$REPO:$VERSION")
fi

# Check if we're on a branch other than main
if [[ "$GITHUB_REF" == refs/heads/* && "$GITHUB_REF" != "refs/heads/main" ]]; then
  BRANCH=${GITHUB_REF#refs/heads/}
  TAGS+=("$REPO:$BRANCH")
fi

# Always add latest tag
TAGS+=("$REPO:latest")

# Ensure buildx builder exists
if ! docker buildx inspect multiarch-builder >/dev/null 2>&1; then
  docker buildx create --name multiarch-builder --use
else
  docker buildx use multiarch-builder
fi

echo "Building and pushing multi-arch image..."

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  $(for TAG in "${TAGS[@]}"; do echo --tag "$TAG"; done) \
  --push \
  .

echo "✅ Multi-arch Docker build and push completed successfully!"