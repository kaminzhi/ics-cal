import argparse
import json

from .query import fetch_events_by_keyword


def main():
    parser = argparse.ArgumentParser(description="依年份與關鍵字查詢雲科大行事曆事件")
    parser.add_argument("--year", type=int, required=True, help="要查詢的年份，例如 2025")
    parser.add_argument("--query", type=str, required=True, help="事件說明的關鍵字，例如 暑假、開學、期末考")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式輸出結果")
    args = parser.parse_args()

    matches = fetch_events_by_keyword(args.year, args.query)
    if args.json:
        output = [
            {"date": date_str, "description": desc}
            for date_str, desc in matches
        ]
        print(json.dumps(output, ensure_ascii=False))
    else:
        if not matches:
            print("未找到符合的事件。")
            return
        for date_str, desc in matches:
            print(f"{date_str} - {desc}")


if __name__ == "__main__":
    main()


