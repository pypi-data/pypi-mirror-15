# cython: profile=False
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True


from libc.math cimport exp, sqrt
from libc.stdlib cimport malloc, free
import numpy as np
cimport numpy as np
from scipy import sparse
cimport cython
np.import_array()


__author__ = "mathewlee11"
cdef class FMRegressor(object):
    """def FM(self, int n_factors= 10, int n_iter=3, int k0=1, int k1=1,
    double w0=0, double lambda_w0=0, double lambda_w=0, double lambda_v=0,
    int min_target=0, int max_target=0, int shuffle=0, double init_stdev=0.01,
    int seed=42, int verbose=1)


    Factorization machine fitted with Alternating Least Squares

    Parameters
    ----------

    n_factors : int
        The dimensionality of the factorized 2-way interactions
    n_iter : int
        Number of iterations
    test_size: double
        Percent of the training set to use for validation
        Defaults to 0.01
    k0 : bool
        Use bias. Defaults to True.
    k1 : bool
        Use 1-way interactions (learn feature weights).
        Defaults to true.
    init_stdev : double, optional
        Standard deviation for initialization of 2-way factors.
        Defaults to 0.01.
    learning_rate_schedule : string, optional
        The learning rate:
            constant: eta = eta0
            optimal: eta = 1.0/(t+t0) [default]
            invscaling: eta = eta0 / pow(t, power_t)
    shuffle: bool
        Whether or not to shuffle training dataset before learning
    seed : int
        The seed of the pseudo random number generator
    verbose : bool
        Whether or not to print current iteration, training error


    """
    cdef:

        int n_factors
        int n_iter
        int n_samples
        int n_features
        int k0
        int k1
        int task
        int verbose
        int seed
        double w0
        double lambda_w0
        double lambda_w
        double lambda_v
        double min_target
        double max_target
        double init_stdev

        double [:] w
        double [:,:] V
        double * e
        double [:, :] q
        double [:] y


    def __init__(self,
                 int n_factors= 10,
                 int n_iter=3,
                 int k0=1,
                 int k1=1,
                 double lambda_w=0.0,
                 double lambda_v=0.0,
                 double min_target=0.0,
                 double max_target=0.0,
                 int shuffle=0,
                 double init_stdev=0.01,
                 int seed=42,
                 int verbose=1,
                ):

        self.n_factors = n_factors
        self.init_stdev = init_stdev
        self.n_iter = n_iter
        self.k0 = k0
        self.k1 = k1
        self.verbose = verbose
        self.min_target = min_target
        self.max_target = max_target
        self.seed = seed
        self.lambda_w = lambda_w
        self.lambda_v = lambda_v

    cdef double _scale_prediction(self, double p):
        p = _min(self.max_target, p)
        p = _max(self.min_target, p)
        return p

    cdef double _predict_instance(self,
                          int * feature_indices,
                          double * feature_values,
                          int start_index,
                          int end_index) :

        cdef int n_factors = self.n_factors
        cdef double * sum_ = <double *> malloc(n_factors * sizeof(double))
        cdef double * sum_sqr_ = <double *> malloc(n_factors * sizeof(double))
        cdef Py_ssize_t i, latent_index

        for i in range(n_factors):
            sum_[i] = 0.0
            sum_sqr_[i] = 0.0

        cdef double [:] w = self.w
        cdef double [:, :] V = self.V
        cdef double result = 0
        cdef double d
        cdef int f_index
        cdef double f_value


        if self.k0:
            result += self.w0

        if self.k1:
            for i in range(start_index, end_index):
                f_index = feature_indices[i]
                f_value = feature_values[i]
                result += w[f_index] * f_value

        for latent_index in range(n_factors):
            sum_[latent_index] = 0.0
            sum_sqr_[latent_index] = 0.0

            for i in range(start_index, end_index):
                f_index = feature_indices[i]
                f_value = feature_values[i]

                d = V[latent_index, f_index] * f_value
                sum_[latent_index] += d
                sum_sqr_[latent_index] += d*d

            result += 0.5 * (sum_[latent_index] * sum_[latent_index] - sum_sqr_[latent_index])
        free(sum_)
        free(sum_sqr_)
        return self._scale_prediction(result)

    cdef void _init_eq(self,
                  int * indptr,
                  int * indices,
                  double * data) :

        cdef int n_factors = self.n_factors
        cdef int n_samples = self.n_samples
        cdef double result
        cdef double [:, :] q = self.q
        cdef double [:] y = self.y
        cdef double [:, :] V = self.V
        cdef double * e = self.e
        cdef Py_ssize_t row, f, i
        for row in range(n_samples):


            e[row] = self._predict_instance(indices, data, indptr[row], indptr[row+1]) - y[row]

            for f in range(n_factors):

                result = 0.0

                for i in range(indptr[row], indptr[row+1]):
                    result += V[f, indices[i]] * data[i]

                q[row, f] = result

    cdef void _one_way_interactions_als(self,
                               int * col_indptr,
                               int * col_indices,
                               double * col_data) :

        cdef int n_samples = self.n_samples
        cdef int n_features = self.n_features
        cdef double lambda_w = self.lambda_w
        cdef double w_l, num, den, x_l
        cdef double * e = self.e
        cdef double [:] w = self.w
        cdef Py_ssize_t l, ind
        cdef int row
        for l in range(n_features):
                w_l = 0.0
                num = 0.0
                den = 0.0
                for ind in range(col_indptr[l], col_indptr[l+1]):
                    row = col_indices[ind]
                    x_l = col_data[ind]


                    num += (e[row] - w[l] * x_l) * x_l

                    den += x_l * x_l + lambda_w
                # add lambda_w for the x_ls with value 0
                den += lambda_w * (n_samples - (col_indptr[l+1] - col_indptr[l]))
                if num != 0.0:
                    w_l = -num/den
                else:
                    w_l = 0.0
                for ind in range(col_indptr[l], col_indptr[l+1]):
                    row = col_indices[ind]
                    x_l = col_data[ind]
                    self.e[row] += (w_l - w[l]) * x_l


                self.w[l] = w_l

    cdef void _one_way_interactions_sgd(self, int * row_indptr,
                                        int * row_indices, double * row_data):
        cdef double [:] y = self.y
        cdef int n_samples = self.n_samples
        cdef int n_features = self.n_features
        cdef double p
        cdef int i

        for i in range(n_samples):
            target = y[i]
            p = self._predict_instance(row_indices, row_data,
                                       row_indptr[i], row_indptr[i+1])


    cdef void _two_way_interactions_als(self,
                               int * col_indptr,
                               int * col_indices,
                               double * col_data) :

        cdef int n_factors = self.n_factors
        cdef int n_features = self.n_features
        cdef int n_samples = self.n_samples
        cdef int row
        cdef double vlf, den, num, x_l, h_vlf
        cdef Py_ssize_t f, l, x, ind
        cdef double lambda_v = self.lambda_v
        cdef double [:, :] q = self.q
        cdef double [:, :] V = self.V
        cdef double * e = self.e
        for f in range(n_factors):
            for l in range(n_features):
                vlf = 0.0
                den = 0.0
                num = 0.0
                for ind in range(col_indptr[l], col_indptr[l+1]):
                    row = col_indices[ind]
                    x_l = col_data[ind]
                    h_vlf = x_l * q[row, f] - x_l * x_l * V[f, l]
                    num += (e[row] - V[f, l] * h_vlf) * h_vlf
                    den += h_vlf * h_vlf + lambda_v

                # add lambda_w for the x_ls with value 0
                den += self.lambda_v * (n_samples - (col_indptr[l+1] - col_indptr[l]))
                vlf = -num/den
                if num != 0.0:
                    vlf = -num/den
                else:
                    vlf = 0.0
                for ind in range(col_indptr[l], col_indptr[l+1]):
                    row = col_indices[ind]
                    x_l = col_data[ind]
                    h_vlf = x_l * q[row, f] - x_l * x_l * V[f, l]
                        # gettin experimental
                    e[row] += (vlf - V[f, l]) * h_vlf
                    q[row, f] += (vlf - V[f, l]) * x_l

                V[f, l] = vlf

    cdef void _fit(self,
              int * row_indptr,
              int * row_indices,
              double * row_data,
              int * col_indptr,
              int * col_indices,
              double * col_data) :


        cdef double error = 0
        cdef int n_samples = self.n_samples
        self._init_eq(row_indptr, row_indices, row_data)
        cdef double * e = self.e
        cdef double lambda_w0 = self.lambda_w0
        cdef Py_ssize_t epoch, i, x
        cdef int f_index
        cdef double f_value, w0


        for epoch in range(self.n_iter):

            if self.k0:
                w0 = 0

                for x in range(self.n_samples):
                    w0 -= e[x] - self.w0

                w0 /= n_samples + lambda_w0

                for x in range(n_samples):
                    e[x] += w0 - self.w0
                self.w0 = w0

            if self.k1:
                self._one_way_interactions_als(col_indptr, col_indices, col_data)

            self._two_way_interactions_als(col_indptr, col_indices, col_data)
            error = 0
            for i in range(self.n_samples):
                error += e[i] * e[i]
            if self.verbose:
                print("epoch %d" % (epoch+1)), sqrt(error/ n_samples)


    def fit(self, X, y):
        """Fit factorization machine using Alternating Least Squares

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            Training data

        y : numpy array of shape [n_samples]
            Target values

        Returns
        -------
        self : returns an instance of self.
        """
        self.n_samples = X.shape[0]
        self.n_features = X.shape[1]
        self.w = np.zeros(self.n_features)
        np.random.seed(42)
        self.V = np.random.normal(size=(self.n_factors, self.n_features),
                                  scale=self.init_stdev)
        self.e = <double *> malloc(self.n_samples * sizeof(double))
        self.q = np.zeros((self.n_samples, self.n_factors))

        self.y = y.astype(np.double)
        if X.dtype != np.double:
            X = X.astype(np.double)

        # predictions are row based and interactions are column based so
        # by doing it this way we get the best of both worlds!
        if type(X) != sparse.csr_matrix:
            X_row = sparse.csr_matrix(X)
        else:
            X_row = X

        X_col = X_row.tocsc()

        cdef int [:] row_indptr = X_row.indptr
        cdef int [:] row_indices = X_row.indices
        cdef double [:] row_data = X_row.data

        cdef int [:] col_indptr = X_col.indptr
        cdef int [:] col_indices = X_col.indices
        cdef double [:] col_data = X_col.data

        self._fit(&row_indptr[0], &row_indices[0], &row_data[0],
                  &col_indptr[0], &col_indices[0], &col_data[0])
        free(self.e)

        return self

    @property
    def _V(self):
        return np.asarray(self.V)
    @property
    def _w(self):
        return np.asarray(self.w)
    cdef _predict(self,
                  int * indptr,
                  int * indices,
                  double * data,
                  int num_preds):

        preds = np.empty(num_preds)
        cdef Py_ssize_t i

        for i in range(num_preds):
            preds[i] = self._predict_instance(indices, data, indptr[i], indptr[i+1])
        return preds
    def predict(self, X):
        """Predict using the factorization machine

        Parameters
        ----------
        X : sparse matrix, shape = [n_samples, n_features]


        Returns
        -------

        array, shape = [n_samples]
           Predicted target values per element in X.
        """
        dtype = X.dtype
        if X.dtype != np.double:
            X = X.astype(np.double)
        if type(X) != sparse.csr_matrix:
            X = sparse.csr_matrix(X)

        cdef int [:] indptr = X.indptr
        cdef int [:] indices = X.indices
        cdef double [:] data = X.data
        num_preds = X.shape[0]
        preds = self._predict(&indptr[0], &indices[0], &data[0], num_preds)
        return preds.astype(dtype)


cdef inline double _max(double a, double b) :
    return a if a >= b else b

cdef inline double _min(double a, double b) :
    return a if a <= b else b
