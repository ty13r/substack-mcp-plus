import {Server} from "@modelcontextprotocol/sdk/server/index.js";
import {StdioServerTransport} from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import {z} from "zod";
import {zodToJsonSchema} from "zod-to-json-schema";
import {createDraftPostSchema, createDraftPostHandler} from "./tools/create_draft_post.js";

const SESSION_ID = process.env.SESSION_ID;
if (!SESSION_ID) {
  throw new Error("SESSION_ID must be set");
}

// Create an MCP server
const server = new Server({
    name: "Substack MCP",
    version: "1.0.0"
  },
  {
    capabilities: {
      tools: {},
      resources: {}
    },
  });


server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "create_draft_post",
        description:
          "create a draft post on your Substack account.",
        inputSchema: zodToJsonSchema(createDraftPostSchema),
      }
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const {name, arguments: args} = request.params;

  try {
    switch (name) {
      case "create_draft_post": {
        const result = await createDraftPostHandler(args);
        return {
          content: [{type: "text", text: JSON.stringify(result, null, 2)}],
        };
      }
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new Error(`Invalid input: ${JSON.stringify(error.errors)}`);
    }
    throw error;
  }
});


const transport = new StdioServerTransport();
server.connect(transport).catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});