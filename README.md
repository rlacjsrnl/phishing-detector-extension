
# Phishing URL Detection Extension (피싱 URL 탐지 확장 프로그램)

이 프로젝트는 크롬 확장 프로그램과 머신러닝 기반 피싱 탐지 모델을 결합하여,  
실시간으로 URL을 분석하고 피싱 여부를 판단하는 시스템입니다.

## 프로젝트 구조

```
phishing-detector-extension/
├── api/
├── data/
├── extension/
├── ml_model/
├── shap_explanations/
└── ml_model/test_log.txt
```

### api/

| 파일 | 설명 |
|------|------|
| `app.py` | URL 분석 서버. 화이트/블랙리스트 대조 → 모델 예측 → SHAP 설명까지 수행하는 Flask 기반 API |

### data/

| 파일 | 설명 |
|------|------|
| `all_phishing_urls.csv` | 원본 피싱 URL 전체 목록 |
| `normal_urls.csv` | 원본 정상 URL 목록 |
| `all_phishing_urls_train.csv` | 학습용 피싱 URL 세트 |
| `normal_urls_train_scheme.csv` | 스킴 검증이 완료된 학습용 정상 URL 세트 |
| `dataset_train.csv` | 최종 학습 데이터 (정상/피싱 병합 + 라벨링) |
| `whitelist.txt` | 정규화된 화이트리스트 도메인/IP 목록 |
| `blacklist.txt` | 정규화된 블랙리스트 도메인/IP 목록 |
| `update_blacklist.py` | 블랙리스트 최신화 스크립트 (abuse.ch 등에서 자동 수집) |
| `seen_urls.txt` | URL 중복 누적 방지 기록 파일 |
| `scheme_tester.py` | 정상 URL의 스킴 테스트 자동화 (https→http→ftp) |
| `combine_url.py` | 학습용 URL을 비율에 따라 병합하고 중복 방지 기능 포함 |

### extension/

| 파일 | 설명 |
|------|------|
| `manifest.json` | 크롬 확장 프로그램 메타 정보 |
| `popup.html` | UI 인터페이스 |
| `popup.js` | 백엔드 API와 연동 및 DOM 처리 |
| `icon.png` | 확장 프로그램 아이콘 |

### ml_model/

#### 학습 및 추론

| 파일 | 설명 |
|------|------|
| `train_model_features.py` | 전체 학습 스크립트 (피처 벡터로부터 모델 생성) |
| `test_model.py` | 모델 단독 성능 테스트 |
| `test_model_list.py` | 화이트/블랙리스트 → 모델 순으로 판단 구조를 테스트 (확장 구조 기반) |
| `phishing_model.pkl` | 저장된 모델 파일 |
| `extract_features.py` | URL에서 F01~F30 피처를 통합 추출 |

#### 피처 추출 및 조작

| 파일 | 설명 |
|------|------|
| `vectorize_test_csv.py` | URL 목록 → 피처 벡터 (`csv`, `arff`)로 저장 |
| `update_feature.py` | 특정 피처 하나만 병렬로 재계산 및 기존 벡터에 덮어쓰기 |
| `combine_dataset_urls.py` | 정상/피싱 URL을 비율에 따라 병합, 중복 방지 및 누적 지원 |

#### 피처 선택 및 평가

| 파일 | 설명 |
|------|------|
| `foward_selection.py` | 순차적으로 피처를 추가해 가장 좋은 조합 탐색 |
| `genetic_feature_selection.py` | 유전 알고리즘을 통해 최적 피처 조합 탐색 |
| `select_feature.py` | 사용자가 선택한 피처 조합으로 모델 성능 평가 |
| `f1-score.py` | 개별 피처 하나씩 사용한 경우의 F1-score 비교 분석 |

#### 피처 모듈

- `features/feature_01_xxx.py` ~ `feature_30_xxx.py`: 30개의 피싱 관련 피처를 각각 정의
- `single_feature/`: 단일 피처 `.arff` 벡터 저장 경로
- `seen_urls/`: 각 피처별 중복 URL 추적 기록

### shap_explanations/

- SHAP 기반 예측 설명 결과가 `.csv` 파일로 저장되는 폴더  
- 확장 프로그램의 예측 이유 표시용

### ml_model/test_log.txt

- 테스트 수행 기록 로그
  - 날짜 및 시간
  - URL 총 개수
  - 예측 결과 분포
  - 화이트/블랙/모델 판단 근거별 정확도 등

## 주요 사용 예시

```bash
# 학습용 데이터 생성
python combine_url.py --count 10000

# 피처 벡터 추출
python vectorize_test_csv.py --csv data/test_urls.csv

# 모델 학습
python train_model_features.py

# 확장 구조 기반 모델 테스트
python test_model_list.py
```

## 피처 구조

- F01~F30까지 UCI 기준 피처로 구성
- 각 피처는 `features/feature_##_name.py`에 정의됨
- 주요 피처: `Have_IP`, `Domain_Registration_Length`, `Google_Index`, `Page_Rank` 등
