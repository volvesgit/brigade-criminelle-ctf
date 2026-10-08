#!/usr/bin/env python3
"""
Railway startup script for Brigade Criminelle CTF Backend
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the FastAPI application"""
    try:
        # Get port from environment
        port = int(os.getenv("PORT", 8000))
        logger.info(f"🚀 Starting Brigade Criminelle CTF Backend on port {port}")
        
        # Import and run
        import uvicorn
        from main import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
