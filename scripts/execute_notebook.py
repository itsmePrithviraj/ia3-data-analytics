"""Execute in a fresh project kernel and save the checked notebook."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
path = root / "notebooks/01_screen_time_analysis.ipynb"
notebook = nbformat.read(path, as_version=4)
client = NotebookClient(notebook, timeout=180, kernel_name="screentime", resources={"metadata": {"path": str(root)}})
client.execute()
nbformat.write(notebook, path)
print(f"Executed {sum(c.cell_type == 'code' for c in notebook.cells)} code cells without errors: {path}")
