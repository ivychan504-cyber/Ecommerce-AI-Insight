import pandas as pd
import json
import time
import os
from openai import OpenAI

# ==========================================
# 1. 权限配置 (职场博弈点：绝不硬编码敏感信息)
# ==========================================
# 在本地运行前，请填入你的 Key。提交到 GitHub 前，请将其删除。
DEEPSEEK_API_KEY = "需要输入自己的 API Key" 

client = OpenAI(
    api_key=DEEPSEEK_API_KEY, 
    base_url="https://api.deepseek.com"
)

def run_ecommerce_analysis():
    """
    电商评论自动化分析引擎
    功能：从原始 Excel 中提取核心痛点，转化为结构化 JSON 数据
    """
    try:
        # 2. 读取情报源 (Excel)
        # 确保文件名为 reviews.xlsx 且包含 '评论文本' 和 '星级' 列
        df = pd.read_excel("reviews.xlsx")
        results = []

        print(f"🚀 电商 AI 特工启动，准备分析 {len(df)} 条核心情报...")

        for index, row in df.iterrows():
            # 3. 设计硬核 Prompt (PM 的核心功力)
            prompt = f"""
            你是一个电商评论分析助手。请分析以下评论，提取产品缺陷信息。
            
            评论内容：{row["评论文本"]}
            星级：{row["星级"]}

            严格只返回如下 JSON 格式，不要任何解释或多余文字：
            {{
              "有无缺陷": "有" 或 "无",
              "缺陷描述": "具体描述，没有则填null",
              "严重程度": "高/中/低，没有则填null"
            }}
            """
            
            try:
                # 4. 调用 DeepSeek 模型进行推理
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个只输出JSON的分析专家"},
                        {"role": "user", "content": prompt},
                    ],
                    response_format={'type': 'json_object'} # 强制 JSON 模式，确保数据整洁
                )
                
                raw_content = response.choices[0].message.content.strip()
                data = json.loads(raw_content)
                
                # 5. 整合数据资产
                results.append({
                    "评论文本": row["评论文本"],
                    "星级": row["星级"],
                    "有无缺陷": data.get("有无缺陷", "未知"),
                    "缺陷描述": data.get("缺陷描述", "null"),
                    "严重程度": data.get("严重程度", "null"),
                })
                
                print(f"✅ 第 {index+1} 条处理完成")

                # 为避免触发 API 频率限制，设置 1 秒缓冲
                time.sleep(1) 

            except Exception as e:
                print(f"❌ 第 {index+1} 条处理异常: {e}")
                continue # 确保单条错误不中断整个自动化链路

        # 6. 资产导出
        df_result = pd.DataFrame(results)
        df_result.to_excel("reviews_analyzed_deepseek.xlsx", index=False)
        print("\n🏆 全部完成！商业洞察已存为：reviews_analyzed_deepseek.xlsx")

    except FileNotFoundError:
        print("📁 错误：未找到 reviews.xlsx。请确保文件放在脚本同一目录下。")
    except Exception as e:
        print(f"⚠️ 系统运行错误: {e}")

if __name__ == "__main__":
    run_ecommerce_analysis()
