#!/usr/bin/env python
"""
AI Roast Machine - Main Entry Point

This script provides a unified entry point to all functionality of the AI Roast Machine.
It delegates to the appropriate scripts based on the command-line arguments.
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

def run_script(script_name, *args):
    """Run a script from the scripts directory with the given arguments."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"Error: Script {script_name} not found")
        return 1
    
    cmd = [sys.executable, str(script_path)] + list(args)
    return subprocess.call(cmd)

def run_shell_script(script_name, *args):
    """Run a shell script from the scripts directory with the given arguments."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"Error: Script {script_name} not found")
        return 1
    
    cmd = [str(script_path)] + list(args)
    return subprocess.call(cmd)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AI Roast Machine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Docker commands
    docker_parser = subparsers.add_parser("docker", help="Docker commands")
    docker_parser.add_argument("--openrouter", action="store_true", help="Include OpenRouter services")
    docker_parser.add_argument("--only-openrouter", action="store_true", help="Run only OpenRouter services")
    
    # OpenRouter commands
    openrouter_parser = subparsers.add_parser("openrouter", help="OpenRouter commands")
    openrouter_subparsers = openrouter_parser.add_subparsers(dest="openrouter_command", help="OpenRouter command")
    
    # CLI command
    cli_parser = openrouter_subparsers.add_parser("cli", help="Run the OpenRouter CLI")
    
    # API command
    api_parser = openrouter_subparsers.add_parser("api", help="Run the OpenRouter API server")
    
    # List models command
    list_models_parser = openrouter_subparsers.add_parser("list-models", help="List available models")
    
    # Test command
    test_parser = openrouter_subparsers.add_parser("test", help="Test a model with a prompt")
    test_parser.add_argument("model", help="Model to test")
    test_parser.add_argument("prompt", help="Prompt to test with")
    
    # Bias test command
    bias_test_parser = openrouter_subparsers.add_parser("bias-test", help="Run bias tests on a model")
    bias_test_parser.add_argument("model", help="Model to test")
    
    # Test commands
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("--openrouter", action="store_true", help="Run OpenRouter tests")
    test_parser.add_argument("--api", action="store_true", help="Run API tests")
    test_parser.add_argument("--all", action="store_true", help="Run all tests")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "docker":
        docker_args = []
        if args.openrouter:
            docker_args.append("--openrouter")
        if args.only_openrouter:
            docker_args.append("--only-openrouter")
        return run_shell_script("run_docker.sh", *docker_args)
    
    elif args.command == "openrouter":
        if args.openrouter_command == "cli":
            return run_shell_script("run_openrouter.sh", "cli")
        elif args.openrouter_command == "api":
            return run_shell_script("run_openrouter.sh", "api")
        elif args.openrouter_command == "list-models":
            return run_shell_script("run_openrouter.sh", "list-models")
        elif args.openrouter_command == "test":
            return run_shell_script("run_openrouter.sh", "test", args.model, args.prompt)
        elif args.openrouter_command == "bias-test":
            return run_shell_script("run_openrouter.sh", "bias-test", args.model)
        else:
            print("Error: Unknown OpenRouter command")
            return 1
    
    elif args.command == "test":
        if args.openrouter:
            return run_script("test_openrouter.py")
        elif args.api:
            return run_script("test_api.py")
        elif args.all:
            run_script("test_openrouter.py")
            run_script("test_api.py")
            return run_script("test_ai_roast.py")
        else:
            return run_script("test_ai_roast.py")
    
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main()) 