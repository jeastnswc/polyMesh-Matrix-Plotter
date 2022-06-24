import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse as sps

#casedir = '/home/eastridge/Documents/OpenFOAM/thrusterPod/run09/'
casedir = 'sampleMeshes/'
#f = open(casedir + 'constant/polyMesh-airfoilTRex/neighbour', 'r')
#g = open(casedir + 'constant/polyMesh-airfoilTRex/owner', 'r')
#f = open(casedir + 'constant/polyMesh-airfoilTRex-renumbered/neighbour', 'r')
#g = open(casedir + 'constant/polyMesh-airfoilTRex-renumbered/owner', 'r')
#f = open(casedir + 'polyMesh7x7/neighbour', 'r')
#g = open(casedir + 'polyMesh7x7/owner', 'r')
f = open(casedir + 'polyMesh-thruster/neighbour', 'r')
g = open(casedir + 'polyMesh-thruster/owner', 'r')

#f = open('constant/polyMesh/neighbour', 'r')
#g = open('constant/polyMesh/owner', 'r')

while True:
    line = f.readline()
    _ = g.readline()
    if 'nCells' in line:
        nCells = int([i.split(':')[1] for i in line.split() if 'nCells' in i][0])
    if '(' in line:
        break

#nCells = 3784 # just for airfoilTRex

#matrix = np.zeros([nCells, nCells], dtype=int)
#np.fill_diagonal(matrix, 1)

cell1list = []
cell2list = []
while True:
    line_neighbour = f.readline()
    line_owner = g.readline()
    if ')' in line_neighbour:
        f.close()
        g.close()
        break
    try:
        cell1 = int(line_neighbour)
        cell2 = int(line_owner)
        cell1list.append(cell1)
        cell2list.append(cell2)
        cell1list.append(cell2)
        cell2list.append(cell1)
        #matrix[cell1, cell2] = 1
        #matrix[cell2, cell1] = 1
    except:
        cells1 = [int(cell) for cell in line_neighbour.split()]
        cells2 = [int(cell) for cell in line_owner.split()]
        for i, cell1 in enumerate(cells1):
            cell2 = cells2[i]
            cell1list.append(cell1)
            cell2list.append(cell2)
            cell1list.append(cell2)
            cell2list.append(cell1)
            #matrix[cell1, cell2] = 1
            #matrix[cell2, cell1] = 1

for i in range(nCells):
    cell1list.append(i)
    cell2list.append(i)

oneslist = np.ones(len(cell1list), dtype=int)
matrix = sps.csr_matrix((oneslist, (cell1list, cell2list)))

#plt.matshow(matrix)
plt.spy(matrix)
plt.tight_layout()
plt.show()

