import unittest
from ai_art_creation.api import chatgpt, dall_e

class TestDallE(unittest.TestCase):

    def test_generate_images(self):
        # Call the generate_prompts() function from the chatgpt module to get the prompts list
        prompts = chatgpt.generate_prompts()

        # Call the generate_images() function from the dall_e module with the prompts list
        image_paths = dall_e.generate_images(prompts)

        # Check if the output is a list
        self.assertIsInstance(image_paths, list)

        # Check if every element in the list is a string
        for image_path in image_paths:
            self.assertIsInstance(image_path, str)

        # Add more assertions as needed to test other aspects of the generate_images() function

if __name__ == '__main__':
    unittest.main()
