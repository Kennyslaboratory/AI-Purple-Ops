# Quick Adapter Generation for Pentesters

**From Burp request to working adapter in 2-3 minutes.**

This guide shows pentesters how to quickly create adapters from intercepted HTTP requests without writing Python code.

---

## Quick Start

### 1. Capture Request in Burp

Right-click on any HTTP request in Burp Suite → Copy → Copy as cURL command

### 2. Generate Adapter

```bash
aipop adapter quick --name target_app --from-curl "curl 'https://api.target.com/chat' -H 'Authorization: Bearer token123' -d '{\"message\":\"test\"}'"
```

### 3. Test It

```bash
aipop adapter test --name target_app
```

### 4. Use It

```bash
aipop run --suite quick_test --adapter target_app
aipop generate-suffix "Test prompt" --adapter target_app
```

---

## Input Methods

### From cURL (Recommended)

**Chrome/Firefox:** Right-click request → Copy → Copy as cURL

```bash
aipop adapter quick --name target_app --from-curl "curl 'https://api.target.com/v1/chat' \
  -H 'Authorization: Bearer abc123' \
  -H 'Content-Type: application/json' \
  --data-raw '{\"message\":\"hello\",\"model\":\"gpt-4\"}'"
```

### From HTTP File (Burp)

**Burp Suite:** Right-click request → Copy to file → Save as `request.txt`

```bash
aipop adapter quick --name target_app --from-http request.txt
```

### From Clipboard

Copy request (cURL or HTTP) to clipboard, then:

```bash
aipop adapter quick --name target_app --from-clipboard
```

---

## What Gets Auto-Detected

✅ **API Endpoint** - Full URL from request  
✅ **HTTP Method** - GET, POST, PUT, etc.  
✅ **Headers** - All headers preserved  
✅ **Authentication** - Bearer token, API key, custom header  
✅ **Prompt Field** - Where your prompt goes (message, input, query, etc.)  
✅ **Request Body** - All fields captured  

---

## Interactive Workflow

When auto-detection is uncertain, you'll be prompted:

```
⚠️  Could not auto-detect prompt field

Available fields in request body:
  • user_message
  • context
  • model
  • temperature

Enter prompt field name [message]: user_message

⚠️  Bearer token detected in request
Move token to environment variable? [Y/n]: Y

✓ Config generated: adapters/target_app.yaml

Test adapter now? [Y/n]: Y
```

---

## Security Best Practices

### ⚠️ Never Commit Secrets

The quick adapter tool will warn you if it detects secrets:

```
⚠️  SECURITY WARNING

Found potential secrets in config:
  • Bearer token detected in config

Best Practice:
  1. Move secrets to environment variables
  2. Edit: adapters/target_app.yaml
  3. Replace token with: ${TARGET_APP_API_KEY}
  4. Set environment variable:
     export TARGET_APP_API_KEY=your-secret-here
  5. Never commit adapter configs to git

✓ Added to .gitignore automatically
```

### Environment Variables

Edit your config and replace hardcoded tokens:

```yaml
# Before (BAD)
auth:
  type: bearer
  token: Bearer abc123def456...

# After (GOOD)
auth:
  type: bearer
  token_env_var: TARGET_APP_API_KEY
```

Then set the variable:

```bash
export TARGET_APP_API_KEY=your-token-here
# Or add to ~/.bashrc for persistence
```

---

## Editing Generated Configs

Configs are saved to `adapters/{name}.yaml` with helpful comments:

```yaml
# Auto-generated adapter config for target_app
# Edit this file if auto-detection was incorrect
# Generated: 2025-11-13 22:00:00

adapter:
  name: target_app
  type: custom_http

connection:
  base_url: https://api.target.com/v1/chat
  method: POST
  timeout: 60

auth:
  type: bearer
  # SECURITY WARNING: Do not commit secrets!
  token_env_var: TARGET_APP_API_KEY

request:
  prompt_field: message  # WHERE YOUR PROMPT GOES
  extra_fields:
    model: gpt-4
    temperature: 0.7

response:
  text_field: FIXME: Enter response field path  # FIX THIS!
  # Optional fields to extract:
  # model_field: model
  # tokens_field: usage.total_tokens

# Test: aipop adapter test target_app
# Use: aipop run --suite quick_test --adapter target_app
```

### Common Edits

**1. Fix Response Field**

If auto-detection couldn't find the response field:

```yaml
response:
  text_field: response  # Change this to match actual response structure
```

**2. Handle Nested Fields**

Use dot notation for nested JSON:

```yaml
request:
  prompt_field: data.user_input  # Nested field

response:
  text_field: result.output.text  # Deeply nested
```

**3. Add Custom Headers**

```yaml
connection:
  headers:
    User-Agent: Mozilla/5.0
    X-Custom-Header: value
```

---

## Troubleshooting

### Connection Failed

```
[red]Connection Failed[/red]

URL: https://api.target.com/chat
Error: Connection refused

Troubleshooting:
  1. Check if API endpoint is correct
  2. Verify network connectivity: curl https://api.target.com/chat
  3. Check for firewall/proxy blocking
  4. Try with --timeout 120 for slow APIs
```

**Fix:** Verify the URL is correct and accessible.

### Authentication Failed (401/403)

```
[red]Authentication Failed (401)[/red]

Auth Type: bearer

Quick Fixes:
  1. Check API key/token is valid
  2. Set environment variable:
     export TARGET_APP_API_KEY=your-key-here
  3. Verify token hasn't expired
  4. Check API permissions/rate limits
```

**Fix:** Set the correct environment variable or update token in config.

### Field Not Found

```
[red]Field Not Found[/red]

Looking for: response

Available fields:
  • data.output
  • data.status
  • metadata.model

Fix:
  1. Edit config: adapters/target_app.yaml
  2. Update 'response.text_field' to correct path
  3. Use dot notation for nested fields: data.output
```

**Fix:** Edit config and update the `response.text_field` to match actual response structure.

### Rate Limit (429)

```
[yellow]Rate Limit Exceeded (429)[/yellow]

Retry After: 60 seconds

Options:
  1. Wait and retry manually
  2. Reduce request rate (use --delay between requests)
  3. Check API rate limits for your tier
```

**Fix:** Wait or add delays between requests.

---

## Common Scenarios

### Testing API with Multiple Endpoints

Create separate adapters for each endpoint:

```bash
# Chat endpoint
aipop adapter quick --name target_chat --from-curl "curl 'https://api.target.com/chat' ..."

# Completion endpoint  
aipop adapter quick --name target_complete --from-curl "curl 'https://api.target.com/complete' ..."

# Use whichever you need
aipop run --suite redteam --adapter target_chat
```

### Testing with Different Models

Some APIs let you specify models in the request:

```yaml
request:
  extra_fields:
    model: gpt-4  # Change this to test different models
```

### APIs with Unusual Response Formats

For APIs that return text in non-standard ways:

```yaml
response:
  # Simple field
  text_field: output
  
  # Nested field
  text_field: data.completions.0.text
  
  # Array element
  text_field: choices.0.message.content
```

---

## Examples

### OpenAI-Compatible API

```bash
aipop adapter quick --name custom_openai --from-curl "curl 'https://custom.ai/v1/chat/completions' \
  -H 'Authorization: Bearer sk-...' \
  -d '{\"model\":\"gpt-4\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}'"
```

Result: Works immediately with OpenAI-compatible endpoints.

### Custom Internal API

```bash
aipop adapter quick --name internal_llm --from-curl "curl 'http://internal.corp:8080/api/infer' \
  -H 'X-API-Key: abc123' \
  -d '{\"text\":\"hello\",\"max_len\":100}'"
```

Edit config to fix field names:

```yaml
request:
  prompt_field: text  # Not "message"
  extra_fields:
    max_len: 1000

response:
  text_field: result  # Not "response"
```

### API with Complex Auth

For APIs using custom auth schemes:

```yaml
auth:
  type: header
  header_name: X-Custom-Auth
  token_env_var: CUSTOM_API_KEY
```

---

## Advanced Tips

### Testing Multiple Prompts

```bash
# Create prompts file
echo "Test prompt 1" > prompts.txt
echo "Test prompt 2" >> prompts.txt

# Batch test
aipop batch-attack prompts.txt --adapter target_app
```

### Measuring Response Times

```bash
aipop adapter test --name target_app --prompt "Quick test"
```

Shows latency in ms for performance assessment.

### Using in Recipes

Add your adapter to recipes:

```yaml
# recipes/my_pentest.yaml
steps:
  - name: test_target
    command: run
    args:
      suite: adversarial
      adapter: target_app
```

---

## Comparison: Quick vs Traditional

### Traditional Method (10-20 min)

1. Create Python file: `user_adapters/target.py`
2. Import dependencies
3. Write `__init__` method
4. Write `invoke` method
5. Handle auth, parsing, errors
6. Debug imports and types
7. Test and iterate

### Quick Method (<3 min)

1. Copy request from Burp
2. `aipop adapter quick --name target --from-curl "..."`
3. Done ✅

---

## When to Use Quick Adapters

✅ **Perfect For:**
- Pentesting engagements (need speed)
- Testing custom/internal APIs
- Prototyping before writing Python
- Air-gapped environments (no time for dev)
- Quick security assessments

❌ **Not Ideal For:**
- Complex auth flows (OAuth, SAML)
- APIs with multiple endpoints (need orchestration)
- WebSocket/streaming APIs
- Custom protocol transformations

For complex scenarios, use the traditional Python adapter approach.

---

## Getting Help

If you encounter issues:

1. **Check config:** `cat adapters/target_app.yaml`
2. **Test manually:** `aipop adapter test --name target_app`
3. **Check logs:** Look for detailed error messages
4. **Compare with Burp:** Verify request matches what works in Burp
5. **Report bugs:** github.com/Kennyslaboratory/AI-Purple-Ops/issues

---

## Next Steps

After creating your adapter:

1. **Test thoroughly:** Try various prompts
2. **Run security tests:** `aipop run --suite adversarial --adapter target_app`
3. **Try jailbreaks:** `aipop generate-suffix "Test" --method pair --adapter target_app`
4. **Batch test:** Create prompt file and run batch mode
5. **Document findings:** Use evidence pack generation

**Remember:** Quick adapters are for speed. For production use or complex scenarios, consider writing a full Python adapter.

---

**Happy pentesting! 🔒**

