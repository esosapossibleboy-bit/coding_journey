class RateLimiter:
    def __init__(self, max_requests):
        self.max_requests = max_requests
        self.request_counts = {}

    def allow_request(self, user_id):
        # Look up the user's current request count
        current_count = self.request_counts.get(user_id, 0)

        # Check whether the user is within the limit
        if current_count < self.max_requests:
            self.request_counts[user_id] = current_count + 1
            return True

        # Request limit reached
        return False
