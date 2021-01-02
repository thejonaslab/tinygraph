from rdkit import Chem
from tinygraph import io
import tinygraph.io.rdkit
import pytest
import pickle

simple_smiles = ['C', 'CC', 'C=C', 'C#C'
                 'COC', 'CCO', 'CC=O', 
                 'C#N', 'C1=CC=CC=C1']

harder_smiles = ['[Cu+2].[O-]S(=O)(=O)[O-]',
    'OC[C@@H](O1)[C@@H](O)[C@H](O)[C@@H](O)[C@H](O)1'
]


@pytest.mark.parametrize("smiles_set", [simple_smiles, harder_smiles])
def test_smiles_io(smiles_set):
    """
    Test simple smiles strings
    """
    for s in smiles_set:
        for add_h in [False, True]:
            
            mol = Chem.MolFromSmiles(s)
            Chem.SanitizeMol(mol)
            if add_h:
                mol = Chem.AddHs(mol)
                
            canonical_smiles = Chem.MolToSmiles(mol)
            
            g = io.rdkit.from_rdkit_mol(mol, use_charge=True, use_chiral=True)
            
            new_mol = io.rdkit.to_rdkit_mol(g, charge_prop='charge',
                                            chiral_prop='chiral')

            assert new_mol.GetNumAtoms() == mol.GetNumAtoms()
            
            new_smiles = Chem.MolToSmiles(new_mol)

            assert new_smiles == canonical_smiles
            

def test_complex_ring():
    """
    Test a more complex ring that has explicit and implicit hydrogens
    """
    s = 'CCc(c1)ccc2[n+]1ccc3c2[nH]c4c3cccc4'
    
    mol = Chem.MolFromSmiles(s)
    Chem.SanitizeMol(mol)
    #if add_h:
    #    mol = Chem.AddHs(mol)

    canonical_smiles = Chem.MolToSmiles(mol)

    g = io.rdkit.from_rdkit_mol(mol, use_charge=True, use_chiral=True,
                                use_implicit_h=True, use_explicit_h=True)

    new_mol = io.rdkit.to_rdkit_mol(g, charge_prop='charge',
                                    chiral_prop='chiral',
                                    explicit_h_prop = 'explicit_h', sanitize=True)

    assert new_mol.GetNumAtoms() == mol.GetNumAtoms()
    new_smiles = Chem.MolToSmiles(new_mol)

    assert new_smiles == canonical_smiles

    
def test_raise_exception():
    """
    Test if adding an unknown bond order edge results in an exception
    upon conversion
    
    """
    s = "CCCC"
    mol = Chem.MolFromSmiles(s)
    Chem.SanitizeMol(mol)
            
    g = io.rdkit.from_rdkit_mol(mol)
    g[1, 2] = 4.18

    with pytest.raises(ValueError):
        io.rdkit.to_rdkit_mol(g)
        
