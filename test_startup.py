#!/usr/bin/env python3
"""
Quick test to verify the FastAPI app can start.
Run this after installing dependencies.
"""

import sys
import asyncio
from main import app


async def test_app():
    """Test that FastAPI app initializes without errors."""
    print("✓ FastAPI app imported successfully")

    # Verify app has the required endpoints
    routes = [route.path for route in app.routes]
    assert "/" in routes, "Root endpoint not found"
    assert "/ingest" in routes, "Ingest endpoint not found"
    assert "/chat" in routes, "Chat endpoint not found"

    print("✓ All required endpoints defined")
    print(f"✓ Available routes: {routes}")
    print("\n✅ All tests passed! App is runnable.")


if __name__ == "__main__":
    try:
        asyncio.run(test_app())
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
