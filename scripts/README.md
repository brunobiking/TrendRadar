# TrendRadar Scripts

Helper scripts for managing and configuring TrendRadar.

## check_ai_config.py

Validates and tests AI provider configurations for TrendRadar's MCP features.

### Features

- ✅ Validates YAML syntax and structure
- ✅ Checks required fields for each provider type
- ✅ Tests connectivity to enabled providers
- ✅ Shows available models for connected providers
- ✅ Provides clear error messages and debugging info
- ✅ Color-coded output for easy reading

### Usage

#### Basic Validation

```bash
# Validate the default configuration file
python scripts/check_ai_config.py

# Validate a custom configuration file
python scripts/check_ai_config.py --config path/to/config.yaml
```

#### Test Connectivity

```bash
# Validate and test connectivity to enabled providers
python scripts/check_ai_config.py --test-connectivity

# Verbose output with detailed information
python scripts/check_ai_config.py --test-connectivity --verbose
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `--config CONFIG_FILE` | Path to AI providers config file (default: `config/ai_providers.yaml`) |
| `--test-connectivity` | Test actual connectivity to enabled providers |
| `--verbose` | Show detailed output including configuration fields |
| `--help` | Show help message and exit |

### Examples

#### Example 1: First-time Setup

```bash
# Copy the example configuration
cp config/ai_providers.yaml.example config/ai_providers.yaml

# Edit the configuration with your preferences
nano config/ai_providers.yaml

# Validate the configuration
python scripts/check_ai_config.py
```

#### Example 2: Enable Ollama (Local, Free)

```bash
# Install Ollama from https://ollama.com
ollama pull llama3

# Validate and test Ollama connectivity
python scripts/check_ai_config.py --test-connectivity
```

Expected output:
```
Provider: ollama
  Type: ollama
  Enabled: True
✓ Configuration is valid

Testing: ollama
✓ Connected successfully. Available models: llama3, qwen2.5
```

#### Example 3: Enable OpenAI

```bash
# Set your API key as environment variable
export OPENAI_API_KEY="sk-..."

# Edit config to enable OpenAI
nano config/ai_providers.yaml

# Test connectivity
python scripts/check_ai_config.py --test-connectivity
```

#### Example 4: Debugging Connection Issues

```bash
# Run with verbose output to see detailed error information
python scripts/check_ai_config.py --test-connectivity --verbose
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All provider configurations are valid |
| `1` | Some providers have configuration errors |

### Common Issues

#### Environment Variable Not Set

**Error:**
```
✗ Configuration has errors:
    - Environment variable not set: ${OPENAI_API_KEY}
```

**Solution:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

#### Ollama Not Running

**Error:**
```
✗ Connection refused. Is Ollama running? Start it with: ollama serve
```

**Solution:**
```bash
# Ollama usually auto-starts, but you can manually start it:
ollama serve

# Or check if it's running:
ollama list
```

#### Invalid API Key

**Error:**
```
✗ Authentication failed. Check your API key.
```

**Solution:**
- Verify your API key is correct
- Check API key permissions in provider dashboard
- Ensure no extra spaces or characters
- Verify environment variable is set correctly

### Provider-Specific Notes

#### Ollama (Local)
- Requires Ollama to be installed and running
- No API key needed
- Test endpoint: `http://localhost:11434/api/tags`
- Change port if 11434 is in use

#### OpenAI / OpenAI-Compatible
- Requires API key
- Test endpoint: `/v1/models`
- Check rate limits and billing

#### Anthropic Claude
- Requires API key from https://console.anthropic.com
- Uses different API format than OpenAI

#### Google Gemini
- Requires API key from https://makersuite.google.com
- Free tier available with rate limits
- Different API endpoint structure

#### Azure OpenAI
- Requires Azure subscription and deployment
- Different endpoint format with deployment names
- Multiple required fields: endpoint, API key, deployment name

### Security Best Practices

1. **Always use environment variables for API keys:**
   ```yaml
   api_key: "${OPENAI_API_KEY}"  # Good
   api_key: "sk-1234..."          # Bad - never commit keys!
   ```

2. **Never commit `config/ai_providers.yaml` to version control**
   - The file is in `.gitignore` for protection
   - Only commit the `.example` file

3. **Restrict file permissions:**
   ```bash
   chmod 600 config/ai_providers.yaml
   ```

4. **Rotate API keys regularly** and monitor usage for unauthorized access

### Troubleshooting

If you encounter issues:

1. **Check YAML syntax:**
   ```bash
   python -c "import yaml; yaml.safe_load(open('config/ai_providers.yaml'))"
   ```

2. **Verify environment variables:**
   ```bash
   echo $OPENAI_API_KEY
   ```

3. **Test with example config:**
   ```bash
   python scripts/check_ai_config.py --config config/ai_providers.yaml.example
   ```

4. **Run with verbose output:**
   ```bash
   python scripts/check_ai_config.py --verbose
   ```

### See Also

- [AI Provider Configuration Guide](../docs/CONFIGURATION.md#ai-provider-configuration) - Detailed setup instructions
- [MCP FAQ](../README-MCP-FAQ.md) - Ollama setup and usage
- [config/ai_providers.yaml.example](../config/ai_providers.yaml.example) - Full configuration reference
