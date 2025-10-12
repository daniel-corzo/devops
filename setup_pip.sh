#!/bin/bash
# Set environment variable to use public PyPI instead of organization's internal one
export PIP_INDEX_URL=https://pypi.org/simple/

echo "✅ PIP_INDEX_URL set to: $PIP_INDEX_URL"
echo "You can now use pip install commands and they will use the public PyPI repository."
echo ""
echo "To make this permanent for your current shell session, run:"
echo "source ./setup_pip.sh"
