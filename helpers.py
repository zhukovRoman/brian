import matplotlib.pyplot as plt
from numpy import *

def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plt.plot(ones(Nt), arange(Nt), 'ok', ms=10)
    print(zip(S.i, S.j))
    for i, j in zip(S.i, S.j):
        print(i,j)
        plt.plot([0, 1], [i, j], '-k')
    plt.xticks([0, 1], ['Source', 'Target'])
    plt.ylabel('Neuron index')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-1, max(Ns, Nt))
    plt.subplot(122)
    plt.plot(S.i, S.j, 'ok')
    plt.xlim(-1, Ns)
    plt.ylim(-1, Nt)
    plt.xlabel('Source neuron index')
    plt.ylabel('Target neuron index')
    plt.savefig('conectivity'+'.png');

    # plt.figure(figsize=(5, 5))
    # plt.scatter(Ns.row[Nt.row], Ns.column[Nt.column], S.w*20)
    # plt.xlabel('Source neuron position (um)')
    # plt.ylabel('Target neuron position (um)');
    # plt.savefig('conectivity2'+'.png');
