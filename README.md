docker build -t substack-mcp .

docker run -i --rm --name substack-mcp -e SESSION_ID=123 substack-mcp