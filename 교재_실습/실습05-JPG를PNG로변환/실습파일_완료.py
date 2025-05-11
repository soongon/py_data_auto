# JPG를 PNG로 변환하는 프로그램
from PIL import Image
import os
import time
import argparse

def convert_jpg_to_png(source_dir, output_dir, quality=100):
    """
    JPG 이미지를 PNG로 변환하여 저장합니다.
    
    Args:
        source_dir (str): JPG 이미지가 있는 소스 폴더 경로
        output_dir (str): 변환된 PNG 이미지를 저장할 폴더 경로
        quality (int): PNG 저장 품질 (1-100, 기본값 100)
    
    Returns:
        int: 변환된 이미지 파일 수
    """
    # 출력 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 변환된 파일 카운터
    converted_count = 0
    
    # 소스 폴더의 모든 파일 처리
    for filename in os.listdir(source_dir):
        # 파일 전체 경로
        file_path = os.path.join(source_dir, filename)
        
        # 디렉토리는 건너뛰기
        if os.path.isdir(file_path):
            continue
            
        # JPG 파일만 처리 (.jpg, .jpeg, .JPG, .JPEG)
        if filename.lower().endswith(('.jpg', '.jpeg')):
            try:
                # 이미지 열기
                img = Image.open(file_path)
                
                # 파일명과 확장자 분리
                name, _ = os.path.splitext(filename)
                
                # 새 PNG 파일명
                new_name = f"{name}.png"
                new_path = os.path.join(output_dir, new_name)
                
                # 이름 충돌 처리
                if os.path.exists(new_path):
                    count = 1
                    while os.path.exists(os.path.join(output_dir, f"{name}_{count}.png")):
                        count += 1
                    new_name = f"{name}_{count}.png"
                    new_path = os.path.join(output_dir, new_name)
                
                # PNG로 저장
                img.save(new_path, "PNG", quality=quality)
                converted_count += 1
                
                # 변환 상태 출력
                print(f"변환 완료: {filename} -> {new_name}")
                
            except Exception as e:
                print(f"오류: {filename} 변환 중 문제 발생 - {e}")
    
    return converted_count

def convert_with_options(source_dir, output_dir, options=None):
    """
    다양한 옵션을 적용하여 JPG 이미지를 PNG로 변환합니다.
    
    Args:
        source_dir (str): JPG 이미지가 있는 소스 폴더 경로
        output_dir (str): 변환된 PNG 이미지를 저장할 폴더 경로
        options (dict): 변환 옵션 (resize, rotate 등)
    
    Returns:
        int: 변환된 이미지 파일 수
    """
    # 기본 옵션 설정
    if options is None:
        options = {}
    
    # 출력 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 변환된 파일 카운터
    converted_count = 0
    
    # 소스 폴더의 모든 파일 처리
    for filename in os.listdir(source_dir):
        # 파일 전체 경로
        file_path = os.path.join(source_dir, filename)
        
        # 디렉토리는 건너뛰기
        if os.path.isdir(file_path):
            continue
            
        # JPG 파일만 처리 (.jpg, .jpeg, .JPG, .JPEG)
        if filename.lower().endswith(('.jpg', '.jpeg')):
            try:
                # 이미지 열기
                img = Image.open(file_path)
                
                # 옵션 적용
                # 크기 조정
                if 'resize' in options:
                    width, height = options['resize']
                    img = img.resize((width, height), Image.LANCZOS)
                
                # 회전
                if 'rotate' in options:
                    angle = options['rotate']
                    img = img.rotate(angle, expand=True)
                
                # 밝기 조정
                if 'brightness' in options:
                    from PIL import ImageEnhance
                    factor = options['brightness']
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(factor)
                
                # 파일명과 확장자 분리
                name, _ = os.path.splitext(filename)
                
                # 새 PNG 파일명
                new_name = f"{name}.png"
                new_path = os.path.join(output_dir, new_name)
                
                # 이름 충돌 처리
                if os.path.exists(new_path):
                    count = 1
                    while os.path.exists(os.path.join(output_dir, f"{name}_{count}.png")):
                        count += 1
                    new_name = f"{name}_{count}.png"
                    new_path = os.path.join(output_dir, new_name)
                
                # PNG로 저장
                img.save(new_path, "PNG")
                converted_count += 1
                
                # 적용된 옵션 정보
                options_info = ", ".join(f"{k}: {v}" for k, v in options.items())
                
                # 변환 상태 출력
                print(f"변환 완료: {filename} -> {new_name} (옵션: {options_info if options else '없음'})")
                
            except Exception as e:
                print(f"오류: {filename} 변환 중 문제 발생 - {e}")
    
    return converted_count

def batch_conversion_with_preview(source_dir, output_dir):
    """
    미리보기 기능이 있는 일괄 변환 함수
    
    Args:
        source_dir (str): JPG 이미지가 있는 소스 폴더 경로
        output_dir (str): 변환된 PNG 이미지를 저장할 폴더 경로
    
    Returns:
        int: 변환된 이미지 파일 수
    """
    # 출력 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 미리보기용 임시 폴더
    preview_dir = os.path.join(output_dir, "preview")
    os.makedirs(preview_dir, exist_ok=True)
    
    # JPG 파일 목록 가져오기
    jpg_files = [f for f in os.listdir(source_dir) 
                if os.path.isfile(os.path.join(source_dir, f)) and 
                f.lower().endswith(('.jpg', '.jpeg'))]
    
    if not jpg_files:
        print("변환할 JPG 파일이 없습니다.")
        return 0
    
    print(f"총 {len(jpg_files)}개의 JPG 파일을 찾았습니다.")
    
    # 첫 번째 이미지로 미리보기 생성
    preview_file = jpg_files[0]
    preview_path = os.path.join(source_dir, preview_file)
    
    try:
        img = Image.open(preview_path)
        name, _ = os.path.splitext(preview_file)
        preview_output = os.path.join(preview_dir, f"{name}_preview.png")
        img.save(preview_output, "PNG")
        
        print(f"\n미리보기가 생성되었습니다: {preview_output}")
        print("---")
        
        # 확인 요청
        confirm = input("모든 JPG 파일을 PNG로 변환하시겠습니까? (y/n): ")
        
        if confirm.lower() != 'y':
            print("변환이 취소되었습니다.")
            return 0
            
        # 미리보기 폴더 정리
        for f in os.listdir(preview_dir):
            os.remove(os.path.join(preview_dir, f))
        os.rmdir(preview_dir)
        
        # 실제 변환 수행
        return convert_jpg_to_png(source_dir, output_dir)
        
    except Exception as e:
        print(f"미리보기 생성 중 오류 발생: {e}")
        return 0

def main():
    # 소스 및 출력 폴더 경로
    source_dir = "data/images"
    output_dir = "output/converted"
    
    # 소스 폴더가 없으면 오류 메시지 출력
    if not os.path.exists(source_dir):
        print(f"오류: 소스 폴더 '{source_dir}'가 존재하지 않습니다.")
        return
    
    print("===== JPG를 PNG로 변환하는 프로그램 =====")
    print("1. 기본 변환 (단순 포맷 변환)")
    print("2. 옵션 적용 변환 (크기 조정)")
    print("3. 일괄 변환 (미리보기 기능)")
    print("4. 종료")
    
    choice = input("\n원하는 작업을 선택하세요 (1-4): ")
    
    if choice == "1":
        # 기본 변환
        start_time = time.time()  # 시작 시간
        
        count = convert_jpg_to_png(source_dir, output_dir)
        
        end_time = time.time()  # 종료 시간
        elapsed_time = end_time - start_time  # 소요 시간
        
        if count > 0:
            print(f"\n변환 완료: {count}개의 JPG 파일이 PNG로 변환되었습니다.")
        else:
            print("\n변환할 JPG 파일이 없습니다.")
            
        print(f"소요 시간: {elapsed_time:.2f}초")
    
    elif choice == "2":
        # 옵션 적용 변환
        print("\n적용할 옵션을 선택하세요:")
        print("1. 크기 조정")
        print("2. 회전")
        print("3. 밝기 조정")
        
        option_choice = input("옵션 번호를 입력하세요 (1-3): ")
        options = {}
        
        if option_choice == "1":
            # 크기 조정 옵션
            try:
                width = int(input("너비(픽셀): "))
                height = int(input("높이(픽셀): "))
                options['resize'] = (width, height)
            except ValueError:
                print("유효한 숫자를 입력하세요.")
                return
                
        elif option_choice == "2":
            # 회전 옵션
            try:
                angle = float(input("회전 각도(도): "))
                options['rotate'] = angle
            except ValueError:
                print("유효한 숫자를 입력하세요.")
                return
                
        elif option_choice == "3":
            # 밝기 조정 옵션
            try:
                factor = float(input("밝기 계수(1.0=원본, 0.5=어둡게, 2.0=밝게): "))
                options['brightness'] = factor
            except ValueError:
                print("유효한 숫자를 입력하세요.")
                return
                
        else:
            print("잘못된 옵션 선택입니다.")
            return
        
        # 옵션 적용 변환 실행
        start_time = time.time()
        
        count = convert_with_options(source_dir, output_dir, options)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if count > 0:
            print(f"\n변환 완료: {count}개의 JPG 파일이 옵션을 적용하여 PNG로 변환되었습니다.")
        else:
            print("\n변환할 JPG 파일이 없습니다.")
            
        print(f"소요 시간: {elapsed_time:.2f}초")
    
    elif choice == "3":
        # 일괄 변환 (미리보기 기능)
        start_time = time.time()
        
        count = batch_conversion_with_preview(source_dir, output_dir)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if count > 0:
            print(f"\n일괄 변환 완료: {count}개의 JPG 파일이 PNG로 변환되었습니다.")
            
        print(f"전체 소요 시간: {elapsed_time:.2f}초")
    
    elif choice == "4":
        print("프로그램을 종료합니다.")
    
    else:
        print("잘못된 선택입니다. 1-4 사이의 숫자를 입력하세요.")

if __name__ == "__main__":
    main()
