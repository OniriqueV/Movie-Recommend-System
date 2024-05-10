import math


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

def centered(data, n, m):
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

def xuly():
    m = int(input())
    n = int(input())
    matrix = [[-1]*n for i in range(m)]
    data = [[-1]*n for i in range(m)]
    for i in range(m):
        tmp = input().split()
        for t in range(len(tmp)):
            tmp1 = tmp[t].split(":")
            matrix[i][int(tmp1[0])] = int(tmp1[1])
            data[i][int(tmp1[0])] = matrix[i][int(tmp1[0])]

    centered(data, n, m)

    target = int(input("Give a target id: "))

    recomend = list()
    result_all = list()


    #Code này đang xét toàn bộ movie chưa được rated bởi target:
    for movie in range(m):
        if matrix[movie][target] == -1:
            print("Movie " + str(movie) + " with:", end = " ")
            similarity = list()
            for i in range(m):
                if i != movie:
                    tmp = sim(x=movie ,y=i, n=n, data=data)
                    similarity.append((i, tmp))

            similarity.sort(key = lambda x:x[1], reverse = True)


            print(similarity) #trả danh sách độ tương đồng giữa movie\
                             #ta đang xét và các movie còn lại


            #Công thức tính dự đoán đánh giá của target lên các movie
            x = 0
            y = 0
            for i in range(2):
                if matrix[similarity[i][0]][target] != -1:
                    x += matrix[similarity[i][0]][target]*similarity[i][1]
                    y += similarity[i][1]
            predict = x/y

            result_all.append((movie, "{:.2f}".format(predict)))


            #tính giá trị trung bình đánh giá của target:
            average = 0
            cnt = 0
            for i in range(m):
                if matrix[i][target] != -1:
                    average += matrix[i][target]
                    cnt+=1
            average /= cnt


            #Điều kiện: chỉ đề xuất cho target các movie
            #có đánh giá dự đoán cao hơn mức trung bình
            if predict >= average:
                recomend.append((movie,"{:.2f}".format(predict)))


    print("Movies that target " + str(target) + " may like:", end = " ")

    if len(recomend) != 0:
        print(recomend) #in ra danh sách các movie đề xuất cho target
                        #kèm dự đoán

    print("All predict rating of other movies:" )
    result_all.sort(key=lambda x:x[1], reverse=True)
    print(result_all)
    return


if __name__ == '__main__':
    xuly()
