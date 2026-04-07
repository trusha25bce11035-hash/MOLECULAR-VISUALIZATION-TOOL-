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

# INPUT
user_input = input("Enter molecule name or SMILES: ")

smiles = name_to_smiles(user_input) or user_input
print("SMILES:", smiles)

viewer = show_molecule(smiles)
display(viewer.show())
