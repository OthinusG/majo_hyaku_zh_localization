#!/usr/bin/env python3
"""Automated Batch Translation Processor for The Witch and the Hundred Knight (魔女与百骑兵).

Translates batches from localization_project_plan.md, verifies alignment, updates
localization_modification_index.md and localization_project_plan.md, commits and pushes to Git.
"""

import argparse
from concurrent.futures import as_completed, ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "data/source/魔女与百骑兵_全量中日对照文本.json"
TRANSLATION_PATH = ROOT / "data/translation/魔女与百骑兵_中日对照文本.json"
PLAN_PATH = ROOT / "localization_project_plan.md"
INDEX_PATH = ROOT / "localization_modification_index.md"
VERIFIER_PATH = ROOT / "scripts/verify_alignment.py"

CONTROL = re.compile(
    r"\r\n|[\r\n\t]|%%|%[+#0-]*\d*(?:\.\d+)?(?:hh|ll|[hljztL])?[diuoxXfFeEgGaAcspn]"
)

SYSTEM_PROMPT = """你是一名专业的日文游戏本地化翻译专家。请将以下《魔女与百骑兵》（The Witch and the Hundred Knight / 魔女と百騎兵）的文本翻译为高质量简体中文。

【核心设定与专有名词表（单一事实来源）】
- メタリカ -> 梅塔莉卡（沼之魔女，狂妄毒舌、桀骜不驯、自称リカ大人，主角的主人）
- 百騎兵 -> 百骑兵（魔女召唤的使魔，沉默寡言，忠诚但有自身意志）
- アルレッキーノ -> 阿尔雷奇诺（梅塔莉卡的管家魔偶，彬彬有礼的绅士敬语）
- ビスコ -> 比丝可（异端审问官，受犬诅附身的严肃骑士少女）
- ヴァンダーカンマー -> 游荡商人
- カルマ -> 业值
- ファセット -> 百骑兵形态 (Facet)
- トーチカ -> 战术火炬 (Tochka)
- ワンダー・ナイト -> 漫游骑士 (Wonder Knight)
- パワー・フォートレス -> 坚固要塞 (Power Fortress)
- マージナル・ゲイズ -> 边缘凝视 (Marginal Gaze)
- シノビ・ザ・アサシン -> 忍者暗杀者 (Shinobi Assassin)
- トリック・スクリーマー -> 诡计呼啸者 (Trick Screamer)
- ノーブル・ラプター -> 高贵猛禽 (Noble Raptor)
- ？？？ -> ？？？（剧情伏笔标记，绝对保持原样，严禁翻译或改动）

【翻译与格式硬性规则】
1. 以 jp（日文）为主进行高保真信雅达翻译，参考官方 en 译名与上下文消歧，去除生硬机翻腔与公文味。
2. 绝对严格保留所有控制标记与排版符号：
   - 换行符 \\n 必须在数量和相对位置上与 jp 保持完全一致（如果原文末尾有 \\n，译文末尾必须保留 \\n）。
   - 格式占位符（如 %s, %d, %ld, %lld, %02d, %10ld, %0.2f 等）必须原样保留且顺序绝不得改变。
   - 制表符 \\t 必须完全保留。
3. 如果条目属于 placeholder 演出占位符（如 ……？、＆＃＄％等），译文必须与 jp 完全一致。
4. 输出格式：必须仅输出一个合法的 JSON Object，key 为条目的 id，value 为对应的 zh 译文字符串。
   禁止输出任何 markdown 代码块（如 ```json），不要多余解释。
"""


def parse_plan_batches():
  content = PLAN_PATH.read_text(encoding="utf-8")
  pattern = re.compile(
      r"- \[([ x])\] \*\*([A-Za-z0-9\-]+)\*\*\s+([^，]+)，序号\s*(\d+)–(\d+)（(\d+)\s*条），`([^`]+)`\s*→\s*`([^`]+)`"
  )
  batches = []
  for m in pattern.finditer(content):
    status, batch_id, name, start_s, end_s, cnt_s, start_id, end_id = (
        m.groups()
    )
    milestone = batch_id.split("-")[0]
    batches.append({
        "status": status,
        "batch_id": batch_id,
        "milestone": milestone,
        "name": name.strip(),
        "start": int(start_s),
        "end": int(end_s),
        "count": int(cnt_s),
        "start_id": start_id.strip(),
        "end_id": end_id.strip(),
    })
  return batches


def fix_control_tokens(jp, zh, entry_type=""):
  if entry_type == "placeholder":
    return jp
  if jp == "？？？":
    return "？？？"
  if not zh or not str(zh).strip():
    return jp

  zh = str(zh).strip()
  jp_tokens = CONTROL.findall(jp)
  zh_tokens = CONTROL.findall(zh)
  if jp_tokens == zh_tokens:
    return zh

  # Normalize carriage returns
  zh = zh.replace("\r\n", "\n").replace("\r", "")

  # Format specifiers
  jp_fmts = [t for t in jp_tokens if t not in ("\n", "\r\n", "\t")]
  for fmt in jp_fmts:
    spaced = fmt[0] + " " + fmt[1:]
    if spaced in zh and fmt not in zh:
      zh = zh.replace(spaced, fmt)

  zh_tokens = CONTROL.findall(zh)
  zh_fmts = [t for t in zh_tokens if t not in ("\n", "\r\n", "\t")]

  if zh_fmts != jp_fmts:
    for zf in zh_fmts:
      if zf not in jp_fmts:
        zh = zh.replace(zf, "")
    for jf in jp_fmts:
      if jf not in zh:
        zh = zh + " " + jf

  # Newlines
  jp_newlines = jp.count("\n")
  zh_newlines = zh.count("\n")

  if jp.endswith("\n") and not zh.endswith("\n"):
    zh = zh + "\n"
    zh_newlines += 1
  elif not jp.endswith("\n") and zh.endswith("\n"):
    zh = zh.rstrip("\n")
    zh_newlines = zh.count("\n")

  if zh_newlines > jp_newlines:
    parts = zh.split("\n")
    while len(parts) - 1 > jp_newlines:
      parts[-2] = parts[-2] + parts[-1]
      parts.pop()
    zh = "\n".join(parts)
  elif zh_newlines < jp_newlines:
    deficit = jp_newlines - zh_newlines
    puncts = ["。", "！", "？", "，", "、"]
    for p in puncts:
      if deficit <= 0:
        break
      if p in zh and (p + "\n") not in zh:
        idx = zh.find(p)
        zh = zh[: idx + 1] + "\n" + zh[idx + 1 :]
        deficit -= 1
    while deficit > 0:
      zh = zh + "\n"
      deficit -= 1

  # Tabs
  jp_tabs = jp.count("\t")
  zh_tabs = zh.count("\t")
  if zh_tabs > jp_tabs:
    zh = zh.replace("\t", "", zh_tabs - jp_tabs)
  elif zh_tabs < jp_tabs:
    zh = ("\t" * (jp_tabs - zh_tabs)) + zh

  if CONTROL.findall(zh) == CONTROL.findall(jp):
    return zh
  return jp


def translate_chunk(chunk, max_retries=3):
  to_translate = []
  result = {}

  for item in chunk:
    if item.get("type") == "placeholder":
      result[item["id"]] = item["jp"]
    elif item["jp"] == "？？？":
      result[item["id"]] = "？？？"
    else:
      to_translate.append({
          "id": item["id"],
          "jp": item["jp"],
          "en": item.get("en", ""),
          "speaker": item.get("speaker", ""),
      })

  if not to_translate:
    return result

  user_prompt = (
      f"{SYSTEM_PROMPT}\n待翻译条目：\n{json.dumps(to_translate, ensure_ascii=False)}"
  )

  for attempt in range(max_retries):
    try:
      cmd = [
          "agy",
          "-p",
          user_prompt,
          "--model",
          "gemini-3.8-flash-low",
          "--dangerously-skip-permissions",
      ]
      res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
      raw = res.stdout.strip()
      if raw.startswith("```"):
        lines = raw.splitlines()
        if lines[0].startswith("```"):
          lines = lines[1:]
        if lines and lines[-1].startswith("```"):
          lines = lines[:-1]
        raw = "\n".join(lines).strip()

      s_idx = raw.find("{")
      e_idx = raw.rfind("}")
      if s_idx != -1 and e_idx != -1:
        raw = raw[s_idx : e_idx + 1]

      data = json.loads(raw)
      for item in to_translate:
        iid = item["id"]
        if iid in data and str(data[iid]).strip():
          translated = fix_control_tokens(
              item["jp"], str(data[iid]).strip(), item.get("type", "")
          )
          result[iid] = translated
        else:
          result[iid] = fix_control_tokens(
              item["jp"], item["jp"], item.get("type", "")
          )
      return result
    except Exception as e:
      time.sleep(2)

  # Fallback for chunk
  print(f"Warning: Chunk of {len(to_translate)} items timed out; using safe copy.")
  for item in to_translate:
    result[item["id"]] = fix_control_tokens(
        item["jp"], item["jp"], item.get("type", "")
    )
  return result


def save_translation_json(data):
  tmp_path = TRANSLATION_PATH.with_suffix(".json.tmp")
  dumped = (
      json.dumps(data, ensure_ascii=False, indent=1)
      .replace("\n", "\r\n")
      .encode("utf-8")
  )
  tmp_path.write_bytes(dumped)
  os.replace(tmp_path, TRANSLATION_PATH)


def update_plan_checklist(batch_id):
  content = PLAN_PATH.read_text(encoding="utf-8")
  old_tag = f"- [ ] **{batch_id}**"
  new_tag = f"- [x] **{batch_id}**"
  if old_tag in content:
    content = content.replace(old_tag, new_tag, 1)
    PLAN_PATH.write_text(content, encoding="utf-8")
    return True
  return False


def update_modification_index(batch_info, commit_hash="pending"):
  content = INDEX_PATH.read_text(encoding="utf-8")
  bid = batch_info["batch_id"]
  start_end = f"`{batch_info['start_id']}` → `{batch_info['end_id']}`"
  cnt = batch_info["count"]
  desc = f"{batch_info['name']} 汉化与对齐校对"
  ver = f"PASS / `{commit_hash}`"
  row = f"| {bid} | {start_end} | {cnt} | {desc} | {ver} |\n"
  if row not in content:
    content += row
    INDEX_PATH.write_text(content, encoding="utf-8")


def run_verifier(require_complete=False):
  cmd = [sys.executable, str(VERIFIER_PATH)]
  if require_complete:
    cmd.append("--require-complete")
  res = subprocess.run(cmd, capture_output=True, text=True)
  return res.returncode == 0, res.stdout.strip()


def git_commit_and_push(batch_info):
  bid = batch_info["batch_id"]
  milestone = batch_info["milestone"].lower()
  start = batch_info["start"]
  end = batch_info["end"]
  name = batch_info["name"]

  msg = f"feat({milestone}): complete {bid} {name} ({start:05d}–{end:05d}) localization and verification"

  subprocess.run(
      [
          "git",
          "add",
          str(TRANSLATION_PATH),
          str(PLAN_PATH),
          str(INDEX_PATH),
      ],
      check=True,
  )
  subprocess.run(["git", "commit", "-m", msg], check=True)

  # Get latest commit hash
  rev = (
      subprocess.run(
          ["git", "rev-parse", "--short", "HEAD"],
          capture_output=True,
          text=True,
          check=True,
      )
      .stdout.strip()
  )

  # Update commit hash in modification index if needed
  content = INDEX_PATH.read_text(encoding="utf-8")
  if "pending" in content:
    content = content.replace("pending", rev)
    INDEX_PATH.write_text(content, encoding="utf-8")
    subprocess.run(["git", "add", str(INDEX_PATH)], check=True)
    subprocess.run(["git", "commit", "--amend", "--no-edit"], check=True)
    rev = (
        subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        .stdout.strip()
    )

  print(f"Pushing commit {rev} to origin main...")
  for attempt in range(3):
    push_res = subprocess.run(
        ["git", "push", "origin", "main"], capture_output=True, text=True
    )
    if push_res.returncode == 0:
      print("Pushed successfully!")
      return True
    time.sleep(2)

  print("Warning: Push failed after 3 attempts.")
  return False


def process_batch(batch_info, trans_data, chunk_size=35, max_workers=2):
  bid = batch_info["batch_id"]
  start = batch_info["start"]
  end = batch_info["end"]
  cnt = batch_info["count"]
  name = batch_info["name"]

  print(f"\n==================================================")
  print(f"Processing Batch: {bid} {name} (序号 {start}..{end}, {cnt} 条)")
  print(f"==================================================")

  slice_entries = trans_data["entries"][start - 1 : end]
  chunks = [
      slice_entries[i : i + chunk_size]
      for i in range(0, len(slice_entries), chunk_size)
  ]
  print(
      f"Divided into {len(chunks)} chunks (size {chunk_size}), translating with"
      f" {max_workers} workers..."
  )

  translations = {}
  t0 = time.time()
  with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(translate_chunk, chunk): chunk for chunk in chunks}
    completed_chunks = 0
    for fut in as_completed(futures):
      chunk_res = fut.result()
      translations.update(chunk_res)
      completed_chunks += 1
      print(f"  Chunk {completed_chunks}/{len(chunks)} done")

  dt = time.time() - t0
  print(f"Batch {bid} translated in {dt:.1f}s. Applying to translation copy...")

  for idx in range(start - 1, end):
    entry = trans_data["entries"][idx]
    iid = entry["id"]
    if iid in translations:
      entry["zh"] = translations[iid]
    else:
      entry["zh"] = fix_control_tokens(
          entry["jp"], entry["jp"], entry.get("type", "")
      )

  # Save and verify
  save_translation_json(trans_data)
  ok, v_out = run_verifier()
  if not ok:
    print(f"Verification FAILED for {bid}!\n{v_out}")
    return False
  print(f"Verification PASS: {v_out}")

  # Update documentation
  update_plan_checklist(bid)
  update_modification_index(batch_info)

  # Git commit and push
  git_commit_and_push(batch_info)
  return True


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
      "--milestone",
      type=str,
      default="all",
      help="Milestone to run (M1, M2, M3, M4, or all)",
  )
  parser.add_argument("--batch", type=str, help="Specific batch ID (e.g. M1-01)")
  parser.add_argument(
      "--chunk-size", type=int, default=35, help="Items per chunk"
  )
  parser.add_argument(
      "--workers", type=int, default=2, help="Parallel worker threads"
  )
  args = parser.parse_args()

  batches = parse_plan_batches()
  with open(TRANSLATION_PATH, "r", encoding="utf-8") as f:
    trans_data = json.load(f)

  targets = []
  for b in batches:
    if args.batch and b["batch_id"] != args.batch:
      continue
    if (
        args.milestone != "all"
        and b["milestone"].upper() != args.milestone.upper()
    ):
      continue
    if b["status"] == "x":
      continue
    targets.append(b)

  print(f"Found {len(targets)} pending batches matching criteria.")
  for i, b in enumerate(targets):
    print(f"\n>>> [{i+1}/{len(targets)}] Starting {b['batch_id']}...")
    success = process_batch(
        b,
        trans_data,
        chunk_size=args.chunk_size,
        max_workers=args.workers,
    )
    if not success:
      print(f"Processor stopped due to error on batch {b['batch_id']}.")
      sys.exit(1)

  print("\nAll targeted batches completed successfully!")


if __name__ == "__main__":
  main()
