#!/usr/bin/env python3
"""
Main application for exploring LLM story fixpoints.
This project investigates how stories retold by LLMs develop and if there are
fixpoints where stories converge over multiple retellings.
"""

from ui.cli import CLIUserInterface
from llm.ollama_service import OllamaLLMService
from story.manager import StoryManager

class Application:
    """Main application class for LLM Fixpoints Explorer."""

    def __init__(self):
        """Initialize the application components."""
        self.ui = CLIUserInterface()
        self.llm_service = OllamaLLMService(model_name="llama3.2:latest")
        self.story_manager = None

    def run(self):
        """Run the main application logic."""
        print("Welcome to the LLM Fixpoints Explorer!")

        # Get story name and cornerstones from user
        story_name = input("Enter a name for your story: ").strip()
        if not story_name:
            print("Story name cannot be empty.")
            return

        self.story_manager = StoryManager(story_name)

        # Try to load existing cornerstones
        cornerstones, retell_count = self.story_manager.load_cornerstones()

        if not cornerstones:
            # Get story cornerstones from user
            cornerstones = self.ui.get_story_cornerstones()
            retell_count = self.ui.get_retell_count()

            # Save cornerstones and retell count as JSON
            self.story_manager.save_cornerstones(cornerstones, retell_count)
        else:
            print(f"Loaded existing story settings: {cornerstones}")
            print(f"Retell count: {retell_count}")

        # Create initial prompt and generate first story
        prompt = self.story_manager.get_prompt(cornerstones)
        original_story = self.llm_service.generate_story(prompt)


        # Save the original story
        self.story_manager.save_story(original_story, 0)
        self.ui.display_story(original_story)

        # Retell the story multiple times
        current_story = original_story
        for i in range(201, retell_count + 1):
            new_story = self.llm_service.retell_story(current_story)
            self.story_manager.save_story(new_story, i)

            # Display the story if it's the last iteration
            if i == retell_count:
                print(f"\nFinal story after {retell_count} retellings:")
                self.ui.display_story(new_story)

            current_story = new_story

        print("\nStory evolution complete!")

if __name__ == "__main__":
    app = Application()
    app.run()