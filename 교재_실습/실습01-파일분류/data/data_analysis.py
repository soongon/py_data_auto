# 데이터 분석 파이썬 스크립트
import pandas as pd
import matplotlib.pyplot as plt

def analyze_data(file_path):
    data = pd.read_csv(file_path)
    print("데이터 분석 시작...")
    print(f"총 레코드 수: {len(data)}")
    print(f"컬럼 목록: {data.columns.tolist()}")
    
    # 간단한 시각화
    data.hist(figsize=(10, 8))
    plt.tight_layout()
    plt.savefig('analysis_result.png')
    
    return data.describe()

if __name__ == "__main__":
    result = analyze_data("sample_data.csv")
    print(result)
