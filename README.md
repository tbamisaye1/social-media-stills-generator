# Social Media Stills Generator

An agentic AI workflow that scores and ranks game-day photo dumps for Yale Rugby's social media.

The problem. I work as a player and photographer(when injured) for Yale Rugby. We shoots thousands of photos per match, but only a small slice works for scoreline graphics, game-day posts, player features, and other team content. This project turns a raw folder of images into a ranked shortlist tagged by post type.

## Problem

Manual processing is extremely slow and took dozens of hours

## Approach

A multi-step agent pipeline:

1. **Ingest**: load a folder of match photos
2. **Filter**: drop obvious rejects (blur, extreme exposure, near-duplicates)
3. **Score**: vision LLM rates composition, emotion, jersey/face visibility, action clarity
4. **Classify**: map keepers to post types (scoreline, game day hype, player spotlight, etc.)
5. **Rank & export**: output a shortlist with reasons and suggested crop notes

## Project layout

```
social-media-stills-generator/
├── src/
│   ├── agents/      # agent roles (filter, scorer, classifier, orchestrator)
│   ├── tools/       # image I/O, blur checks, duplicate detection, API calls
│   ├── prompts/     # vision / LLM prompt templates
│   └── pipeline/    # end-to-end run orchestration
├── data/
│   ├── input/       # raw photo dumps (gitignored)
│   ├── output/      # ranked results (gitignored)
│   └── samples/     # tiny public/demo set for README screenshots
├── tests/
├── scripts/         # CLI entrypoints you add
└── docs/            # design notes, post-type rubric
```

## Setup (You will need a OPENAI key for the underlying LLM)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add your API keys to .env

```
