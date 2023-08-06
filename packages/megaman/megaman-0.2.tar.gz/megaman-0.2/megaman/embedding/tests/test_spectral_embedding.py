# LICENSE: Simplified BSD https://github.com/mmp2/megaman/blob/master/LICENSE

from nose.tools import assert_true
from nose.tools import assert_equal

from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix
from scipy.sparse import isspmatrix
import scipy.sparse as sp
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_allclose
import warnings

from nose.tools import assert_raises
from nose.plugins.skip import SkipTest

from megaman.embedding.spectral_embedding import SpectralEmbedding, spectral_embedding, _graph_is_connected
import megaman.geometry.geometry as geom

from sklearn.metrics import normalized_mutual_info_score
from sklearn.datasets.samples_generator import make_blobs


# non centered, sparse centers to check the
centers = np.array([
    [0.0, 5.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 4.0, 0.0, 0.0],
    [1.0, 0.0, 0.0, 5.0, 1.0],
])
n_samples = 1000
n_clusters, n_features = centers.shape
S, true_labels = make_blobs(n_samples=n_samples, centers=centers,
                            cluster_std=1., random_state=42)


def _check_with_col_sign_flipping(A, B, tol=0.0):
    """ Check array A and B are equal with possible sign flipping on
    each columns"""
    sign = True
    for column_idx in range(A.shape[1]):
        sign = sign and ((((A[:, column_idx] -
                            B[:, column_idx]) ** 2).mean() <= tol ** 2) or
                         (((A[:, column_idx] +
                            B[:, column_idx]) ** 2).mean() <= tol ** 2))
        if not sign:
            return False
    return True

def test_spectral_embedding_two_components(seed=36):
    """Test spectral embedding with two components"""
    random_state = np.random.RandomState(seed)
    n_sample = 100
    affinity = np.zeros(shape=[n_sample * 2,
                               n_sample * 2])
    # first component
    affinity[0:n_sample,
             0:n_sample] = np.abs(random_state.randn(n_sample, n_sample)) + 2
    # second component
    affinity[n_sample::,
             n_sample::] = np.abs(random_state.randn(n_sample, n_sample)) + 2
    # connection
    affinity[0, n_sample + 1] = 1
    affinity[n_sample + 1, 0] = 1
    affinity.flat[::2 * n_sample + 1] = 0
    affinity = 0.5 * (affinity + affinity.T)

    true_label = np.zeros(shape=2 * n_sample)
    true_label[0:n_sample] = 1

    se_precomp = SpectralEmbedding(n_components=1,
                                   random_state=np.random.RandomState(seed),
                                   eigen_solver = 'arpack')
    embedded_coordinate = se_precomp.fit_transform(affinity,
                                                   input_type='affinity')

    # thresholding on the first components using 0.
    label_ = np.array(embedded_coordinate.ravel() < 0, dtype="float")
    assert_equal(normalized_mutual_info_score(true_label, label_), 1.0)

def test_diffusion_embedding_two_components_no_diffusion_time(seed=36):
    """Test spectral embedding with two components"""
    random_state = np.random.RandomState(seed)
    n_sample = 100
    affinity = np.zeros(shape=[n_sample * 2,
                               n_sample * 2])
    # first component
    affinity[0:n_sample,
             0:n_sample] = np.abs(random_state.randn(n_sample, n_sample)) + 2
    # second component
    affinity[n_sample::,
             n_sample::] = np.abs(random_state.randn(n_sample, n_sample)) + 2
    # connection
    affinity[0, n_sample + 1] = 1
    affinity[n_sample + 1, 0] = 1
    affinity.flat[::2 * n_sample + 1] = 0
    affinity = 0.5 * (affinity + affinity.T)

    true_label = np.zeros(shape=2 * n_sample)
    true_label[0:n_sample] = 1
    geom_params = {'laplacian_method':'geometric'}
    se_precomp = SpectralEmbedding(n_components=1,
                                   random_state=np.random.RandomState(seed),
                                   eigen_solver = 'arpack',
                                   diffusion_maps = True,
                                   geom = geom_params)
    embedded_coordinate = se_precomp.fit_transform(affinity,
                                                   input_type='affinity')

    # thresholding on the first components using 0.
    label_ = np.array(embedded_coordinate.ravel() < 0, dtype="float")
    assert_equal(normalized_mutual_info_score(true_label, label_), 1.0)

def test_diffusion_embedding_two_components_diffusion_time_one(seed=36):
    """Test spectral embedding with two components"""
    random_state = np.random.RandomState(seed)
    n_sample = 100
    affinity = np.zeros(shape=[n_sample * 2,
                               n_sample * 2])
    # first component
    affinity[0:n_sample,
             0:n_sample] = np.abs(random_state.randn(n_sample, n_sample)) + 2
    # second component
    affinity[n_sample::,
             n_sample::] = np.abs(random_state.randn(n_sample, n_sample)) + 2
    # connection
    affinity[0, n_sample + 1] = 1
    affinity[n_sample + 1, 0] = 1
    affinity.flat[::2 * n_sample + 1] = 0
    affinity = 0.5 * (affinity + affinity.T)

    true_label = np.zeros(shape=2 * n_sample)
    true_label[0:n_sample] = 1
    geom_params = {'laplacian_method':'geometric'}
    se_precomp = SpectralEmbedding(n_components=1,
                                   random_state=np.random.RandomState(seed),
                                   eigen_solver = 'arpack',
                                   diffusion_maps = True,
                                   diffusion_time = 1.0,
                                   geom = geom_params)
    embedded_coordinate = se_precomp.fit_transform(affinity,
                                                   input_type='affinity')

    # thresholding on the first components using 0.
    label_ = np.array(embedded_coordinate.ravel() < 0, dtype="float")
    assert_equal(normalized_mutual_info_score(true_label, label_), 1.0)

def test_spectral_embedding_precomputed_affinity(seed=36,almost_equal_decimals=5):
    """Test spectral embedding with precomputed kernel"""
    radius = 4.0
    se_precomp = SpectralEmbedding(n_components=2,
                                   random_state=np.random.RandomState(seed))
    geom_params = {'affinity_kwds':{'radius':radius}, 'adjacency_kwds':{'radius':radius},
                   'adjacency_method':'brute'}
    se_rbf = SpectralEmbedding(n_components=2, random_state=np.random.RandomState(seed),
                               geom = geom_params)
    G = geom.Geometry(adjacency_method = 'brute', adjacency_kwds = {'radius':radius},
                      affinity_kwds = {'radius':radius})
    G.set_data_matrix(S)
    A = G.compute_affinity_matrix()
    embed_precomp = se_precomp.fit_transform(A, input_type = 'affinity')
    embed_rbf = se_rbf.fit_transform(S, input_type = 'data')
    assert_array_almost_equal(
        se_precomp.affinity_matrix_.todense(), se_rbf.affinity_matrix_.todense(),
        almost_equal_decimals)
    assert_true(_check_with_col_sign_flipping(embed_precomp, embed_rbf, 0.05))


def test_spectral_embedding_amg_solver(seed=20):
    """Test spectral embedding with amg solver vs arpack using symmetric laplacian"""
    radius = 4.0
    geom_params = {'affinity_kwds':{'radius':radius}, 'adjacency_kwds':{'radius':radius}, 'adjacency_method':'brute',
                   'laplacian_method':'symmetricnormalized'}
    try:
        import pyamg
    except ImportError:
        raise SkipTest("pyamg not available.")
    se_amg = SpectralEmbedding(n_components=2,eigen_solver="amg",
                               random_state=np.random.RandomState(seed), geom = geom_params)
    se_arpack = SpectralEmbedding(n_components=2, eigen_solver="arpack", geom = geom_params,
                                  random_state=np.random.RandomState(seed))
    embed_amg = se_amg.fit_transform(S)
    embed_arpack = se_arpack.fit_transform(S)
    assert_true(_check_with_col_sign_flipping(embed_amg, embed_arpack, 0.05))


def test_spectral_embedding_symmetrzation(seed=36):
    """Test spectral embedding with amg solver vs arpack using non symmetric laplacian"""
    radius = 4.0
    geom_params = {'affinity_kwds':{'radius':radius}, 'adjacency_kwds':{'radius':radius}, 'adjacency_method':'brute',
                   'laplacian_method':'geometric'}
    try:
        import pyamg
    except ImportError:
        raise SkipTest("pyamg not available.")
    se_amg = SpectralEmbedding(n_components=2,eigen_solver="amg",
                               random_state=np.random.RandomState(seed), geom = geom_params)
    se_arpack = SpectralEmbedding(n_components=2, eigen_solver="arpack", geom = geom_params,
                                  random_state=np.random.RandomState(seed))
    embed_amg = se_amg.fit_transform(S)
    embed_arpack = se_arpack.fit_transform(S)
    assert_true(_check_with_col_sign_flipping(embed_amg, embed_arpack, 0.05))


def test_spectral_embedding_unknown_eigensolver(seed=36):
    """Test that SpectralClustering fails with an unknown eigensolver"""
    se = SpectralEmbedding(n_components=1,
                           random_state=np.random.RandomState(seed),
                           eigen_solver="<unknown>")
    assert_raises(ValueError, se.fit, S)


def test_connectivity(seed=36):
    """Test that graph connectivity test works as expected"""
    graph = np.array([[1, 0, 0, 0, 0],
                      [0, 1, 1, 0, 0],
                      [0, 1, 1, 1, 0],
                      [0, 0, 1, 1, 1],
                      [0, 0, 0, 1, 1]])
    assert_equal(_graph_is_connected(graph), False)
    assert_equal(_graph_is_connected(csr_matrix(graph)), False)
    assert_equal(_graph_is_connected(csc_matrix(graph)), False)
    graph = np.array([[1, 1, 0, 0, 0],
                      [1, 1, 1, 0, 0],
                      [0, 1, 1, 1, 0],
                      [0, 0, 1, 1, 1],
                      [0, 0, 0, 1, 1]])
    assert_equal(_graph_is_connected(graph), True)
    assert_equal(_graph_is_connected(csr_matrix(graph)), True)
    assert_equal(_graph_is_connected(csc_matrix(graph)), True)
