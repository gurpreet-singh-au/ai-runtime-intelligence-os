import json
from pathlib import Path

from normalize_claude_run import normalize


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj), encoding="utf-8")


def test_normalizer_preserves_unknowns_and_observed_usage(tmp_path: Path):
    write_json(
        tmp_path / "RUN_METADATA.json",
        {
            "run_id": "B2-001-baseline-r01",
            "benchmark_id": "B2-001",
            "policy_variant": "baseline",
            "started_at": "2026-08-22T00:00:00+00:00",
            "ended_at": "2026-08-22T00:00:02+00:00",
            "runtime": "Claude Code",
            "runtime_version": "test",
            "repository_commit": "abc123",
        },
    )

    events = [
        {
            "type": "assistant",
            "message": {
                "content": [
                    {"type": "tool_use", "name": "Read", "input": {"file_path": "pricing.py"}}
                ],
                "usage": {"input_tokens": 100, "output_tokens": 20},
            },
        },
        {
            "type": "result",
            "duration_ms": 1500,
            "total_cost_usd": 0.01,
        },
    ]
    (tmp_path / "claude-stream.jsonl").write_text(
        "\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8"
    )
    (tmp_path / "tests-after.txt").write_text("3 passed\n", encoding="utf-8")

    normalized, report = normalize(tmp_path)

    assert normalized["resources"]["input_tokens"] == 100
    assert normalized["resources"]["output_tokens"] == 20
    assert normalized["resources"]["tool_calls"] == 1
    assert normalized["resources"]["duration_ms"] == 1500
    assert normalized["cost"]["total"] == 0.01

    # Missing telemetry is not silently converted into zero.
    assert normalized["resources"]["instruction_tokens"] is None
    assert normalized["resources"]["context_peak_tokens"] is None
    assert report["field_evidence"]["resources.instruction_tokens"]["evidence"] == "UNKNOWN"


def test_normalizer_does_not_infer_success_from_model_result(tmp_path: Path):
    write_json(
        tmp_path / "RUN_METADATA.json",
        {
            "run_id": "B2-001-baseline-r01",
            "benchmark_id": "B2-001",
            "started_at": "2026-08-22T00:00:00+00:00",
            "ended_at": "2026-08-22T00:00:01+00:00",
        },
    )
    (tmp_path / "claude-stream.jsonl").write_text(
        json.dumps({"type": "result", "result": "Fixed successfully"}) + "\n",
        encoding="utf-8",
    )

    normalized, _ = normalize(tmp_path)
    assert normalized["outcome"]["success"] is False
    assert normalized["outcome"]["mandatory_compliance"] is False
