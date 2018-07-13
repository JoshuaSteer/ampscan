# -*- coding: utf-8 -*-
"""
Created on Wed Nov 01 14:13:50 2017

@author: js22g12
"""

import numpy as np
from numpy.linalg import solve

class feMixin(object):
    """
    Finite element docstring.

    """
    
    def addFE(self, files):
        """
        Numpy style docstring

        """
        if len(files) == 1:
            data = np.load(files[0], encoding='bytes').item()
            for k in list(data.keys()):
                data[str(k, 'utf-8')] = data.pop(k)
            for k, v in data.items():
                setattr(self, k, v)
        if len(files) == 3:
            data = {}
            names = ['vert', 'faces', 'values']
            for n, f in zip(names, files):
                data[n] = np.loadtxt(f)
        self.getSurf()
        
        
    def getSurf(self):
        """
        Numpy style docstring

        """
        # Find verts with a pressure value for external surface
        valInd = self.values[:, 0].astype(int)
        # Find faces in array 
        log = np.isin(self.faces, valInd)
        f = self.faces[log].reshape([-1, 4])
        log = np.zeros(len(self.vert), dtype=bool)
        log[valInd] = True
        fInd = np.cumsum(log) - 1
        self.vert = self.vert[log, :]
        self.faces = fInd[f].astype(np.int64)
        self.values = np.array(self.values[:, 1])
        # order for ABAQUS hex element 
        self.edges = np.reshape(self.faces[:, [0, 1, 1, 2, 2, 3, 3, 0]], [-1, 2])
        self.edges = np.sort(self.edges, 1)
        # Unify the edges
        self.edges, indC = np.unique(self.edges, return_inverse=True, axis=0)
    
    def calcPPI(self):
        """
        Function to calculate the peak pressure indicies

        """
        self.values
    
    def calcGradients(self):
        """
        Function to calculate the gradients in values along z and theta

        """
        np.gradient(self.values)
    
    def addSurrogate(self, dat, theta=True):
        """
        Numpy style docstring

        """
        if isinstance(dat, str):
            self.surrogate = np.load(dat).item()
        else:
            self.surrogate = dat
        #surr = self.surrogate
        if theta is True:
            self.surrogate['sm_theta'] = 10 ** self.surrogate['sm_theta']

    def surrPred(self, x, norm = True):
        """
        Numpy style docstring

        """
        surr = self.surrogate
        sh = surr['sm_U'].shape
        one = np.ones(sh[0])
        eigs = np.zeros(sh[2])
        for i in range(sh[2]):
            u = surr['sm_U'][:, : ,i]
            mu = surr['sm_mu'][i]
            y = surr['Y'][:, i]
            pl = surr['sm_pl'][:, i]
            theta = surr['sm_theta'][:,i]
            psi = np.exp(-np.sum(theta*np.power(np.abs(surr['X']-x), pl), axis=1))
            eigs[i] = mu + np.dot(psi.T, feMixin.comp(u, feMixin.comp(u.T,y-one*mu)))
            if norm is True:
                yNorm = surr['sm_yRange'][:, i]
                eigs[i] = (eigs[i] * (yNorm[1] - yNorm[0])) + yNorm[0]
        sf = (surr['pc_U'] * eigs).sum(axis=1)
        self.values[:] = surr['pc_mean'] + sf
    
    @staticmethod
    def comp(a, b):
        """
        Numpy style docstring

        """
        return solve(np.dot(a.T, a), np.dot(a.T, b))