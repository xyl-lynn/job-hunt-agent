import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

RESUME_PATH = "resume.pdf"


def read_resume() -> str:
    """
    读取简历 PDF，返回纯文本内容
    """
    if not os.path.exists(RESUME_PATH):
        raise FileNotFoundError(f"简历文件未找到，请把你的简历放在项目根目录，命名为 resume.pdf")

    reader = PdfReader(RESUME_PATH)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    if not text.strip():
        raise ValueError("简历内容为空，PDF 可能是扫描版图片，无法直接读取文字")

    return text.strip()


def get_resume_summary(resume_text: str, jd_info: dict) -> str:
    """
    根据 JD 要求，从简历中提取最相关的内容
    返回填写企业官网简历表单的建议
    """
    import os
    from http import HTTPStatus
    from dashscope import Generation

    requirements = "\n".join(jd_info.get("requirements", []))
    responsibilities = "\n".join(jd_info.get("responsibilities", []))

    prompt = f"""
你是一个求职助手。我要应聘以下职位：

公司：{jd_info.get('company', '未知')}
职位：{jd_info.get('position', '未知')}

职位要求：
{requirements}

主要职责：
{responsibilities}

我的简历内容：
{resume_text}

请根据这个职位，给我提供填写企业官网简历表单的具体建议，包括：

1. 【个人简介/自我介绍】应该怎么写（针对这个职位定制，50-80字）
2. 【兴趣爱好】填写哪些最加分
3. 【特长/技能】重点突出哪些
4. 【项目经历】哪些项目最相关，每个项目的描述建议怎么写
5. 【实习/工作经历】哪些经历最相关，描述重点放在哪里
6. 【匹配度分析】我的背景和这个职位的匹配度（高/中/低），以及差距在哪里

请用清晰的格式输出，每个部分给出具体的填写内容建议，而不是泛泛而谈。
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