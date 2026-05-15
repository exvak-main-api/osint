def compute_score(corr, anomaly):
    risk = corr.get("risk_score", 0)
    anomaly_score = anomaly.get("anomaly_score", 0)

    final = (risk * 0.6) + (anomaly_score * 0.4)

    if final >= 70:
        level = "HIGH CONFIDENCE RISK"
    elif final >= 40:
        level = "MEDIUM CONFIDENCE RISK"
    else:
        level = "LOW CONFIDENCE RISK"

    return {
        "final_score": round(final, 2),
        "level": level
    }
