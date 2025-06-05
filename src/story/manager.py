"""Story Manager for LLM Fixpoints Explorer."""

import os
import json

class StoryManager:
    """Manages stories and their evolutions."""

    def __init__(self, story_name: str, cache_dir: str = "story_cache"):
        """Initialize the story manager with a name and cache directory."""
        self.story_name = story_name
        self.cache_dir = cache_dir

        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)

    def save_story(self, story: str, iteration: int):
        """Save a story to a file."""
        filename = f"{self.story_name}_{iteration}.txt"
        filepath = os.path.join(self.cache_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(story)
        print(f"Saved story iteration {iteration} to {filepath}")

    def load_story(self, iteration: int) -> str:
        """Load a story from a file."""
        filename = f"{self.story_name}_{iteration}.txt"
        filepath = os.path.join(self.cache_dir, filename)

        if not os.path.exists(filepath):
            print(f"Story iteration {iteration} does not exist.")
            return ""

        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def save_cornerstones(self, cornerstones: dict[str, str], retell_count: int):
        """Save story cornerstones and retell count as JSON."""
        data = {
            "cornerstones": cornerstones,
            "retell_count": retell_count
        }
        filepath = os.path.join(self.cache_dir, f"{self.story_name}_settings.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Saved story settings to {filepath}")

    def load_cornerstones(self) -> tuple[dict[str, str], int]:
        """Load cornerstones and retell count from JSON."""
        filepath = os.path.join(self.cache_dir, f"{self.story_name}_settings.json")

        if not os.path.exists(filepath):
            print(f"No settings file found for {self.story_name}.")
            return {}, 0

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data.get("cornerstones", {}), data.get("retell_count", 0)

    def get_prompt(self, cornerstones: dict[str, str]) -> str:
        """Create a prompt from story cornerstones dictionary."""
        prompt = "Write a short story based on the following elements:\n\n"
        for key, value in cornerstones.items():
            prompt += f"{key.capitalize()}: {value}\n"
        prompt += "\nThe story should be creative and engaging."
        return prompt