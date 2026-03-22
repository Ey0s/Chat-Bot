from __future__ import annotations

import datetime as dt
import json
import random
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Tuple


class ChatBot:
    def __init__(self, json_file: Path, creator_name: str = "Eyosyas"):
        self.creator = creator_name
        self.responses = self._load_responses(json_file)

    def _load_responses(self, json_file: Path) -> Dict[str, Any]:
        if not json_file.exists():
            return {}

        try:
            with json_file.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    @staticmethod
    def _normalize(text: str) -> str:
        lowered = text.lower().strip()
        return re.sub(r"[^a-z0-9\s]", " ", lowered)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return [token for token in text.split() if token]

    def _score_pattern(self, message: str, pattern: str) -> float:
        if not pattern:
            return 0.0

        msg = self._normalize(message)
        pat = self._normalize(pattern)

        if pat in msg:
            return min(1.0, 0.75 + (len(pat.split()) * 0.05))

        msg_tokens = set(self._tokenize(msg))
        pat_tokens = set(self._tokenize(pat))

        token_overlap = 0.0
        if pat_tokens:
            token_overlap = len(msg_tokens & pat_tokens) / len(pat_tokens)

        fuzzy_ratio = SequenceMatcher(None, msg, pat).ratio()
        return max(token_overlap * 0.8, fuzzy_ratio * 0.6)

    def _best_category_match(self, message: str) -> Tuple[str, Dict[str, Any], float]:
        categories: Dict[str, Dict[str, Any]] = {}
        categories.update(self.responses.get("static_responses", {}))
        categories.update(self.responses.get("extended_responses", {}))

        best_name = ""
        best_data: Dict[str, Any] = {}
        best_score = 0.0

        for category_name, category_data in categories.items():
            patterns = category_data.get("patterns", [])
            if not isinstance(patterns, list):
                continue

            score = 0.0
            for pattern in patterns:
                score = max(score, self._score_pattern(message, str(pattern)))

            if score > best_score:
                best_name = category_name
                best_data = category_data
                best_score = score

        return best_name, best_data, best_score

    def _render_dynamic_response(self, message: str) -> str:
        dynamic = self.responses.get("dynamic_responses", {})
        message_norm = self._normalize(message)

        for dynamic_data in dynamic.values():
            keywords = [self._normalize(k) for k in dynamic_data.get("keywords", [])]
            if not keywords:
                continue

            if not any(keyword and keyword in message_norm for keyword in keywords):
                continue

            function_name = dynamic_data.get("function", "")
            if not isinstance(function_name, str) or not hasattr(self, function_name):
                continue

            value = getattr(self, function_name)()
            responses = dynamic_data.get("responses", [])
            if isinstance(responses, list) and responses:
                template = random.choice(responses)
                if "{time}" in template:
                    return template.format(time=value)
                if "{date}" in template:
                    return template.format(date=value)
                return template
            return value

        return ""

    def get_time(self) -> str:
        return dt.datetime.now().strftime("%H:%M:%S")

    def get_date(self) -> str:
        return dt.datetime.now().strftime("%Y-%m-%d")

    def get_response(self, message: str) -> str:
        if not message.strip():
            return "Please type a message so I can help."

        dynamic_response = self._render_dynamic_response(message)
        if dynamic_response:
            return dynamic_response

        _, best_data, best_score = self._best_category_match(message)
        threshold = 0.45

        if best_data and best_score >= threshold:
            responses = best_data.get("responses", [])
            if isinstance(responses, list) and responses:
                return random.choice(responses)

        default_data = self.responses.get("static_responses", {}).get("default", {})
        default_responses = default_data.get("responses", [])
        if isinstance(default_responses, list) and default_responses:
            return random.choice(default_responses)

        return "Sorry, I did not understand that yet."
