from sympy.utilities.iterables import multiset_permutations
from scipy.special import binom
from scipy.linalg import norm

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit

import numpy as np

def dicke_state_psi(n_qubits = 4, n_ones = None):
    ## Outputs the Dicke state from Marcel Bergmann and Otfried Gühne 2013 J. Phys. A: Math. Theor. 46 385304
    ## Dicke state looks like |11100> + |11010> + .. (all other permutations), normalized
    assert n_qubits > 1, "n_qubits must be > 1"

    if n_ones != None:
        assert n_qubits >= n_ones >= 0, "n_ones must not be larger than n_qubits or smaller than 0"
    else:
        # default the n_ones to n_qubits - 1 (the W-state)
        n_ones = n_qubits - 1
    
    n_zeros = n_qubits - n_ones    

    # initialize vector with n_zeros of zeros and n_ones of ones
    zeros = ["0" for _ in range(n_zeros)]
    ones = ["1" for _ in range(n_ones)]
    statevector_init = zeros + ones
    
    # generate all permutations
    statevect_permutations = multiset_permutations(statevector_init)
    
    # join the string of 0s and 1s, convert it to an integer from base 2, 
    # these will be the locations of nonzero probabilities
    positiveproblocations = [int("".join(vect_permutation),2) for vect_permutation in statevect_permutations]
    
    # generate Dicke state
    dicke_state = [0.]*2**n_qubits
    for loc in positiveproblocations:
        dicke_state[loc] = 1.
        
    # normalize
    dicke_state /= np.sqrt(binom(n_qubits,n_ones))
    return dicke_state
    

def dicke_state_circuit(n_qubits = 4, n_ones = None):
    dicke_state = dicke_state_psi(n_qubits, n_ones)
    q = QuantumRegister(n_qubits)
    qc = QuantumCircuit(q)
    qc.initialize(dicke_state, list(range(n_qubits)))
    
    return qc


def hyper_dicke_state_psi(n_qubits = 4, lbda = 0):
    ## From PhysRevA.69.054101
    ## works for even number of qubits (so far)
    assert n_qubits%2 == 0, "n_qubits must be even"
    
    # define all the prefactors from paper
    eta = np.arctanh(lbda/(2*n_qubits))
    alphafactor = lambda j: binom(n_qubits, j) / np.sqrt(binom(n_qubits, 2*j))
    alpha = lambda j: np.exp(-eta * (n_qubits - 2 * j)) * alphafactor(j) ## check the coefficient of j
    
    # initialize state
    hyper_dicke_state = np.zeros(2**n_qubits)
    
    # hyper_dicke_state is defined as a superposition of dicke states with some prefactors
    for j in range(n_qubits//2):
        hyper_dicke_state += alpha(j) * dicke_state_psi(n_qubits = n_qubits, n_ones=j)
    
    # normalize
    hyper_dicke_state /= norm(hyper_dicke_state)
    
    return hyper_dicke_state

def hyper_dicke_state_circuit(n_qubits = 4, lbda = 0):
    hyper_dicke_state = hyper_dicke_state_psi(n_qubits, lbda)
    q = QuantumRegister(n_qubits)
    qc = QuantumCircuit(q)
    qc.initialize(hyper_dicke_state, list(range(n_qubits)))
    
    return qc


def tony_state_psi():
    # 6-qubit ground state of spin Ising model in the computational basis
    # numerically calculated by Tony with Mathematica
    vector = np.array([-0.654068, 0, 0, 0.216952, 0, -0.15362, 0.216952, 0, 0, 0.140428, \
        -0.15362, 0, 0.216952, 0, 0, -0.0824614, 0, -0.15362, 0.140428, 0, \
        -0.15362, 0, 0, 0.0689281, 0.216952, 0, 0, -0.0778927, 0, 0.0689281, \
        -0.0824614, 0, 0, 0.216952, -0.15362, 0, 0.140428, 0, 0, -0.0824614, \
        -0.15362, 0, 0, 0.0689281, 0, -0.0778927, 0.0689281, 0, 0.216952, 0, \
        0, -0.0824614, 0, 0.0689281, -0.0778927, 0, 0, -0.0824614, 0.0689281, \
        0, -0.0824614, 0, 0, 0.0390498])
    
    vector /= norm(vector)
    return vector

def tony_state_circuit():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.initialize(tony_state_psi(), list(range(6)))

    return qc

def q_instability_psi(n_qubits):
    # from Phys. Rev. A 79, 022302 , eq. 4