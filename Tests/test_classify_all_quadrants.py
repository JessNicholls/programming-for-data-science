import pandas as pd

def test_classify_all_quadrants():
    hub_med, auth_med = 0.50, 0.50

    # Synthetic rows that hit all 4 quadrants + boundary equals medians
    rows = pd.DataFrame([
        {"hub_score": 0.70, "authority_score": 0.75, "exp": "Core (High Hub, High Authority)"},
        {"hub_score": 0.70, "authority_score": 0.40, "exp": "Origin Hub (High Hub, Low Authority)"},
        {"hub_score": 0.40, "authority_score": 0.70, "exp": "Destination Authority (Low Hub, High Authority)"},
        {"hub_score": 0.40, "authority_score": 0.40, "exp": "Peripheral (Low Hub, Low Authority)"},
        # boundaries
        {"hub_score": 0.50, "authority_score": 0.50, "exp": "Core (High Hub, High Authority)"},
        {"hub_score": 0.50, "authority_score": 0.49, "exp": "Origin Hub (High Hub, Low Authority)"},
        {"hub_score": 0.49, "authority_score": 0.50, "exp": "Destination Authority (Low Hub, High Authority)"},
    ])

    def classify(row, hub_med, auth_med):
        if row["hub_score"] >= hub_med and row["authority_score"] >= auth_med:
            return "Core (High Hub, High Authority)"
        elif row["hub_score"] >= hub_med and row["authority_score"] < auth_med:
            return "Origin Hub (High Hub, Low Authority)"
        elif row["hub_score"] < hub_med and row["authority_score"] >= auth_med:
            return "Destination Authority (Low Hub, High Authority)"
        else:
            return "Peripheral (Low Hub, Low Authority)"

    out = rows.apply(lambda r: classify(r, hub_med, auth_med), axis=1)
    assert list(out) == list(rows["exp"])
