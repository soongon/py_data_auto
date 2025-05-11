## **🔧 [자동화 프로그램 02] 파일 이름 일괄 변경 프로그램 만들기**

### **🎯 목표**

- 지정된 폴더 내 파일들을 **일정한 규칙에 따라 일괄적으로 이름 변경**
- 예: image_001.jpg, image_002.jpg, …

---

### **📂 입력 예시**

- data/rename/ 폴더에 다음과 같은 파일이 존재

```
IMG_A1.jpg
IMG_A2.jpg
IMG_A3.jpg
```

---

### **📁 출력 예시**

- 다음과 같이 이름 변경되어 저장됨

```
image_001.jpg
image_002.jpg
image_003.jpg
```

### **🛠️ 주요 코드 구성**
### **⚙️ 주요 기능**

| **기능** | **설명** |
| --- | --- |
| 🔢 순차 번호 부여 | 파일 순서에 따라 001, 002, 003 형식 자동 부여 |
| 🔤 접두사 지정 | 사용자가 접두어(ex: image_)를 입력할 수 있도록 설정 |
| ❌ 예외 처리 | 이미 동일한 이름의 파일이 존재할 경우 덮어쓰기 방지 |

---

### **🛠️ 코드 예시**

```python
import os

def rename_files(folder_path, prefix="file_"):
    files = sorted(os.listdir(folder_path))
    for idx, filename in enumerate(files):
        ext = os.path.splitext(filename)[-1]
        new_name = f"{prefix}{idx+1:03}{ext}"
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_name)
        os.rename(src, dst)
        print(f"{filename} → {new_name}")
```

---

### **✅ 실습 포인트**

- 파일명 변경 시 순차 넘버링 형식 001, 002… 처리
- os.path.splitext()을 이용한 확장자 분리
- 정렬 후 이름 변경 시 이름 충돌 방지

---

### **📝 연습문제**

1. img_001.png, img_002.png, … 형식으로 PNG 파일만 일괄 이름 변경
2. 파일 이름 앞에 날짜(2025-05-11_)를 접두어로 추가
3. 같은 이름이 이미 존재하는 경우에는 뒤에 _1, _2를 붙여 저장

## 🚀 실행 방법
```bash
   python 실습파일.py
```