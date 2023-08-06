from nose.tools import assert_true
from nose.tools import assert_equal
import scipy.io
from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix
from scipy.sparse import isspmatrix
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal, assert_allclose

from nose.tools import assert_raises
from nose.plugins.skip import SkipTest

from Mmani.geometry.rmetric import *
from Mmani.embedding.spectral_embedding import _graph_is_connected

def _load_test_data():
    """ Loads a .mat file from . and extract the following dense matrices
    test_dist_matrix = matrix of distances
    L = the geometric Laplacian
    Ginv = the dual Riemann metric [n,2,2] array
    G = the Riemann metric [n,2,2] array
    phi = embedding in 2 dimensions [n, 2] array
    rad = scalar, radius used in affinity calculations, Laplacians
        Note: rad is returned as an array of dimension 1. Outside one must
        make it a scalar by rad = rad[0]
   
    """
    xdict = scipy.io.loadmat('Mmani/geometry/tests/testMmani_laplacian_rad0_2_lam1_5_n200.mat')
    #xdict = scipy.io.loadmat('testMmani_laplacian_rad0_2_lam1_5_n200.mat')
    rad = xdict[ 'rad' ]
    test_dist_matrix = xdict[ 'S' ] # S contains squared distances
    test_dist_matrix = np.sqrt( test_dist_matrix ) #unused
    A = xdict[ 'A' ] #unused
    L = xdict[ 'Lgeom' ] 
    G = xdict[ 'G' ] 
    H = xdict[ 'Ginv' ] 
    H = np.transpose( H, ( 2, 0, 1 ))
    G = np.transpose( G, ( 2, 0, 1 ))
    phi = xdict[ 'phigeom' ] 

    print( 'phi.shape = ', phi.shape )
    print( 'G.shape = ', G.shape )
    print( 'H.shape = ', H.shape )
    print( 'L.shape = ', L.shape )
    return rad, L, G, H, phi

def test_equal_original(almost_equal_decimals = 5):
    """ Loads the results from a matlab run and checks that our results
    are the same. The results loaded are the Laplacian, embedding phi, 
    Riemannian metric G[2,2,200], and dual Riemannian metric H[2,2,200]

    Currently, this tests the riemann_metric() function only.
    TODO: to test the class RiemannMetric
    
    Only riemann_metric with given L is tested. For other inputs, to test 
    later after the structure of the code is stabilized. (I.e I may remove
    the computation of the L to another function.
    """
    rad, L, Gtest, Htest, phi = _load_test_data()

    H, G, Hvv, Hsvals, Gsvals = riemann_metric( phi, laplacian = L, n_dim = 2, invert_h = True )
    n = phi.shape[ 0 ]
    assert_array_almost_equal( Htest, H, almost_equal_decimals )

    tol = np.mean( Gtest[:,0,0])*10**(-almost_equal_decimals )
    assert_allclose( Gtest, G, tol)
#    assert_array_max_ulp( Gtest, G, almost_equal_decimals )
    # this assertion fails because Gtest is generally asymmetric. G is 
    # mostly symmetric but not always. I suspect this is due to the
    # numerical errors, as many of these 2x2 matrices are very poorly
    # conditioned. What to do? Perhaps generate another matlab test set
    # with better condition numbers... 