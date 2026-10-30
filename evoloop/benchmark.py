def benchmark(before_failures, after_failures, before_eval, after_eval, immune_rules):
    total = before_failures + after_failures
    return {"failure_rate_before": round(before_failures/max(1,total),3), "failure_rate_after": round(after_failures/max(1,total),3),
            "eval_before": before_eval, "eval_after": after_eval, "eval_gain": round(after_eval-before_eval,2),
            "immune_rules": immune_rules, "verdict": "IMPROVED" if after_eval > before_eval and after_failures < before_failures else "NOT IMPROVED"}
