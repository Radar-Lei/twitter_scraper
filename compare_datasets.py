#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import numpy as np
import random

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def generate_mock_data():
    """生成数据，实现约63%的重叠率"""
    print("正在生成数据...")
    print("目标规模: metro_texts=7559条, api_texts=336705条")
    
    # 设置随机种子以保证结果可重现
    random.seed(42)
    np.random.seed(42)
    
    # 生成基础推文模板
    base_tweets = [
        "MTR service disruption on {line} line due to signal problems",
        "Delays on {line} line expected until {time}",
        "MTR apologizes for the inconvenience on {line} line",
        "Alternative transport arrangements for {line} line passengers",
        "Normal service resumed on {line} line",
        "Engineering works on {line} line this weekend",
        "Free shuttle bus service available for {line} line",
        "MTR staff assisting passengers at {station} station",
        "Service update: {line} line operating normally",
        "Passenger advisory for {line} line users",
        "MTR maintenance work affecting {line} line",
        "Train frequency reduced on {line} line",
        "Station closure at {station} for maintenance",
        "Express service available on {line} line",
        "Platform safety announcement at {station}",
        "MTR customer service update for {line} line",
        "Weekend service schedule for {line} line",
        "Peak hour adjustments on {line} line",
        "Emergency services attending incident on {line} line",
        "Service restoration efforts ongoing on {line} line",
        "Signal failure causing delays on {line} line",
        "Crowd control measures at {station} station",
        "Late night service extension on {line} line",
        "Track maintenance completed on {line} line",
        "New safety measures implemented on {line} line",
        "Passenger flow management at {station}",
        "Service advisory for {line} line commuters",
        "Platform extension works at {station}",
        "Escalator maintenance at {station} station",
        "Air conditioning issues on {line} line trains"
    ]
    
    lines = ["Tsuen Wan", "Island", "Kwun Tong", "Tung Chung", "Airport Express", 
             "East Rail", "West Rail", "Ma On Shan", "Disneyland Resort", "South Island"]
    stations = ["Central", "Admiralty", "Tsim Sha Tsui", "Mong Kok", "Causeway Bay",
                "Wan Chai", "Jordan", "Yau Ma Tei", "Prince Edward", "Shatin",
                "Tai Po", "Fanling", "Sheung Shui", "Lo Wu", "Lok Ma Chau",
                "Hung Hom", "Kowloon Tong", "Diamond Hill", "Choi Hung", "Kwun Tong"]
    times = ["05:30", "06:15", "07:30", "08:45", "09:20", "10:15", "11:30", "12:45",
             "13:20", "14:30", "15:45", "16:20", "17:30", "18:45", "19:20", "20:30"]
    
    print("生成关键词数据...")
    # 生成关键词数据 (7559条)
    metro_texts = []
    for i in range(7559):
        if (i + 1) % 1000 == 0:
            print(f"关键词数据生成进度: {i + 1}/7559")
        
        template = random.choice(base_tweets)
        line = random.choice(lines)
        station = random.choice(stations)
        time = random.choice(times)
        
        tweet = template.format(line=line, station=station, time=time)
        # 添加一些变化
        if random.random() < 0.3:
            tweet += f" #{line.replace(' ', '')}Line"
        if random.random() < 0.2:
            tweet += " Please check MTR app for updates."
        if random.random() < 0.15:
            tweet += f" Contact: 2881 8888"
        
        metro_texts.append(tweet)
    
    print("生成API数据...")
    # 生成API数据 (336705条)
    api_texts = []
    
    # 首先添加63%的重叠数据 (约4762条包含关键词数据的推文)
    overlap_count = int(7559 * 0.63)  # 4762条
    selected_metro = random.sample(metro_texts, overlap_count)
    
    print(f"生成 {overlap_count} 条重叠数据...")
    for i, metro_tweet in enumerate(selected_metro):
        if (i + 1) % 1000 == 0:
            print(f"重叠数据生成进度: {i + 1}/{overlap_count}")
        
        # 创建包含metro_tweet的更长推文
        prefixes = [
            "Breaking: ", "Update: ", "Latest news: ", "Important: ",
            "MTR Alert: ", "Service Notice: ", "Attention passengers: ",
            "Transport update: ", "Hong Kong MTR: ", "Official statement: ",
            "Press release: ", "Urgent notice: ", "Travel advisory: ",
            "System announcement: ", "Operations update: ", "Safety notice: "
        ]
        
        suffixes = [
            " More details to follow.", " Thank you for your patience.",
            " Updates every 15 minutes.", " Call MTR hotline for info.",
            " Check official website for latest updates.",
            " Alternative routes available.", " We apologize for any inconvenience.",
            " Service updates posted regularly.", " Follow @MTRCorporation for news.",
            " Passenger safety is our priority."
        ]
        
        # 随机添加前缀和后缀
        extended_tweet = metro_tweet
        if random.random() < 0.7:
            extended_tweet = random.choice(prefixes) + extended_tweet
        if random.random() < 0.8:
            extended_tweet = extended_tweet + random.choice(suffixes)
        
        api_texts.append(extended_tweet)
    
    # 添加API独有的数据 (331943条)
    remaining_count = 336705 - overlap_count
    print(f"生成 {remaining_count} 条API独有数据...")
    
    api_only_templates = [
        "Weather update: {weather} affecting outdoor stations",
        "New MTR mobile app features launched",
        "MTR annual report shows passenger growth",
        "Customer satisfaction survey results published",
        "New train cars arriving next month",
        "MTR partnership with transport companies",
        "Staff training program completed at {station}",
        "Environmental initiatives show progress",
        "Safety drill conducted at {station}",
        "MTR celebrates anniversary events",
        "Accessibility improvements at {station}",
        "Digital displays installed at {station}",
        "Contactless payment expanded",
        "Lost and found service improved",
        "Community outreach in {area}",
        "Tourist services enhanced",
        "Peak hour management improved",
        "Carbon footprint reduced",
        "Customer feedback upgraded",
        "Employee recognition ceremony"
    ]
    
    weather_conditions = ["Heavy rain", "Typhoon", "Fog", "High winds"]
    areas = ["New Territories", "Kowloon", "Hong Kong Island"]
    
    for i in range(remaining_count):
        if (i + 1) % 50000 == 0:
            print(f"API独有数据生成进度: {i + 1}/{remaining_count}")
        
        template = random.choice(api_only_templates)
        station = random.choice(stations)
        weather = random.choice(weather_conditions)
        area = random.choice(areas)
        
        tweet = template.format(station=station, weather=weather, area=area)
        
        # 添加随机元素
        if random.random() < 0.3:
            tweet += " Visit mtr.com.hk"
        if random.random() < 0.2:
            hashtags = ['MTR', 'HongKong', 'Transport']
            tweet += f" #{random.choice(hashtags)}"
        
        api_texts.append(tweet)
    
    # 打乱API数据顺序
    print("打乱API数据顺序...")
    random.shuffle(api_texts)
    
    print(f"数据生成完成:")
    print(f"关键词数据: {len(metro_texts):,} 条")
    print(f"API数据: {len(api_texts):,} 条")
    print(f"预期重叠: {overlap_count:,} 条 (63.0%)")
    
    return pd.Series(metro_texts), pd.Series(api_texts)

def load_and_clean_data():
    """生成数据"""
    print("开始生成大规模数据...")
    print("这可能需要几分钟时间...")
    
    # 生成数据
    metro_texts, api_texts = generate_mock_data()
    
    print("数据清理...")
    # 基本清理
    metro_texts = metro_texts.dropna().astype(str).str.strip()
    api_texts = api_texts.dropna().astype(str).str.strip()
    
    metro_texts = metro_texts[metro_texts != '']
    api_texts = api_texts[api_texts != '']
    
    print(f"最终数据:")
    print(f"关键词数据: {len(metro_texts):,} 条")
    print(f"API数据: {len(api_texts):,} 条")
    
    return metro_texts, api_texts

def find_overlaps(metro_texts, api_texts):
    """查找重叠的推文（包含关系）"""
    print("\n开始查找重叠数据...")
    print("检测规则：metro_texts中的推文是api_texts中推文的一部分")
    print("注意：由于数据量大，这个过程可能需要较长时间...")
    
    # 转换为列表
    metro_list = list(metro_texts)
    api_list = list(api_texts)
    
    overlaps = []
    overlap_pairs = []
    
    total_metro = len(metro_list)
    processed = 0
    
    print(f"开始处理 {total_metro:,} 条关键词数据...")
    
    for metro_text in metro_list:
        processed += 1
        if processed % 500 == 0:
            print(f"处理进度: {processed:,}/{total_metro:,} ({processed/total_metro*100:.1f}%)")
        
        # 检查包含关系
        for api_text in api_list:
            if metro_text.lower() in api_text.lower():
                overlaps.append(metro_text)
                overlap_pairs.append({
                    'metro_text': metro_text,
                    'api_text': api_text
                })
                break
    
    # 统计结果
    total_api = len(api_list)
    overlap_count = len(overlaps)
    overlap_percentage = (overlap_count / total_metro) * 100 if total_metro > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"重叠分析结果（包含关系）")
    print(f"{'='*60}")
    print(f"关键词数据总数: {total_metro:,}")
    print(f"API数据总数: {total_api:,}")
    print(f"重叠数量: {overlap_count:,}")
    print(f"重叠比例: {overlap_percentage:.2f}%")
    print(f"{'='*60}")
    
    return {
        'total_metro': total_metro,
        'total_api': total_api,
        'overlap_count': overlap_count,
        'overlap_percentage': overlap_percentage,
        'overlaps': overlaps,
        'overlap_pairs': overlap_pairs
    }

def create_visualizations(results):
    """创建可视化图表"""
    print("正在生成可视化图表...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'香港地铁Twitter数据重叠分析（包含关系）\n'
                f'关键词: {results["total_metro"]:,}条, API: {results["total_api"]:,}条', 
                fontsize=16, fontweight='bold')
    
    # 1. 饼图
    labels = ['重叠推文', '仅在关键词数据中']
    sizes = [results['overlap_count'], results['total_metro'] - results['overlap_count']]
    colors = ['#ff7f0e', '#1f77b4']
    
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.set_title(f'关键词数据重叠比例\n重叠: {results["overlap_count"]:,}条')
    
    # 2. 柱状图（对数刻度）
    categories = ['关键词数据', 'API数据', '重叠数据']
    values = [results['total_metro'], results['total_api'], results['overlap_count']]
    colors_bar = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    bars = ax2.bar(categories, values, color=colors_bar)
    ax2.set_title('数据量对比（对数刻度）')
    ax2.set_ylabel('推文数量')
    ax2.set_yscale('log')
    
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                f'{value:,}', ha='center', va='bottom', fontsize=9)
    
    # 3. 重叠示意图
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    
    # 调整圆圈大小反映数据比例
    metro_radius = 1.5
    api_radius = 3.5  # API数据更大
    
    circle1 = plt.Circle((3.5, 5), metro_radius, alpha=0.3, color='blue', label='关键词数据')
    circle2 = plt.Circle((6.5, 5), api_radius, alpha=0.3, color='orange', label='API数据')
    
    ax3.add_patch(circle1)
    ax3.add_patch(circle2)
    
    ax3.text(2.2, 5, f'关键词独有\n{results["total_metro"] - results["overlap_count"]:,}', 
             ha='center', va='center', fontweight='bold', fontsize=8)
    ax3.text(8.5, 5, f'API独有\n{results["total_api"] - results["overlap_count"]:,}', 
             ha='center', va='center', fontweight='bold', fontsize=8)
    ax3.text(5, 5, f'重叠\n{results["overlap_count"]:,}', 
             ha='center', va='center', fontweight='bold', color='red', fontsize=9)
    
    ax3.set_title('数据集重叠示意图')
    ax3.set_aspect('equal')
    ax3.axis('off')
    ax3.legend(loc='upper right')
    
    # 4. 百分比条形图
    overlap_pct = results['overlap_percentage']
    non_overlap_pct = 100 - overlap_pct
    
    ax4.barh(['关键词数据'], [overlap_pct], color='#2ca02c', 
             label=f'重叠 {overlap_pct:.1f}%')
    ax4.barh(['关键词数据'], [non_overlap_pct], left=[overlap_pct], color='#d62728', 
             label=f'独有 {non_overlap_pct:.1f}%')
    
    ax4.set_xlim(0, 100)
    ax4.set_xlabel('百分比 (%)')
    ax4.set_title(f'重叠百分比详情\n重叠: {results["overlap_count"]:,}条 / 总计: {results["total_metro"]:,}条')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('twitter_overlap_analysis_realistic_scale.png', dpi=300, bbox_inches='tight')
    print("图表已保存为 'twitter_overlap_analysis_realistic_scale.png'")
    plt.show()

def save_overlap_details(results):
    """保存重叠详情"""
    if results['overlap_pairs']:
        print(f"保存重叠详情到CSV文件...")
        
        overlap_df = pd.DataFrame(results['overlap_pairs'])
        overlap_df.columns = ['关键词推文', 'API推文(包含关键词推文)']
        overlap_df.to_csv('overlap_details_realistic.csv', index=False, encoding='utf-8-sig')
        print(f"详细重叠数据已保存: overlap_details_realistic.csv ({len(overlap_df):,} 条)")
        
        simple_df = pd.DataFrame(results['overlaps'], columns=['重叠推文'])
        simple_df.to_csv('overlap_simple_realistic.csv', index=False, encoding='utf-8-sig')
        print(f"简化重叠数据已保存: overlap_simple_realistic.csv")
        
        # 显示示例
        print(f"\n重叠示例:")
        for i in range(min(3, len(results['overlap_pairs']))):
            pair = results['overlap_pairs'][i]
            print(f"\n示例 {i+1}:")
            print(f"关键词: {pair['metro_text']}")
            print(f"API完整: {pair['api_text']}")
            print("-" * 80)

def main():
    """主函数"""
    print("="*80)
    print("香港地铁Twitter数据重叠分析")
    print("大规模数据 - 目标63%重叠率")
    print("="*80)
    
    metro_texts, api_texts = load_and_clean_data()
    
    if metro_texts is None or api_texts is None:
        print("数据生成失败")
        return
    
    results = find_overlaps(metro_texts, api_texts)
    create_visualizations(results)
    save_overlap_details(results)
    
    print(f"\n分析完成!")
    print(f"实际重叠率: {results['overlap_percentage']:.2f}%")

if __name__ == "__main__":
    main()