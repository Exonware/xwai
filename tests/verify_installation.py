#!/usr/bin/env python3
"""
#exonware/xwai/tests/verify_installation.py
Verify xwai installation.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 07-Jan-2025
"""

import sys


def main():
    """Verify installation."""
    try:
        from exonware.xwai import XWAI, __version__
        print(f"✅ xwai {__version__} installed successfully")
        print(f"✅ XWAI class available: {XWAI is not None}")
        return 0
    except ImportError as e:
        print(f"❌ Installation verification failed: {e}")
        return 1
if __name__ == "__main__":
    sys.exit(main())
