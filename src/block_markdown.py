from enum import Enum


def markdown_to_blocks(markdown):
    final_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block != "":
            final_blocks.append(block)
    return final_blocks

BlockType = Enum('BlockType',['paragraph', 'heading', 'code', 'quote', 'unordered_list', 'ordered_list'])

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(('# ', '## ', '### ', '#### ', '##### ', '###### ')):
        return BlockType.heading
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.code
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.paragraph
        return BlockType.quote
    elif block.startswith('- '):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.paragraph
        return BlockType.unordered_list
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.paragraph
            i += 1
        return BlockType.ordered_list
    return BlockType.paragraph

