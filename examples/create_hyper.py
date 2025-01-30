import sys
from pathlib import Path
from datetime import datetime, timezone
from pipeline.tableau import TableauDataConverter, TableauDataRow
from pipeline.hyper import HyperFileManager
from models.ranking import RankingResult, RankingItem

def create_realistic_ranking() -> RankingResult:
    """Create realistic programming language ranking data"""
    languages = [
        {
            "name": "Python",
            "rank": 1,
            "score": 9.5,
            "advantages": [
                "Excellent for data science and ML",
                "Large ecosystem of libraries",
                "Easy to learn and read"
            ],
            "metrics": {
                "github_stars": 9.8,
                "job_demand": 9.5,
                "community_size": 9.2
            },
            "description": "Python continues to dominate as a versatile language, particularly strong in data science, "
                         "machine learning, and web development. Its simple syntax and extensive library ecosystem make "
                         "it an excellent choice for both beginners and experts."
        },
        {
            "name": "JavaScript",
            "rank": 2,
            "score": 9.2,
            "advantages": [
                "Universal web platform support",
                "Rich frontend frameworks",
                "Full-stack capabilities with Node.js"
            ],
            "metrics": {
                "github_stars": 9.5,
                "job_demand": 9.8,
                "community_size": 9.0
            },
            "description": "JavaScript remains essential for web development, with powerful frameworks like React and Vue.js. "
                         "Node.js has established it as a viable server-side language, making it a full-stack solution."
        },
        {
            "name": "Java",
            "rank": 3,
            "score": 8.8,
            "advantages": [
                "Enterprise-grade stability",
                "Strong typing and performance",
                "Extensive enterprise adoption"
            ],
            "metrics": {
                "github_stars": 8.5,
                "job_demand": 9.0,
                "community_size": 8.8
            },
            "description": "Java maintains its position as a top enterprise language, known for reliability and performance. "
                         "Its strong typing and JVM make it ideal for large-scale applications and Android development."
        },
        {
            "name": "TypeScript",
            "rank": 4,
            "score": 8.6,
            "advantages": [
                "Type safety for JavaScript",
                "Enhanced IDE support",
                "Growing enterprise adoption"
            ],
            "metrics": {
                "github_stars": 9.0,
                "job_demand": 8.5,
                "community_size": 8.2
            },
            "description": "TypeScript's static typing has revolutionized JavaScript development, providing better tooling "
                         "and catching errors early. It's become the standard for large-scale JavaScript projects."
        },
        {
            "name": "Go",
            "rank": 5,
            "score": 8.4,
            "advantages": [
                "Excellent for microservices",
                "Built-in concurrency",
                "Fast compilation"
            ],
            "metrics": {
                "github_stars": 8.8,
                "job_demand": 8.0,
                "community_size": 7.8
            },
            "description": "Go excels in building microservices and cloud infrastructure. Its simplicity, strong "
                         "performance, and excellent concurrency support make it popular for modern backend systems."
        },
        {
            "name": "Rust",
            "rank": 6,
            "score": 8.2,
            "advantages": [
                "Memory safety without GC",
                "High performance",
                "Growing system programming adoption"
            ],
            "metrics": {
                "github_stars": 9.2,
                "job_demand": 7.5,
                "community_size": 7.2
            },
            "description": "Rust offers unparalleled memory safety without garbage collection, making it ideal for "
                         "systems programming. It's gaining traction in blockchain and WebAssembly development."
        },
        {
            "name": "C#",
            "rank": 7,
            "score": 8.0,
            "advantages": [
                "Strong .NET ecosystem",
                "Game development with Unity",
                "Modern language features"
            ],
            "metrics": {
                "github_stars": 8.0,
                "job_demand": 8.5,
                "community_size": 8.0
            },
            "description": "C# continues to evolve with modern features while maintaining its strong position in enterprise "
                         "development and game development through Unity. The .NET ecosystem provides excellent tools."
        },
        {
            "name": "PHP",
            "rank": 8,
            "score": 7.8,
            "advantages": [
                "Dominant in web hosting",
                "Easy deployment",
                "Improved modern syntax"
            ],
            "metrics": {
                "github_stars": 7.5,
                "job_demand": 8.0,
                "community_size": 8.5
            },
            "description": "PHP powers a large portion of the web, with modern frameworks like Laravel making it more "
                         "appealing. Recent versions have significantly improved its syntax and performance."
        },
        {
            "name": "Swift",
            "rank": 9,
            "score": 7.6,
            "advantages": [
                "Native iOS development",
                "Strong safety features",
                "Growing server-side usage"
            ],
            "metrics": {
                "github_stars": 8.2,
                "job_demand": 7.8,
                "community_size": 7.0
            },
            "description": "Swift is the primary language for iOS development, known for its safety features and "
                         "performance. It's expanding beyond mobile into server-side development."
        },
        {
            "name": "Kotlin",
            "rank": 10,
            "score": 7.4,
            "advantages": [
                "Modern Java alternative",
                "Android development",
                "Excellent Java interop"
            ],
            "metrics": {
                "github_stars": 8.0,
                "job_demand": 7.5,
                "community_size": 7.0
            },
            "description": "Kotlin has become the preferred language for Android development, offering modern features "
                         "while maintaining excellent Java interoperability. It's also growing in server-side usage."
        }
    ]

    return RankingResult(
        topic="Best Programming Languages 2024",
        generated_at=datetime.now(timezone.utc),
        items=[
            RankingItem(
                rank=lang["rank"],
                name=lang["name"],
                description=lang["description"],
                advantages=lang["advantages"],
                metrics=lang["metrics"],
                score=lang["score"]
            )
            for lang in languages
        ],
        sources=[
            "https://github.blog/2024-01-20-programming-language-trends",
            "https://www.stackoverflow.com/developer-survey-2024",
            "https://www.tiobe.com/tiobe-index/",
            "https://insights.dice.com/tech-jobs-report-2024"
        ],
        methodology="""Our comprehensive analysis of programming languages is based on multiple quantitative and qualitative factors:

1. Developer Community Activity
   - GitHub repository stars and contributions
   - Stack Overflow questions and engagement
   - Open source project adoption

2. Job Market Demand
   - Current job postings across major platforms
   - Salary trends and growth
   - Enterprise adoption rates

3. Technical Capabilities
   - Language feature set and modern programming support
   - Performance characteristics
   - Security considerations
   - Ecosystem maturity

4. Learning Curve and Accessibility
   - Documentation quality
   - Learning resources availability
   - Community support for newcomers

5. Industry Adoption Patterns
   - Usage in production environments
   - Major company endorsements
   - Framework and tool availability

The final rankings combine these metrics with expert analysis of industry trends and future growth potential.""",
        year=2024
    )

def main():
    # 设置输出目录
    output_dir = Path("data/hyper")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建真实的排名数据
    ranking = create_realistic_ranking()
    
    # 转换为 Tableau 数据格式
    tableau_data = TableauDataConverter.convert(ranking)
    
    # 创建 Hyper 文件管理器
    manager = HyperFileManager(output_dir)
    
    # 生成文件名（使用时间戳避免覆盖）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"rankings_{timestamp}"
    
    # 创建 Hyper 文件
    hyper_path = manager.create_hyper_file(file_name, tableau_data)
    print(f"Created Hyper file: {hyper_path}")

if __name__ == "__main__":
    main() 