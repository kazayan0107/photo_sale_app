from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 写真データの読み込み関数
def load_photos():
    photos = []
    try:
        with open('photos.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'カテゴリー' in row:
                    photos.append(row)
                else:
                    print(f"Error: カテゴリーが見つかりません - {row}")
    except Exception as e:
        print(f"Error loading photos: {e}")
    return photos

# ルートページ（デフォルト）
@app.route('/')
def index():
    return redirect(url_for('login'))

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_code = request.form['login_code']
        
        # 仮の認証処理
        if login_code == '123456':
            return redirect(url_for('categories'))
        else:
            flash('ログインコードが間違っています。')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# カテゴリーページ
@app.route('/categories')
def categories():
    photos = load_photos()

    if not photos:
        return "写真がありません"

    categorized_photos = {}
    for photo in photos:
        category = photo['カテゴリー']
        if category not in categorized_photos:
            categorized_photos[category] = []
        categorized_photos[category].append(photo)
        print(categorized_photos)

    return render_template('categories.html', categorized_photos=categorized_photos)

app.config['UPLOAD_FOLDER'] = 'static/images/'

# アップロードページ
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('ファイルがありません。')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('ファイル名が無効です。')
        return redirect(request.url)

    # アップロードするファイルを保存
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # フォームから受け取る他のデータ
    title = request.form['title']
    category = request.form['category']
    url = request.form['url']
    price = request.form['price']

    # photos.csv にファイル名と他の情報を追加
    with open('photos.csv', 'a', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['filename', 'title', 'カテゴリー', 'url', 'price'])
        writer.writerow({
            'filename': file.filename,
            'title': title,
            'カテゴリー': category,
            'url': url,
            'price': price
        })

    flash('画像がアップロードされました。')
    return redirect(url_for('index'))

# カートページ
@app.route('/cart', methods=['POST'])
def cart():
    selected_photos = request.form.getlist('selected_photos')
    photos = load_photos()
    
    cart_items = [photo for photo in photos if photo['filename'] in selected_photos]

    if not cart_items:
        flash("カートに写真が追加されていません。")
        return redirect(url_for('categories'))

    return render_template('cart.html', cart_items=cart_items)

# 確認ページ
@app.route('/confirmation', methods=['POST'])
def confirmation():
    selected_photos = request.form.getlist('selected_photos')
    photos = load_photos()
    
    cart_items = [photo for photo in photos if photo['filename'] in selected_photos]

    categorized_cart_items = {}
    for item in cart_items:
        category = item['カテゴリー']
        if category not in categorized_cart_items:
            categorized_cart_items[category] = []
        categorized_cart_items[category].append(item)

    return render_template('confirmation.html', categorized_cart_items=categorized_cart_items)

# 支払いページ
@app.route('/payment', methods=['POST'])
def payment():
    selected_photos = request.form.getlist('selected_photos')
    photos = load_photos()
    cart_items = [photo for photo in photos if photo['filename'] in selected_photos]
    
    flash("支払いが完了しました。ありがとうございました。")
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
