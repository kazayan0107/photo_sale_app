from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションのための秘密鍵

# SQLiteデータベース接続などの設定を行うこともできます

# サンプルデータ
def load_photos():
    photos = []
    with open('photos.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            photos.append(row)
    return photos

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # ログイン処理を実装
        grade = request.form['grade']
        class_number = request.form['class_number']
        student_id = request.form['student_id']
        email = request.form['email']
        phone = request.form['phone']
        login_code = request.form['login_code']
        
        # ここに認証処理を追加
        session['user'] = email  # ログインしたユーザーをセッションに保存
        return redirect(url_for('categories'))
    
    return render_template('login.html')


# CSVファイルを開く
with open('photos.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        filename = row['filename']
        title = row['title']
        category = row['category']
        url = row['url']  # Google ドライブの直接リンク
        price = row['price']  # 金額を取得

        # ここで画像を処理するロジックを追加
        print(f'ファイル名: {filename}, タイトル: {title}, カテゴリー: {category}, URL: {url}, 金額: {price}円')



@app.route('/categories')
def categories():
    photos = load_photos()
    categories = set(photo['category'] for photo in photos)  # カテゴリーを抽出
    return render_template('categories.html', categories=categories, photos=photos)

@app.route('/cart', methods=['POST'])
def cart():
    selected_photos = request.form.getlist('selected_photos')  # カートに入れた写真
    session['cart'] = selected_photos
    return redirect(url_for('confirmation'))

@app.route('/confirmation')
def confirmation():
    cart_items = session.get('cart', [])
    return render_template('confirmation.html', cart_items=cart_items)

if __name__ == '__main__':
    app.run(debug=True)

# ファイルのエンコーディングを推測する
with open('photos.csv', 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    confidence = result['confidence']
    print(f'推測されたエンコーディング: {encoding}, 信頼度: {confidence}')