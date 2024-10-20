from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

images = []


# Маршрут для головної сторінки
@app.route('/')
def home():
    return "Вітаю у Галереї зображень на Flask!"


# (Read)
@app.route('/gallery')
def gallery():
    return render_template('gallery.html', images=images)


# (Create)
@app.route('/add', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "Файл не завантажено", 400

        file = request.files['image']
        if file.filename == '':
            return "Файл не вибрано", 400

        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            images.append(file.filename)
            return redirect(url_for('gallery'))
    return render_template('add_image.html')


# (Update)
@app.route('/edit/<int:image_id>', methods=['GET', 'POST'])
def edit_image(image_id):
    if image_id >= len(images):
        return "Зображення не знайдено", 404

    old_image = images[image_id]
    if request.method == 'POST':
        new_image = request.files['image']
        if new_image:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_image))
            new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], new_image.filename))
            images[image_id] = new_image.filename
            return redirect(url_for('gallery'))
    return render_template('edit_image.html', image=old_image)


# (Delete)
@app.route('/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    if image_id < len(images):
        # Видаляємо файл з диска
        image_to_delete = images.pop(image_id)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_to_delete))
    return redirect(url_for('gallery'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
