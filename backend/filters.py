from scipy import signal

def notch_filter(w0, xi):
    """
    Design a notch filter with the given parameters.

    Parameters
    ----------
    w0 : float
        Notch frequency.
    xi : float
        Damping factor.

    Returns
    -------
    num : ndarray
        Numerator coefficients of the filter transfer function.
    den : ndarray
        Denominator coefficients of the filter transfer function.
    """
    num = [w0**(-2), 0.0, 1.0]
    den = [w0**(-2), (2.0 * xi) / w0, 1.0]
    return signal.TransferFunction(num, den)