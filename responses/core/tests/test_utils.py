from django.test import TestCase
from django.contrib.auth.models import Permission

from botify_saas.core.utils import chop_queryset


def create_permissions(number):
    p = Permission.objects.all()[0]
    for i in xrange(number):
        p.id = None
        p.codename = 'plop-%s' % i
        p.save()


class TestUtils(TestCase):

    def test_chop_queryset(self):
        '''test botify_saas.core.utils.chop_queryset'''
        create_permissions(102)
        qs = Permission.objects.filter(codename__startswith='plop-')
        chunks = list(chop_queryset(qs, 10))
        # test chunks number
        self.assertEquals(len(chunks), 11)
        # test chunks size
        for chunk in chunks[:-1]:
            self.assertEquals(len(chunk), 10)
        self.assertEquals(len(chunks[-1]), 2)
        chunk = chunks[0]
        for perm in chunk:
            self.assertIsInstance(perm, Permission)

        # test with a values_list
        chunks = list(chop_queryset(qs, 10, values_list=['id', 'codename']))
        self.assertEquals(len(chunks), 11)
        # test chunks size
        for chunk in chunks[:-1]:
            self.assertEquals(len(chunk), 10)
        self.assertEquals(len(chunks[-1]), 2)
        # test results types
        id_, codename = chunks[0][0]
        self.assertIsInstance(id_, int)
        self.assertIsInstance(codename, basestring)
        self.assertTrue(codename.startswith("plop-"))

        # test with a single value
        chunks = list(chop_queryset(qs, 10, values_list=['id']))
        self.assertEquals(len(chunks), 11)
        # test chunks size
        for chunk in chunks[:-1]:
            self.assertEquals(len(chunk), 10)
        self.assertEquals(len(chunks[-1]), 2)
        id_ = chunks[0][0]
        self.assertIsInstance(id_, int)
