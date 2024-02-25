import sqlite3
import os
import csv
import time


class UserProgressDB:
    def __init__(self, database_url='results/user_progress.db'):
        self.database_url = database_url
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.database_url)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                username TEXT PRIMARY KEY,
                progress INTEGER,
                completed INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def check_completion(self, username):
        conn = sqlite3.connect(self.database_url)
        c = conn.cursor()
        c.execute('SELECT completed FROM user_progress WHERE username = ?', (username,))
        result = c.fetchone()
        conn.close()
        if result is None:
            return False  # 用户不存在，认为未完成
        return result[0] == 1  # 如果 completed 字段为 1，则返回 True

    def mark_completion(self, username):
        conn = sqlite3.connect(self.database_url)
        c = conn.cursor()
        c.execute('UPDATE user_progress SET completed = 1 WHERE username = ?', (username,))
        conn.commit()
        conn.close()

    def get_or_create_user_progress(self, username):
        conn = sqlite3.connect(self.database_url)
        c = conn.cursor()
        # 检查用户是否存在
        c.execute('SELECT progress FROM user_progress WHERE username = ?', (username,))
        result = c.fetchone()
        if result is None:
            # 用户不存在，创建新用户并设置进度为 0
            c.execute('INSERT INTO user_progress \
                    (username, progress, completed) VALUES (?, 0, 0)', (username,))
            conn.commit()
            progress = 0
        else:
            progress = result[0]
        conn.close()
        return progress

    def update_user_progress(self, username, progress):
        conn = sqlite3.connect(self.database_url)
        c = conn.cursor()
        c.execute('UPDATE user_progress SET progress = ? WHERE username = ?', (progress, username))
        conn.commit()
        conn.close()


class CSVFile:
    def __init__(self, csv_url='results/selected_images.csv'):
        self.csv_url = csv_url

    def init_csv_file(self):
        # 检查文件是否存在
        if not os.path.exists(self.csv_url):
            # 创建文件并写入表头
            with open(self.csv_url, mode='w', newline='') as file:
                writer = csv.writer(file)
                # 定义表头
                header = ['Timestamp', 'Username', 'Progress', 
                        'Method', 'Concept', 'CR_Chosen']
                # 写入表头
                writer.writerow(header)

    def write_to_csv(self, username, progress, method, concept, cr_chosen):
        with open(self.csv_url, mode='a', newline='') as file:
            writer = csv.writer(file)
            timestamp = time.time()
            local_time = time.localtime(timestamp)
            readable_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            writer.writerow([readable_time, username, progress, method, concept, cr_chosen])

    def read_from_csv(self):
        with open(self.csv_url, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)