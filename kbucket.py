class KBucket:
    def __init__(self, k):
        self._k = k
        self._contacts = {}

    def add(self, contact, distance):
        if not self._contacts.__contains__(distance):
            self._contacts[distance] = []

        if(len(self._contacts[distance]) == self._k):
            raise Exception("Bucket full")

        self._contacts[distance].append(contact)

    def getBucket(self, distance):
        return self._contacts[distance]

import unittest

contact = 'contact'
contact2 = 'contact2'

class KBucketTest(unittest.TestCase):
    def testAddAContact(self):
        kbucket = KBucket(2)

        kbucket.add(contact, 1);

        self.assertEqual(contact, kbucket.getBucket(1)[0])

    def testAppendNewContact(self):
        kbucket = KBucket(2)
        kbucket.add(contact, 1)
        kbucket.add(contact2, 1)

        self.assertEqual(contact, kbucket.getBucket(1)[0])
        self.assertEqual(contact2, kbucket.getBucket(1)[1])

    def testBucketFull(self):
        kbucket = KBucket(2)

        kbucket.add(contact, 1)
        kbucket.add(contact, 1)

        self.assertRaises(Exception, kbucket.add, contact, 1)



