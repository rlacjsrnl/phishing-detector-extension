from concurrent.futures import ThreadPoolExecutor, as_completed

from ml_model.features.feature_01_ip_address import feature_01_ip_address
from ml_model.features.feature_02_url_length import feature_02_url_length
from ml_model.features.feature_03_shortening_service import feature_03_shortening_service
from ml_model.features.feature_04_having_at_symbol import feature_04_having_at_symbol
from ml_model.features.feature_05_double_slash_redirecting import feature_05_double_slash_redirecting
from ml_model.features.feature_06_prefix_suffix import feature_06_prefix_suffix
from ml_model.features.feature_07_sub_domain import feature_07_sub_domain
from ml_model.features.feature_08_sslfinal_state import feature_08_sslfinal_state
from ml_model.features.feature_09_domain_registration_length import feature_09_domain_registration_length
from ml_model.features.feature_10_favicon import feature_10_favicon
from ml_model.features.feature_11_port import feature_11_port
from ml_model.features.feature_12_https_token import feature_12_https_token
from ml_model.features.feature_13_request_url import feature_13_request_url
from ml_model.features.feature_14_url_of_anchor import feature_14_url_of_anchor
from ml_model.features.feature_15_links_in_tags import feature_15_links_in_tags
from ml_model.features.feature_16_sfh import feature_16_sfh
from ml_model.features.feature_17_submitting_to_email import feature_17_submitting_to_email
from ml_model.features.feature_18_abnormal_url import feature_18_abnormal_url
from ml_model.features.feature_19_request_availability import feature_19_request_availability
from ml_model.features.feature_20_on_mouseover import feature_20_on_mouseover
from ml_model.features.feature_21_rightclick import feature_21_rightclick
from ml_model.features.feature_22_popup_window import feature_22_popup_window
from ml_model.features.feature_23_iframe import feature_23_iframe
from ml_model.features.feature_24_age_of_domain import feature_24_age_of_domain
from ml_model.features.feature_25_dns_record import feature_25_dns_record
from ml_model.features.feature_26_web_traffic import feature_26_web_traffic
from ml_model.features.feature_27_page_rank import feature_27_page_rank
from ml_model.features.feature_28_google_index import feature_28_google_index
from ml_model.features.feature_29_links_pointing_to_page import feature_29_links_pointing_to_page
from ml_model.features.feature_30_statistical_report import feature_30_statistical_report

FEATURE_FUNCS = {
    "F01": feature_01_ip_address,
    "F02": feature_02_url_length,
    "F03": feature_03_shortening_service,
    "F04": feature_04_having_at_symbol,
    "F05": feature_05_double_slash_redirecting,
    "F06": feature_06_prefix_suffix,
    "F07": feature_07_sub_domain,
    "F08": feature_08_sslfinal_state,
    "F09": feature_09_domain_registration_length,
    "F10": feature_10_favicon,
    "F11": feature_11_port,
    "F12": feature_12_https_token,
    "F13": feature_13_request_url,
    "F14": feature_14_url_of_anchor,
    "F15": feature_15_links_in_tags,
    "F16": feature_16_sfh,
    "F17": feature_17_submitting_to_email,
    "F18": feature_18_abnormal_url,
    "F19": feature_19_request_availability,
    "F20": feature_20_on_mouseover,
    "F21": feature_21_rightclick,
    "F22": feature_22_popup_window,
    "F23": feature_23_iframe,
    "F24": feature_24_age_of_domain,
    "F25": feature_25_dns_record,
    "F26": feature_26_web_traffic,
    "F27": feature_27_page_rank,
    "F28": feature_28_google_index,
    "F29": feature_29_links_pointing_to_page,
    "F30": feature_30_statistical_report,
}

def extract_features(url: str) -> dict:
    """
    URL을 입력받아 30개 속성 값 딕셔너리 반환 (병렬 처리)
    """
    features = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(func, url): name for name, func in FEATURE_FUNCS.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                features[name] = future.result()
            except Exception:
                features[name] = -1
    return features

def extract_feature_by_name(url: str, feature_name: str) -> int:
    import importlib
    import os

    feature_dir = "ml_model.features"
    feature_prefix = f"feature_{feature_name[1:]}"

    path = os.path.join("ml_model", "features")
    matches = [f for f in os.listdir(path) if f.startswith(feature_prefix)]
    if not matches:
        raise ImportError(f"No file found for {feature_name}")

    module_name = matches[0].replace(".py", "")
    module_path = f"{feature_dir}.{module_name}"

    module = importlib.import_module(module_path)
    func_name = [f for f in dir(module) if f.startswith("feature_")][0]
    func = getattr(module, func_name)
    return func(url)

if __name__ == "__main__":
    test_url = "https://www.google.com"
    features = extract_features(test_url)
    print(f"URL: {test_url}")
    print(f"Extracted Features: {features}")
    print(f"Feature Count: {len(features)}")
