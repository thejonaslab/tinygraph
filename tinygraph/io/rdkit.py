"""
RDKit IO. 


"""

import numpy as np

try:
    from rdkit import Chem
    import rdkit
except ModuleNotFoundError as e:
    print("Module rdkit was not found, it must be installed to use rdkit IO")
    raise

from .. import TinyGraph


def from_rdkit_mol(mol, use_charge=False, use_chiral=False,
                   use_implicit_h = False,
                   use_explicit_h = False,
                   other_vert_props = {},
                   other_edge_props={}):
    """
    Create a new tinygraph from a given molecule where the weights 
    are the corresponding bond orders per RDKit (1, 1.5, 2, 3) as 32-bit floats and 
    the atomic numbers are a uint8-based vertex property. 

    Inputs: 
       mol: rdkit mol, with or without explicit hydrogens
       use_charge: create a vertex prop for atomic charges named 'charge'
       use_chiral: create a vertex prop for chiral flags
                   flags named 'chiral'
       use_implicit_h: create a vertex prop for implicit hydrogens
                       flags named 'implicit_h'
       use_explicit_h: create a vertex prop for explicit hydrogens
                       flags named 'explicit_h'
    
    Returns: new TinyGraph
   
    """

    ATOM_N = mol.GetNumAtoms()
    vp = {'atomicno' : np.uint8}
    if use_charge:
        vp['charge'] = np.int8
    if use_chiral:
        vp['chiral'] = np.int8
        
    if use_implicit_h:
        vp['implicit_h'] = np.int8
        
    if use_explicit_h:
        vp['explicit_h'] = np.int8
        
    g = TinyGraph(ATOM_N, np.float32, vp_types = vp)

    for i in range(ATOM_N):
        a = mol.GetAtomWithIdx(i)
        g.v['atomicno'][i] = a.GetAtomicNum()
        if use_charge:
            g.v['charge'][i] = a.GetFormalCharge()
        if use_chiral:
            g.v['chiral'][i] = int(a.GetChiralTag())
        if use_implicit_h:
            g.v['implicit_h'][i] = int(a.GetNumImplicitHs())
        if use_explicit_h:
            g.v['explicit_h'][i] = int(a.GetNumExplicitHs())
            
    for b in mol.GetBonds():
        head = b.GetBeginAtomIdx()
        tail = b.GetEndAtomIdx()
        order = b.GetBondTypeAsDouble()
        g[head, tail] = order

    return g
    

def to_rdkit_mol(g, atomicno_prop='atomicno',
                 charge_prop = None,
                 chiral_prop = None,
                 explicit_h_prop = None,
                 sanitize=True):
    """
    Create a new rdkit Mol from a TinyGraph with edge weights representing
    the bond order. 

    Inputs: 
         g: TinyGraph with weights as bond orders
         atomicno_prop: vertex property to use for atomic numbers 
                        (default is 'atomicno')
         charge_prop: vertex property to use for per-atom-charges
         chiral_prop: vertex property to use for chiral tags
         explicit_h_prop: vertex property to use for explicit hydrogens
         sanitize: whether to sanitize the molecule 
 
    Retruns: RDMol
    """

    # check atomicnos are valid


    ATOM_N = g.node_N
    m = Chem.RWMol()
    for i in range(ATOM_N):
        atom = Chem.Atom(int(g.v[atomicno_prop][i]))
        if charge_prop is not None:
            atom.SetFormalCharge(int(g.v[charge_prop][i]))

        if chiral_prop is not None:
            atom.SetChiralTag(rdkit.Chem.rdchem.ChiralType(int(g.v[chiral_prop][i])))
            
        if explicit_h_prop is not None:
            atom.SetNumExplicitHs(int(g.v[explicit_h_prop][i]))
            
            
        idx = m.AddAtom(atom)
        

    for i in range(ATOM_N):
        for j in range(i+1, ATOM_N):
            bo = g[i, j]
            if bo == 0:
                continue
            if bo == 0:
                pass
            elif bo == 1:
                m.AddBond(i, j,Chem.BondType.SINGLE)
            elif bo == 2:
                m.AddBond(i, j,Chem.BondType.DOUBLE)
            elif bo == 1.5:
                m.AddBond(i, j,Chem.BondType.AROMATIC)
                m.GetAtomWithIdx(i).SetIsAromatic(True)
                m.GetAtomWithIdx(j).SetIsAromatic(True)
            elif bo == 3:
                m.AddBond(i, j,Chem.BondType.TRIPLE)
            else:
                raise ValueError(f"Unknown Bond Order {bo}")

    m.UpdatePropertyCache()
    
    m = Chem.Mol(m)
            
    if sanitize:
        Chem.SanitizeMol(m)

    return m
