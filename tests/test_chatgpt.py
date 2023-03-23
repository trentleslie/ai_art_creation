import unittest
from ai_art_creation.api import chatgpt

class TestChatGPT(unittest.TestCase):

    def test_generate_prompts(self):
        # Call the generate_prompts() function from the chatgpt module
        prompts = chatgpt.generate_prompts()

        # Check if the output is a list
        self.assertIsInstance(prompts, list)

        # Check if every element in the list is a string
        for prompt in prompts:
            self.assertIsInstance(prompt, str)

if __name__ == '__main__':
    unittest.main()
