# 🔧 실습 시작 파일
# 문자열 포함 파일 검색 프로그램
import os

def find_files_with_keyword(folder_path, keyword, extensions=None):
    """
    지정된 폴더에서 특정 키워드가 포함된 파일 목록을 반환합니다.
    
    Args:
        folder_path (str): 검색할 폴더 경로
        keyword (str): 찾을 키워드
        extensions (list): 검색할 파일 확장자 목록 (기본값: ['.txt'])
    
    Returns:
        list: 키워드가 포함된 파일 이름 목록
    """
    # 기본 확장자 설정
    if extensions is None:
        extensions = ['.txt']
    
    # 키워드가 포함된 파일 목록
    matched_files = []
    
    # 폴더 내 파일 목록 가져오기
    try:
        files = os.listdir(folder_path)
        
        # 각 파일에 대해 처리
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            
            # 디렉토리는 건너뛰기
            if os.path.isdir(file_path):
                continue
                
            # 확장자 확인
            _, ext = os.path.splitext(filename)
            if ext.lower() not in extensions:
                continue
                
            # 파일 내용 읽기
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 키워드 포함 여부 확인
                    if keyword in content:
                        matched_files.append(filename)
            except Exception as e:
                print(f"파일 {filename} 읽기 오류: {e}")
    
    except Exception as e:
        print(f"폴더 {folder_path} 접근 오류: {e}")
    
    return matched_files

def save_results_to_file(result_list, output_path):
    """
    검색 결과를 파일에 저장합니다.
    
    Args:
        result_list (list): 저장할 결과 목록
        output_path (str): 결과를 저장할 파일 경로
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("===== 키워드 검색 결과 =====\n\n")
            
            if result_list:
                f.write("포함된 파일 목록:\n")
                for i, filename in enumerate(result_list, 1):
                    f.write(f"{i}. {filename}\n")
                f.write(f"\n총 {len(result_list)}개의 파일이 발견되었습니다.\n")
            else:
                f.write("검색 결과가 없습니다.\n")
                
        print(f"결과가 {output_path}에 저장되었습니다.")
    except Exception as e:
        print(f"결과 저장 오류: {e}")

def search_multiple_keywords(folder_path, keywords, extensions=None):
    """
    여러 키워드가 포함된 파일을 검색합니다.
    
    Args:
        folder_path (str): 검색할 폴더 경로
        keywords (list): 찾을 키워드 목록
        extensions (list): 검색할 파일 확장자 목록
    
    Returns:
        dict: 각 키워드별 포함된 파일 목록
    """
    # 검색 결과를 저장할 딕셔너리
    results = {}
    
    # 각 키워드별로 검색 수행
    for keyword in keywords:
        results[keyword] = find_files_with_keyword(folder_path, keyword, extensions)
    
    return results

def main():
    # 검색 폴더 경로
    search_folder = "data/search"
    
    print("===== 문자열 포함 파일 검색 프로그램 =====")
    print("1. 단일 키워드 검색")
    print("2. 다중 키워드 검색")
    print("3. 다양한 파일 형식 검색 (.txt, .log)")
    print("4. 결과를 파일로 저장")
    print("5. 종료")
    
    choice = input("\n원하는 작업을 선택하세요 (1-5): ")
    
    if choice == "1":
        # 단일 키워드 검색
        keyword = input("검색할 키워드를 입력하세요: ")
        result = find_files_with_keyword(search_folder, keyword)
        
        print(f"\n키워드 '{keyword}'가 포함된 파일 목록:")
        if result:
            for file in result:
                print(f" - {file}")
        else:
            print("  일치하는 파일이 없습니다.")
    
    elif choice == "2":
        # 다중 키워드 검색 (연습문제 1번)
        keywords = ["에러", "실패", "클레임"]
        results = search_multiple_keywords(search_folder, keywords)
        
        print("\n키워드 검색 결과:")
        for keyword, files in results.items():
            print(f"\n'{keyword}'가 포함된 파일:")
            if files:
                for file in files:
                    print(f" - {file}")
            else:
                print("  일치하는 파일이 없습니다.")
    
    elif choice == "3":
        # .txt와 .log 파일 모두 검색 (연습문제 3번)
        keyword = input("검색할 키워드를 입력하세요: ")
        result = find_files_with_keyword(search_folder, keyword, extensions=['.txt', '.log'])
        
        print(f"\n.txt와 .log 파일 중 '{keyword}'가 포함된 파일 목록:")
        if result:
            for file in result:
                print(f" - {file}")
                # 파일 확장자 표시
                ext = os.path.splitext(file)[1]
                print(f"   (파일 형식: {ext})")
        else:
            print("  일치하는 파일이 없습니다.")
    
    elif choice == "4":
        # 결과를 파일로 저장 (연습문제 2번)
        keyword = input("검색할 키워드를 입력하세요: ")
        result = find_files_with_keyword(search_folder, keyword, extensions=['.txt', '.log'])
        
        output_path = os.path.join(search_folder, "result.txt")
        save_results_to_file(result, output_path)
        
        print(f"\n키워드 '{keyword}'가 포함된 파일 목록이 {output_path}에 저장되었습니다.")
    
    elif choice == "5":
        print("프로그램을 종료합니다.")
    
    else:
        print("잘못된 선택입니다. 1-5 사이의 숫자를 입력하세요.")

if __name__ == "__main__":
    main()
if __name__ == '__main__':
    print('실습 실행 준비 완료')
