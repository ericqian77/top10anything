import os
import asyncio
import sys
from pathlib import Path

# 设置 PYTHONPATH 以包含 src 目录
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
os.environ["PYTHONPATH"] = src_path

from datetime import datetime
from pipeline.tableau import TableauDataConverter
from pipeline.hyper import HyperFileManager
from agent.ranking_agent import generate_ranking

async def create_and_store_ranking(query: str):
    """Generate ranking using agent and store it in hyper format"""
    try:
        # 使用 agent 生成排名数据
        print(f"\n=== Generating ranking for: {query} ===\n")
        ranking_result = await generate_ranking(query)
        
        print(f"Generated ranking for topic: {ranking_result.topic}")
        print(f"Number of items: {len(ranking_result.items)}")
        
        # 转换为 Tableau 格式
        tableau_data = TableauDataConverter.convert(ranking_result)
        
        # 设置输出目录
        output_dir = Path("data/hyper")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 Hyper 文件管理器
        manager = HyperFileManager(output_dir)
        
        # 生成文件名（使用时间戳和主题）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_topic = "".join(c for c in ranking_result.topic if c.isalnum() or c in (' ', '-', '_')).strip()
        file_name = f"{sanitized_topic}_{timestamp}"
        
        # 创建 Hyper 文件
        hyper_path = manager.create_hyper_file(file_name, tableau_data)
        print(f"\nCreated Hyper file: {hyper_path}")
        
        # 打印排名摘要
        print("\nRanking Summary:")
        for item in ranking_result.items:
            print(f"\n{item.rank}. {item.name}")
            print(f"Score: {item.score}")
            print("Advantages:")
            for advantage in item.advantages:
                print(f"  - {advantage}")
            if item.metrics:
                print(f"Metrics: {item.metrics}")
        
    except Exception as e:
        print(f"Error processing ranking: {str(e)}")
        raise

async def main():
    # 测试查询
    queries = [
        "Best public high schools in Ottawa based on Fraser rankings",
        # 可以添加更多查询
    ]
    
    for query in queries:
        await create_and_store_ranking(query)

if __name__ == "__main__":
    asyncio.run(main()) 