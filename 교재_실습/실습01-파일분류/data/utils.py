# 유틸리티 함수 모음
import os
import datetime
import random
import string

def get_current_datetime():
    """현재 날짜와 시간을 반환"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_random_string(length=10):
    """지정된 길이의 랜덤 문자열 생성"""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def list_files_in_directory(directory_path):
    """디렉토리 내 모든 파일 목록 반환"""
    if not os.path.exists(directory_path):
        return []
    
    return [f for f in os.listdir(directory_path) 
            if os.path.isfile(os.path.join(directory_path, f))]

def get_file_extension(file_path):
    """파일 확장자 반환"""
    return os.path.splitext(file_path)[1].lower()
