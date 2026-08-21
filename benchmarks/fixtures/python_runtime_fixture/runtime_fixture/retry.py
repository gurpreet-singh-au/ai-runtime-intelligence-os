from dataclasses import dataclass


@dataclass
class RetryPolicy:
    max_attempts: int = 3


def should_retry(attempt_number: int, status_code: int, policy: RetryPolicy) -> bool:
    """Return whether another request should be attempted.

    `attempt_number` is 1-based and identifies the request that just completed.
    Retry only transient 5xx responses and never exceed max_attempts total requests.
    """
    if policy.max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    transient = 500 <= status_code <= 599
    # Deliberate benchmark defect: <= permits one extra attempt.
    return transient and attempt_number <= policy.max_attempts
