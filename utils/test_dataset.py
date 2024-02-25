import unittest
from utils.dataset import dat

class TestDataset(unittest.TestCase):
    def setUp(self):
        self.upload_folder = 'static/images'
        self.total_num = 160
        self.dataset = dat(self.upload_folder, self.total_num)

    def test_init(self):
        self.assertEqual(self.dataset.total_num, self.total_num)
        self.assertEqual(self.dataset.order, ['Content', 'Style', 'PhotoWCT', 'WCT2', 'ASTMAN', 'StyTR2', 'DSTN', 'Dreamstyler', 'pro'])
        self.assertEqual(self.dataset.suffix, ['', '', '', '', '', '', '_cfg_9.00*'])
        self.assertEqual(self.dataset.upload_folder, self.upload_folder)
        self.assertEqual(len(self.dataset.pid2concept), 8)
        self.assertEqual(len(self.dataset.chosen), self.total_num)
        self.assertEqual(len(self.dataset.chosen_style), self.total_num)
        self.assertEqual(len(self.dataset.chosen_content), self.total_num)

    def test_getitem(self):
        # Assuming the dataset has been properly initialized
        index = 0
        filename_url, pid2concept, cr_chosen = self.dataset[index]
        print(f"filename_url: {filename_url}, pid2concept: {pid2concept}, cr_chosen: {cr_chosen}")
        self.assertIsInstance(filename_url, list)
        self.assertIsInstance(pid2concept, str)
        self.assertIsInstance(cr_chosen, int)

    def test_len(self):
        # Assuming the dataset has been properly initialized
        self.assertEqual(len(self.dataset), self.total_num)

if __name__ == '__main__':
    unittest.main()