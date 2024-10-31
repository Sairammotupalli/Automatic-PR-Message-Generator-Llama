class Prompt:
    MAX_TOKENS = 2048

    def __init__(self, text: str, max_tokens: Union[int, None] = None):
        self.max_tokens = max_tokens if max_tokens is not None else self.MAX_TOKENS
        self._text = text

    @property
    def length(self):
        # Approximate length based on characters rather than tokens
        return len(self._text)

    @property
    def text(self):
        return self._text

    @property
    def is_valid(self):
        # Validate length by character count approximation
        return self.length <= self.max_tokens

    @property
    def remaining_length(self):
        return self.max_tokens - self.length

    def concat(self, prompt: "Prompt"):
        max_tokens = min(self.max_tokens, prompt.max_tokens)
        return Prompt(self.text + "\n" + prompt.text, max_tokens)

    def split(self):
        if self.is_valid:
            return [Prompt(self.text, self.max_tokens)]

        prompts = []
        for i in range(0, len(self._text), self.max_tokens):
            partial_prompt = Prompt(self._text[i : i + self.max_tokens])
            prompts.append(partial_prompt)
        return prompts

    def wrap(self, wrapper: str):
        prefix = Prompt(wrapper + "\n")
        suffix = Prompt("\n" + wrapper)
        return prefix.concat(self).concat(suffix)

    def __repr__(self):
        return self.text
