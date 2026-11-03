import sys
from pathlib import Path

# Permite "import duplicados", "import organizar"... desde los tests
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
