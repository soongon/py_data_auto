# 🔧 파일 분류 자동화 프로그램
import os
import shutil

def classify_files(source_dir, target_dir):
    """
    다양한 확장자의 파일들을 자동으로 분류하는 함수

    Args:
        source_dir (str): 분류할 파일들이 있는 소스 디렉토리 경로
        target_dir (str): 분류된 파일들이 저장될 대상 디렉토리 경로
    """
    # 소스 디렉토리에 파일이 없으면 종료
    if not os.path.exists(source_dir):
        print(f"소스 디렉토리 {source_dir}가 존재하지 않습니다.")
        return

    # 타겟 디렉토리가 없으면 생성
    os.makedirs(target_dir, exist_ok=True)

    # 파일 분류 작업 시작
    file_count = 0

    for filename in os.listdir(source_dir):
        source_file_path = os.path.join(source_dir, filename)

        # 디렉토리는 무시
        if os.path.isdir(source_file_path):
            continue

        # 파일 확장자 추출 (마지막 점 이후 문자열)
        file_extension = filename.split('.')[-1].lower()

        # 확장자별 폴더 생성
        extension_dir = os.path.join(target_dir, file_extension)
        os.makedirs(extension_dir, exist_ok=True)

        # 대상 경로 설정
        destination_file_path = os.path.join(extension_dir, filename)

        # 이미 같은 이름의 파일이 있는 경우 처리
        if os.path.exists(destination_file_path):
            base_name, ext = os.path.splitext(filename)
            count = 1
            while os.path.exists(os.path.join(extension_dir, f"{base_name}_{count}{ext}")):
                count += 1
            destination_file_path = os.path.join(extension_dir, f"{base_name}_{count}{ext}")

        # 파일 이동
        try:
            shutil.copy2(source_file_path, destination_file_path)
            print(f"파일 이동: {filename} -> {extension_dir}/")
            file_count += 1
        except Exception as e:
            print(f"오류 발생: {filename} 이동 중 - {str(e)}")

    print(f"분류 완료: 총 {file_count}개 파일 처리됨")

if __name__ == '__main__':
    # 실행 경로 기준 상대 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_directory = os.path.join(current_dir, "data")
    target_directory = os.path.join(current_dir, "output")

    # 분류 실행
    classify_files(source_directory, target_directory)
    print("프로그램 실행 완료!")
