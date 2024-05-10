import math
import evaluate

def sim(x , y, n, data):
    a = 0
    b = 0
    c = 0
    for i in range(n):
        a += data[x][i] * data[y][i]
        b += math.pow(data[x][i],2)
        c += math.pow(data[y][i],2)

    result = "{:.2f}".format(a/(math.sqrt(b)*math.sqrt(c)))

    return float(result)

def centered(matrix, n, m):
    data = [[-1]*n for i in range(m)]

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
                cnt+=1
        avg.append(sum/cnt)

    for i in range(m):
        for t in range(n):
            if data[i][t] != -1:
                data[i][t] = data[i][t] - avg[i]
            else:
                data[i][t] = 0

    return data

def getData():
    m = 0
    n = 0
    a = list()
    tmp = list()
    while tmp != [-1,-1,-1]:
        tmp = [int(i) for i in input().split()]
        m = max(m, tmp[1])
        n = max(n, tmp[0])
        a.append(tmp)
    a.pop()
    print(a)
    m += 1
    n += 1
    matrix = [[-1]*n for i in range(m)]
    for i in range(len(a)):
        matrix[a[i][1]][a[i][0]] = a[i][2]
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

    # Trả về kết quả dự đoán:
    if x != 0 and y != 0:
        predict = x / y
    else:
        predict = -1

    return predict, similarity

def xuly():
    matrix, m, n = getData()
    target = int(input("Give a target id: "))
    print(matrix)
    result_all = list()


    #Code này đang xét toàn bộ movie chưa được rated bởi target:
    for movie in range(m):
        if matrix[movie][target] == -1:
            predict, similarity = getPredict(matrix, m, n, target, movie)
            result_all.append((movie, "{:.2f}".format(predict)))
            print("Movie " + str(movie) + " with:", end=" ")
            print(similarity) # Trả danh sách các bộ phim tương đồng

    result_all.sort(key=lambda x: x[1], reverse=True)
    print("All predict rating from user {} (movie_id, predict):".format(target))
    print(result_all)
    print("Recommend to user {} top 3 movies:".format(target))
    cnt = 0
    for i in range(len(result_all)):
        if cnt == 3:
            break
        if result_all[i][1] != "{:.2f}".format(-1):
            print(result_all[i], end = " ")
            cnt+=1
    print()
    rsme = evaluate.rsme(matrix, m, n, target)
    if rsme != -1:
        print("RSME value: {:.2f}".format(rsme))
    else:
        print("RSME value: Can't evaluate")

    return


if __name__ == '__main__':
    xuly()
