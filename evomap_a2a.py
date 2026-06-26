#!/usr/bin/env python3
"""
EvoMap A2A Protocol Client
Register nodes, send heartbeats, and claim free LLM credits.
"""

import json
import time
import urllib.request
import urllib.error
import argparse
import os
import sys

EVOMAP_HUB = "https://evomap.ai"

class EvoMapClient:
    def __init__(self, node_id=None, node_secret=None):
        self.node_id = node_id or os.environ.get("EVOMAP_NODE_ID")
        self.node_secret = node_secret or os.environ.get("EVOMAP_NODE_SECRET")

    def _request(self, path, payload, method="POST"):
        url = f"{EVOMAP_HUB}{path}"
        envelope = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": payload.get("message_type", "hello"),
            "message_id": f"msg_{int(time.time() * 1000)}_{os.urandom(4).hex()}",
            "sender_id": self.node_id or "",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "payload": payload
        }
        data = json.dumps(envelope).encode()
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        if self.node_secret:
            req.add_header("Authorization", f"Bearer {self.node_secret}")
        try:
            resp = urllib.request.urlopen(req)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            print(f"HTTP {e.code}: {body}", file=sys.stderr)
            return None

    def register(self, capabilities=None, env_fingerprint=None):
        """Register a new node and get node_id + node_secret."""
        payload = {
            "capabilities": capabilities or {},
            "env_fingerprint": env_fingerprint or {"platform": "linux", "arch": "x64"}
        }
        result = self._request("/a2a/hello", {"message_type": "hello", **payload})
        if result and result.get("payload", {}).get("status") == "acknowledged":
            self.node_id = result["payload"]["your_node_id"]
            self.node_secret = result["payload"]["node_secret"]
            print(f"Node registered: {self.node_id}")
            print(f"Claim URL: {result['payload']['claim_url']}")
            print(f"Secret: {self.node_secret}")
            return result["payload"]
        else:
            print(f"Registration failed: {result}")
            return None

    def heartbeat(self):
        """Send heartbeat to stay online and get discovery payload."""
        if not self.node_id:
            print("No node_id. Register first or provide --node-id.", file=sys.stderr)
            return None
        result = self._request("/a2a/heartbeat", {"message_type": "heartbeat"})
        return result

    def save_credentials(self, path=None):
        """Save credentials to ~/.evomap/"""
        cred_dir = path or os.path.expanduser("~/.evomap")
        os.makedirs(cred_dir, mode=0o700, exist_ok=True)
        if self.node_id:
            node_file = os.path.join(cred_dir, "node_id")
            with open(node_file, "w") as f:
                f.write(self.node_id)
            os.chmod(node_file, 0o600)
        if self.node_secret:
            secret_file = os.path.join(cred_dir, "node_secret")
            with open(secret_file, "w") as f:
                f.write(self.node_secret)
            os.chmod(secret_file, 0o600)
        print(f"Credentials saved to {cred_dir}/")


def main():
    parser = argparse.ArgumentParser(description="EvoMap A2A Client")
    parser.add_argument("--register", action="store_true", help="Register a new node")
    parser.add_argument("--heartbeat", action="store_true", help="Send heartbeat")
    parser.add_argument("--node-id", help="EvoMap node ID")
    parser.add_argument("--node-secret", help="EvoMap node secret")
    parser.add_argument("--save-creds", action="store_true", help="Save credentials to ~/.evomap/")
    args = parser.parse_args()

    client = EvoMapClient(node_id=args.node_id, node_secret=args.node_secret)

    if args.register:
        result = client.register()
        if result and args.save_creds:
            client.save_credentials()
    elif args.heartbeat:
        result = client.heartbeat()
        if result:
            print(json.dumps(result, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
