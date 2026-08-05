# Social Media Stills Generator

An agentic AI workflow that scores and ranks game-day photo dumps for Yale Rugby's social media.

The problem. I work as a player and photographer(when injured) for Yale Rugby. We shoots thousands of photos per match, but only a small slice works for scoreline graphics, game-day posts, player features, and other team content. This project turns a raw folder of images into a ranked shortlist tagged by post type.

## Problem

Manual processing is extremely slow and took dozens of hours

## Current approach

A **LangGraph** pipeline:

1. **Ingest**: load images from `data/input` (optionally synced from Google Drive via rclone)
2. **Classify**: vision LLM (`gpt-4o-mini`) returns `keep` or `discard` plus a short reason
3. **Export**: write `data/output/results.json` and copy keepers into `data/output/`
   Empty input folders exit cleanly via a conditional edge before classification starts.

### Planned / not built yet

- Cheap prefilters (blur, exposure, near-duplicates)
- Post-type tagging (scoreline, hype, player spotlight, etc.)
- Ranking / crop notes for graphics

## Stack

- Python 3.11+
- LangGraph + LangChain OpenAI
- OpenAI vision (`gpt-4o-mini`)
- Pillow / base64 image encoding
- python-dotenv
- rclone (optional, for Google Drive ingest)

## Project layout

Paste this over your current README.md (or merge section by section). It matches what the project actually does today, plus the rclone ingest path.

# Social Media Stills Generator

An agentic AI workflow that reviews Yale Rugby match photo dumps and decides which frames are usable for team social media and design.
Built around a real workflow: we shoot thousands of photos per match, but only a small slice works for scoreline graphics, gameday posts, player features, and related content. This project takes a folder of images, classifies each with a vision LLM, writes a results report, and copies keepers into an output folder.

## Problem

Manual culling is slow. Soft focus, weak action, cluttered backgrounds, and branding conflicts waste hours before anyone starts editing.

## Current approach

A **LangGraph** pipeline:

1. **Ingest** — load images from `data/input` (optionally synced from Google Drive via rclone)
2. **Classify** — vision LLM (`gpt-4o-mini`) returns `keep` or `discard` plus a short reason
3. **Export** — write `data/output/results.json` and copy keepers into `data/output/`
   Empty input folders exit cleanly via a conditional edge before classification starts.

### Planned / not built yet

- Cheap prefilters (blur, exposure, near-duplicates)
- Post-type tagging (scoreline, hype, player spotlight, etc.)
- Ranking / crop notes for graphics
- a cluster algorithm for player identification

## Stack

- Python 3.11+
- LangGraph + LangChain OpenAI
- OpenAI vision (`gpt-4o-mini`)
- Pillow / base64 image encoding
- python-dotenv
- rclone (optional, for Google Drive ingest)

## Project layout

## Project layout

```text
social-media-stills-generator/
├── src/
│   ├── agents/      # graph nodes (load, classify, advance, save)
│   ├── tools/       # image helpers (e.g. path → data URL)
│   ├── prompts/     # vision system / user prompts
│   └── pipeline/    # state + LangGraph wiring + run entry
├── data/
│   ├── input/       # raw photos
│   ├── output/      # results.json + keepers
│   └── samples/     # optional small demo set
├── docs/            # design notes / rubric drafts
├── tests/
├── scripts/         # optional helper scripts
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
```

## How to run it Run

1. Add photos to `data/input/` (or sync from Google Drive)
2. Activate the venv and run from the project root:

```bash
source .venv/bin/activate
PYTHONPATH=src python3 src/pipeline/graph.py
```
