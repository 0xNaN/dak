from kbucket import KBucket
import unittest

contact = 'contact'
contact2 = 'contact2'
contact3 = 'contact3'

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
        kbucket.add(contact2, 1)

        self.assertRaises(Exception, kbucket.add, contact3, 1)

    def testUpdateAContact(self):
        kbucket = KBucket(2)
        kbucket.add(contact, 1)
        kbucket.add(contact2, 1)

        kbucket.add(contact, 1)
        self.assertEqual(2, len(kbucket.getBucket(1)))
        self.assertEqual(contact, kbucket.getBucket(1)[1])

    def testGetKCloseSimple(self):
        kbucket = KBucket(2)
        kbucket.add(contact, 1)
        kbucket.add(contact2, 1)

        self.assertEqual([contact, contact2], kbucket.getkclose(1))

    def testGetKCloseContactsWhenBucketIsNotFull(self):
        kbucket = KBucket(2)
        kbucket.add(contact, 1)
        kbucket.add(contact2, 2)
        kbucket.add(contact3, 5)

        self.assertEqual([contact, contact2], kbucket.getkclose(1))
        self.assertEqual([contact3, contact2], kbucket.getkclose(5))

        kbucket = KBucket(4)
        kbucket.add("a", 1)
        kbucket.add("b", 1)

        kbucket.add("c", 2)
        kbucket.add("d", 6)
        kbucket.add("e", 6)
        kbucket.add("f", 6)
        kbucket.add("g", 6)

        self.assertEqual(["a", "b", "c", "d"], kbucket.getkclose(1))
        self.assertEqual(["d", "e", "f", "g"], kbucket.getkclose(6))
        self.assertEqual(["c", "a", "b", "d"], kbucket.getkclose(2))
