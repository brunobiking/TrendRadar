#!/usr/bin/env python3
"""
AI Provider Configuration Checker

This script validates and tests AI provider configurations for TrendRadar.
It helps users debug connection issues and verify their AI provider setup.

Usage:
    python scripts/check_ai_config.py [--config CONFIG_FILE]
    
Options:
    --config CONFIG_FILE    Path to AI providers config file
                           (default: config/ai_providers.yaml)
    --test-connectivity     Test actual connectivity to providers
    --verbose               Show detailed output
    --help                  Show this help message
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML is not installed. Install it with: pip install PyYAML")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests is not installed. Install it with: pip install requests")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output"""
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"


def print_header(text: str) -> None:
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}\n")


def print_success(text: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_info(text: str) -> None:
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def expand_env_vars(value: str) -> str:
    """Expand environment variables in format ${VAR_NAME}"""
    if not isinstance(value, str):
        return value
    
    # Simple regex-like replacement for ${VAR_NAME}
    import re
    pattern = r'\$\{([^}]+)\}'
    
    def replace_var(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))
    
    return re.sub(pattern, replace_var, value)


def load_config(config_path: str) -> Optional[Dict]:
    """Load and parse the AI providers configuration file"""
    if not os.path.exists(config_path):
        print_error(f"Configuration file not found: {config_path}")
        print_info("Did you copy ai_providers.yaml.example to ai_providers.yaml?")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as e:
        print_error(f"Failed to parse YAML configuration: {e}")
        return None
    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        return None


def validate_provider_config(provider_name: str, provider_config: Dict, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Validate a single provider configuration"""
    errors = []
    
    # Check required fields
    if 'type' not in provider_config:
        errors.append("Missing required field: 'type'")
    
    provider_type = provider_config.get('type', '')
    
    # Type-specific validation
    if provider_type == 'ollama':
        if 'base_url' not in provider_config:
            errors.append("Missing required field: 'base_url' for Ollama")
    
    elif provider_type in ['openai', 'openai-compatible']:
        if 'api_key' not in provider_config:
            errors.append("Missing required field: 'api_key'")
        else:
            api_key = expand_env_vars(provider_config['api_key'])
            if api_key.startswith('${'):
                errors.append(f"Environment variable not set: {provider_config['api_key']}")
    
    elif provider_type == 'anthropic':
        if 'api_key' not in provider_config:
            errors.append("Missing required field: 'api_key'")
        else:
            api_key = expand_env_vars(provider_config['api_key'])
            if api_key.startswith('${'):
                errors.append(f"Environment variable not set: {provider_config['api_key']}")
    
    elif provider_type == 'google':
        if 'api_key' not in provider_config:
            errors.append("Missing required field: 'api_key'")
        else:
            api_key = expand_env_vars(provider_config['api_key'])
            if api_key.startswith('${'):
                errors.append(f"Environment variable not set: {provider_config['api_key']}")
    
    elif provider_type == 'azure':
        required_fields = ['base_url', 'api_key', 'deployment_name']
        for field in required_fields:
            if field not in provider_config:
                errors.append(f"Missing required field: '{field}' for Azure")
            else:
                value = expand_env_vars(provider_config[field])
                if value.startswith('${'):
                    errors.append(f"Environment variable not set: {provider_config[field]}")
    
    # Check for default_model
    if 'default_model' not in provider_config:
        errors.append("Missing recommended field: 'default_model'")
    
    if verbose and not errors:
        print_info(f"  Configuration fields: {', '.join(provider_config.keys())}")
    
    return len(errors) == 0, errors


def test_ollama_connectivity(base_url: str, verbose: bool = False) -> Tuple[bool, str]:
    """Test connectivity to Ollama server"""
    try:
        # Test Ollama API endpoint
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        
        if response.status_code == 200:
            models_data = response.json()
            models = models_data.get('models', [])
            if models:
                model_names = [m.get('name', 'unknown') for m in models]
                return True, f"Connected successfully. Available models: {', '.join(model_names[:5])}"
            else:
                return True, "Connected successfully. No models installed yet."
        else:
            return False, f"Server returned status code: {response.status_code}"
    
    except requests.exceptions.ConnectionError:
        return False, "Connection refused. Is Ollama running? Start it with: ollama serve"
    except requests.exceptions.Timeout:
        return False, "Connection timed out. Check if Ollama is running."
    except Exception as e:
        return False, f"Connection failed: {str(e)}"


def test_openai_connectivity(base_url: str, api_key: str, verbose: bool = False) -> Tuple[bool, str]:
    """Test connectivity to OpenAI or OpenAI-compatible API"""
    try:
        # Test with models endpoint
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(f"{base_url}/models", headers=headers, timeout=10)
        
        if response.status_code == 200:
            models_data = response.json()
            models = models_data.get('data', [])
            if models:
                model_ids = [m.get('id', 'unknown') for m in models[:5]]
                return True, f"Connected successfully. Available models: {', '.join(model_ids)}"
            else:
                return True, "Connected successfully."
        elif response.status_code == 401:
            return False, "Authentication failed. Check your API key."
        elif response.status_code == 403:
            return False, "Access forbidden. Check your API key permissions."
        else:
            return False, f"Server returned status code: {response.status_code}"
    
    except requests.exceptions.ConnectionError:
        return False, f"Connection refused. Check base_url: {base_url}"
    except requests.exceptions.Timeout:
        return False, "Connection timed out."
    except Exception as e:
        return False, f"Connection failed: {str(e)}"


def test_provider_connectivity(provider_name: str, provider_config: Dict, verbose: bool = False) -> Tuple[bool, str]:
    """Test connectivity to a provider"""
    provider_type = provider_config.get('type', '')
    
    if not provider_config.get('enabled', False):
        return False, "Provider is disabled in configuration"
    
    if provider_type == 'ollama':
        base_url = provider_config.get('base_url', 'http://localhost:11434')
        return test_ollama_connectivity(base_url, verbose)
    
    elif provider_type in ['openai', 'openai-compatible', 'anthropic']:
        base_url = provider_config.get('base_url', '')
        api_key = expand_env_vars(provider_config.get('api_key', ''))
        
        if not base_url:
            return False, "Missing base_url in configuration"
        if not api_key or api_key.startswith('${'):
            return False, "API key not configured or environment variable not set"
        
        return test_openai_connectivity(base_url, api_key, verbose)
    
    elif provider_type == 'azure':
        base_url = expand_env_vars(provider_config.get('base_url', ''))
        api_key = expand_env_vars(provider_config.get('api_key', ''))
        
        if not base_url or base_url.startswith('${'):
            return False, "Base URL not configured or environment variable not set"
        if not api_key or api_key.startswith('${'):
            return False, "API key not configured or environment variable not set"
        
        # Azure uses different endpoint format
        api_version = provider_config.get('api_version', '2024-02-15-preview')
        deployment = provider_config.get('deployment_name', '')
        
        try:
            headers = {
                'api-key': api_key,
                'Content-Type': 'application/json'
            }
            
            # Test with a simple deployments endpoint
            test_url = f"{base_url}/openai/deployments?api-version={api_version}"
            response = requests.get(test_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return True, f"Connected successfully to Azure deployment: {deployment}"
            elif response.status_code == 401:
                return False, "Authentication failed. Check your API key."
            else:
                return False, f"Server returned status code: {response.status_code}"
        
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    elif provider_type == 'google':
        api_key = expand_env_vars(provider_config.get('api_key', ''))
        
        if not api_key or api_key.startswith('${'):
            return False, "API key not configured or environment variable not set"
        
        # Google Gemini uses different API structure
        try:
            base_url = provider_config.get('base_url', 'https://generativelanguage.googleapis.com/v1beta')
            test_url = f"{base_url}/models?key={api_key}"
            
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                models_data = response.json()
                models = models_data.get('models', [])
                if models:
                    model_names = [m.get('name', 'unknown').split('/')[-1] for m in models[:5]]
                    return True, f"Connected successfully. Available models: {', '.join(model_names)}"
                return True, "Connected successfully."
            elif response.status_code == 400:
                return False, "Invalid API key format."
            elif response.status_code == 403:
                return False, "API key not authorized. Check your key and enable Gemini API."
            else:
                return False, f"Server returned status code: {response.status_code}"
        
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    else:
        return False, f"Unknown provider type: {provider_type}"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AI Provider Configuration Checker for TrendRadar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Validate configuration file
    python scripts/check_ai_config.py
    
    # Test connectivity to providers
    python scripts/check_ai_config.py --test-connectivity
    
    # Use custom config file
    python scripts/check_ai_config.py --config my_config.yaml --verbose
        """
    )
    
    parser.add_argument(
        '--config',
        default='config/ai_providers.yaml',
        help='Path to AI providers config file (default: config/ai_providers.yaml)'
    )
    
    parser.add_argument(
        '--test-connectivity',
        action='store_true',
        help='Test actual connectivity to enabled providers'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_header("TrendRadar AI Provider Configuration Checker")
    
    # Load configuration
    print_info(f"Loading configuration from: {args.config}")
    config = load_config(args.config)
    
    if config is None:
        sys.exit(1)
    
    if 'ai_providers' not in config:
        print_error("Configuration file does not contain 'ai_providers' section")
        sys.exit(1)
    
    providers = config['ai_providers']
    
    if not providers:
        print_warning("No providers configured in ai_providers.yaml")
        sys.exit(0)
    
    print_success(f"Configuration loaded successfully with {len(providers)} provider(s)")
    
    # Validate each provider
    print_header("Validating Provider Configurations")
    
    validation_results = {}
    enabled_providers = []
    
    for provider_name, provider_config in providers.items():
        print(f"\n{Colors.BOLD}Provider: {provider_name}{Colors.RESET}")
        print(f"  Type: {provider_config.get('type', 'unknown')}")
        print(f"  Enabled: {provider_config.get('enabled', False)}")
        
        if args.verbose and 'description' in provider_config:
            print(f"  Description: {provider_config['description']}")
        
        is_valid, errors = validate_provider_config(provider_name, provider_config, args.verbose)
        validation_results[provider_name] = is_valid
        
        if is_valid:
            print_success("Configuration is valid")
            if provider_config.get('enabled', False):
                enabled_providers.append(provider_name)
        else:
            print_error("Configuration has errors:")
            for error in errors:
                print(f"    - {error}")
    
    # Test connectivity if requested
    if args.test_connectivity:
        print_header("Testing Provider Connectivity")
        
        if not enabled_providers:
            print_warning("No enabled providers to test")
        else:
            for provider_name in enabled_providers:
                provider_config = providers[provider_name]
                print(f"\n{Colors.BOLD}Testing: {provider_name}{Colors.RESET}")
                
                success, message = test_provider_connectivity(provider_name, provider_config, args.verbose)
                
                if success:
                    print_success(message)
                else:
                    print_error(message)
    
    # Summary
    print_header("Summary")
    
    valid_count = sum(1 for v in validation_results.values() if v)
    invalid_count = len(validation_results) - valid_count
    
    print(f"Total providers: {len(providers)}")
    print(f"Valid configurations: {Colors.GREEN}{valid_count}{Colors.RESET}")
    print(f"Invalid configurations: {Colors.RED}{invalid_count}{Colors.RESET}")
    print(f"Enabled providers: {Colors.CYAN}{len(enabled_providers)}{Colors.RESET}")
    
    if enabled_providers:
        print(f"\nEnabled providers: {', '.join(enabled_providers)}")
    
    # Exit code
    if invalid_count > 0:
        print_warning("\nSome providers have configuration errors. See details above.")
        sys.exit(1)
    else:
        print_success("\nAll provider configurations are valid!")
        sys.exit(0)


if __name__ == '__main__':
    main()
