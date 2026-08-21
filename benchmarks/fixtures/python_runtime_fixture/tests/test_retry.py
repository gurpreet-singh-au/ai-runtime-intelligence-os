from runtime_fixture.retry import RetryPolicy, should_retry


def test_retry_transient_before_limit():
    policy = RetryPolicy(max_attempts=3)
    assert should_retry(1, 503, policy) is True
    assert should_retry(2, 503, policy) is True


def test_stop_after_max_attempts():
    policy = RetryPolicy(max_attempts=3)
    assert should_retry(3, 503, policy) is False


def test_do_not_retry_non_transient_status():
    policy = RetryPolicy(max_attempts=3)
    assert should_retry(1, 404, policy) is False
