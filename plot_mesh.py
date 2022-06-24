import numpy as np
import matplotlib.pyplot as plt

#casedir = '/home/eastridge/Documents/OpenFOAM/thrusterPod/run09/'
casedir = ''
#f = open(casedir + 'constant/polyMesh-airfoilTRex/neighbour', 'r')
#g = open(casedir + 'constant/polyMesh-airfoilTRex/owner', 'r')
#f = open(casedir + 'constant/polyMesh-airfoilTRex-renumbered/neighbour', 'r')
#g = open(casedir + 'constant/polyMesh-airfoilTRex-renumbered/owner', 'r')
f = open(casedir + '1/polyMesh/neighbour', 'r')
g = open(casedir + '1/polyMesh/owner', 'r')

#f = open('constant/polyMesh/neighbour', 'r')
#g = open('constant/polyMesh/owner', 'r')

while True:
    line = f.readline()
    _ = g.readline()
    if 'nCells' in line:
        nCells = int([i.split(':')[1] for i in line.split() if 'nCells' in i][0])
    if '(' in line:
        break

nCells = 3784 # just for airfoilTRex

matrix = np.zeros([nCells, nCells], dtype=int)
np.fill_diagonal(matrix, 1)

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
        matrix[cell1, cell2] = 1
        matrix[cell2, cell1] = 1
    except:
        cells1 = [int(cell) for cell in line_neighbour.split()]
        cells2 = [int(cell) for cell in line_owner.split()]
        for i, cell1 in enumerate(cells1):
            cell2 = cells2[i]
            matrix[cell1, cell2] = 1
            matrix[cell2, cell1] = 1


plt.matshow(matrix)
plt.tight_layout()
plt.show()

