from scipy.linalg import expm
import numpy as np

#solve expm error
A=[[1, 0], [0, 1]]; A = np.array(A); expm(-1j * A)

import inspect
import tensorcircuit as tc
import random
import math
import matplotlib.pyplot as plt
import time

tc.set_backend("tensorflow")

#calculate the matirx of kth qubit exert matrix[[a, b], [c, d]]
def up_to_matrixx(k, a, b, c, d):
    I2 = np.array([[1,0],[0,1]])*(1+0j); K=np.array([[a,b],[c,d]])*(1+0j); um=I2;
    if k == 0:
        um = K;
    for i in range(1, N):
        if i == k:
            um = np.kron(um, K)
        else:
            um = np.kron(um, I2)
    return um

#realize R gates in paper
def R_gate(k):
    if door[k][0] == 0:
        c.rx(door[k][1]+1,theta=ODE_theta[k])
    if door[k][0] == 1:
        c.ry(door[k][1]+1,theta=ODE_theta[k])
    if door[k][0] == 2:
        c.rz(door[k][1]+1,theta=ODE_theta[k])
    if door[k][0] == 3:
        c.rxx(door[k][1]+1,door[k][2]+1,theta=ODE_theta[k])
    if door[k][0] == 4:
        c.ryy(door[k][1]+1,door[k][2]+1,theta=ODE_theta[k])
    if door[k][0] == 5:
        c.rzz(door[k][1]+1,door[k][2]+1,theta=ODE_theta[k])
    if door[k][0] == 6:
        c.crx(door[k][1]+1,door[k][2]+1,theta=ODE_theta[k])
    if door[k][0] == 7:
        c.cry(door[k][1]+1,door[k][2]+1,theta=ODE_theta[k])
    if door[k][0] == 8:
        c.crz(door[k][1]+1,door[k][2]+1,theta=ODE_theta[k])

#realize U gates in paper
def U_gate(k):
    if door[k][0] == 0:
        c.cx(0,door[k][1]+1)
    if door[k][0] == 1:
        c.cy(0,door[k][1]+1)
    if door[k][0] == 2:
        c.cz(0,door[k][1]+1)
    if door[k][0] == 3:
        c.multicontrol(0,door[k][1]+1,door[k][2]+1,ctrl=[0],unitary=tc.gates._xx_matrix)
    if door[k][0] == 4:
        c.multicontrol(0,door[k][1]+1,door[k][2]+1,ctrl=[0],unitary=tc.gates._yy_matrix)
    if door[k][0] == 5:
        c.multicontrol(0,door[k][1]+1,door[k][2]+1,ctrl=[0],unitary=tc.gates._zz_matrix)
    if door[k][0] == 6:
        c.multicontrol(0,door[k][1]+1,door[k][2]+1,ctrl=[0,door[k][1]+1],unitary=tc.gates._xx_matrix)
    if door[k][0] == 7:
        c.multicontrol(0,door[k][1]+1,door[k][2]+1,ctrl=[0,door[k][1]+1],unitary=tc.gates._yy_matrix)
    if door[k][0] == 8:
        c.multicontrol(0,door[k][1]+1,door[k][2]+1,ctrl=[0,door[k][1]+1],unitary=tc.gates._zz_matrix)

#realize Hamilton gates in ancillary circuit
def H_gate(q):
    if h_door[q][0] == 0:
        c.cx(0,h_door[q][1]+1)
    if h_door[q][0] == 1:
        c.cy(0,h_door[q][1]+1)
    if h_door[q][0] == 2:
        c.cz(0,h_door[q][1]+1)
    if h_door[q][0] == 3:
        c.multicontrol(0,h_door[q][1]+1,h_door[q][2]+1,ctrl=[0],unitary=tc.gates._xx_matrix)
    if h_door[q][0] == 4:
        c.multicontrol(0,h_door[q][1]+1,h_door[q][2]+1,ctrl=[0],unitary=tc.gates._yy_matrix)
    if h_door[q][0] == 5:
        c.multicontrol(0,h_door[q][1]+1,h_door[q][2]+1,ctrl=[0],unitary=tc.gates._zz_matrix)
    if h_door[q][0] == 6:
        c.multicontrol(0,door[k][1]+1,door[k][2]+1,ctrl=[0,door[k][1]+1],unitary=tc.gates._xx_matrix)
    if h_door[q][0] == 7:
        c.multicontrol(0,door[k][1]+1,door[k][2]+1,ctrl=[0,door[k][1]+1],unitary=tc.gates._yy_matrix)
    if h_door[q][0] == 8:
        c.multicontrol(0,door[k][1]+1,door[k][2]+1,ctrl=[0,door[k][1]+1],unitary=tc.gates._zz_matrix)

#use quantum circuit to calculate coefficient of variation A and C in paper
def find_ACkq(mod, theta_x, k, q, whi):
    #mod: a in paper; theta_x: theta in paper; k, q: A[k, q] or C[k] qth term; whi: whi=0 A whi=1 C
    global c
    ancilla = np.array([1, np.exp(1j * theta_x)]) / np.sqrt(2)
    c = tc.Circuit(N+1,inputs = np.kron(ancilla, state))
    for i in range(len(door)):
        if i == k:
            c.x(0)
            U_gate(i)
            c.x(0)
        if whi == 0 and i == q:
            U_gate(i)
            R_gate(i)
            break
        R_gate(i)
    if whi == 1:
        H_gate(q)
    pstar = np.real(np.array(c.expectation([np.array([[1, 1], [1, 1]]) / 2, [0]])))
    return mod * (2 * pstar - 1)

#use original quantum circuit simulate with c
def simulation():
    global c
    c=tc.Circuit(N,inputs=state)
    for k in range(len(door)):
        if door[k][0]==0:
            c.rx(door[k][1],theta=ODE_theta[k])
        if door[k][0]==1:
            c.ry(door[k][1],theta=ODE_theta[k])
        if door[k][0]==2:
            c.rz(door[k][1],theta=ODE_theta[k])
        if door[k][0]==3:
            c.rxx(door[k][1],door[k][2],theta=ODE_theta[k])
        if door[k][0]==4:
            c.ryy(door[k][1],door[k][2],theta=ODE_theta[k])
        if door[k][0]==5:
            c.rzz(door[k][1],door[k][2],theta=ODE_theta[k])

if __name__ == '__main__':
    
    #l: layers; h and J: coefficient of Hamilton; L_var and L_num: results of variation method and numerical method
    N=3; l=2; J=1/4; dt=0.05; t=1; h=[]; L_var=[]; L_num=[]; x_value=[];
    
    how_variation = 0 #0 McLachlan 1 time-dependent
    
    #the priciple correspond with all gates
    #the first term: 0rx,1ry,2rz,3rxx,4ryy,5rzz,6crx,7cry,8crz;
    #the second and the third term: num/ctrl+num
    #f: coefficient with simulation gates in paper
    door = []; h_door = []; f = []
    for k in range(l):
        for i in range(N):
            f.append(-0.5j)
            door.append([0, i])
        for i in range(N - 1):
            f.append(-1j)
            door.append([5, i, i + 1])
        for i in range(N - 1):
            f.append(-1j)
            door.append([3, i, i + 1])
    for i in range(N):
        h.append(1)
        h_door.append([0, i])
    for i in range(N-1):
        h.append(J); h_door.append([5, i, i + 1])
    
    #initial state
    state = np.zeros(1 << N); state[0]=1
    
    #numerical realize H
    H = np.zeros((1<<N, 1<<N)) * 1j
    for i in range(N-1):
        H += J*up_to_matrixx(i, 1, 0, 0, -1) @ up_to_matrixx(i + 1, 1, 0, 0, -1)
    for i in range(N):
        H += h[i] * up_to_matrixx(i, 0, 1, 1, 0)
    
    #variation realize
    ODE_theta = np.zeros(len(door))
    for T in range(int(t / dt)):
        #calculate coefficient in paper
        A = np.zeros((len(door), len(door))); C = np.zeros(len(door))
        for k in range(len(door)):
            for q in range(len(door)):
                if k > q:
                    A[k, q] = A[q, k]
                    continue
                if how_variation == 0:
                    A[k, q] = find_ACkq(abs(f[k] * f[q]), np.angle(f[q]) - np.angle(f[k]), k, q, 0)
                if how_variation == 1:
                    A[k, q] = find_ACkq(abs(f[k] * f[q]), np.angle(f[q]) - np.angle(f[k]) - math.pi / 2, k, q, 0)
        for k in range(len(door)):
            for q in range(len(h)):
                if how_variation == 0:
                    C[k] += find_ACkq(abs(f[k] * h[q]), np.angle(h[q]) - np.angle(f[k]) - math.pi / 2, k, q, 1)
                if how_variation == 1:
                    C[k] += find_ACkq(-abs(f[k] * h[q]), np.angle(h[q]) - np.angle(f[k]), k, q, 1)
        
        #calculate parameter and its derivative
        A += np.eye(len(door)) * 1e-5
        ODE_dtheta = np.linalg.solve(A, C)
        print(ODE_dtheta)
        for i in range(len(door)):
            ODE_theta[i] += ODE_dtheta[i] * dt
        
        #numerical results
        simulation()
        ep = expm(-1j * H * (T + 1) * dt) @ state
        L_num.append(np.real(np.array(ep.conj().T @ up_to_matrixx(1, 0, 1, 1, 0) @ ep)).tolist())
        
        #variation results
        L_var.append(np.real(np.array(c.expectation([tc.gates.x(), [1]]))).tolist())
        
        x_value.append((T + 1) * dt)
        print([(T + 1) * dt, L_num[T] - L_var[T]])
    plt.plot(x_value, L_var, color = 'green')
    plt.plot(x_value, L_num, color = 'red')
    plt.show()