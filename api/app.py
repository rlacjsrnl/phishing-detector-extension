import os
from urllib.parse import urlparse
from flask import Flask, request, jsonify
import joblib
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np
import shap
from ml_model.extract_features import extract_features

app = Flask(__name__)

# 도메인 정규화 함수
def normalize_host(value: str) -> str:
    return value.strip().lower().lstrip("www.").rstrip("/")

# 도메인 추출 후 정규화
def get_domain(url):
    parsed = urlparse(url)
    raw = parsed.hostname if parsed.hostname else url
    return normalize_host(raw)

# txt 파일 로딩 (정규화 포함)
def load_txt_set(path):
    if not os.path.exists(path):
        print(f"[경고] 파일 없음: {path}")
        return set()
    return set(normalize_host(line) for line in open(path, encoding="utf-8") if line.strip())

# 리스트 로딩
whitelist = load_txt_set("data/whitelist.txt")
blacklist = load_txt_set("data/blacklist.txt")

# 모델 & SHAP 초기화
model = joblib.load("ml_model/phishing_model.pkl")
explainer = shap.Explainer(model)
executor = ThreadPoolExecutor(max_workers=10)

# 피처 설명
feature_desc = {
    "F01": "Have_IP", "F02": "URL_Length", "F03": "Shortening_Service",
    "F04": "Have_At_Symbol", "F05": "Double_Slash_Redirecting", "F06": "Prefix_Suffix",
    "F07": "Having_Sub_Domain", "F08": "SSLfinal_State", "F09": "Domain_Registration_Length",
    "F10": "Favicon", "F11": "Port", "F12": "HTTPS_token", "F13": "Request_URL",
    "F14": "URL_of_Anchor", "F15": "Links_in_tags", "F16": "SFH", "F17": "Submitting_to_email",
    "F18": "Abnormal_URL", "F19": "Redirect", "F20": "on_mouseover", "F21": "RightClick",
    "F22": "PopupWindow", "F23": "Iframe", "F24": "Age_of_Domain", "F25": "DNSRecord",
    "F26": "Web_Traffic", "F27": "Page_Rank", "F28": "Google_Index",
    "F29": "Links_Pointing_to_Page", "F30": "Statistical_Report"
}

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"error": "URL이 제공되지 않았습니다."}), 400

        domain = get_domain(url)
        print(f"[DEBUG] 추출된 도메인: {domain}")
        print(f"[DEBUG] 블랙리스트 포함 여부: {domain in blacklist}")
        print(f"[DEBUG] 화이트리스트 포함 여부: {domain in whitelist}")

        if domain in blacklist:
            return jsonify({
                "url": url,
                "is_phishing": True,
                "prediction_label": "phishing",
                "confidence": 1.0,
                "reason": "도메인 또는 IP가 블랙리스트에 등록되어 있음",
                "top_features": []
            })

        if domain in whitelist:
            return jsonify({
                "url": url,
                "is_phishing": False,
                "prediction_label": "normal",
                "confidence": 1.0,
                "reason": "도메인이 화이트리스트에 등록되어 있음",
                "top_features": []
            })

        future = executor.submit(extract_features, url)
        features = future.result()

        print("[DEBUG] 분석 대상 URL:", url)
        print("[DEBUG] 추출된 피처:", features)

        model_features = list(model.feature_names_in_)
        df_features = pd.DataFrame([features])[model_features]

        prob = model.predict_proba(df_features)[0]
        prediction_index = int(np.argmax(prob))
        prediction_label = model.classes_[prediction_index]
        confidence = prob[prediction_index]

        print("[DEBUG] model.classes_:", model.classes_)
        print("[DEBUG] 예측 확률:", prob)
        print("[DEBUG] 예측 클래스:", prediction_label)
        print("[DEBUG] 예측 확신도:", confidence)

        shap_values = explainer(df_features)

        if shap_values.values.ndim == 3:
            shap_value_row = shap_values.values[0, :, prediction_index]
        elif shap_values.values.ndim == 2:
            shap_value_row = shap_values.values[0]
        else:
            raise ValueError(f"예상치 못한 SHAP 값 구조: shape = {shap_values.values.shape}")

        base = shap_values.base_values[0][prediction_index] if isinstance(shap_values.base_values, np.ndarray) and shap_values.base_values.ndim == 2 else shap_values.base_values[0]
        shap_sum = np.sum(shap_value_row)
        total_prediction = base + shap_sum

        print(f"[SHAP 총합]: {shap_sum:.6f}")
        print(f"[SHAP 기반 예측값 = expected_value + shap_sum]: {total_prediction:.6f}")
        print(f"[모델 confidence (확신도)]: {confidence:.6f}")

        impact_scores = [
            (fname, float(shap_value_row[i]))
            for i, fname in enumerate(model_features)
        ]
        sorted_impacts = sorted(impact_scores, key=lambda x: abs(x[1]), reverse=True)

        print("[SHAP 영향도 순서]:")
        for fname, val in sorted_impacts:
            desc = feature_desc.get(fname, "Unknown")
            print(f"  - {fname} ({desc}): {val:.6f}")
        print(f"[SHAP 피처 개수]: {len(sorted_impacts)} / 기대: {len(model_features)}")
        print("-" * 40)

        top_features = [
            {
                "feature": fname,
                "description": feature_desc.get(fname, "Unknown"),
                "shap_value": round(val, 4)
            }
            for fname, val in sorted_impacts
        ]

        return jsonify({
            "url": url,
            "is_phishing": (prediction_label == "phishing"),
            "prediction_label": prediction_label,
            "confidence": round(float(confidence), 4),
            "top_features": top_features
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/check_blacklist", methods=["POST"])
def check_blacklist():
    url = request.get_json().get("url")
    domain = get_domain(url)
    return jsonify({
        "domain": domain,
        "in_blacklist": domain in blacklist
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
