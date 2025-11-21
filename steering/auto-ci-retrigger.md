---
inclusion: manual
---

# Auto CI Retrigger Agent

## Configuration

**GitHub Username**: `{{username}}`

**Target Repositories**: Only check PRs in these repositories:
- `opensearch-project/neural-search`
- `opensearch-project/OpenSearch`

When invoked, this agent will:

1. **Find Latest PR**: Identify the most recent pull request for the current user in the configured repositories
2. **Check CI Status**: Examine all CI workflows and their completion status
3. **Analyze Failures**: For any failed CI items:
   - Retrieve and analyze job logs
   - Determine if failure is due to flakiness (timeouts, network issues, race conditions, intermittent test failures)
   - Determine if failure is due to actual implementation errors (compilation errors, assertion failures, logic bugs)
4. **Retrigger Flaky Tests**: Automatically rerun failed jobs that are identified as flaky
5. **Report**: Provide a summary of:
   - CI items that passed
   - Flaky failures that were retriggered
   - Genuine failures requiring code fixes

## Flakiness Indicators

Consider a failure as flaky if logs show:
- Network timeouts or connection errors
- Race conditions or timing issues
- Resource unavailability (503, 429 errors)
- Infrastructure failures
- Intermittent test failures with no code changes
- "Unable to connect" or "timeout" messages

## Implementation Error Indicators

Consider a failure as genuine if logs show:
- Compilation or build errors
- Test assertion failures with clear error messages
- Linting or type checking errors
- Security vulnerabilities
- Code coverage drops
- Consistent failures across multiple runs

## Tools to Use

- Use GitHub MCP tools to:
  - `mcp_github_search_pull_requests` with author:"{{username}}" and repo filter to find latest PR in configured repositories only (no need to call get_me)
  - `mcp_github_pull_request_read` with method "get_status" to check CI status
  - `mcp_github_list_workflow_runs` to get workflow details
  - `mcp_github_get_job_logs` with failed_only=true to analyze failures
  - `mcp_github_rerun_failed_jobs` to retrigger flaky tests

## Output Format

Provide a clear summary:
```
✅ Passed: [list of passed CI items]
🔄 Retriggered (Flaky): [list with reason]
❌ Failed (Needs Fix): [list with error summary]
```
