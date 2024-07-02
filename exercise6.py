import numpy as np

def eta_epsilon(r, epsilon):
    return np.exp(-r**2 / (4 * epsilon**2)) / np.sqrt(4 * np.pi * epsilon**2)


def pse_diffusion_1d(D, epsilon, u, x, verlet, N, V):
    du = np.zeros_like(u)
    for p in range(N):
        for q in verlet[p]:
            du[p] += (u[q] - u[p])*eta_epsilon(x[q] - x[p], epsilon)*V[q]
    return V*D/epsilon**2*du

def pse_diffusion_2d(D, epsilon, u, positions, verlet, N, V):
    du = np.zeros_like(u)
    for p in range(N):
        for q in verlet[p]:
            r = np.linalg.norm(positions[q] - positions[p])
            du[p] += (u[q] - u[p])*eta_epsilon(r, epsilon)*V[q]
    return V*D/epsilon**2*du

def periodic_boundaries(u):
    n = int(np.sqrt(len(u)))
    u_reshaped = u.reshape((n, n))
    
    u_reshaped[:, 0] = u_reshaped[:, -2]
    u_reshaped[:, -1] = u_reshaped[:, 1]
    u_reshaped[0, :] = u_reshaped[-2, :]
    u_reshaped[-1, :] = u_reshaped[1, :]
    
    return u_reshaped.flatten()
