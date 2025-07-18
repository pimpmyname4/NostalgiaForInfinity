import re
import sys
from pathlib import Path

BOX_CHARS = "┌┐└┘├┤┬┴┼═╞╡╤╧╪╫╬─━┏┓┗┛╺╸╹╻╼╽╀╁╂╃╄╅╆╇╈╉╊╋"

SECTION_HEADERS = [
  "BACKTESTING REPORT",
  "LEFT OPEN TRADES REPORT",
  "ENTER TAG STATS",
  "EXIT REASON STATS",
  "MIXED TAG STATS",
  "DAY BREAKDOWN",
  "SUMMARY METRICS",
  "STRATEGY SUMMARY",
]


def clean_line(line):
  # Remove box drawing characters, keep pipes
  for ch in BOX_CHARS:
    line = line.replace(ch, "")
  line = re.sub(r" +\|", "|", line)
  line = re.sub(r"\| +", "|", line)
  return line.strip()


def is_table_row(line):
  return line.count("|") >= 2 and not line.strip().startswith("##")


def format_file(file_path: Path):
  output_lines = []
  last_was_table = False

  with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

  for line in lines:
    stripped = clean_line(line)

    # Convert section headers to markdown
    if stripped in SECTION_HEADERS:
      output_lines.append(f"\n## {stripped}\n")
      last_was_table = False
      continue

    # Handle table formatting
    if is_table_row(stripped):
      if not last_was_table:
        # Insert alignment row under header
        cols = stripped.count("|") - 1
        output_lines.append(stripped)
        output_lines.append("|" + "|".join(["---"] * cols) + "|")
      else:
        output_lines.append(stripped)
      last_was_table = True
    else:
      output_lines.append(stripped)
      last_was_table = False

  with open(file_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python format_backtest_md.py <file1> [file2 ...]")
    sys.exit(1)

  for arg in sys.argv[1:]:
    path = Path(arg)
    if path.exists() and path.suffix == ".txt":
      format_file(path)
      print(f"Formatted: {path}")
    else:
      print(f"Skipped: {path}")
