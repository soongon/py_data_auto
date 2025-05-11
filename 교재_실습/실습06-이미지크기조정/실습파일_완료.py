# 이미지 크기 일괄 조정 프로그램
from PIL import Image
import os
import time
import argparse

def resize_images(source_dir, output_dir, size=(800, 800), maintain_aspect_ratio=True, quality=90):
    """
    폴더 내 이미지 파일의 크기를 일괄 조정하는 함수
    
    Args:
        source_dir (str): 원본 이미지가 있는 폴더 경로
        output_dir (str): 크기 조정된 이미지를 저장할 폴더 경로
        size (tuple): 조정할 크기 (가로, 세로) 픽셀
        maintain_aspect_ratio (bool): 가로세로 비율 유지 여부
        quality (int): JPEG 저장 품질 (1-95)
    
    Returns:
        int: 처리된 이미지 수
    """
    # 출력 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 이미지 처리 카운터
    processed_count = 0
    
    # 지원하는 이미지 확장자
    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    
    # 소스 폴더의 모든 파일 처리
    for filename in os.listdir(source_dir):
        # 파일 전체 경로
        file_path = os.path.join(source_dir, filename)
        
        # 디렉토리는 건너뛰기
        if os.path.isdir(file_path):
            continue
        
        # 지원하는 이미지 파일만 처리
        if filename.lower().endswith(supported_extensions):
            try:
                # 이미지 열기
                img = Image.open(file_path)
                
                # 가로세로 비율 유지 옵션 적용
                if maintain_aspect_ratio:
                    # 원본 이미지 크기
                    original_width, original_height = img.size
                    
                    # 가로와 세로 중 더 큰 비율을 기준으로 조정
                    width_ratio = size[0] / original_width
                    height_ratio = size[1] / original_height
                    
                    # 더 작은 비율을 선택하여 이미지가 목표 크기를 넘지 않도록 함
                    ratio = min(width_ratio, height_ratio)
                    
                    # 새 크기 계산
                    new_size = (int(original_width * ratio), int(original_height * ratio))
                    
                    # 이미지 리사이즈
                    img_resized = img.resize(new_size, Image.LANCZOS)
                else:
                    # 비율 유지 없이 지정한 크기로 조정
                    img_resized = img.resize(size, Image.LANCZOS)
                
                # 출력 파일 경로
                output_path = os.path.join(output_dir, filename)
                
                # 파일 형식에 따라 적절한 저장 방식 사용
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    img_resized.save(output_path, 'JPEG', quality=quality)
                elif filename.lower().endswith('.png'):
                    img_resized.save(output_path, 'PNG')
                else:
                    img_resized.save(output_path)
                
                processed_count += 1
                
                # 원본 크기와 조정된 크기 정보
                original_size_kb = os.path.getsize(file_path) / 1024
                new_size_kb = os.path.getsize(output_path) / 1024
                reduction = (1 - new_size_kb / original_size_kb) * 100
                
                print(f"처리: {filename} - 원본: {img.size} → 조정: {img_resized.size}")
                print(f"  크기 변화: {original_size_kb:.1f}KB → {new_size_kb:.1f}KB ({reduction:.1f}% 감소)")
                
            except Exception as e:
                print(f"오류: {filename} 처리 중 문제 발생 - {e}")
    
    return processed_count

def create_thumbnails(source_dir, output_dir, thumbnail_size=(200, 200)):
    """
    이미지 파일의 썸네일을 생성하는 함수
    
    Args:
        source_dir (str): 원본 이미지가 있는 폴더 경로
        output_dir (str): 썸네일을 저장할 폴더 경로
        thumbnail_size (tuple): 썸네일 크기 (가로, 세로) 픽셀
    
    Returns:
        int: 생성된 썸네일 수
    """
    # 출력 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 썸네일 생성 카운터
    thumbnail_count = 0
    
    # 지원하는 이미지 확장자
    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    
    # 소스 폴더의 모든 파일 처리
    for filename in os.listdir(source_dir):
        # 파일 전체 경로
        file_path = os.path.join(source_dir, filename)
        
        # 디렉토리는 건너뛰기
        if os.path.isdir(file_path):
            continue
        
        # 지원하는 이미지 파일만 처리
        if filename.lower().endswith(supported_extensions):
            try:
                # 이미지 열기
                img = Image.open(file_path)
                
                # 파일명과 확장자 분리
                name, ext = os.path.splitext(filename)
                
                # 썸네일 생성
                img.thumbnail(thumbnail_size)
                
                # 썸네일 파일명
                thumbnail_filename = f"{name}_thumb{ext}"
                
                # 출력 파일 경로
                output_path = os.path.join(output_dir, thumbnail_filename)
                
                # 파일 형식에 따라 적절한 저장 방식 사용
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    img.save(output_path, 'JPEG')
                elif filename.lower().endswith('.png'):
                    img.save(output_path, 'PNG')
                else:
                    img.save(output_path)
                
                thumbnail_count += 1
                print(f"썸네일 생성: {filename} → {thumbnail_filename} ({img.size})")
                
            except Exception as e:
                print(f"오류: {filename} 썸네일 생성 중 문제 발생 - {e}")
    
    return thumbnail_count

def batch_resize_with_options(source_dir, output_dir, options=None):
    """
    다양한 옵션을 적용하여 이미지 크기를 일괄 조정하는 함수
    
    Args:
        source_dir (str): 원본 이미지가 있는 폴더 경로
        output_dir (str): 조정된 이미지를 저장할 폴더 경로
        options (dict): 크기 조정 옵션
    
    Returns:
        int: 처리된 이미지 수
    """
    # 기본 옵션 설정
    if options is None:
        options = {
            'size': (800, 800),
            'maintain_aspect_ratio': True,
            'quality': 90,
            'format': None  # None이면 원본 형식 유지
        }
    
    # 출력 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 이미지 처리 카운터
    processed_count = 0
    
    # 지원하는 이미지 확장자
    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    
    # 소스 폴더의 모든 파일 처리
    for filename in os.listdir(source_dir):
        # 파일 전체 경로
        file_path = os.path.join(source_dir, filename)
        
        # 디렉토리는 건너뛰기
        if os.path.isdir(file_path):
            continue
        
        # 지원하는 이미지 파일만 처리
        if filename.lower().endswith(supported_extensions):
            try:
                # 이미지 열기
                img = Image.open(file_path)
                
                # 가로세로 비율 유지 옵션 적용
                if options.get('maintain_aspect_ratio', True):
                    # 원본 이미지 크기
                    original_width, original_height = img.size
                    
                    # 목표 크기
                    target_size = options.get('size', (800, 800))
                    
                    # 가로와 세로 중 더 큰 비율을 기준으로 조정
                    width_ratio = target_size[0] / original_width
                    height_ratio = target_size[1] / original_height
                    
                    # 더 작은 비율을 선택하여 이미지가 목표 크기를 넘지 않도록 함
                    ratio = min(width_ratio, height_ratio)
                    
                    # 새 크기 계산
                    new_size = (int(original_width * ratio), int(original_height * ratio))
                    
                    # 이미지 리사이즈
                    img_resized = img.resize(new_size, Image.LANCZOS)
                else:
                    # 비율 유지 없이 지정한 크기로 조정
                    target_size = options.get('size', (800, 800))
                    img_resized = img.resize(target_size, Image.LANCZOS)
                
                # 파일명과 확장자 분리
                name, ext = os.path.splitext(filename)
                
                # 출력 파일 형식 결정
                output_format = options.get('format')
                if output_format:
                    # 사용자가 지정한 형식으로 변환
                    new_ext = f".{output_format.lower()}"
                    new_filename = f"{name}{new_ext}"
                else:
                    # 원본 형식 유지
                    new_filename = filename
                
                # 출력 파일 경로
                output_path = os.path.join(output_dir, new_filename)
                
                # 품질 설정
                quality = options.get('quality', 90)
                
                # 파일 형식에 따라 적절한 저장 방식 사용
                if new_filename.lower().endswith(('.jpg', '.jpeg')):
                    img_resized.save(output_path, 'JPEG', quality=quality)
                elif new_filename.lower().endswith('.png'):
                    img_resized.save(output_path, 'PNG')
                else:
                    img_resized.save(output_path)
                
                processed_count += 1
                print(f"처리: {filename} → {new_filename} ({img_resized.size})")
                
            except Exception as e:
                print(f"오류: {filename} 처리 중 문제 발생 - {e}")
    
    return processed_count

def main():
    # 소스 및 출력 폴더 경로
    source_dir = "data/images"
    output_dir = "output/resize"
    
    # 소스 폴더가 없으면 오류 메시지 출력
    if not os.path.exists(source_dir):
        print(f"오류: 소스 폴더 '{source_dir}'가 존재하지 않습니다.")
        return
    
    print("===== 이미지 크기 일괄 조정 프로그램 =====")
    print("1. 기본 이미지 리사이즈 (가로세로 비율 유지)")
    print("2. 썸네일 생성")
    print("3. 다양한 옵션으로 일괄 변환")
    print("4. 명령줄 모드")
    print("5. 종료")
    
    choice = input("\n원하는 작업을 선택하세요 (1-5): ")
    
    if choice == "1":
        # 기본 이미지 리사이즈
        print("\n== 이미지 리사이즈 설정 ==")
        try:
            width = int(input("리사이즈할 가로 크기(픽셀, 기본 800): ") or "800")
            height = int(input("리사이즈할 세로 크기(픽셀, 기본 800): ") or "800")
            maintain_ratio = input("가로세로 비율을 유지할까요? (y/n, 기본 y): ").lower() != 'n'
            quality = int(input("JPEG 품질(1-95, 기본 90): ") or "90")
            
            start_time = time.time()
            
            count = resize_images(source_dir, output_dir, size=(width, height),
                               maintain_aspect_ratio=maintain_ratio, quality=quality)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"\n크기 조정 완료: {count}개 이미지가 {output_dir}에 저장되었습니다.")
            print(f"소요 시간: {elapsed_time:.2f}초")
            
        except ValueError:
            print("유효한 숫자를 입력하세요.")
    
    elif choice == "2":
        # 썸네일 생성
        print("\n== 썸네일 생성 설정 ==")
        try:
            thumb_width = int(input("썸네일 가로 크기(픽셀, 기본 200): ") or "200")
            thumb_height = int(input("썸네일 세로 크기(픽셀, 기본 200): ") or "200")
            
            thumb_dir = os.path.join(output_dir, "thumbnails")
            
            start_time = time.time()
            
            count = create_thumbnails(source_dir, thumb_dir, thumbnail_size=(thumb_width, thumb_height))
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"\n썸네일 생성 완료: {count}개 썸네일이 {thumb_dir}에 저장되었습니다.")
            print(f"소요 시간: {elapsed_time:.2f}초")
            
        except ValueError:
            print("유효한 숫자를 입력하세요.")
    
    elif choice == "3":
        # 다양한 옵션으로 일괄 변환
        print("\n== 고급 변환 옵션 ==")
        print("1. 모든 이미지를 JPG로 변환")
        print("2. 모든 이미지를 PNG로 변환")
        print("3. 모든 이미지 압축 (저품질)")
        print("4. 모든 이미지 고품질 변환")
        
        option_choice = input("옵션을 선택하세요 (1-4): ")
        options = {}
        
        if option_choice == "1":
            # JPG 변환
            options = {
                'size': (800, 800),
                'maintain_aspect_ratio': True,
                'quality': 85,
                'format': 'jpg'
            }
            output_subdir = os.path.join(output_dir, "jpg_converted")
            
        elif option_choice == "2":
            # PNG 변환
            options = {
                'size': (800, 800),
                'maintain_aspect_ratio': True,
                'format': 'png'
            }
            output_subdir = os.path.join(output_dir, "png_converted")
            
        elif option_choice == "3":
            # 저품질 압축
            options = {
                'size': (800, 800),
                'maintain_aspect_ratio': True,
                'quality': 50,
                'format': 'jpg'
            }
            output_subdir = os.path.join(output_dir, "compressed")
            
        elif option_choice == "4":
            # 고품질 변환
            options = {
                'size': (1024, 1024),
                'maintain_aspect_ratio': True,
                'quality': 95,
                'format': 'png'
            }
            output_subdir = os.path.join(output_dir, "high_quality")
            
        else:
            print("잘못된 옵션을 선택했습니다.")
            return
        
        start_time = time.time()
        
        count = batch_resize_with_options(source_dir, output_subdir, options)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\n변환 완료: {count}개 이미지가 {output_subdir}에 저장되었습니다.")
        print(f"소요 시간: {elapsed_time:.2f}초")
    
    elif choice == "4":
        # 명령줄 모드 (터미널에서 실행할 경우 유용)
        print("명령줄 모드 사용법:")
        print("python 실습파일_완료.py --source ./data/images --output ./output/resize --width 800 --height 600")
        
        # 여기서는 간단히 안내만 하고 별도로 구현하지 않습니다.
        parser = argparse.ArgumentParser(description='이미지 크기 일괄 조정 프로그램')
        parser.add_argument('--source', type=str, help='원본 이미지 폴더')
        parser.add_argument('--output', type=str, help='출력 폴더')
        parser.add_argument('--width', type=int, default=800, help='가로 크기')
        parser.add_argument('--height', type=int, default=800, help='세로 크기')
        parser.add_argument('--maintain-ratio', action='store_true', help='가로세로 비율 유지')
        parser.add_argument('--quality', type=int, default=90, help='JPEG 품질(1-95)')
        
    elif choice == "5":
        print("프로그램을 종료합니다.")
    
    else:
        print("잘못된 선택입니다. 1-5 사이의 숫자를 입력하세요.")

if __name__ == "__main__":
    # 명령줄 인수로 실행할 경우
    if len(os.sys.argv) > 1:
        parser = argparse.ArgumentParser(description='이미지 크기 일괄 조정 프로그램')
        parser.add_argument('--source', type=str, default='data/images', help='원본 이미지 폴더')
        parser.add_argument('--output', type=str, default='output/resize', help='출력 폴더')
        parser.add_argument('--width', type=int, default=800, help='가로 크기')
        parser.add_argument('--height', type=int, default=800, help='세로 크기')
        parser.add_argument('--maintain-ratio', action='store_true', default=True, help='가로세로 비율 유지')
        parser.add_argument('--quality', type=int, default=90, help='JPEG 품질(1-95)')
        
        args = parser.parse_args()
        
        print(f"이미지 크기 조정 중... {args.source} -> {args.output}")
        count = resize_images(args.source, args.output, 
                           size=(args.width, args.height),
                           maintain_aspect_ratio=args.maintain_ratio, 
                           quality=args.quality)
        
        print(f"크기 조정 완료: {count}개 이미지가 처리되었습니다.")
    else:
        # 대화형 모드로 실행
        main()
