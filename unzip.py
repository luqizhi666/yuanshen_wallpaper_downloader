import os,sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')

def is_zipfile(file_path):
    return zipfile.is_zipfile(file_path)

def unzip_all(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                extract_path = os.path.join(root, file[:-4])
                if is_zipfile(file_path):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_path)
                    print(f'Unzipped {file_path} to {extract_path}')
                    # 递归解压新解压出的文件夹中的压缩包
                    unzip_all(extract_path)
                    os.remove(file_path)  # 删除原始ZIP文件
                else:
                    print(f'Skipped {file_path}, not a valid zip file')

if __name__ == "__main__":
    directory = '.'  # Change this to your target directory
    unzip_all(directory)
