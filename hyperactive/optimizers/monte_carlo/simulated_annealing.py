# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import numpy as np

from ..local import StochasticHillClimbingOptimizer


class SimulatedAnnealingOptimizer(StochasticHillClimbingOptimizer):
    def __init__(
        self,
        search_config,
        n_iter,
        metric="accuracy",
        n_jobs=1,
        cv=5,
        verbosity=1,
        random_state=None,
        warm_start=False,
        memory=True,
        scatter_init=False,
        eps=1,
        t_rate=0.98,
        n_neighbours=1,
    ):
        super().__init__(
            search_config,
            n_iter,
            metric,
            n_jobs,
            cv,
            verbosity,
            random_state,
            warm_start,
            memory,
            scatter_init,
        )

        self.pos_para = {"eps": eps}
        self.t_rate = t_rate
        self.temp = 0.01

        self.initializer = self._init_annealing

    # use _consider from simulated_annealing
    """
    def _consider(self, _p_, p_accept):
        rand = random.uniform(0, 1)

        if p_accept > rand:
            _p_.score_current = _p_.score_new
            _p_.pos_current = _p_.pos_new
    """

    def _accept(self, _p_):
        score_diff_norm = (_p_.score_new - _p_.score_current) / (
            _p_.score_new + _p_.score_current
        )
        return np.exp(-(score_diff_norm / self.temp))

    def _iterate(self, i, _cand_, _p_, X, y):
        _p_.pos_new = _p_.move_climb(_cand_, _p_.pos_current)
        _p_.score_new = _cand_.eval_pos(_p_.pos_new, X, y)

        if _p_.score_new > _cand_.score_best:
            _cand_, _p_ = self._update_pos(_cand_, _p_)
        else:
            p_accept = self._accept(_p_)
            self._consider(_p_, p_accept)

        self.temp = self.temp * self.t_rate

        return _cand_

    def _init_annealing(self, _cand_, X, y):
        return super()._initialize(_cand_, X, y, pos_para=self.pos_para)
