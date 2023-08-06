from __future__ import division
import gc

import numpy as np
from numpy import deg2rad

import modelDB
import compmech.panel.modelDB as panmodelDB
from compmech.logger import msg, warn
from compmech.composite import laminate


class BladeStiff2D(object):
    r"""Blade Stiffener using 2D Formulation for Flange

    Blade-type of stiffener model using a 2D formulation for the flange and a
    2D formulation for the base (padup)::


                 || --> flange       |
                 ||                  |-> stiffener
               ======  --> padup     |
      =========================  --> panels
         Panel1      Panel2

    Both the flange and the base are optional. The stiffener's base is modeled
    using the same approximation functions as the skin, with the proper
    offset.

    Each stiffener has a constant `y_s` coordinate.

    """
    def __init__(self, bay, mu, panel1, panel2, ys, bb, bf, bstack, bplyts,
            blaminaprops, fstack, fplyts, flaminaprops):
        self.bay = bay
        self.panel1 = panel1
        self.panel2 = panel2
        self.model = 'bladestiff2d_clt_donnell_bardell'
        self.m1 = 14
        self.n1 = 11
        self.mu = mu
        self.ys = ys
        self.bb = bb
        self.hb = 0.
        self.bf = bf
        self.hf = 0.
        self.forces = []

        self.kt = 1.e8
        self.kr = 1.e8

        self.Nxx = None
        self.Nxy = None

        self.bstack = bstack
        self.bplyts = bplyts
        self.blaminaprops = blaminaprops
        self.fstack = fstack
        self.fplyts = fplyts
        self.flaminaprops = flaminaprops
        self.blam = None
        self.flam = None

        self.k0 = None
        self.kM = None
        self.kG0 = None

        self.u1txf = 0.
        self.u1rxf = 1.
        self.u2txf = 0.
        self.u2rxf = 1.
        self.v1txf = 0.
        self.v1rxf = 1.
        self.v2txf = 0.
        self.v2rxf = 1.
        self.w1txf = 0.
        self.w1rxf = 1.
        self.w2txf = 0.
        self.w2rxf = 1.

        self.u1tyf = 1.
        self.u1ryf = 1.
        self.u2tyf = 1.
        self.u2ryf = 1.
        self.v1tyf = 1.
        self.v1ryf = 1.
        self.v2tyf = 1.
        self.v2ryf = 1.
        self.w1tyf = 1.
        self.w1ryf = 1.
        self.w2tyf = 1.
        self.w2ryf = 1.

        self._rebuild()


    def _rebuild(self):
        if self.fstack is not None:
            self.hf = sum(self.fplyts)
            self.flam = laminate.read_stack(self.fstack, plyts=self.fplyts,
                                            laminaprops=self.flaminaprops)
            self.flam.calc_equivalent_modulus()

        h = 0.5*sum(self.panel1.plyts) + 0.5*sum(self.panel2.plyts)
        if self.bstack is not None:
            hb = sum(self.bplyts)
            self.dpb = h/2. + hb/2.
            self.blam = laminate.read_stack(self.bstack, plyts=self.bplyts,
                                            laminaprops=self.blaminaprops,
                                            offset=(-h/2.-hb/2.))
            self.hb = hb

        assert self.panel1.model == self.panel2.model
        assert self.panel1.m == self.panel2.m
        assert self.panel1.n == self.panel2.n
        assert self.panel1.r == self.panel2.r
        assert self.panel1.alphadeg == self.panel2.alphadeg


    def calc_k0(self, size=None, row0=0, col0=0, silent=False, finalize=True):
        """Calculate the linear constitutive stiffness matrix
        """
        self._rebuild()
        msg('Calculating k0... ', level=2, silent=silent)

        panmod = panmodelDB.db[self.panel1.model]['matrices']
        mod = modelDB.db[self.model]['matrices']

        bay = self.bay
        a = bay.a
        b = bay.b
        r = bay.r if bay.r is not None else 0.
        m = bay.m
        n = bay.n
        alphadeg = self.panel1.alphadeg
        alphadeg = alphadeg if alphadeg is not None else 0.
        alpharad = deg2rad(alphadeg)

        m1 = self.m1
        n1 = self.n1
        bf = self.bf

        k0 = 0.
        if self.blam is not None:
            # stiffener pad-up
            Fsb = self.blam.ABD
            y1 = self.ys - self.bb/2.
            y2 = self.ys + self.bb/2.
            k0 += panmod.fk0y1y2(y1, y2, a, b, r, alpharad, Fsb, m, n,
                                 bay.u1tx, bay.u1rx, bay.u2tx, bay.u2rx,
                                 bay.v1tx, bay.v1rx, bay.v2tx, bay.v2rx,
                                 bay.w1tx, bay.w1rx, bay.w2tx, bay.w2rx,
                                 bay.u1ty, bay.u1ry, bay.u2ty, bay.u2ry,
                                 bay.v1ty, bay.v1ry, bay.v2ty, bay.v2ry,
                                 bay.w1ty, bay.w1ry, bay.w2ty, bay.w2ry,
                                 size, 0, 0)

        #TODO add contribution from Nxx_cte from flange and padup
        if self.flam is not None:
            kt = self.kt
            kr = self.kr
            F = self.flam.ABD
            k0 += mod.fk0f(a, bf, F, m1, n1,
                           self.u1txf, self.u1rxf, self.u2txf, self.u2rxf,
                           self.v1txf, self.v1rxf, self.v2txf, self.v2rxf,
                           self.w1txf, self.w1rxf, self.w2txf, self.w2rxf,
                           self.u1tyf, self.u1ryf, self.u2tyf, self.u2ryf,
                           self.v1tyf, self.v1ryf, self.v2tyf, self.v2ryf,
                           self.w1tyf, self.w1ryf, self.w2tyf, self.w2ryf,
                           size, row0, col0)

            # connectivity between skin-stiffener flange
            k0 += mod.fkCss(kt, kr, self.ys, a, b, m, n,
                            bay.u1tx, bay.u1rx, bay.u2tx, bay.u2rx,
                            bay.v1tx, bay.v1rx, bay.v2tx, bay.v2rx,
                            bay.w1tx, bay.w1rx, bay.w2tx, bay.w2rx,
                            bay.u1ty, bay.u1ry, bay.u2ty, bay.u2ry,
                            bay.v1ty, bay.v1ry, bay.v2ty, bay.v2ry,
                            bay.w1ty, bay.w1ry, bay.w2ty, bay.w2ry,
                            size, 0, 0)
            k0 += mod.fkCsf(kt, kr, self.ys, a, b, bf, m, n, m1, n1,
                            bay.u1tx, bay.u1rx, bay.u2tx, bay.u2rx,
                            bay.v1tx, bay.v1rx, bay.v2tx, bay.v2rx,
                            bay.w1tx, bay.w1rx, bay.w2tx, bay.w2rx,
                            bay.u1ty, bay.u1ry, bay.u2ty, bay.u2ry,
                            bay.v1ty, bay.v1ry, bay.v2ty, bay.v2ry,
                            bay.w1ty, bay.w1ry, bay.w2ty, bay.w2ry,
                            self.u1txf, self.u1rxf, self.u2txf, self.u2rxf,
                            self.v1txf, self.v1rxf, self.v2txf, self.v2rxf,
                            self.w1txf, self.w1rxf, self.w2txf, self.w2rxf,
                            self.u1tyf, self.u1ryf, self.u2tyf, self.u2ryf,
                            self.v1tyf, self.v1ryf, self.v2tyf, self.v2ryf,
                            self.w1tyf, self.w1ryf, self.w2tyf, self.w2ryf,
                            size, 0, col0)
            k0 += mod.fkCff(kt, kr, a, bf, m1, n1,
                            self.u1txf, self.u1rxf, self.u2txf, self.u2rxf,
                            self.v1txf, self.v1rxf, self.v2txf, self.v2rxf,
                            self.w1txf, self.w1rxf, self.w2txf, self.w2rxf,
                            self.u1tyf, self.u1ryf, self.u2tyf, self.u2ryf,
                            self.v1tyf, self.v1ryf, self.v2tyf, self.v2ryf,
                            self.w1tyf, self.w1ryf, self.w2tyf, self.w2ryf,
                            size, row0, col0)

        if finalize:
            assert np.any(np.isnan(k0.data)) == False
            assert np.any(np.isinf(k0.data)) == False
            k0 = csr_matrix(make_symmetric(k0))

        self.k0 = k0

        #NOTE forcing Python garbage collector to clean the memory
        #     it DOES make a difference! There is a memory leak not
        #     identified, probably in the csr_matrix process
        gc.collect()

        msg('finished!', level=2, silent=silent)


    def calc_kG0(self, size=None, row0=0, col0=0, silent=False, finalize=True,
            c=None):
        """Calculate the linear geometric stiffness matrix
        """
        #TODO
        if c is not None:
            raise NotImplementedError('numerical kG0 not implemented')

        self._rebuild()
        msg('Calculating kG0... ', level=2, silent=silent)

        mod = modelDB.db[self.model]['matrices']

        bay = self.bay
        a = bay.a

        kG0 = 0.

        if self.blam is not None:
            # stiffener pad-up
            #TODO include kG0 for pad-up (Nxx load that arrives there)
            pass

        if self.flam is not None:
            F = self.flam.ABD
            # stiffener flange

            Nxx = self.Nxx if self.Nxx is not None else 0.
            Nxy = self.Nxy if self.Nxy is not None else 0.
            kG0 += mod.fkG0f(Nxx, 0., Nxy, a, self.bf, self.m1, self.n1,
                             self.w1txf, self.w1rxf, self.w2txf, self.w2rxf,
                             self.w1tyf, self.w1ryf, self.w2tyf, self.w2ryf,
                             size, row0, col0)

        if finalize:
            assert np.any((np.isnan(kG0.data) | np.isinf(kG0.data))) == False
            kG0 = csr_matrix(make_symmetric(kG0))

        self.kG0 = kG0

        #NOTE forcing Python garbage collector to clean the memory
        #     it DOES make a difference! There is a memory leak not
        #     identified, probably in the csr_matrix process
        gc.collect()

        msg('finished!', level=2, silent=silent)


    def calc_kM(self, size=None, row0=0, col0=0, silent=False, finalize=True):
        """Calculate the mass matrix
        """
        self._rebuild()
        msg('Calculating kM... ', level=2, silent=silent)

        panmod = panmodelDB.db[self.panel1.model]['matrices']
        mod = modelDB.db[self.model]['matrices']

        bay = self.bay
        a = bay.a
        b = bay.b
        r = bay.r if bay.r is not None else 0.
        m = bay.m
        n = bay.n
        alphadeg = self.panel1.alphadeg
        alphadeg = alphadeg if alphadeg is not None else 0.
        alpharad = deg2rad(alphadeg)

        m1 = self.m1
        n1 = self.n1
        bf = self.bf

        kM = 0.

        if self.blam is not None:
            # stiffener pad-up
            y1 = self.ys - self.bb/2.
            y2 = self.ys + self.bb/2.
            kM += panmod.fkMy1y2(y1, y2, self.mu, self.dpb, self.hb,
                          a, b, r, alpharad, m, n,
                          bay.u1tx, bay.u1rx, bay.u2tx, bay.u2rx,
                          bay.v1tx, bay.v1rx, bay.v2tx, bay.v2rx,
                          bay.w1tx, bay.w1rx, bay.w2tx, bay.w2rx,
                          bay.u1ty, bay.u1ry, bay.u2ty, bay.u2ry,
                          bay.v1ty, bay.v1ry, bay.v2ty, bay.v2ry,
                          bay.w1ty, bay.w1ry, bay.w2ty, bay.w2ry,
                          size, 0, 0)

        if self.flam is not None:
            kM += mod.fkMf(self.mu, self.hf, a, bf, 0., m1, n1,
                           self.u1txf, self.u1rxf, self.u2txf, self.u2rxf,
                           self.v1txf, self.v1rxf, self.v2txf, self.v2rxf,
                           self.w1txf, self.w1rxf, self.w2txf, self.w2rxf,
                           self.u1tyf, self.u1ryf, self.u2tyf, self.u2ryf,
                           self.v1tyf, self.v1ryf, self.v2tyf, self.v2ryf,
                           self.w1tyf, self.w1ryf, self.w2tyf, self.w2ryf,
                           size, row0, col0)

        if finalize:
            assert np.any(np.isnan(kM.data)) == False
            assert np.any(np.isinf(kM.data)) == False
            kM = csr_matrix(make_symmetric(kM))

        self.kM = kM

        #NOTE forcing Python garbage collector to clean the memory
        #     it DOES make a difference! There is a memory leak not
        #     identified, probably in the csr_matrix process
        gc.collect()

        msg('finished!', level=2, silent=silent)


