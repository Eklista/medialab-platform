#!/usr/bin/env python3
"""
MediaLab Platform - Development Server Runner
"""
import os
import sys
import argparse
import uvicorn

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import get_settings
from app.core.config_utils import get_environment_info


def main():
    """Main runner function"""
    parser = argparse.ArgumentParser(description='MediaLab Platform Development Server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    parser.add_argument('--log-level', default='info', help='Log level')
    parser.add_argument('--env-info', action='store_true', help='Show environment info and exit')
    
    args = parser.parse_args()
    
    # Show environment info if requested
    if args.env_info:
        settings = get_settings()
        env_info = get_environment_info()
        print("=== MediaLab Platform Environment Info ===")
        for key, value in env_info.items():
            print(f"{key}: {value}")
        return
    
    # Load settings
    settings = get_settings()
    
    # Override with command line args
    host = args.host
    port = args.port
    reload = args.reload or settings.DEBUG
    log_level = args.log_level
    
    print(f"🚀 Starting MediaLab Platform v{settings.APP_VERSION}")
    print(f"📍 Environment: {settings.ENVIRONMENT}")
    print(f"🌐 Server: http://{host}:{port}")
    if settings.features.ENABLE_API_DOCS:
        print(f"📚 Docs: http://{host}:{port}/docs")
    print("=" * 50)
    
    # Run the server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
        access_log=settings.DEBUG
    )


if __name__ == "__main__":
    main()