import configparser
import os
from unittest import TestCase, main

from erisk2018data.handler import Task, batchify, infinify


class TestTask(TestCase):

    def setUp(self):
        self.task = Task('../data/task2/', reader=Task.verbatim_xml)
        config = configparser.RawConfigParser()
        config.read('config.cfg')
        dataset_base_path = config.get('Dataset', 'path')
        self.path_task2 = dataset_base_path + '/task2'
        self.task = Task(self.path_task2)

    def test_get_split(self):
        train, test = self.task.get_split('b')
        first = next(train[0])
        self.assertEquals(len(first), 3)

    def test_batchify(self):
        train, _ = self.task.get_split('b')
        size = 16
        train_batches = batchify(train[0], size)
        first_batch = next(train_batches)
        self.assertEqual(len(first_batch), size)

        batches = batchify(train[1])
        first = next(batches)
        self.assertEqual(len(first), 32)

    def test_text_only_xml(self):
        text = Task.text_only_xml(os.path.join(self.path_task2, 'chunks', 'chunk5', 'subject322_5.xml'))

    def test_with_dates(self):
        text = Task.with_dates_xml(os.path.join(self.path_task2, 'chunks', 'chunk5', 'subject322_5.xml'))

    def test_infinify(self):
        train, _ = self.task.get_split('f')
        length = len(train[0])
        gen = infinify(train[0])
        first = next(gen)
        for _ in range(length):
            again = next(gen)
        self.assertEqual(first, again)


if __name__ == '__main__':
    main()
