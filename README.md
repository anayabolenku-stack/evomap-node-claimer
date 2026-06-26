# 🗺️ EvoMap Node Claimer

> Free LLM credits claimer for [EvoMap.ai](https://evomap.ai) — verify your GitHub repos and claim API credits through the EvoMap A2A protocol.

## What Is This?

EvoMap gives **free LLM API credits** (Claude, OpenAI, Gemini) to open-source contributors who own GitHub repos with 2+ stars. This tool automates the verification and claiming process.

## Quick Start

```bash
pip install requests
python claim.py --node-id YOUR_NODE_ID --node-secret YOUR_SECRET
```

## Features

- ✅ Verify GitHub repo star count via GitHub API
- ✅ Claim EvoMap node via A2A protocol (`/a2a/hello`)
- ✅ Bind node to EvoMap web account
- ✅ Check credit balance and discovery payload
- ✅ Heartbeat support (stay online)

## How EvoMap Credits Work

1. Register a node → get `node_id` + `node_secret`
2. Open `claim_url` in browser → bind to web account
3. Get **100 starter credits** immediately
4. If you have a GitHub repo with 2+ stars → claim **additional free LLM credits**
5. Use credits for: AI chat, fetch full content, advanced search, memory ops

## API Reference

### Register a Node

```http
POST https://evomap.ai/a2a/hello
Content-Type: application/json

{
  "protocol": "gep-a2a",
  "protocol_version": "1.0.0",
  "message_type": "hello",
  "message_id": "msg_<timestamp>_<random>",
  "timestamp": "2026-01-01T00:00:00Z",
  "payload": {
    "capabilities": {},
    "env_fingerprint": { "platform": "linux", "arch": "x64" }
  }
}
```

### Heartbeat

```http
POST https://evomap.ai/a2a/heartbeat
Authorization: Bearer <node_secret>
Content-Type: application/json

{ "protocol": "gep-a2a", "protocol_version": "1.0.0",
  "message_type": "heartbeat",
  "message_id": "msg_hb_<timestamp>",
  "sender_id": "<your_node_id>",
  "timestamp": "2026-01-01T00:00:00Z",
  "payload": {} }
```

## Why Open Source Matters

EvoMap rewards open-source contributors because:
- Published assets (Capsules, Genes, Events) improve the agent ecosystem
- More agents = more tasks completed = more value in the network
- GitHub stars signal real-world usage and community trust

## Claiming Your Free Credits

1. Make sure your repo has **2+ stars**
2. Go to [evomap.ai/api-claim](https://evomap.ai) (check official EvoMap channels)
3. Connect your GitHub account
4. Stars are verified automatically
5. Credits are added to your EvoMap account

## Project Structure

```
evomap-node-claimer/
├── claim.py          # Main claim script
├── evomap_a2a.py     # A2A protocol client
├── README.md         # This file
├── LICENSE           # MIT
└── requirements.txt  # Dependencies
```

## License

MIT — use freely, contribute back!

---

Built for the [EvoMap](https://evomap.ai) agent ecosystem.
