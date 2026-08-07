# Social Media Stills Generator

An agentic AI workflow that scores and ranks game-day photo dumps for Yale Rugby's social media.

I play for Yale Rugby and also shoot when I'm injured. We take thousands of photos per match, but only a small slice works for scoreline graphics, game-day posts, player features, and other team content. This project turns a raw folder of images into a shortlist of usable stills.

## Problem

Manual processing is extremely slow and took dozens of hours.

## Current approach

A **LangGraph** pipeline:

1. **Ingest**: load images from `data/input` (optionally synced from Google Drive via rclone)
2. **Classify**: vision LLM (`gpt-4o-mini`) returns `keep` or `discard` plus a short reason (with few-shot calibration examples)
3. **Export**: write `data/output/results.json` and copy keepers into `data/output/`

Empty input folders exit cleanly before classification starts.

### Planned / not built yet

- Cheap prefilters (blur, exposure, near-duplicates)
- Post-type tagging (scoreline, hype, player spotlight, etc.)
- Ranking / crop notes for graphics
- A cluster algorithm for player identification

## Stack

- Python 3.11+
- LangGraph + LangChain OpenAI
- OpenAI vision (`gpt-4o-mini`)
- Pillow / base64 image encoding
- python-dotenv
- rclone (optional, for Google Drive ingest)

## Project layout

```text
social-media-stills-generator/
├── src/
│   ├── agents/      # graph nodes (load, classify, advance, save)
│   ├── tools/       # image helpers (e.g. path → data URL)
│   ├── prompts/     # vision system / user prompts
│   └── pipeline/    # state + LangGraph wiring + run entry
├── data/
│   ├── input/       # raw photos (gitignored)
│   ├── output/      # results.json + keepers (gitignored)
│   └── samples/     # optional small demo set
├── docs/
├── tests/
├── scripts/
├── .env.example
└── requirements.txt
```

## Setup

```bash
cd social-media-stills-generator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add OPENAI_API_KEY to .env
```

## How to run it

1. Add photos to `data/input/` (or sync from Google Drive with rclone)
2. From the project root:

```bash
source .venv/bin/activate
PYTHONPATH=src python src/pipeline/graph.py
```

3. Check `data/output/results.json` and any keepers in `data/output/`

### Optional: pull photos from Google Drive

```bash
rclone copy "tobibgdrive:Yale rugby/YOUR_FOLDER" "./data/input" \
  --include "*.{jpg,JPG,jpeg,JPEG,png,PNG}" \
  --exclude "*del*" \
  --ignore-case \
  --progress
```

Remote names need a trailing colon (`tobibgdrive:` not `tobibgdrive`).
