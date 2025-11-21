#!/bin/bash
# Wrapper script with hardcoded token (TEMPORARY - for testing only)
TOKEN="{{token}}"
exec $(which finch) run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN="$TOKEN" \
  -e GITHUB_TOOLSETS="default,actions,code_security,experiments" \
  ghcr.io/github/github-mcp-server \
  "$@"
