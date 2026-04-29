"""
M/M/1 Queueing System (from your notes: A(t), B(t), Sn = Wn + Xn)
"""
import numpy as np

class MM1Queue:
    def __init__(self, arrival_rate, service_rate):
        self.lam = arrival_rate    # λ
        self.mu = service_rate     # μ
        self.rho = arrival_rate / service_rate  # utilization

    def avg_waiting_time(self):
        """W_q = ρ / (μ - λ)"""
        if self.rho >= 1:
            return float('inf')
        return self.rho / (self.mu - self.lam)

    def avg_service_time(self):
        """X_n = 1/μ"""
        return 1 / self.mu

    def avg_total_time(self):
        """S_n = W_n + X_n"""
        return self.avg_waiting_time() + self.avg_service_time()

    def avg_population(self):
        """L = ρ / (1 - ρ)"""
        if self.rho >= 1:
            return float('inf')
        return self.rho / (1 - self.rho)

    def simulate(self, num_packets=1000):
        """Discrete-event simulation"""
        inter_arrivals = np.random.exponential(1/self.lam, num_packets)
        service_times = np.random.exponential(1/self.mu, num_packets)
        arrival_times = np.cumsum(inter_arrivals)
        departure_times = np.zeros(num_packets)
        wait_times = np.zeros(num_packets)

        for i in range(num_packets):
            start_service = max(arrival_times[i],
                                departure_times[i-1] if i > 0 else 0)
            wait_times[i] = start_service - arrival_times[i]
            departure_times[i] = start_service + service_times[i]

        return {
            "avg_wait": np.mean(wait_times),
            "avg_service": np.mean(service_times),
            "avg_total": np.mean(departure_times - arrival_times),
            "max_wait": np.max(wait_times)
        }