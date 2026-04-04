from pipeline.storage import get_source_stats

def source_success_report():
    rows = get_source_stats()
    print(f"\n{'Source':<25} {'Total':>6} {'Success':>8} {'Paywalled':>10} {'Failed':>7} {'Rate':>6}")
    print("-" * 65)
    for row in rows:
        print(f"{row[0]:<25} {row[1]:>6} {row[2]:>8} {row[3]:>10} {row[4]:>7} {row[5]:>5}%")

if __name__ == "__main__":
    source_success_report()