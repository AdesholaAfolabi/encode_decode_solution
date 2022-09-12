import re
import math
import unittest

# messageToEncode = "Hi Bob, this is Alice. Any news?"
# messageToDecode = "eestHwAAhisnliB yiso ncib"
# dictionary = ["hi", "this", "news", "alice", "ice", "sis", "bob", "any", "is"]

class AliceMessage:
    @staticmethod
    def encode(message: str)->str:

        """Encode input message. Basic text cleaning such as removal of
            non-alphaneumeric character is done.
        Args:
            message: the message to be encoded.
        Returns:
            str: Endoded message.
        """
        
        # Strip out non-alphanumeric chars
        clean_message = re.sub(r'\W+', '', message)
        grid_size = math.ceil(math.sqrt(len(clean_message)))

        # Create a matrix of empty strings based on the gridSize
        message_grid = [[' ' for x in range(grid_size)] for y in range(grid_size)]

        for index, char in enumerate(list(clean_message)):
            row = math.floor(index / grid_size)
            col = index % grid_size

            message_grid[row][col] = char

        # Reverse the grid and set the new rows as columns and vice-versa (clock-wise rotation)
        message_grid.reverse()
        encoded_message = ""
        for i in range(grid_size):
            for j in range(grid_size):
                char = message_grid[j][i]
                encoded_message = encoded_message + char

        return encoded_message

    @staticmethod
    def decode(message: str) -> str:

        """Decode input message. 
        Args:
            message: the message to be decoded.
        Returns:
            Decoded message.
        """
        # Create a matrix of empty strings based on the gridSize
        grid_size = math.ceil(math.sqrt(len(message)))
        message_grid = [[' ' for x in range(grid_size)] for y in range(grid_size)]

        for index, char in enumerate(list(message)):
            # Reverse how the rows were generated
            row = index % grid_size
            col = math.floor(index / grid_size)
            message_grid[row][col] = char

        # Reverse grid to complete anti-clockwise rotation
        message_grid.reverse()

        # Turn matrix list into a flat string
        return ''.join(list(map(lambda x: ''.join(x), message_grid))).strip()

    @staticmethod
    def isSafe(decoded_message: str, _dict: list) -> bool:

        """Validate that the message is not compromised. 
        Args:
            decoded_message: the message to validate.
            _dict: the dictionary of words provided(as a list)
        Returns:
            True or False.
        """
        
        last_match_index = 0
        message = decoded_message.lower()
        for index in range(len(message)):
            # Skip iteration if current index was used as a match in previous iteration
            if last_match_index == index:
                continue

            # Check if word is in dict and set last_match_index
            word = message[last_match_index: index + 1]
            if word in _dict:
                last_match_index = index + 1

        return last_match_index == len(message)

class TestAliceMessage(unittest.TestCase):
    def setUp(self) -> None:
        self.alice = AliceMessage()

    def test_encode(self):
        self.assertEqual(self.alice.encode("Hi Bob, this is Alice. Any news?"), "eestHwAAhisnliB yiso ncib")
        self.assertEqual(self.alice.encode(""), "")
        self.assertEqual(self.alice.encode(",.?"), "")
        
        
    def test_decode(self):
        self.assertEqual(self.alice.decode(""), "")
        self.assertEqual(self.alice.decode("eestHwAAhisnliB yiso ncib"), "HiBobthisisAliceAnynews")
        
    def test_isSafe(self):
      Dict = ['hi', 'this', 'news', 'alice', 'ice', 'sis', 'bob', 'any', 'is']
      decoded = 'HiBobthisisAliceAnynews'
      self.assertTrue(self.alice.isSafe(decoded, Dict))
      self.assertFalse(self.alice.isSafe("HiBobthisisAliceAnynew", Dict))
      self.assertFalse(self.alice.isSafe(decoded, []))
      self.assertTrue(self.alice.isSafe('', Dict))
      
if __name__ == '__main__':
    unittest.main()


