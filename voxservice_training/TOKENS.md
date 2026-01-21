TOKENS.md
===========

Date: 2026-01-20
Source: `voxservice_training/training_data/training.jsonl`
Tokenizer: `tiktoken` (used locally to compute counts)

Summary
-------
Total tokens in the training set: **152,330**

Breakdown by role
-----------------
- **System:** 16,137 tokens — 10.6% (783 messages) — avg 21 tokens/message
- **User:** 7,880 tokens — 5.2% (783 messages) — avg 10 tokens/message
- **Assistant:** 128,313 tokens — 84.2% (783 messages) — avg 164 tokens/message

Totals
------
- Total messages: 2,349 (783 system + 783 user + 783 assistant)
- Total tokens: 152,330

Notes
-----
- Counts were calculated using the `tiktoken` Python library.
- The dataset is heavily weighted toward assistant responses (long reference-style replies), which is typical for knowledge-heavy training material.

Python snippet used (for reproducibility):

```python
import json
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")  # used locally for encoding
system_tokens = user_tokens = assistant_tokens = 0
message_count = {'system': 0, 'user': 0, 'assistant': 0}
with open('training.jsonl') as f:
    for line in f:
        data = json.loads(line)
        for msg in data.get('messages', []):
            role = msg['role']
            tokens = len(enc.encode(msg['content']))
            message_count[role] += 1
            if role == 'system':
                system_tokens += tokens
            elif role == 'user':
                user_tokens += tokens
            elif role == 'assistant':
                assistant_tokens += tokens
total = system_tokens + user_tokens + assistant_tokens
print(system_tokens, user_tokens, assistant_tokens, total)
```