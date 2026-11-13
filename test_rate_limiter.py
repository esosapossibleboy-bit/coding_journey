from rate_limiter import RateLimiter

def test_api_rate_limiter():
    limiter = RateLimiter(max_requests=2)

    # User "esosa" is allowed 2 requests
    assert limiter.allow_request("esosa") == True
    assert limiter.allow_request("esosa") == True

    # 3rd request from "esosa" is blocked!
    assert limiter.allow_request("esosa") == False

    # Meanwhile, a different user "aria" still has her own 2 tickets!
    assert limiter.allow_request("aria") == True
