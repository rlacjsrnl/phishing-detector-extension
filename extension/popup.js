document.addEventListener("DOMContentLoaded", () => {
  const resultDiv = document.getElementById("result");

  // 현재 탭 URL 검사
  document.getElementById("checkBtn").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const url = tabs[0].url;
      console.log("[DEBUG] 현재 탭 URL:", url);
      checkUrl(url);
    });
  });

  // 직접 입력한 URL 검사
  document.getElementById("submitBtn").addEventListener("click", () => {
    const inputUrl = document.getElementById("urlInput").value.trim();
    if (!inputUrl) {
      resultDiv.textContent = "URL을 입력해주세요.";
      resultDiv.style.color = "gray";
      return;
    }
    console.log("[DEBUG] 입력된 URL:", inputUrl);
    checkUrl(inputUrl);
  });

  function checkUrl(url) {
    const apiUrl = "https://249f-61-98-139-158.ngrok-free.app" + Date.now(); // 캐시 방지용 timestamp 추가

    fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: url })
    })
      .then(response => response.json())
      .then(data => {
        console.log("[DEBUG] 서버 응답:", data);

        if (data.is_phishing) {
          resultDiv.textContent = `피싱 사이트로 의심됩니다\n예측 확률: ${(data.confidence * 100).toFixed(2)}%`;
          resultDiv.style.color = "red";
        } else {
          resultDiv.textContent = `안전한 사이트입니다\n예측 확률: ${(data.confidence * 100).toFixed(2)}%`;
          resultDiv.style.color = "green";
        }
        

        // 영향도 리스트 표시
        /*
        if (data.top_features) {
          const ul = document.createElement("ul");
          data.top_features.slice(0, 5).forEach(item => {
            const li = document.createElement("li");
            li.textContent = `${item.feature} (${item.description}): ${item.shap_value}`;
            ul.appendChild(li);
          });
          resultDiv.appendChild(ul);
        }
        */
      })
      .catch(err => {
        console.error("API 호출 실패:", err);
        resultDiv.textContent = "오류: 서버 응답 없음";
        resultDiv.style.color = "gray";
      });
  }
});
