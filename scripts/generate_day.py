# scripts/generate_day.py
from __future__ import annotations

import random
import re
from pathlib import Path

CONTENT_DIR = Path("content")

TOPICS = [
    {
        "tag": "일상",
        "items": [
            ("今日は時間があります。", "쿄오와 지칸가 아리마스", "きょうは じかんが あります", "오늘은 시간이 있어요."),
            ("今ちょっと忙しいです。", "이마 촛토 이소가시이데스", "いま ちょっと いそがしいです", "지금 좀 바빠요."),
            ("無理しないでください。", "무리 시나이데 쿠다사이", "むり しないで ください", "무리하지 마세요."),
        ],
    },
    {
        "tag": "쇼핑",
        "items": [
            ("これ、いくらですか？", "코레 이쿠라 데스까", "これ いくらですか", "이거 얼마예요?"),
            ("試着してもいいですか？", "시차쿠 시테모 이이데스까", "しちゃく しても いいですか", "입어봐도 될까요?"),
            ("これの別の色はありますか？", "코레노 베츠노 이로와 아리마스까", "これの べつの いろは ありますか", "이거 다른 색도 있나요?"),
        ],
    },
    {
        "tag": "식당",
        "items": [
            ("おすすめは何ですか？", "오스스메와 난데스까", "おすすめは なんですか", "추천은 뭐예요?"),
            ("辛くしないでください。", "카라쿠 시나이데 쿠다사이", "からく しないで ください", "맵지 않게 해주세요."),
            ("お会計お願いします。", "오카이케이 오네가이시마스", "おかいけい おねがいします", "계산 부탁해요."),
        ],
    },
    {
        "tag": "이동/여행",
        "items": [
            ("ここはどこですか？", "코코와 도코데스까", "ここは どこですか", "여기는 어디예요?"),
            ("駅までどのくらいですか？", "에키마데 도노쿠라이데스까", "えきまで どのくらいですか", "역까지 얼마나 걸려요?"),
            ("写真を撮ってもらえますか？", "샤신오 톳테 모라에마스까", "しゃしんを とって もらえますか", "사진 좀 찍어주실 수 있나요?"),
        ],
    },
    {
        "tag": "감정/관계",
        "items": [
            ("助かりました。", "타스카리마시타", "たすかりました", "도움 됐어요/살았어요."),
            ("それ、いいですね。", "소레 이이데스네", "それ いいですね", "그거 좋네요."),
            ("また連絡します。", "마타 렌라쿠시마스", "また れんらくします", "다시 연락할게요."),
        ],
    },
]

def next_day_number() -> int:
    if not CONTENT_DIR.exists():
        CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    nums = []
    for p in CONTENT_DIR.glob("day-*.md"):
        m = re.match(r"day-(\d+)\.md$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 1

def pick_five() -> list[tuple[str, str, str, str]]:
    pool = []
    for t in TOPICS:
        pool.extend(t["items"])
    # 중복 방지
    random.shuffle(pool)
    picked = pool[:5]
    return picked

def write_markdown(day_num: int, items: list[tuple[str, str, str, str]]) -> Path:
    filename = f"day-{day_num:03d}.md"
    path = CONTENT_DIR / filename

    lines = []
    lines.append(f"# Day {day_num:03d} - 하루 5문장 일본어\n")
    for i, (jp, kr_read, hira, 뜻) in enumerate(items, start=1):
        lines.append(f"## {i}\n")
        lines.append(f"- JP: {jp}\n")
        lines.append(f"- 읽는법(한글): {kr_read}\n")
        lines.append(f"- 읽는법(히라가나): {hira}\n")
        lines.append(f"- 뜻: {뜻}\n")

    path.write_text("".join(lines), encoding="utf-8")
    return path

def main():
    random.seed()  # 매일 조금씩 바뀌게
    n = next_day_number()
    items = pick_five()
    created = write_markdown(n, items)
    print(f"Created: {created}")

if __name__ == "__main__":
    main()
