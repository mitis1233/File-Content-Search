import os
import concurrent.futures
# 指定要搜尋的文件夾路徑
folder_path = input(u'輸入文件夾路徑:')

# 要搜索的關鍵字
search_keyword = input(u'輸入搜索的關鍵字:')

# 用於儲存包含關鍵字的檔案名的列表
matching_files = []

# 用於追蹤已處理的文件數量
processed_files = 0
total_files = sum(len(files) for _, _, files in os.walk(folder_path))

# 創建並打開用於保存結果的文本文件
result_file_path = "matching_files.txt"
result_file = open(result_file_path, "w", encoding="utf-8")

def search_in_file(file_path):
    global processed_files
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            file_content = f.read()
            if search_keyword in file_content:
                matching_files.append(file_path)
                result_file.write(f"Found '{search_keyword}' in: {file_path}\n")
                result_file.flush()  # 立刻將結果寫入檔案
                print(f"Found '{search_keyword}' in: {file_path}")
            processed_files += 1
            print(f"Processed {processed_files}/{total_files} files. Current file: {file_path}", end='\r')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# 使用多執行緒池
#with concurrent.futures.ThreadPoolExecutor(max_workers=min(32, os.cpu_count() + 4)) as executor:
with concurrent.futures.ThreadPoolExecutor() as executor:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            executor.submit(search_in_file, file_path)

# 關閉結果文件
result_file.close()

# 列印包含關鍵字的文件列表（如果搜尋到文件，上面的 print 語句已經列印）
if not matching_files:
    print(f"No files containing '{search_keyword}' found.")
else:
    print(f"Matching files have been saved to '{result_file_path}'.")
