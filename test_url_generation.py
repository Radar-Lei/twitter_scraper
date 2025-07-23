#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试搜索URL生成功能
验证修改后的build_search_url方法是否正确工作
"""

from scweet import Scweet

def test_url_generation():
    print("=== 测试搜索URL生成功能 ===\n")
    
    # 初始化Scweet（不需要实际启动浏览器）
    scweet = Scweet(headless=True)
    
    # 测试关键词
    keywords = ['지하철', '서울지하철', 'seoul metro']
    
    print("1. 测试仅关键词搜索（无时间和地理限制）：")
    urls = scweet.build_search_url(
        since=None,
        until=None,
        words=keywords,
        geocode=None
    )
    print(f"生成的URL: {urls[0]}")
    print("应该包含: (지하철 OR 서울지하철 OR seoul metro)")
    print("不应该包含: until:, since:, geocode:")
    print()
    
    print("2. 测试带时间限制的搜索：")
    urls = scweet.build_search_url(
        since="2024-01-01",
        until="2024-01-02",
        words=keywords,
        geocode=None,
        n=1  # 只生成一个URL用于测试
    )
    print(f"生成的URL: {urls[0]}")
    print("应该包含: until:2024-01-02, since:2024-01-01")
    print()
    
    print("3. 测试带地理限制的搜索：")
    urls = scweet.build_search_url(
        since=None,
        until=None,
        words=keywords,
        geocode="37.5665,126.9780,25km"
    )
    print(f"生成的URL: {urls[0]}")
    print("应该包含: geocode:37.5665,126.9780,25km")
    print()
    
    print("4. 测试完整搜索（时间+地理+关键词）：")
    urls = scweet.build_search_url(
        since="2024-12-30",
        until="2024-12-30",
        words=keywords,
        geocode="37.5665,126.9780,25km",
        n=1
    )
    print(f"生成的URL: {urls[0]}")
    print("应该包含: (지하철 OR 서울지하철 OR seoul metro) until:2024-12-30 since:2024-12-30 geocode:37.5665,126.9780,25km")
    print()
    
    print("5. 测试空参数处理：")
    urls = scweet.build_search_url(
        since="",
        until="",
        words=keywords,
        geocode=""
    )
    print(f"生成的URL: {urls[0]}")
    print("应该是仅关键词搜索")
    print()

if __name__ == '__main__':
    test_url_generation() 