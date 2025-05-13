import shutil
from pathlib import Path

def rename_files_with_prefix(source_dir: Path, target_dir: Path, prefix: str):
    # 대상 폴더가 없으면 생성
    target_dir.mkdir(parents=True, exist_ok=True)

    # 파일 정렬 (이름 기준)
    files = sorted([f for f in source_dir.iterdir() if f.is_file()])

    for idx, file in enumerate(files, start=1):
        ext = file.suffix  # 확장자 추출
        number = f"{idx:03}"  # 순번 형식 (001, 002, ...)
        new_name = f"{prefix}-{number}{ext}"
        shutil.copy2(file, target_dir / new_name)

def main():
    prefix = 'sample'  # 접두어 설정
    source_dir = Path('./data/rename').resolve()
    target_dir = Path('./data/result').resolve()

    if not source_dir.exists():
        print("❌ 원본 폴더가 존재하지 않습니다.")
        return

    rename_files_with_prefix(source_dir, target_dir, prefix)
    print("✅ 파일 이름 변경 및 복사 완료.")

if __name__ == '__main__':
    main()
