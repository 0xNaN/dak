class KBucket:
    def __init__(self, k):
        self._k = k
        self._contacts = {}

    def add(self, contact, distance):
        if not self._contacts.__contains__(distance):
            self._contacts[distance] = []

        if(self._contacts[distance].__contains__(contact)):
            self._contacts[distance].remove(contact)
        elif (len(self._contacts[distance]) == self._k):
            raise Exception("Bucket full")

        self._contacts[distance].append(contact)

    def getkclose(self, distance):
        close = []

        distances = [d for d in self._contacts.keys()]
        while(len(close) < self._k and len(distances) > 0):
            closest = self._find_close(distances, distance)

            remaining = self._k - len(close)
            close.extend(self._contacts[closest][:remaining])
            distances.remove(closest)


        return close

    def _find_close(self, distances, distance):
        assert(len(distances) > 0)
        distances.sort()
        closest, delta = distances[0], abs(distance - distances[0])

        for k in distances[1:]:
            if(delta > abs(distance - k)):
                delta = abs(distance - k)
                closest = k
            else:
                break

        return closest

    def getBucket(self, distance):
        return self._contacts[distance]

    def __str__(self):
        return "Key into Bucket:\n{}\n{}".format(self._contacts.keys(), self._contacts.values())

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
