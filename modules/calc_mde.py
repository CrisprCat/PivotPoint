from statsmodels.stats.power import zt_ind_solve_power
import math

def calculate_mde(alpha, power, p1, n, alternative):
    # Calculate the effect size using statsmodels
    effect_size = zt_ind_solve_power(effect_size=None # returns the effect size as a standardized value
                                     , nobs1=n 
                                     , alpha=alpha 
                                     , power=power 
                                     , alternative=alternative
                                     , ratio = 1.0
                                     )
    # Translate effect size to MDE
    mde = effect_size * math.sqrt(p1 * (1 - p1))
    return mde