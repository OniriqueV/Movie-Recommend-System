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



# Sử dụng hàm parse_recommend_movies
output_str = "Top 3 Recommend Movies: [(0, '4.00'), (5, '4.00'), (1, '2.00')]"
recommend_movies = parse_recommend_movies(output_str)
print(recommend_movies)
