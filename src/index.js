#!/usr/bin/env node

import {Server} from "@modelcontextprotocol/sdk/server/index.js";
import {StdioServerTransport} from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import {z} from "zod";
import {zodToJsonSchema} from "zod-to-json-schema";
import {createDraftPostSchema, createDraftPostHandler} from "./tools/create_draft_post.js";

// Create an MCP server
const server = new Server({
    name: "Substack MCP",
    version: "1.0.0"
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      logging: {}
    },
  });

// check envs
if (!process.env.SUBSTACK_PUBLICATION_URL || !process.env.SUBSTACK_SESSION_TOKEN || !process.env.SUBSTACK_USER_ID) {
  throw new Error("SUBSTACK_PUBLICATION_URL, SUBSTACK_SESSION_TOKEN and SUBSTACK_USER_ID must be set");
}

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
server.connect(transport).catch(() => {
  process.exit(1);
});