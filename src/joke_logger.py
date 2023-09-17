def log_joke(joke_text, rating):
    with open('../jokes.log', 'a') as file:
        log_line = f'{rating_prefix(rating)} {joke_text}\n'
        print(log_line)
        file.write(log_line)


def rating_prefix(rating):
    return '[10]' if rating == 10 else f'[ {rating}]'

