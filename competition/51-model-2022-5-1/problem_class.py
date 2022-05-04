import numpy as np
import cvxpy as cp


class MicroRobotProgramming:

    def __init__(self, requirements, k, waste=0):
        self.total_week = len(requirements)
        self.requirements = requirements
        self.K = k

        if waste:
            self.waste = cp.Variable(self.total_week, integer=True)
        else:
            self.waste = None
        
        self.hand_new = cp.Variable(self.total_week, integer=True)
        self.hand_work = cp.Variable(self.total_week, integer=True)
        self.hand_rest = cp.Variable(self.total_week, integer=True)
        self.hand_teach = cp.Variable(self.total_week, integer=True)
        self.hand_skill = cp.Variable(self.total_week, integer=True)
        self.body_new = cp.Variable(self.total_week, integer=True)
        self.body_work = cp.Variable(self.total_week, integer=True)
        self.body_rest = cp.Variable(self.total_week, integer=True)
        self.body_tested = cp.Variable(self.total_week, integer=True)

        self.prob = None

        if waste:
            self.cons.append(self.waste >= 0)
    
    def solve(self):
        self.cons = [
            self.hand_new >= 0,
            self.hand_rest >= 0,
            self.hand_work >= 0,
            self.hand_teach >= 0,
            self.body_new >= 0,
            self.body_rest >= 0,
            self.body_work >= 0,

            self.hand_work == 4 * self.requirements,
            self.body_work == self.requirements,
            self.K * self.hand_teach >= self.hand_new,
            self.hand_skill == self.hand_work + self.hand_rest + self.hand_teach,
            self.body_tested == self.body_work + self.body_rest,

            self.hand_skill[0] == 50,
            self.body_tested[0] == 13
        ]

        self.obj = cp.Minimize(
            200 * cp.sum(self.body_new) + 
            100 * cp.sum(self.hand_new) + 
            5 * cp.sum(self.hand_rest) + 
            10 * cp.sum(self.body_rest) +
            10 * cp.sum(self.hand_new + self.hand_teach)
        )

        if self.waste is not None:
            self.cons.append(self.waste <= 0.2 * self.hand_work + 0.5)
            self.cons.append(self.waste >= 0.2 * self.hand_work - 0.49999)
            for t in range(self.total_week - 1):
                self.cons.append(self.hand_rest[t+1] >= self.hand_work[t] - self.waste[t])
                self.cons.append(self.hand_skill[t+1] == self.hand_skill[t] + self.hand_new[t])
                self.cons.append(self.body_tested[t+1] == self.body_tested[t] + self.body_new[t])
        else:
            for t in range(self.total_week - 1):
                self.cons.append(self.hand_rest[t+1] >= self.hand_work[t])
                self.cons.append(self.hand_skill[t+1] == self.hand_skill[t] + self.hand_new[t])
                self.cons.append(self.body_tested[t+1] == self.body_tested[t] + self.body_new[t])

        self.prob = cp.Problem(self.obj, self.cons)
        self.prob.solve()
        
    def week(self, num_week: int):
        return np.array([
            self.body_new.value[num_week - 1],
            self.hand_new.value[num_week - 1],
            self.hand_rest.value[num_week - 1],
            self.body_rest.value[num_week - 1],
            self.hand_new[num_week - 1] + self.hand_teach[num_week - 1],
            200 * self.body_new + 100 * self.hand_new + 5 * self.hand_rest + \
            10 * self.body_rest + 10 * self.hand_new + self.hand_teach
        ])
    
    def get_weeks(self, weeks=[12, 26, 52, 78, 101, 102, 103, 104]):
        return np.concatenate([self.week(w) for w in weeks])

if __name__ == '__main__':
    import pandas as pd
    requirements1 = pd.read_excel('E:\program\synthetical_learning\mathematical-models-learning\competition\51-model-2022-5-1\51代码\data.xlsx', header=None).values.flatten()[0:8]
    mrb = MicroRobotProgramming(requirements=requirements1, k=10)
    mrb.solve()
