#!/usr/bin/env python3
"""
Generate fragment pair training data for Astravus Collection: Calista Arc.

Reads fragment list from FRAGMENTS.md and generates before/after pairs
as training data in JSONL format for the VoxService.
"""

import json
import re
from pathlib import Path


def extract_fragments_from_md(md_file):
    """Extract fragment number and name from FRAGMENTS.md."""
    fragments = []
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all table rows with fragment data
    # Pattern: | NUMBER | Fragment Name | Summary |
    pattern = r'\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+)\s*\|'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        frag_num = int(match.group(1))
        frag_name = match.group(2).strip()
        summary = match.group(3).strip()
        
        # Skip header rows and empty matches
        if frag_name and frag_name not in ['Fragment Name', '#']:
            fragments.append({
                'number': frag_num,
                'name': frag_name,
                'summary': summary
            })
    
    return sorted(fragments, key=lambda x: x['number'])


def generate_fragment_pairs(fragments):
    """Generate before/after fragment pairs as training messages."""
    pairs = []
    
    for i, frag in enumerate(fragments):
        frag_num = frag['number']
        frag_name = frag['name']
        
        # Generate "what comes before" pair
        if i == 0:
            # First fragment - no predecessor
            before_response = (
                f"Fragment #{frag_num} \"{frag_name}\" is the opening fragment of the Calista Arc, "
                f"so there is no fragment before it."
            )
        else:
            prev_frag = fragments[i - 1]
            before_response = (
                f"The fragment that comes before #{frag_num} \"{frag_name}\" is "
                f"Fragment #{prev_frag['number']} \"{prev_frag['name']}\"."
            )
        
        pair_before = {
            "messages": [
                {"role": "system", "content": ""},
                {"role": "user", "content": f"What fragment comes before \"{frag_name}\"?"},
                {"role": "assistant", "content": before_response}
            ]
        }
        pairs.append(pair_before)
        
        # Generate "what comes after" pair
        if i == len(fragments) - 1:
            # Last fragment - no successor
            after_response = (
                f"Fragment #{frag_num} \"{frag_name}\" is the final fragment of the Calista Arc, "
                f"so there is no fragment after it."
            )
        else:
            next_frag = fragments[i + 1]
            after_response = (
                f"The fragment that comes after #{frag_num} \"{frag_name}\" is "
                f"Fragment #{next_frag['number']} \"{next_frag['name']}\"."
            )
        
        pair_after = {
            "messages": [
                {"role": "system", "content": ""},
                {"role": "user", "content": f"What fragment comes after \"{frag_name}\"?"},
                {"role": "assistant", "content": after_response}
            ]
        }
        pairs.append(pair_after)
    
    return pairs


def save_pairs_to_jsonl(pairs, output_file):
    """Save fragment pairs to JSONL file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for pair in pairs:
            f.write(json.dumps(pair) + '\n')
    
    print(f"✓ Generated {len(pairs)} fragment pairs")
    print(f"✓ Saved to {output_file}")


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    rebuild_dir = script_dir.parent.parent  # Navigate to Rebuild directory
    
    fragments_md = rebuild_dir / 'revision' / 'FRAGMENTS.md'
    output_jsonl = rebuild_dir / 'revision' / 'training_data' / 'fragment_pairs.jsonl'
    
    if not fragments_md.exists():
        print(f"✗ Error: FRAGMENTS.md not found at {fragments_md}")
        return 1
    
    print(f"Reading fragments from {fragments_md}")
    fragments = extract_fragments_from_md(str(fragments_md))
    print(f"✓ Extracted {len(fragments)} fragments")
    
    print("\nGenerating fragment pairs...")
    pairs = generate_fragment_pairs(fragments)
    
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    save_pairs_to_jsonl(pairs, str(output_jsonl))
    
    return 0


if __name__ == '__main__':
    exit(main())
