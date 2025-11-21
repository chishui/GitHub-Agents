---
inclusion: manual
repositories:
  - owner: opensearch-project
    name: neural-search
---

# Maintainer Routine Agent

This agent retrieves and summarizes the 5 most recently created issues and pull requests from configured GitHub repositories, helping maintainers quickly identify items requiring attention.

## Usage

To run this agent, use one of the following methods:

1. **Via Chat**: Type `#maintainer-routine` in the Kiro chat to trigger the agent
2. **Via Command Palette**: Search for "maintainer-routine" in the command palette
3. **Via Hook**: Create a manual hook that references this steering file

The agent will retrieve data from all configured repositories and display a formatted report.

## Configuration

You can configure which repositories to monitor by editing the `repositories` array in the frontmatter above. Each repository requires:
- `owner`: The GitHub organization or user name
- `name`: The repository name

### Example Configuration

```yaml
---
inclusion: manual
repositories:
  - owner: opensearch-project
    name: neural-search
  - owner: opensearch-project
    name: k-NN
  - owner: opensearch-project
    name: ml-commons
---
```

## What This Agent Does

1. **Retrieves Recent Issues**: Fetches the 5 most recently created open issues from each configured repository
2. **Retrieves Recent Pull Requests**: Fetches the 5 most recently created **open** pull requests from each configured repository (excludes merged and closed PRs)
3. **Formats Output**: Displays a structured report with:
   - Issue/PR number and title
   - Author username
   - Creation date
   - Assigned labels
   - A summary of the description
   - Direct link to the item on GitHub

## Requirements

- GitHub MCP server must be configured and authenticated
- You must have read access to the configured repositories

## Output Format

The agent generates a markdown report with sections for each repository, grouping issues and pull requests separately. Each item includes all relevant metadata to help you quickly triage and prioritize work.

### Example Output

```markdown
# Maintainer Routine Report
Generated: 11/20/2025, 10:30:00 AM

## Repository: opensearch-project/neural-search

### Recent Issues (Top 5)

#### #123 - Bug in neural search query
- **Author**: johndoe
- **Created**: 2025-11-19
- **Labels**: bug, priority-high
- **Description**: When executing a neural search query with specific parameters, the system returns unexpected results...
- **Link**: https://github.com/opensearch-project/neural-search/issues/123

### Recent Pull Requests (Top 5)

#### #456 - Add support for new embedding model
- **Author**: janedoe
- **Created**: 2025-11-18
- **Labels**: enhancement, documentation
- **Description**: This PR adds support for the latest embedding model and includes comprehensive documentation...
- **Link**: https://github.com/opensearch-project/neural-search/pull/456

---
```

## Troubleshooting

### GitHub MCP Not Configured

If you see an error about GitHub MCP not being available:

1. Check your MCP configuration at `.kiro/settings/mcp.json`
2. Ensure the GitHub MCP server is listed and enabled
3. Verify your GitHub Personal Access Token is set correctly
4. Restart Kiro to reload the MCP configuration

### Authentication Errors

If you see 401 or 403 errors:

1. Verify your GitHub PAT has the necessary scopes:
   - `repo` (for private repositories)
   - `public_repo` (for public repositories)
2. Check that your PAT hasn't expired
3. Ensure you have access to the configured repositories

### Rate Limiting

If you see 429 errors:

1. GitHub API has rate limits (5,000 requests/hour for authenticated users)
2. Wait a few minutes before retrying
3. Consider reducing the number of configured repositories

### No Results

If the agent returns "No issues found" or "No pull requests found":

- This is normal if the repository has no recent activity
- Verify the repository name and owner are correct
- Check that the repository exists and is accessible

## Advanced Configuration

### Multiple Repositories

You can monitor multiple repositories by adding them to the configuration:

```yaml
---
inclusion: manual
repositories:
  - owner: opensearch-project
    name: neural-search
  - owner: opensearch-project
    name: k-NN
  - owner: opensearch-project
    name: ml-commons
  - owner: myorg
    name: my-private-repo
---
```

The agent will process each repository sequentially and group results by repository in the output.

### Single Repository

For a single repository, use:

```yaml
---
inclusion: manual
repositories:
  - owner: opensearch-project
    name: neural-search
---
```

## Technical Details

- **API Calls**: The agent makes 2 API calls per repository (one for issues, one for PRs)
- **Execution Time**: Typically 2-5 seconds per repository
- **Data Freshness**: Always fetches the latest data (no caching)
- **Sorting**: Items are sorted by creation date (newest first)
- **Limit**: Returns up to 5 items per category (issues and PRs)
- **Filter**: Only fetches **open** issues and **open** pull requests (excludes closed and merged items)
- **Description Length**: Truncates descriptions to 200 characters for readability
