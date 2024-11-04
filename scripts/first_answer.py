import random as rd
import time
import copy
from collections import deque
import logging


class Simulater:
    def __init__(self, edges):
        self.n_node = len(edges)
        self.edges = edges

        self.times_test = 1

        self.start_pos = rd.randint(0, len(self.edges) - 1)
        self.origin_cost = self.pape(self.edges, self.n_node, self.start_pos, set())

    def evaluate(self, selected_jobs):
        # ランダムでstart地点を選ぶ
        for _ in range(self.times_test):
            suggest_cost = self.pape(
                self.edges, self.n_node, self.start_pos, selected_jobs
            )

        ans = suggest_cost - self.origin_cost

        return ans

    def pape(self, G, N, s, selected_job):
        INF = 10**18
        dist = [INF] * N

        used = [0] * N
        used[s] = 1
        dist[s] = 0
        que = deque([s])
        while que:
            v = que.popleft()
            c = dist[v]
            for w, (d, job_id) in G[v].items():
                if job_id in selected_job:
                    continue
                if dist[w] <= c + d:
                    continue
                dist[w] = c + d
                if used[w] == 0:
                    que.append(w)
                    used[w] = 1
                elif used[w] == 2:
                    que.appendleft(w)
                    used[w] = 1
            used[v] = 2
        return sum(dist)


def make_day_num_task(task_num, day):

    base = -(-task_num // day)
    norma = []
    for d in range(day):
        base = -(-task_num // (day - d))
        norma.append(min(base, task_num))
        task_num -= base

    return norma


def solve(limit=5.7):

    N, M, D, K = map(int, input().split())

    edges = [{} for i in range(N)]
    jobs = []
    g = [[0 for _ in range(N)] for _ in range(N)]
    for m in range(M):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        edges[u][v] = [w, m]
        edges[v][u] = [w, m]
        jobs.append([w, u, v])
        g[u][v] = 1
        g[v][u] = 1

    pos = []
    for _ in range(N):
        x, y = map(int, input().split())
        pos.append([x, y])

    # init
    start_time = time.time()
    env = Simulater(edges[:])

    normas = make_day_num_task(M, D)

    # 初期解生成 適当な奴一個でいいんだよなあ
    init_schedule = []
    for days, norma in enumerate(normas):
        for n in range(norma):
            init_schedule.append(days + 1)

    # ランダムで入れ替えてよくなったらみたいな
    day_selected_jobs = [set() for d in range(D)]

    for num_jobs, d in enumerate(init_schedule):
        day_selected_jobs[d - 1].add(num_jobs)

    fix = []

    for day, item in enumerate(day_selected_jobs):
        score = env.evaluate(item)
        fix.append([score, day])

    count = 0
    schedule = [-1 for m in range(M)]
    high_score = 10**27
    burn = 0.0
    size = K

    while time.time() - start_time < limit:

        count += 1
        # choice 確率はscoreに比例する
        idx_a = rd.sample([i for i in range(len(fix))], k=1)[0]
        score_a, day_a = fix.pop(idx_a)

        idx_b = rd.sample([i for i in range(len(fix))], k=1)[0]
        score_b, day_b = fix.pop(idx_b)

        # exchange
        temp_sel_a_list = list(day_selected_jobs[day_a])
        for _ in range(K - len(temp_sel_a_list)):
            temp_sel_a_list.append(-1)
        temp_sel_a_list = rd.sample(temp_sel_a_list, k=len(temp_sel_a_list))
        temp_sel_b_list = list(day_selected_jobs[day_b])
        for _ in range(K - len(temp_sel_b_list)):
            temp_sel_b_list.append(-1)
        temp_sel_b_list = rd.sample(temp_sel_b_list, k=len(temp_sel_b_list))

        for i in range(size):
            temp_sel_a_list[i], temp_sel_b_list[i] = (
                temp_sel_b_list[i],
                temp_sel_a_list[i],
            )
        temp_selected = temp_sel_a_list + temp_sel_b_list

        middle = len(temp_selected) // 2
        temp_sel_a = set(temp_selected[:middle])
        if -1 in temp_sel_a:
            temp_sel_a.remove(-1)
        temp_sel_b = set(temp_selected[middle:])
        if -1 in temp_sel_b:
            temp_sel_b.remove(-1)

        temp_score_a = env.evaluate(temp_sel_a)
        temp_score_b = env.evaluate(temp_sel_b)
        temp_score = temp_score_a + temp_score_b

        if temp_score < (score_a + score_b) or (
            rd.random() < burn and temp_score < 10**9
        ):
            day_selected_jobs[day_a] = set(temp_selected[:middle])
            day_selected_jobs[day_b] = set(temp_selected[middle:])
            fix.append([temp_score_a, day_a])
            fix.append([temp_score_b, day_b])

            todays_score = sum([item[0] for item in fix])
            size = min(2 * size, K)
            if todays_score < high_score:
                high_score = todays_score

            # print(count,todays_score,high_score)

        else:
            fix.append([score_a, day_a])
            fix.append([score_b, day_b])
            size = max(size // 2, 8)

    for day in range(D):
        for job_id in day_selected_jobs[day]:
            schedule[job_id] = day
    print(*[x + 1 for x in schedule])

    logging.error(f"high_score:{high_score}")

    return high_score


if __name__ == "__main__":
    solve()
