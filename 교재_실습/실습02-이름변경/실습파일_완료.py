# 🔧 실습 시작 파일
# 파일 이름 일괄 변경 프로그램
import os
import datetime
import shutil

def rename_files(folder_path, prefix="file_"):
    """
    지정된 폴더 내의 모든 파일을 정렬하여 순차적으로 이름 변경
    
    Args:
        folder_path: 파일이 있는 폴더 경로
        prefix: 새 파일 이름의 접두어
    """
    # 폴더 내 파일 목록 가져오기 및 정렬
    files = sorted(os.listdir(folder_path))
    
    # 각 파일에 대해 이름 변경 작업 수행
    for idx, filename in enumerate(files, 1):
        # 파일 경로
        file_path = os.path.join(folder_path, filename)
        
        # 디렉토리는 건너뛰기
        if os.path.isdir(file_path):
            continue
            
        # 파일명과 확장자 분리
        _, ext = os.path.splitext(filename)
        
        # 새 파일명 생성 (001, 002, ... 형식)
        new_name = f"{prefix}{idx:03d}{ext}"
        new_path = os.path.join(folder_path, new_name)
        
        # 이름 변경
        os.rename(file_path, new_path)
        print(f"{filename} → {new_name}")
    
    print(f"총 {idx}개 파일의 이름이 변경되었습니다.")

def rename_png_files(folder_path, prefix="img_"):
    """
    PNG 파일만 img_001.png, img_002.png 형식으로 이름 변경
    
    Args:
        folder_path: 파일이 있는 폴더 경로
        prefix: 새 파일 이름의 접두어
    """
    # PNG 파일만 필터링
    png_files = [f for f in os.listdir(folder_path) 
                if os.path.isfile(os.path.join(folder_path, f)) and 
                f.lower().endswith('.png')]
    
    # 파일 정렬
    png_files.sort()
    
    # 순차적으로 이름 변경
    for idx, filename in enumerate(png_files, 1):
        old_path = os.path.join(folder_path, filename)
        new_name = f"{prefix}{idx:03d}.png"
        new_path = os.path.join(folder_path, new_name)
        
        # 이름 변경
        os.rename(old_path, new_path)
        print(f"{filename} → {new_name}")
    
    print(f"총 {len(png_files)}개의 PNG 파일 이름이 변경되었습니다.")

def add_date_prefix(folder_path, date_str=None):
    """
    파일 이름 앞에 날짜 접두어 추가 (예: 2025-05-11_파일명.확장자)
    
    Args:
        folder_path: 파일이 있는 폴더 경로
        date_str: 추가할 날짜 문자열 (None이면 오늘 날짜 사용)
    """
    # 날짜 문자열이 없으면 오늘 날짜 사용
    if date_str is None:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d_")
    
    # 폴더 내 모든 파일에 대해 처리
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # 디렉토리는 건너뛰기
        if os.path.isdir(file_path):
            continue
            
        # 이미 날짜 접두어가 있으면 건너뛰기
        if filename.startswith(date_str):
            print(f"{filename}은(는) 이미 날짜 접두어가.있습니다.")
            continue
            
        # 새 파일명 생성
        new_name = f"{date_str}{filename}"
        new_path = os.path.join(folder_path, new_name)
        
        # 이름 변경
        os.rename(file_path, new_path)
        print(f"{filename} → {new_name}")

def handle_filename_conflict(folder_path, filename, target_folder):
    """
    같은 이름이 이미 존재하는 경우 _1, _2 등을 붙여서 저장
    
    Args:
        folder_path: 원본 파일이 있는 폴더 경로
        filename: 처리할 파일 이름
        target_folder: 저장할 대상 폴더 경로
    """
    # 원본 파일 경로
    src_path = os.path.join(folder_path, filename)
    
    # 파일명과 확장자 분리
    name, ext = os.path.splitext(filename)
    
    # 대상 파일 경로
    dst_path = os.path.join(target_folder, filename)
    
    # 이름 충돌 확인 및 처리
    counter = 1
    while os.path.exists(dst_path):
        # 이미 같은 이름이 있으면 _1, _2 등을 붙임
        new_name = f"{name}_{counter}{ext}"
        dst_path = os.path.join(target_folder, new_name)
        counter += 1
    
    # 파일 복사
    shutil.copy2(src_path, dst_path)
    print(f"{filename} → {os.path.basename(dst_path)}")

def main():
    # 메인 메뉴 표시
    print("===== 파일 이름 일괄 변경 프로그램 =====")
    print("1. 기본 파일 이름 변경 (순차적 넘버링)")
    print("2. PNG 파일만 일괄 이름 변경")
    print("3. 파일 이름에 날짜 접두어 추가")
    print("4. 이름 충돌 처리 테스트")
    print("5. 종료")
    
    # 사용자 선택
    choice = input("\n원하는 작업을 선택하세요 (1-5): ")
    
    # data 폴더 경로
    data_folder = "data"
    rename_folder = os.path.join(data_folder, "rename")
    result_folder = os.path.join(data_folder, "result")
    
    # result 폴더가 없으면 생성
    os.makedirs(result_folder, exist_ok=True)
    
    if choice == "1":
        # 메뉴 1: 기본 파일 이름 변경
        prefix = input("파일 접두어를 입력하세요 (기본: image_): ") or "image_"
        rename_files(rename_folder, prefix)
    
    elif choice == "2":
        # 메뉴 2: PNG 파일만 일괄 이름 변경
        rename_png_files(data_folder)
    
    elif choice == "3":
        # 메뉴 3: 파일 이름에 날짜 접두어 추가
        add_date_prefix(data_folder, "2025-05-11_")
    
    elif choice == "4":
        # 메뉴 4: 이름 충돌 처리 테스트
        for filename in os.listdir(data_folder):
            if os.path.isfile(os.path.join(data_folder, filename)):
                handle_filename_conflict(data_folder, filename, result_folder)
    
    elif choice == "5":
        # 메뉴 5: 종료
        print("프로그램을 종료합니다.")
    
    else:
        print("잘못된 선택입니다. 1-5 사이의 숫자를 입력하세요.")

if __name__ == "__main__":
    main()
if __name__ == '__main__':
    print('실습 실행 준비 완료')
