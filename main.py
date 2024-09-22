import csv
import os  # tương tác với hệ thống tệp
import sys
import time # truy cập vào các tham số
import pdfplumber

def extract_and_write_tables(pdf_path, output_path, max_pages=None, batch_size=100):
    total_page_processed = 0
    first_write = not os.path.exists(output_path)
    headers = ['Date', 'Time', 'Comment', 'Credit', 'Name']
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        if max_pages is not None:
            total_pages = min(total_pages, max_pages)
        print(f"PDF File has total {total_pages} pages")
        
        for i in range(0, total_pages, batch_size):
            batch_table = []
            end_page = min(i + batch_size, total_pages)
            
            for page_num in range(i, end_page):
                print(f"Processing page {page_num + 1} / {total_pages}")
                page = pdf.pages[page_num]
                tables = page.extract_tables()
                
                for table in tables:
                    for row in table[2:]:
                        # Lấy dữ liệu từ các cột
                        date_time = row[1].split('\n')  # Giả định trường này có ngày và giờ
                        transaction_comment = row[2].replace('\n', ' ')
                        credit = row[3]
                        offset_name = row[4]

                        # Kiểm tra và xử lý date và time
                        if len(date_time) == 2:
                            date = date_time[0]  # Ngày
                            time = date_time[1]  # Thời gian
                        else:
                            date = date_time[0]  # Nếu chỉ có ngày
                            time = ''  # Không có thời gian

                        # Thêm vào batch_table
                        batch_table.append([
                            f'{date}',              # Trường date
                            f'{time}',              # Trường time
                            transaction_comment,    # Trường transaction comment
                            credit.replace('.', '') if credit else '',  # Trường credit
                            offset_name if offset_name else ''  # Trường offset name
                        ])
            
            write_to_csv(batch_table, output_path, headers, first_write)
            first_write = False
            total_page_processed += len(range(i, end_page))
            print(f"Completely processed and wrote {total_page_processed}/{total_pages}")

def write_to_csv(data, output_path, headers, first_write):
    mode = 'w' if first_write else 'a'
    with open(output_path, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')  # Sử dụng dấu phân cách là dấu phẩy
        if first_write:
            writer.writerow(headers)  # Ghi headers nếu là lần ghi đầu tiên
        writer.writerows(data)  # Ghi tất cả các bản ghi

def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: python main.py <path_to_pdf> [max_pages]")
        sys.exit(1)

    pdf_path = sys.argv[1];
    if not os.path.exists(pdf_path):
        print(f"Cannot find file: {pdf_path}")
        sys.exit(1)    
    
    max_pages = None
    if len(sys.argv) == 3:
        try:
            max_pages = int(sys.argv[2])
        except ValueError:
            print("max_pages is not the integer number.")
            sys.exit(1)
            
    output_path = "output.csv"
    
    print("Start extracting data from PDF to CSV...")
    start_time = time.time()
    
    extract_and_write_tables(pdf_path, output_path, max_pages, 100)
    

if __name__ == "__main__":
    main()