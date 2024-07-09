from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Veritabanı ve tablo oluşturma
def create_table():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Kitap ekleme fonksiyonu
def add_book(title, author, year):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()

# Kitap silme fonksiyonu
def remove_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# Kitapları listeleme fonksiyonu
def list_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

@app.route('/')
def index():
    books = list_books()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    add_book(title, author, year)
    return redirect(url_for('index'))

@app.route('/delete/<int:book_id>')
def delete(book_id):
    remove_book(book_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
