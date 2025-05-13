from pathlib import Path
from openpyxl import Workbook

def search_files_with_keyword(directory: Path, keyword: str) -> list[str]:
    matched_files = []

    for file in directory.iterdir():
        if file.is_file():
            try:
                content = file.read_text(encoding='utf-8', errors='ignore')
                if keyword in content:
                    matched_files.append(file.name)
            except Exception as e:
                print(f"⚠️ 파일 읽기 오류: {file.name} - {e}")

    return matched_files

def save_to_excel(file_list: list[str], result_file: Path):
    wb = Workbook()
    ws = wb.active
    ws.title = "검색결과"
    ws.append(['파일명'])  # 헤더

    for filename in file_list:
        ws.append([filename])

    wb.save(result_file)
    print(f"✅ 결과가 엑셀 파일로 저장되었습니다: {result_file}")

def main():
    search_dir = Path('./data/search').resolve()
    result_path = Path('./result.xlsx').resolve()
    keyword = '클레임'

    if not search_dir.exists():
        print("❌ 검색 대상 폴더가 존재하지 않습니다.")
        return

    matched = search_files_with_keyword(search_dir, keyword)
    save_to_excel(matched, result_path)

if __name__ == '__main__':
    main()
