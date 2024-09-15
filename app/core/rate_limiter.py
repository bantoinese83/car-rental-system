import threading
import time


class RateLimiter:
    def __init__(self, max_requests_per_minute, max_tokens_per_minute, max_requests_per_day):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_tokens_per_minute = max_tokens_per_minute
        self.max_requests_per_day = max_requests_per_day

        self.requests_this_minute = 0
        self.tokens_this_minute = 0
        self.requests_today = 0

        self.minute_reset_time = time.time() + 60
        self.day_reset_time = time.time() + 86400

        self.lock = threading.Lock()

    def _reset_limits(self):
        current_time = time.time()
        if current_time >= self.minute_reset_time:
            self.requests_this_minute = 0
            self.tokens_this_minute = 0
            self.minute_reset_time = current_time + 60
        if current_time >= self.day_reset_time:
            self.requests_today = 0
            self.day_reset_time = current_time + 86400

    def can_proceed(self, tokens):
        with self.lock:
            self._reset_limits()
            if (self.requests_this_minute < self.max_requests_per_minute and
                    self.tokens_this_minute + tokens <= self.max_tokens_per_minute and
                    self.requests_today < self.max_requests_per_day):
                self.requests_this_minute += 1
                self.tokens_this_minute += tokens
                self.requests_today += 1
                return True
            return False
