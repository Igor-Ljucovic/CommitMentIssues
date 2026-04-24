CHARACTERS_PER_TOKEN_ESTIMATE = 3.5
RESERVED_OUTPUT_TOKENS = 300


def prompt_character_limit(
    num_ctx: int,
    reserved_output_tokens: int = RESERVED_OUTPUT_TOKENS,
) -> int:
    token_limit = max(num_ctx - reserved_output_tokens, 0)
    
    return int(token_limit * CHARACTERS_PER_TOKEN_ESTIMATE)