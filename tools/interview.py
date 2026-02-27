import os
from http import HTTPStatus
from dashscope import Generation
from dotenv import load_dotenv

load_dotenv()


def generate_interview_prep(resume_text: str, jd_info: dict) -> str:
    """
    根据简历和 JD 生成面试准备问题
    """

    requirements = "\n".join(jd_info.get("requirements", []))
    responsibilities = "\n".join(jd_info.get("responsibilities", []))

    prompt = f"""
你是一个资深面试官和求职顾问。根据以下职位信息和候选人简历，生成一份全面的面试准备清单。

目标职位：
公司：{jd_info.get('company', '未知')}
职位：{jd_info.get('position', '未知')}

职位要求：
{requirements}

主要职责：
{responsibilities}

候选人简历：
{resume_text}

请生成以下几个维度的面试准备内容：

## 一、技术问题（8-10题）
针对该职位的核心技术栈，列出高频面试题，每题附上简要回答思路。

## 二、项目/经历问题（4-5题）
基于候选人简历中的项目和经历，预测面试官会追问的问题，附上回答建议。

## 三、综合能力问题（4-5题）
包括问题解决、团队协作、职业规划等，附上回答框架（如STAR法则）。

## 四、反问环节（3-4题）
候选人可以问面试官的好问题，展示主动性和对职位的深度思考。

## 五、注意事项
针对该候选人背景和该职位，列出2-3个需要特别注意或提前准备的点。

请用清晰的Markdown格式输出，问题要具体、有针对性，不要泛泛而谈。
"""

    response = Generation.call(
        model="qwen-turbo",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        messages=[{"role": "user", "content": prompt}],
        result_format="message"
    )

    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message.content
    else:
        raise Exception(f"API调用失败: {response.message}")