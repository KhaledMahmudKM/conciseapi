"""Make the example modules in the parent folder importable from the tests."""
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(CODE / "grpc_demo"))
