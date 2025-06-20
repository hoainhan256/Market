import pandas as pd
import re


# Đọc stopwords từ file
with open('vietnamese_stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

# Hàm tiền xử lý
def preprocess_text(text):
    # Bỏ ký tự đặc biệt, giữ lại chữ cái và số
    text = re.sub(r'[^\w\s]', ' ', text)
    # Chuyển về chữ thường
    text = text.lower()
    # Tách từ, loại bỏ stopwords
    words = text.split()
    words = [word for word in words if word not in stopwords]
    return ' '.join(words)
# Đọc dữ liệu từ file CSV
df = pd.read_csv('products.csv')

# Gộp title và mô tả nếu muốn tăng độ chính xác
df['combined'] = df['title'] + ' ' + df['des']

# Tiền xử lý
df['processed'] = df['combined'].apply(preprocess_text)
df.to_csv('products.csv', index=False)
