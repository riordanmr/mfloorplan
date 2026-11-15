#!/bin/bash
# Quick start script for the Bike Shop Finder web application

cd "$(dirname "$0")" || exit 1

echo "Starting Bike Shop Finder web application..."
echo ""
echo "Opening http://localhost:8000/find.html in your browser..."
echo "Press Ctrl+C to stop the server"
echo ""

# Start the HTTP server
python3 -m http.server 8000 --bind 127.0.0.1
