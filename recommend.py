import math
import evaluate
import pandas as pd
import subprocess

def sim(x, y, n, data):
    a = 0
    b = 0
    c = 0
    for i in range(n):
        a += data[x][i] * data[y][i]
        b += math.pow(data[x][i], 2)
        c += math.pow(data[y][i], 2)

    result = "{:.2f}".format(a / (math.sqrt(b) * math.sqrt(c)))

    return float(result)

def centered(matrix, n, m):
    data = [[-1] * n for i in range(m)]

    for i in range(m):
        for j in range(n):
            data[i][j] = matrix[i][j]

    avg = list()
    for i in range(m):
        sum = 0
        cnt = 0
        for t in range(n):
            if data[i][t] != -1:
                sum += data[i][t]
                cnt += 1
        avg.append(sum / cnt)

    for i in range(m):
        for t in range(n):
            if data[i][t] != -1:
                data[i][t] = data[i][t] - avg[i]
            else:
                data[i][t] = 0

    return data

def getData(file_path):
    # Đọc dữ liệu từ file Excel
    df = pd.read_excel(file_path)
    
    # Chuyển đổi user_id và movie_id sang kiểu int
    df['User ID'] = df['User ID'].astype(int)
    df['Movie ID'] = df['Movie ID'].astype(int)
    
    # Lấy số lượng unique user_id và movie_id để xác định kích thước của ma trận
    n = df['User ID'].nunique()
    m = df['Movie ID'].nunique()
    
    # Khởi tạo ma trận với giá trị -1
    matrix = [[-1] * n for _ in range(m)]
    
    # Điền dữ liệu vào ma trận
    for _, row in df.iterrows():
        user_id = int(row['User ID'])  # Chuyển đổi thành kiểu số nguyên
        movie_id = int(row['Movie ID'])  # Chuyển đổi thành kiểu số nguyên
        rating = row['Rating']
        matrix[movie_id][user_id] = rating
    
    return matrix, m, n

def getPredict(matrix, m, n, target, movie):
    data = centered(matrix, n, m)
    similarity = list()
    for i in range(m):
        if i != movie:
            tmp = sim(x=movie, y=i, n=n, data=data)
            similarity.append((i, tmp))
    similarity.sort(key=lambda x: x[1], reverse=True)

    x = 0
    y = 0
    predict = 0
    for i in range(len(similarity)):
        if matrix[similarity[i][0]][target] != -1 and similarity[i][1] > 0:
            x += matrix[similarity[i][0]][target] * similarity[i][1]
            y += similarity[i][1]

    if x != 0 and y != 0:
        predict = x / y
    else:
        predict = -1

    return predict, similarity

def xuly(user_id):
    file_path = 'data/ratings_file.xlsx'
    matrix, m, n = getData(file_path)
    target = int(user_id)

    result_all = list()

    for movie in range(m):
        if matrix[movie][target] == -1:
            predict, similarity = getPredict(matrix, m, n, target, movie)
            result_all.append((movie, "{:.2f}".format(predict)))

    result_all.sort(key=lambda x: x[1], reverse=True)
    print("Movie " + str(movie) + " with:", end=" ")
    print(similarity) # Trả danh sách các bộ phim tương đồng

    recommend_movies = []
    cnt = 0
    for i in range(len(result_all)):
        if cnt == 3:
            break
        if result_all[i][1] != "{:.2f}".format(-1):
            recommend_movies.append(result_all[i])
            cnt += 1

    rsme = evaluate.rsme(matrix, m, n, target)

    return recommend_movies, rsme, result_all

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        user_id = sys.argv[1]
        recommend_movies, rsme,result_all = xuly(user_id)
        print("List of unrated movies:",result_all)
        print("Top 3 Recommend Movies:", recommend_movies)
        print("RSME:", rsme)
    else:
        print("Usage: python recommend.py <user_id>")
