# MOLECULAR-VISUALIZATION-TOOL-
# 3D Molecule Viewer

An interactive 3D molecular visualization tool that fetches structure data from PubChem and renders it in the browser using 3Dmol.js. Supports both molecule name lookup and SMILES string input.

---

## Features

- **Name or SMILES input** — search by common name (e.g. `caffeine`, `aspirin`) or paste a SMILES string directly
- **3D structure rendering** — uses PubChem's precomputed MMFF-optimized 3D conformers
- **Multiple display styles** — Stick, Sphere, Cartoon, Surface, and Line
- **Molecule metadata** — displays IUPAC name, molecular formula, molecular weight, and PubChem CID
- **Fallback to 2D** — if no 3D conformer is available, renders the 2D layout instead

---

## Python Version (Jupyter Notebook)

The original implementation uses RDKit for local 3D conformation generation.

### Dependencies

```bash
pip install rdkit pubchempy py3Dmol ipython
```

### Usage

```python
from rdkit import Chem
from rdkit.Chem import AllChem
import py3Dmol
import pubchempy as pcp
from IPython.display import display

def name_to_smiles(name):
    compounds = pcp.get_compounds(name, 'name')
    return compounds[0].isomeric_smiles if compounds else None

def show_molecule(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print("Invalid molecule!")
        return

    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, randomSeed=42)
    AllChem.MMFFOptimizeMolecule(mol)

    viewer = py3Dmol.view(width=400, height=400)
    viewer.addModel(Chem.MolToMolBlock(mol), "mol")
    viewer.setStyle({"stick": {}})
    viewer.zoomTo()
    return viewer

user_input = input("Enter molecule name or SMILES: ")
smiles = name_to_smiles(user_input) or user_input
print("SMILES:", smiles)
viewer = show_molecule(smiles)
display(viewer.show())
```

Run in a Jupyter Notebook environment. The viewer will render inline in the cell output.

---

## Browser Version

The browser version replaces local RDKit conformation generation with PubChem's REST API, using 3Dmol.js for rendering. No installation required.

### Libraries used

| Library | Purpose |
|---|---|
| [3Dmol.js](https://3dmol.csb.pitt.edu/) | 3D molecular rendering |
| [PubChem REST API](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) | Structure and property data |
| jQuery | DOM utilities (required by 3Dmol.js) |

### How it works

1. The user enters a molecule name or SMILES string
2. A lookup is made to the PubChem `/compound/name/` endpoint to resolve the CID and fetch properties
3. The 3D SDF file is fetched from `/compound/cid/{cid}/SDF?record_type=3d`
4. The SDF is passed to `$3Dmol.createViewer()` and rendered with the selected style

---

## Python vs Browser — Key Differences

| | Python (RDKit) | Browser (PubChem API) |
|---|---|---|
| 3D conformation | Generated locally via `EmbedMolecule` + MMFF | Precomputed MMFF conformers from PubChem |
| SMILES resolution | `pubchempy.get_compounds()` | PubChem REST API |
| Environment | Jupyter Notebook | Any modern browser |
| Offline support | Yes (after install) | No (requires internet) |
| Custom molecules | Yes (any valid SMILES) | Only PubChem-indexed compounds |

---

## Example Molecules to Try

| Name | Type |
|---|---|
| `caffeine` | Stimulant |
| `aspirin` | NSAID |
| `cholesterol` | Lipid |
| `penicillin` | Antibiotic |
| `dopamine` | Neurotransmitter |
| `C1=CC=CC=C1` | Benzene (SMILES) |

---

## License

MIT

