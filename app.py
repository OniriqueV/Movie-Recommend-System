from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
app = Flask(__name__)
app.secret_key = 'vanh'

def parse_recommend_movies(output_str):
    lines = output_str.split('\n')
    recommend_movies = []
    for line in lines:
        if line.startswith('Top 3 Recommend Movies:'):
            start_index = line.index(':') + 1
            end_index = start_index + 3
            movies_str = line[start_index:].strip()
            movies_list = eval(movies_str)
            recommend_movies = [(int(movie[0]), float(movie[1])) for movie in movies_list]
            break
    return recommend_movies

def parse_rsme(output_str):
    lines = output_str.split('\n')
    rsme = -1
    for line in lines:
        if line.startswith('RSME:'):
            rsme = float(line.split(': ')[1])
            break
    return rsme



# Route để hiển thị trang index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route để xử lý khi người dùng chọn một user và chuyển sang trang recommend.html
@app.route('/recommend', methods=['GET'])
def recommend():
    # Lấy tham số id từ đường dẫn
    user_id = request.args.get('id')
    # Chuyển hướng đến trang recommend.html và truyền tham số id
    return redirect(url_for('show_recommend', user_id=user_id))

# Route để hiển thị trang recommend.html và nhận tham số id
@app.route('/show_recommend/<user_id>')
def show_recommend(user_id):
    print("User ID:", user_id)
    session['user_id'] = user_id
    # Ở đây bạn có thể xử lý logic để hiển thị trang recommend.html với dữ liệu phù hợp với user_id
    # Đoạn mã dưới đây chỉ là một ví dụ đơn giản
    return render_template('recommend.html', user_id=user_id)
# Route để xử lý khi người dùng nhấn nút "Recommend" trên trang recommend.html
@app.route('/recommend_action', methods=['POST'])
def recommend_action():
    user_id = session.get('user_id', None)
    if user_id is None:
        pass
    else:
        try:
            process = subprocess.Popen(['python', 'recommend.py', str(user_id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print(stdout.decode())
            recommend_movies = parse_recommend_movies(stdout.decode())
            rsme = parse_rsme(stdout.decode())
            print("Recommend Movies:", recommend_movies)
            print("RSME:", rsme)
        except Exception as e:
            print("Error:", e)
        return render_template('recommend.html', user_id=user_id, recommend_movies=recommend_movies, rsme=rsme)

if __name__ == '__main__':
    app.run(debug=True)
