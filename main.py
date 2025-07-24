from read_gmail import get_latest_school_email
from langgraph_flow import run_langgraph_with_email

def main():
    subject, content = get_latest_school_email("school@example.com")
    if content:
        print(f"📩 New email: {subject}")
        run_langgraph_with_email(content)

if __name__ == "__main__":
    main()
