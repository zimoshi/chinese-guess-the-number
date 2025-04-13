import random
import argparse
import csv
from datetime import datetime
import os

def save_score(player_name, attempts, min_num, max_num):
    if not os.path.exists('scores.csv'):
        with open('scores.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['玩家', '尝试次数', '范围', '日期时间'])
    
    with open('scores.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player_name, attempts, f"{min_num}-{max_num}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def show_high_scores():
    if not os.path.exists('scores.csv'):
        print("还没有任何得分记录！")
        return
    
    with open('scores.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        if not (scores := list(reader)):
            print("还没有任何得分记录！")
            return
    
    scores.sort(key=lambda x: int(x[1]))
    
    print("\n=== 最高分排行榜 ===")
    print("排名  玩家    尝试次数  范围      日期时间")
    print("-" * 50)
    for i, score in enumerate(scores[:10], 1):
        print(f"{i:2d}.   {score[0]:<8} {score[1]:<8} {score[2]:<10} {score[3]}")

def guess_number(min_num=1, max_num=100):
    # 生成指定范围内的随机数
    secret_number = random.randint(min_num, max_num)
    attempts = 0
    
    print("欢迎来到猜数字游戏！")
    print(f"我已经想好了一个{min_num}到{max_num}之间的数字，请开始猜测吧！")
    
    while True:
        try:
            # 获取玩家输入
            guess = int(input(f"请输入你的猜测（{min_num}-{max_num}）："))
            attempts += 1
            
            # 检查猜测是否正确
            if guess < min_num or guess > max_num:
                print(f"请输入{min_num}到{max_num}之间的数字！")
                continue
                
            if guess < secret_number:
                print("太小了！再试一次。")
            elif guess > secret_number:
                print("太大了！再试一次。")
            else:
                print("恭喜你！你猜对了！")
                print(f"你总共尝试了{attempts}次。")
                
                # 询问玩家姓名并保存得分
                player_name = input("请输入你的名字以保存得分：").strip()
                if player_name:
                    save_score(player_name, attempts, min_num, max_num)
                    show_high_scores()
                break
                
        except ValueError:
            print("请输入有效的数字！")

def main():
    parser = argparse.ArgumentParser(description='猜数字游戏')
    parser.add_argument('--min', type=int, default=1, help='最小数字（默认：1）')
    parser.add_argument('--max', type=int, default=100, help='最大数字（默认：100）')
    parser.add_argument('--version', action='version', version='猜数字游戏 v1.0')
    parser.add_argument('--scores', action='store_true', help='显示最高分排行榜')
    
    args = parser.parse_args()
    
    if args.scores:
        show_high_scores()
        return
    
    # 验证参数
    if args.min >= args.max:
        print("错误：最小数字必须小于最大数字！")
        return
    
    guess_number(args.min, args.max)

if __name__ == "__main__":
    main()
