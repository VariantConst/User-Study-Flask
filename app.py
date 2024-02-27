from flask import Flask, render_template, request, redirect, url_for, session
from utils.dataset import dat
from utils.util import UserProgressDB, CSVFile

app = Flask(__name__)
app.secret_key = 'cilab'

# 数据集加载
app.config['UPLOAD_FOLDER'] = 'static/images'
dataset = dat(app.config['UPLOAD_FOLDER'])
# 用户进度和数据库加载
total_num = 160
database = UserProgressDB(database_url='results/user_progress.db')
# 用户选择的图片记录
csvfile = CSVFile('results/selected_images.csv')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if database.check_completion(username):
            return redirect(url_for('end'))
        session['username'] = username
        # 读取或创建用户进度并存储在 session 中
        session['progress'] = database.get_or_create_user_progress(username)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    progress = session.get('progress')

    # 在这里检查进度是否已经达到或超过了 dataset 的大小
    if progress >= total_num:  # 假设 total_num 是 dataset 的大小
        # 如果是，重定向到结束页面
        return redirect(url_for('end'))
    
    image_urls, pid2concept, cr_chosen = dataset[progress]

    description = f'best preserves the contents while transferring the \
            photographic concepts. </br>Please focus on the \
            <span class="colorful-text">{pid2concept}</span> (if none, focus on the general performance)'
    return render_template('index.html', 
                           image_urls=image_urls, 
                           pid2concept=pid2concept, 
                           cr_chosen=cr_chosen, 
                           progress=progress, 
                           description=description, 
                           username=session['username'])


@app.route('/next', methods=['POST'])
def next_style():
    if 'username' not in session:
        return redirect(url_for('login'))

    # 从 session 中获取当前进度
    progress = session.get('progress', 0)

    image_url = request.form.get('image_url')  # 获取图片 URL
    cr_chosen = request.form.get('cr_chosen')  # 获取 cr_chosen 值
    pid2concept = request.form.get('pid2concept')  # 获取 pid2concept 值
    user_name = session['username']

    # 将选中的图片名和 cr_chosen 写入到 CSV 文件
    csvfile.write_to_csv(user_name, progress, 
                         image_url.split('/')[-3], 
                         pid2concept, 
                         cr_chosen)

    # 更新进度
    progress += 1
    session['progress'] = progress  # 更新 session 中的进度

    # 更新数据库中的用户进度
    database.update_user_progress(user_name, progress)

    if progress >= total_num:
        # 更新用户完成状态
        database.mark_completion(user_name)
        return redirect(url_for('end'))

    return redirect(url_for('index'))


@app.route('/end', methods=['GET', 'POST'])
def end():
    return render_template('end.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
