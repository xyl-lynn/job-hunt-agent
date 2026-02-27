import os
from http import HTTPStatus
from dashscope import Generation
from dotenv import load_dotenv

load_dotenv()


def parse_jd(jd_text: str) -> dict:
    """
    输入：JD 原始文本
    输出：结构化的 JD 信息
    """

    prompt = f"""
你是一个求职助手，请从以下职位描述中提取关键信息，用JSON格式返回。

职位描述：
{jd_text}

请提取并返回以下字段（JSON格式，不要有多余文字）：
{{
    "company": "公司名称",
    "position": "职位名称",
    "requirements": ["核心技能要求1", "核心技能要求2", ...],
    "responsibilities": ["主要职责1", "主要职责2", ...],
    "preferred": ["加分项1", "加分项2", ...],
    "summary": "一句话总结这个职位"
}}
"""

    response = Generation.call(
        model="qwen-turbo",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        messages=[{"role": "user", "content": prompt}],
        result_format="message"
    )

    if response.status_code == HTTPStatus.OK:
        content = response.output.choices[0].message.content
        # 清理 markdown 代码块标记
        content = content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()

        import json
        return json.loads(content)
    else:
        raise Exception(f"API调用失败: {response.message}")