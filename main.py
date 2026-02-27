from tools.jd_parser import parse_jd
from tools.resume import read_resume, get_resume_summary
from tools.letter import generate_cover_letter
from memory.store import save_application, check_followups, list_all


def run_agent(jd_text: str):
    print("\n" + "="*50)
    print("🦞 Job Hunt Agent 启动")
    print("="*50)

    # Step 1: 解析 JD
    print("\n📋 Step 1: 解析职位描述...")
    jd_info = parse_jd(jd_text)
    print(f"  公司：{jd_info.get('company')}")
    print(f"  职位：{jd_info.get('position')}")
    print(f"  摘要：{jd_info.get('summary')}")

    # Step 2: 读取简历 + 匹配分析
    print("\n📄 Step 2: 读取简历，分析匹配度...")
    resume_text = read_resume()
    resume_advice = get_resume_summary(resume_text, jd_info)
    print("\n【简历表单填写建议】")
    print(resume_advice)

    # Step 3: 生成 Cover Letter
    print("\n✉️  Step 3: 生成求职信...")
    cover_letter = generate_cover_letter(resume_text, jd_info)
    print("\n【定制化求职信】")
    print(cover_letter)

    # Step 4: 记录到 tracking
    print("\n💾 Step 4: 记录投递信息...")
    record = save_application(
        company=jd_info.get("company", "未知"),
        position=jd_info.get("position", "未知"),
        jd_summary=jd_info.get("summary", "")
    )
    print(f"  已记录，ID：{record['id']}，投递日期：{record['applied_date']}")

    print("\n" + "="*50)
    print("✅ 完成！祝面试顺利！")
    print("="*50 + "\n")


def check_followup_reminders():
    """检查需要跟进的职位"""
    print("\n⏰ 检查跟进提醒...")
    need_followup = check_followups()
    if not need_followup:
        print("  暂无需要跟进的职位")
    else:
        print(f"  以下职位超过7天未更新，建议发 follow-up：")
        for app in need_followup:
            print(f"  - [{app['id']}] {app['company']} | {app['position']} | 已过 {app['days_passed']} 天")


def show_all_applications():
    """显示所有投递记录："""
    print("\n📊 所有投递记录：")
    apps = list_all()
    if not apps:
        print("  暂无记录")
    else:
        for app in apps:
            print(f"  [{app['id']}] {app['company']} | {app['position']} | {app['status']} | {app['applied_date']}")


if __name__ == "__main__":
    print("🦞 Job Hunt Agent")
    print("1. 处理新职位")
    print("2. 查看跟进提醒")
    print("3. 查看所有投递记录")

    choice = input("\n请选择（1/2/3）：").strip()

    if choice == "1":
        print("\n请粘贴职位描述（输入完成后按两次回车）：")
        lines = []
        while True:
            line = input()
            if line == "":
                if lines and lines[-1] == "":
                    break
            lines.append(line)
        jd_text = "\n".join(lines[:-1])
        run_agent(jd_text)

    elif choice == "2":
        check_followup_reminders()

    elif choice == "3":
        show_all_applications()

    else:
        print("无效选择")