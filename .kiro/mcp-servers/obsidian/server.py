#!/usr/bin/env python3
import asyncio
import json
import sys
import os
import httpx
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import Tool, TextContent

load_dotenv()

OBSIDIAN_URL = "https://127.0.0.1:27124"
OBSIDIAN_TOKEN = os.getenv("OBSIDIAN_TOKEN")

app = Server("obsidian")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="create_note",
            description="Create or update a note in Obsidian",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the note (e.g., 'folder/note.md')"},
                    "content": {"type": "string", "description": "Content of the note in markdown"}
                },
                "required": ["path", "content"]
            }
        ),
        Tool(
            name="read_note",
            description="Read a note from Obsidian",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the note"}
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="list_notes",
            description="List all notes in the vault",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="search_notes",
            description="Search for notes in the vault",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    async with httpx.AsyncClient(verify=False) as client:
        headers = {"Authorization": f"Bearer {OBSIDIAN_TOKEN}"}
        
        if name == "create_note":
            path = arguments["path"]
            if not path.endswith(".md"):
                path += ".md"
            response = await client.put(
                f"{OBSIDIAN_URL}/vault/{path}",
                data=arguments["content"],
                headers={**headers, "Content-Type": "text/markdown"}
            )
            if response.status_code in [200, 201, 204]:
                return [TextContent(type="text", text=f"Note created/updated successfully: {path}")]
            else:
                return [TextContent(type="text", text=f"Error creating note: {response.text}")]
        
        elif name == "read_note":
            path = arguments["path"]
            if not path.endswith(".md"):
                path += ".md"
            response = await client.get(f"{OBSIDIAN_URL}/vault/{path}", headers=headers)
            return [TextContent(type="text", text=response.text)]
        
        elif name == "list_notes":
            response = await client.get(f"{OBSIDIAN_URL}/vault/", headers=headers)
            data = response.json()
            files = data.get("files", [])
            md_files = [f for f in files if f.endswith(".md")]
            return [TextContent(type="text", text="\n".join(md_files))]
        
        elif name == "search_notes":
            response = await client.post(
                f"{OBSIDIAN_URL}/search/simple/",
                headers=headers,
                json={"query": arguments["query"]}
            )
            return [TextContent(type="text", text=json.dumps(response.json(), indent=2))]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
