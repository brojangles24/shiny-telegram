#!/usr/bin/env python3
"""
Singularity DNS Blocklist Aggregator (v5.8.4)

This is the main entry point for the application.
It imports and runs the main function from the cli module.
"""
import sys
from singularity_aggregator.processor import main

if __name__ == "__main__":
    # The main() function in processor.py handles argparse, logging, and orchestration
    sys.exit(main())
