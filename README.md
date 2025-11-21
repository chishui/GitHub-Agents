This repo includes agents around GitHub work. Agents are in steering folder as Kiro's agent files but they can be definitely used by other platform.
## Configure GitHub MCP server in Kiro

1. **Install Finch or Docker**
   - macOS: `brew install finch` or install Docker Desktop
   - Linux: Install Finch or Docker via your package manager

2. **Create a GitHub Personal Access Token**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - You can use either:
     - **Tokens (classic)** - Recommended for full functionality
       - Generate a new token with these scopes:
         - `repo` (full control of private repositories)
         - `workflow` (update GitHub Action workflows)
         - `read:org` (read org and team membership)
     - **Fine-grained tokens** - More secure but with limitations
       - Note: For public repositories you don't own, fine-grained tokens only have read permission. This means you won't be able to perform write operations like adding comments to PRs you created in repositories you don't own.

3. **Set up the wrapper script**
   - Copy `scripts/github-mcp-wrapper.sh` to your home directory or another location in your PATH
   - Edit the script and replace `{{token}}` with your actual GitHub token
   - Make it executable: `chmod +x ~/github-mcp-wrapper.sh`

4. **Configure Kiro MCP**
   - Add this to `.kiro/settings/mcp.json`:
   ```json
   {
     "mcpServers": {
       "github": {
         "command": "/path/to/your/github-mcp-wrapper.sh",
         "args": [],
         "env": {},
         "disabled": false
       }
     }
   }
   ```
   - Replace `/path/to/your/github-mcp-wrapper.sh` with the actual path

5. **Restart Kiro** or reconnect the MCP server from the MCP Server view

## Agent List

### Maintainer's daily Routine
Retrieves and summarizes the 5 most recently created issues and pull requests from configured GitHub repositories, helping maintainers quickly identify items requiring attention. The agent provides a formatted report with issue/PR details, authors, labels, and descriptions.

### Auto check for PR's CI failure and rerun failed jobs
Automatically monitors your latest pull requests for CI failures, analyzes job logs to distinguish between flaky tests (network issues, timeouts, race conditions) and genuine implementation errors, then automatically retriggers flaky tests while reporting failures that need code fixes.