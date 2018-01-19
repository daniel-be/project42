"""Main module"""
import sys
from lib import robot

def main(*args):
    """Main entry point of the application"""
    print(args)
    return

if __name__ == "__main__":
    main(*sys.argv[1:])
