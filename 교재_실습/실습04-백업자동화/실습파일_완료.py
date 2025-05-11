# 백업 자동화 프로그램
import os
import shutil
import datetime
import time
import argparse

def backup_files(source_dir, backup_root):
    """
    지정한 폴더의 모든 파일을 날짜별 백업 폴더에 복사합니다.
    
    Args:
        source_dir (str): 백업할 소스 폴더 경로
        backup_root (str): 백업 파일이 저장될 루트 폴더 경로
    
    Returns:
        tuple: (백업 파일 수, 백업 폴더 경로)
    """
    # 현재 날짜로 폴더명 생성 (YYYY-MM-DD 형식)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 백업 폴더 경로 생성
    backup_dir = os.path.join(backup_root, date_str)
    
    # 백업 폴더가 없으면 생성
    os.makedirs(backup_dir, exist_ok=True)
    
    # 백업 파일 카운터
    file_count = 0
    
    # 소스 폴더의 모든 파일을 백업 폴더에 복사
    for filename in os.listdir(source_dir):
        # 파일 경로
        src_file = os.path.join(source_dir, filename)
        dst_file = os.path.join(backup_dir, filename)
        
        # 디렉토리는 건너뛰기 (필요한 경우 copytree로 복사 가능)
        if os.path.isdir(src_file):
            continue
        
        # 파일 복사
        shutil.copy2(src_file, dst_file)
        file_count += 1
        
        # 복사 진행 상황 출력
        print(f"백업 중: {filename}")
    
    return file_count, backup_dir

def backup_with_timestamp(source_dir, backup_root):
    """
    지정한 폴더의 모든 파일을 타임스탬프가 추가된 이름으로 백업합니다.
    
    Args:
        source_dir (str): 백업할 소스 폴더 경로
        backup_root (str): 백업 파일이 저장될 루트 폴더 경로
    
    Returns:
        tuple: (백업 파일 수, 백업 폴더 경로)
    """
    # 현재 날짜와 시간으로 폴더명 생성 (YYYY-MM-DD_HHMMSS 형식)
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    
    # 백업 폴더 경로 생성
    backup_dir = os.path.join(backup_root, datetime_str)
    
    # 백업 폴더가 없으면 생성
    os.makedirs(backup_dir, exist_ok=True)
    
    # 백업 파일 카운터
    file_count = 0
    
    # 소스 폴더의 모든 파일을 백업 폴더에 복사
    for filename in os.listdir(source_dir):
        # 파일 경로
        src_file = os.path.join(source_dir, filename)
        
        # 디렉토리는 건너뛰기
        if os.path.isdir(src_file):
            continue
            
        # 파일명과 확장자 분리
        name, ext = os.path.splitext(filename)
        
        # 타임스탬프가 있는 새 파일명 생성
        timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(src_file)).strftime("%Y%m%d_%H%M%S")
        new_filename = f"{name}_{timestamp}{ext}"
        
        # 새 파일 경로
        dst_file = os.path.join(backup_dir, new_filename)
        
        # 파일 복사
        shutil.copy2(src_file, dst_file)
        file_count += 1
        
        # 복사 진행 상황 출력
        print(f"타임스탬프 백업 중: {filename} -> {new_filename}")
    
    return file_count, backup_dir

def incremental_backup(source_dir, backup_root, reference_dir=None):
    """
    증분 백업: 마지막 백업 이후 변경된 파일만 백업합니다.
    
    Args:
        source_dir (str): 백업할 소스 폴더 경로
        backup_root (str): 백업 파일이 저장될 루트 폴더 경로
        reference_dir (str): 비교 기준이 될 이전 백업 폴더 (기본값: 가장 최근 백업)
    
    Returns:
        tuple: (백업 파일 수, 백업 폴더 경로)
    """
    # 현재 날짜와 시간으로 폴더명 생성 (YYYY-MM-DD_HHMMSS_incremental 형식)
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S_incremental")
    
    # 백업 폴더 경로 생성
    backup_dir = os.path.join(backup_root, datetime_str)
    
    # 기준 폴더가 지정되지 않은 경우 가장 최근 백업 폴더 찾기
    if reference_dir is None:
        backup_folders = [d for d in os.listdir(backup_root) 
                        if os.path.isdir(os.path.join(backup_root, d)) and not d.endswith("_incremental")]
        
        if backup_folders:
            # 최신 폴더 찾기
            backup_folders.sort(reverse=True)  # 날짜 형식이므로 역순 정렬하면 최신이 앞에 옴
            reference_dir = os.path.join(backup_root, backup_folders[0])
        else:
            # 기준 폴더가 없으면 전체 백업 수행
            print("기준 백업 폴더가 없어 전체 백업을 수행합니다.")
            return backup_files(source_dir, backup_root)
    
    # 백업 폴더가 없으면 생성
    os.makedirs(backup_dir, exist_ok=True)
    
    # 백업 파일 카운터
    file_count = 0
    
    # 소스 폴더의 모든 파일 검사
    for filename in os.listdir(source_dir):
        # 파일 경로
        src_file = os.path.join(source_dir, filename)
        ref_file = os.path.join(reference_dir, filename)
        dst_file = os.path.join(backup_dir, filename)
        
        # 디렉토리는 건너뛰기
        if os.path.isdir(src_file):
            continue
            
        # 파일이 새로 생성되었거나 수정된 경우에만 백업
        if not os.path.exists(ref_file) or \
           os.path.getmtime(src_file) > os.path.getmtime(ref_file):
            
            # 파일 복사
            shutil.copy2(src_file, dst_file)
            file_count += 1
            
            # 변경 유형 확인
            if not os.path.exists(ref_file):
                change_type = "새 파일"
            else:
                change_type = "수정됨"
                
            # 복사 진행 상황 출력
            print(f"증분 백업 중: {filename} ({change_type})")
    
    return file_count, backup_dir

def main():
    # 소스 및 백업 폴더 경로
    source_dir = "data/original"
    backup_root = "backup"
    
    # 소스 폴더가 없으면 오류 메시지 출력
    if not os.path.exists(source_dir):
        print(f"오류: 소스 폴더 '{source_dir}'가 존재하지 않습니다.")
        return
    
    # 백업 루트 폴더가 없으면 생성
    os.makedirs(backup_root, exist_ok=True)
    
    print("===== 백업 자동화 프로그램 =====")
    print("1. 기본 백업 (날짜별 폴더)")
    print("2. 타임스탬프 백업 (파일명에 시간 추가)")
    print("3. 증분 백업 (변경된 파일만)")
    print("4. 종료")
    
    choice = input("\n원하는 작업을 선택하세요 (1-4): ")
    
    if choice == "1":
        # 기본 백업 실행
        start_time = time.time()  # 시작 시간
        
        count, backup_dir = backup_files(source_dir, backup_root)
        
        end_time = time.time()  # 종료 시간
        elapsed_time = end_time - start_time  # 소요 시간
        
        print(f"\n백업 완료: {count}개 파일이 '{backup_dir}'에 백업되었습니다.")
        print(f"소요 시간: {elapsed_time:.2f}초")
    
    elif choice == "2":
        # 타임스탬프 백업 실행
        start_time = time.time()
        
        count, backup_dir = backup_with_timestamp(source_dir, backup_root)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\n타임스탬프 백업 완료: {count}개 파일이 '{backup_dir}'에 백업되었습니다.")
        print(f"소요 시간: {elapsed_time:.2f}초")
    
    elif choice == "3":
        # 증분 백업 실행
        start_time = time.time()
        
        count, backup_dir = incremental_backup(source_dir, backup_root)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if count > 0:
            print(f"\n증분 백업 완료: {count}개 파일이 '{backup_dir}'에 백업되었습니다.")
        else:
            print("\n백업할 새 파일이나 변경된 파일이 없습니다.")
        
        print(f"소요 시간: {elapsed_time:.2f}초")
    
    elif choice == "4":
        print("프로그램을 종료합니다.")
    
    else:
        print("잘못된 선택입니다. 1-4 사이의 숫자를 입력하세요.")

if __name__ == "__main__":
    main()
