import random

# 定义音符列表
notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# 定义鸟类
class Bird:
    def __init__(self, notes_b, rarity):
        self.notes_b = notes_b
        self.rarity = rarity
        self.attraction_level = 0

    def __str__(self):
        return f"Bird with notes: {self.notes_b}, rarity: {self.rarity}, attraction level: {self.attraction_level}"

# 生成M只鸟
def generate_birds(M):
    birds = []
    for _ in range(M):
        notes_b_length = random.randint(1, 5)  # 鸟的音符长度与稀有度成正比
        notes_b = ''.join([random.choice(notes) for _ in range(notes_b_length)])
        rarity = notes_b_length  # 稀有度与音符长度成正比
        birds.append(Bird(notes_b, rarity))
    return birds


def find_longest_substring_match_dp(string_n, string_b):
    """
    Find the longest substring using dynamic programming.
    """
    len_n = len(string_n)
    len_b = len(string_b)
    # Create a 2D array to store lengths of longest common suffixes
    dp = [[0] * (len_b + 1) for _ in range(len_n + 1)]
    
    max_length = 0

    # Build the dp array
    for i in range(1, len_n + 1):
        for j in range(1, len_b + 1):
            if string_n[i - 1] == string_b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_length = max(max_length, dp[i][j])
            else:
                dp[i][j] = 0  # Ends the common substring here

    return max_length

def calculate_score(max_length):
    """
    Calculate the score based on the length of the matching string.
    """
    return sum(10**k for k in range(max_length))

# 计分模块
def calculate_attraction_level_score(Notes_N, notes_b):
    max_length = find_longest_substring_match_dp(Notes_N, notes_b)
    total_score = calculate_score(len(notes_b))
    truth_score = calculate_score(max_length)
    return truth_score / total_score

# 匹配音符并计算吸引度
def match_notes(Notes_N, birds):
    for bird in birds:
        score = calculate_attraction_level_score(Notes_N, bird.notes_b)
        bird.attraction_level = score

# 根据吸引度获取鸟
def get_birds(birds):
    captured_birds = []
    for bird in birds:
        attraction_level = bird.attraction_level
        if attraction_level >= 1.0:
            captured_birds.append(bird)
        elif attraction_level >= 0.8:
            if random.random() < 0.8:
                captured_birds.append(bird)
        elif attraction_level >= 0.6:
            if random.random() < 0.5:
                captured_birds.append(bird)
        elif attraction_level >= 0.5:
            if random.random() < 0.2:
                captured_birds.append(bird)
    return captured_birds

# 主游戏逻辑
def main():
    M = 5   # 鸟的数量

    # 获取玩家输入的音符序列
    Notes_N = input("Enter your notes (e.g., ABCDEFG): ").upper()
    print(f"Your notes: {Notes_N}")

    birds = generate_birds(M)
    print("Generated birds:")
    for bird in birds:
        print(bird)

    match_notes(Notes_N, birds)

    print("Final birds attraction status:")
    for bird in birds:
        print(bird)

    captured_birds = get_birds(birds)
    print("Captured birds:")
    for bird in captured_birds:
        print(bird)

if __name__ == "__main__":
    main()