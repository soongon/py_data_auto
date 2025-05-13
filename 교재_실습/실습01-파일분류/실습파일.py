import os
import shutil
from pathlib import Path

def prepare_output_directory(output_dir: Path):
    """output 디렉토리가 존재하지 않으면 생성"""
    output_dir.mkdir(exist_ok=True)

def get_extension(file: Path) -> str:
    """파일의 확장자를 소문자로 반환 (없을 경우 'no_extension')"""
    ext = file.suffix.lower().lstrip('.')
    return ext if ext else 'no_extension'

def classify_and_copy_files(data_dir: Path, output_dir: Path):
    """파일을 확장자별로 분류하여 복사"""
    for file in data_dir.iterdir():
        if file.is_file():
            ext = get_extension(file)
            target_dir = output_dir / ext
            target_dir.mkdir(exist_ok=True)
            shutil.copy2(file, target_dir / file.name)

def main():
    data_dir = Path('./data')
    output_dir = Path('./output')

    if not data_dir.exists() or not data_dir.is_dir():
        print("❌ './data' 디렉토리가 존재하지 않거나 폴더가 아닙니다.")
        return

    prepare_output_directory(output_dir)
    classify_and_copy_files(data_dir, output_dir)

    print("✅ 모든 파일이 확장자별로 정리되었습니다.")

if __name__ == '__main__':
    main()
