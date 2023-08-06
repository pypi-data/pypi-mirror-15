#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=False
"""
Hamilton filter

Author: Chad Fulton  
License: Simplified-BSD
"""

# Typical imports
import numpy as np
import warnings
cimport numpy as np
cimport cython

cdef int FORTRAN = 1

def shamilton_filter(int nobs, int k_regimes, int order,
                              np.float32_t [:,:,:] transition,
                              np.float32_t [:,:] conditional_likelihoods,
                              np.float32_t [:] joint_likelihoods,
                              np.float32_t [:,:] predicted_joint_probabilities,
                              np.float32_t [:,:] filtered_joint_probabilities):
    cdef int t, i, j, k, ix, transition_t = 0, time_varying_transition
    cdef:
        int k_regimes_order_m1 = k_regimes**(order - 1)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.float32_t [:] likelihoods, tmp

    time_varying_transition = transition.shape[2] > 1
    likelihoods = np.zeros(k_regimes_order_p1, dtype=np.float32)
    tmp = np.zeros(k_regimes_order, dtype=np.float32)

    for t in range(nobs):
        if time_varying_transition:
            transition_t = t

        ix = 0
        tmp[:] = 0
        for j in range(k_regimes_order):
            for i in range(k_regimes):
                tmp[j] = tmp[j] + filtered_joint_probabilities[ix, t]
                ix = ix + 1

        ix = 0
        for i in range(k_regimes):
            for j in range(k_regimes):
                for k in range(k_regimes_order_m1):
                    predicted_joint_probabilities[ix, t] = (
                        tmp[j * k_regimes_order_m1 + k] *
                        transition[i, j, transition_t])
                    ix += 1

        for i in range(k_regimes_order_p1):
            likelihoods[i] = (
                predicted_joint_probabilities[i, t] *
                conditional_likelihoods[i, t])
            joint_likelihoods[t] = joint_likelihoods[t] + likelihoods[i]

        for i in range(k_regimes_order_p1):
            if joint_likelihoods[t] == 0:
                filtered_joint_probabilities[i, t+1] = np.inf
            else:
                filtered_joint_probabilities[i, t+1] = (
                    likelihoods[i] / joint_likelihoods[t])


def zhamilton_filter(int nobs, int k_regimes, int order,
                              np.complex128_t [:,:,:] transition,
                              np.complex128_t [:,:] conditional_likelihoods,
                              np.complex128_t [:] joint_likelihoods,
                              np.complex128_t [:,:] predicted_joint_probabilities,
                              np.complex128_t [:,:] filtered_joint_probabilities):
    cdef int t, i, j, k, ix, transition_t = 0, time_varying_transition
    cdef:
        int k_regimes_order_m1 = k_regimes**(order - 1)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.complex128_t [:] likelihoods, tmp

    time_varying_transition = transition.shape[2] > 1
    likelihoods = np.zeros(k_regimes_order_p1, dtype=complex)
    tmp = np.zeros(k_regimes_order, dtype=complex)

    for t in range(nobs):
        if time_varying_transition:
            transition_t = t

        ix = 0
        tmp[:] = 0
        for j in range(k_regimes_order):
            for i in range(k_regimes):
                tmp[j] = tmp[j] + filtered_joint_probabilities[ix, t]
                ix = ix + 1

        ix = 0
        for i in range(k_regimes):
            for j in range(k_regimes):
                for k in range(k_regimes_order_m1):
                    predicted_joint_probabilities[ix, t] = (
                        tmp[j * k_regimes_order_m1 + k] *
                        transition[i, j, transition_t])
                    ix += 1

        for i in range(k_regimes_order_p1):
            likelihoods[i] = (
                predicted_joint_probabilities[i, t] *
                conditional_likelihoods[i, t])
            joint_likelihoods[t] = joint_likelihoods[t] + likelihoods[i]

        for i in range(k_regimes_order_p1):
            if joint_likelihoods[t] == 0:
                filtered_joint_probabilities[i, t+1] = np.inf
            else:
                filtered_joint_probabilities[i, t+1] = (
                    likelihoods[i] / joint_likelihoods[t])


def dhamilton_filter(int nobs, int k_regimes, int order,
                              np.float64_t [:,:,:] transition,
                              np.float64_t [:,:] conditional_likelihoods,
                              np.float64_t [:] joint_likelihoods,
                              np.float64_t [:,:] predicted_joint_probabilities,
                              np.float64_t [:,:] filtered_joint_probabilities):
    cdef int t, i, j, k, ix, transition_t = 0, time_varying_transition
    cdef:
        int k_regimes_order_m1 = k_regimes**(order - 1)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.float64_t [:] likelihoods, tmp

    time_varying_transition = transition.shape[2] > 1
    likelihoods = np.zeros(k_regimes_order_p1, dtype=float)
    tmp = np.zeros(k_regimes_order, dtype=float)

    for t in range(nobs):
        if time_varying_transition:
            transition_t = t

        ix = 0
        tmp[:] = 0
        for j in range(k_regimes_order):
            for i in range(k_regimes):
                tmp[j] = tmp[j] + filtered_joint_probabilities[ix, t]
                ix = ix + 1

        ix = 0
        for i in range(k_regimes):
            for j in range(k_regimes):
                for k in range(k_regimes_order_m1):
                    predicted_joint_probabilities[ix, t] = (
                        tmp[j * k_regimes_order_m1 + k] *
                        transition[i, j, transition_t])
                    ix += 1

        for i in range(k_regimes_order_p1):
            likelihoods[i] = (
                predicted_joint_probabilities[i, t] *
                conditional_likelihoods[i, t])
            joint_likelihoods[t] = joint_likelihoods[t] + likelihoods[i]

        for i in range(k_regimes_order_p1):
            if joint_likelihoods[t] == 0:
                filtered_joint_probabilities[i, t+1] = np.inf
            else:
                filtered_joint_probabilities[i, t+1] = (
                    likelihoods[i] / joint_likelihoods[t])


def chamilton_filter(int nobs, int k_regimes, int order,
                              np.complex64_t [:,:,:] transition,
                              np.complex64_t [:,:] conditional_likelihoods,
                              np.complex64_t [:] joint_likelihoods,
                              np.complex64_t [:,:] predicted_joint_probabilities,
                              np.complex64_t [:,:] filtered_joint_probabilities):
    cdef int t, i, j, k, ix, transition_t = 0, time_varying_transition
    cdef:
        int k_regimes_order_m1 = k_regimes**(order - 1)
        int k_regimes_order = k_regimes**order
        int k_regimes_order_p1 = k_regimes**(order + 1)
        np.complex64_t [:] likelihoods, tmp

    time_varying_transition = transition.shape[2] > 1
    likelihoods = np.zeros(k_regimes_order_p1, dtype=np.complex64)
    tmp = np.zeros(k_regimes_order, dtype=np.complex64)

    for t in range(nobs):
        if time_varying_transition:
            transition_t = t

        ix = 0
        tmp[:] = 0
        for j in range(k_regimes_order):
            for i in range(k_regimes):
                tmp[j] = tmp[j] + filtered_joint_probabilities[ix, t]
                ix = ix + 1

        ix = 0
        for i in range(k_regimes):
            for j in range(k_regimes):
                for k in range(k_regimes_order_m1):
                    predicted_joint_probabilities[ix, t] = (
                        tmp[j * k_regimes_order_m1 + k] *
                        transition[i, j, transition_t])
                    ix += 1

        for i in range(k_regimes_order_p1):
            likelihoods[i] = (
                predicted_joint_probabilities[i, t] *
                conditional_likelihoods[i, t])
            joint_likelihoods[t] = joint_likelihoods[t] + likelihoods[i]

        for i in range(k_regimes_order_p1):
            if joint_likelihoods[t] == 0:
                filtered_joint_probabilities[i, t+1] = np.inf
            else:
                filtered_joint_probabilities[i, t+1] = (
                    likelihoods[i] / joint_likelihoods[t])

