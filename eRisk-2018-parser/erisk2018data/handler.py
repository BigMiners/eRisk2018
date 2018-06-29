import os
import csv
import xml.etree.ElementTree as ET


class Task:

    def __init__(self, path, reader=None):
        self.path = path
        if reader:
            self.reader = reader
        else:
            self.reader = Task.text_only_xml

    def get_split(self, name, part, chunks, start=1):
        """
        Gives the group of training users and test users according to the given split
        and during the given number of chunks
        :param name: name of the split
        :param part: 'train' or 'test'
        :param chunks: the number of chunks to concatenate starting with chunk 1.
        :return: training users, test users
        """
        if part != 'train' and part != 'test':
            raise ValueError
        path = os.path.join(self.path, 'splits', name, '%s.csv' % part)
        return self.__generator(path, chunks, start=1)

    def __generator(self, truth_file, chunks, start=1):
        """
        Returns a generator for a given truth file and a chunk
        :param truth_file: File containing the IDs and labels
        :param chunks: Number of the desired chunk
        :return: generator : subjectID, label, content for chunk
        """
        reader = self.reader

        class Gen:

            def __init__(self, truth):
                self.truth = truth
                self.it = 0

            def __iter__(self):
                return self

            def __next__(self):
                if self.it < len(self.truth):
                    subject = self.truth[self.it]
                    self.it += 1
                    content = []
                    for path in subject[2]:
                        content.extend(reader(path))
                    return subject[0], subject[1], content
                else:
                    raise StopIteration

            def __len__(self):
                return len(self.truth)

            def reset(self):
                self.it = 0

        with open(truth_file) as f:
            truth = []
            for row in csv.reader(f, delimiter='\t'):
                if len(row) == 2:
                    paths = [os.path.join(self.path, 'chunks', 'chunk{}'.format(chunk),
                                          '{}_{}.xml'.format(row[0], chunk))
                             for chunk in range(start, chunks + 1)]
                    truth.append((row[0], row[1], paths))
            f.close()
        return Gen(truth)


    @staticmethod
    def text_only_xml(path):
        """
        Retrieves the text (titles and content) from a user's writings at a given chunk. Pass this function
        as a parameter to __init__
        :param path: path to xml file
        :return: concatenated titles (from empty posts) and contents
        """
        with open(path) as file:
            tree = ET.parse(file)
            writings = []
            for writing in tree.findall('.//WRITING'):
                content = writing.find('TITLE').text.strip()
                content += writing.find('TEXT').text.strip()
                writings.append(content)
            return reversed(writings)

    @staticmethod
    def with_dates_xml(path):
        """
        Retrieves the text (titles and content) and dates from a user's writings at a given chunk. Pass this function
        as a parameter to __init__
        :param path: path to xml file
        :return: concatenated dates, titles (from empty posts) and contents
        """
        with open(path) as file:
            tree = ET.parse(file)
            writings = []
            for writing in tree.findall('.//WRITING'):
                date = writing.find('DATE').text.strip()
                text = writing.find('TITLE').text.strip()
                text += writing.find('TEXT').text.strip()
                writings.append({'date': date, 'text': text})
            return reversed(writings)
