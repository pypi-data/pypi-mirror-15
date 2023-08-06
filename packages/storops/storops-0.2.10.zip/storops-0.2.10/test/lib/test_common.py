# coding=utf-8
# Copyright (c) 2015 EMC Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import unicode_literals

import logging
from multiprocessing.pool import ThreadPool
from time import sleep
from unittest import TestCase

from hamcrest import assert_that, equal_to, close_to, only_contains, raises, \
    contains_string

from storops.exception import EnumValueNotFoundError
from storops.lib.common import Dict, Enum, WeightedAverage, \
    synchronized, cache, text_var, int_var, enum_var, \
    yes_no_var, instance_cache, Cache, JsonPrinter, clear_instance_cache, \
    get_lock_file
from storops.vnx.enums import VNXRaidType

log = logging.getLogger(__name__)


class DictTest(TestCase):
    def test_get_attr(self):
        result = Dict()
        result['a'] = 'A'
        assert_that(result.a, equal_to('A'))
        assert_that(result['a'], equal_to('A'))

    def test_get_attr_not_exists(self):
        def f():
            result = Dict()
            log.debug(result.a)

        assert_that(f, raises(AttributeError))


class SampleEnum(Enum):
    TYPE_A = 'type a'
    TYPE_B = 'type b'

    @classmethod
    def get_option_map(cls):
        return {
            None: [],
            cls.TYPE_A: '-a',
            cls.TYPE_B: '-b'
        }

    @classmethod
    def get_int_index(cls):
        return None, cls.TYPE_A, cls.TYPE_B


class SampleIntEnum(Enum):
    OK = 0
    NOT_FOUND = 1
    ERROR = 2


class EnumTest(TestCase):
    def test_verify_allow_none(self):
        # no error raised
        SampleIntEnum.verify(None)

    def test_verify_normal_value(self):
        # no error raised
        SampleIntEnum.verify(SampleIntEnum.NOT_FOUND)

    def test_verify_not_allow_none(self):
        def f():
            SampleIntEnum.verify(None, allow_none=False)

        assert_that(f, raises(ValueError, 'SampleIntEnum'))

    def test_verify_not_valid_value(self):
        def f():
            SampleIntEnum.verify(88)

        assert_that(f, raises(ValueError, 'SampleIntEnum'))

    def test_get_all(self):
        assert_that(len(SampleEnum.get_all()), equal_to(2))

    def test_get_opt(self):
        assert_that(SampleEnum.get_opt(SampleEnum.TYPE_A), equal_to('-a'))

    def test_from_int(self):
        assert_that(SampleEnum.from_int(2), equal_to(SampleEnum.TYPE_B))

    def test_from_int_not_found_in_index(self):
        def f():
            SampleEnum.from_int(10)

        assert_that(f, raises(EnumValueNotFoundError, 'for SampleEnum'))

    def test_from_int_enum(self):
        assert_that(SampleIntEnum.from_int(1),
                    equal_to(SampleIntEnum.NOT_FOUND))

    def test_from_int_not_found(self):
        def f():
            SampleIntEnum.from_int(10)

        assert_that(f, raises(EnumValueNotFoundError, 'for SampleIntEnum'))

    def test_parse_string(self):
        ret = SampleEnum.parse('type a')
        assert_that(ret, equal_to(SampleEnum.TYPE_A))

    def test_parse_invalid_str_enum(self):
        def f():
            SampleEnum.parse('n/a')

        assert_that(f, raises(EnumValueNotFoundError))

    def test_parse_invalid_int_enum(self):
        def f():
            SampleEnum.parse(999)

        assert_that(f, raises(EnumValueNotFoundError))
        assert_that(f, raises(ValueError))

    def test_invalid_value(self):
        def f():
            SampleEnum('type c')

        assert_that(f, raises(ValueError, 'not a valid SampleEnum'))

    def test_values(self):
        assert_that(SampleEnum.values(), only_contains('type a', 'type b'))


class CacheA(object):
    def __init__(self):
        self.base = 0
        pass

    @cache
    def do(self, a, b):
        return a + b * 2 + self.base

    @cache
    def a(self):
        return self.base

    @cache
    def add_base(self, a):
        return a + self.base


class CacheB(object):
    def __init__(self):
        self.base = 0
        pass

    @cache
    def do(self, a, b):
        return a + b

    @cache
    def b(self):
        return CacheA().a()


class SelfCacheA(object):
    def __init__(self):
        self.base = 0

    @instance_cache
    def add_base(self, a):
        return a + self.base

    @clear_instance_cache
    def clear_cache(self):
        pass


class CacheTest(TestCase):
    def setUp(self):
        Cache.clear_cache()
        self.a = CacheA()
        self.b = CacheB()

    def test_cache(self):
        assert_that(self.a.do(2, 4), equal_to(10))
        self.a.base = 1
        assert_that(self.a.do(2, 4), equal_to(10))

        assert_that(self.b.do(2, 4), equal_to(6))
        self.b.base = 1
        assert_that(self.b.do(2, 4), equal_to(6))

    def test_cache_lock(self):
        assert_that(CacheB().b(), equal_to(0))

    def test_instance_cache_hit(self):
        sa1 = SelfCacheA()
        assert_that(sa1.add_base(1), equal_to(1))
        sa1.base = 3
        assert_that(sa1.add_base(1), equal_to(1))
        assert_that(sa1.add_base(0), equal_to(3))

    def test_instance_cache_on_instance(self):
        sa1 = SelfCacheA()
        sa1.base = 5
        assert_that(sa1.add_base(1), equal_to(6))
        sa2 = SelfCacheA()
        assert_that(sa2.add_base(1), equal_to(1))

    def test_global_cache_cleared(self):
        self.a.base = 1
        assert_that(self.a.add_base(2), equal_to(3))
        self.a.base = 3
        assert_that(self.a.add_base(2), equal_to(3))
        Cache.clear_cache()
        assert_that(self.a.add_base(2), equal_to(5))

    def test_instance_cache_not_cleared(self):
        sa = SelfCacheA()
        sa.base = 1
        assert_that(sa.add_base(2), equal_to(3))
        sa.base = 3
        assert_that(sa.add_base(2), equal_to(3))
        Cache.clear_cache()
        assert_that(sa.add_base(2), equal_to(3))

    def test_clear_instance_cache_scope(self):
        sa = SelfCacheA()
        sa.base = 1
        assert_that(sa.add_base(2), equal_to(3))
        sb = SelfCacheA()
        sb.base = 2
        assert_that(sb.add_base(2), equal_to(4))
        sa.base = 5
        sb.base = 6
        # cache hit
        assert_that(sa.add_base(2), equal_to(3))
        assert_that(sb.add_base(2), equal_to(4))
        sa.clear_cache()
        assert_that(sa.add_base(2), equal_to(7))
        assert_that(sb.add_base(2), equal_to(4))


class WeightedAverageTest(TestCase):
    def test_data_full(self):
        avg = WeightedAverage(3)
        avg.add(30, 24, 18, 12, 6)
        assert_that(avg.value(), equal_to(10))
        avg.add(30)
        assert_that(avg.value(), equal_to(19))

    def test_data_full_1(self):
        avg = WeightedAverage(6)
        avg.add(30, 24, 18, 12, 6, 6, 6)
        assert_that(avg.value(), close_to(8.85, 0.01))
        avg.add(30)
        assert_that(avg.value(), equal_to(14))

    def test_data_not_full(self):
        avg = WeightedAverage(3)
        avg.add(12, 6)
        assert_that(avg.value(), equal_to(8.4))

    def test_data_empty(self):
        avg = WeightedAverage(3)
        assert_that(avg.value(), equal_to(0))

    def test_size(self):
        avg = WeightedAverage(3)
        assert_that(avg.size, equal_to(3))
        avg.weight = [3]
        avg.add(4, 5, 7)
        assert_that(avg.size, equal_to(1))
        assert_that(avg.value(), equal_to(7))


class LockDemo(object):
    name = 1

    def __init__(self):
        self.call_count = 0

    @synchronized(name)
    def foo1(self):
        self.call_count += 1
        sleep(0.05)

    def foo2(self, value):
        @synchronized(value)
        def in_foo2():
            self.call_count += 1
            sleep(0.05)

        in_foo2()

    @synchronized()
    def bar(self, _):
        self.call_count += 1
        sleep(0.05)


class SynchronizedTest(TestCase):
    def test_synchronize_simple(self):
        demo = LockDemo()
        pool = ThreadPool(2)
        pool.imap(demo.bar, range(2))
        sleep(0.04)
        assert_that(demo.call_count, equal_to(1))
        sleep(0.05)
        assert_that(demo.call_count, equal_to(2))

    def test_synchronize_with_different_param(self):
        demo = LockDemo()
        pool = ThreadPool(2)
        pool.imap(demo.foo2, range(2))
        sleep(0.02)
        assert_that(demo.call_count, equal_to(2))

    def test_synchronize_with_same_param(self):
        demo = LockDemo()
        pool = ThreadPool(3)
        pool.imap(demo.foo2, (1, 1))
        pool.apply_async(demo.foo1)
        sleep(0.04)
        assert_that(demo.call_count, equal_to(1))
        sleep(0.05)
        assert_that(demo.call_count, equal_to(2))
        sleep(0.05)
        assert_that(demo.call_count, equal_to(3))


class VarTest(TestCase):
    def test_text_var(self):
        assert_that(text_var('-a', 'a'), only_contains('-a', 'a'))
        assert_that(text_var(None, 'a'), only_contains('a'))
        assert_that(text_var('-a', None), equal_to([]))

    def test_int_var(self):
        assert_that(int_var('-a', '1'), only_contains('-a', 1))
        assert_that(int_var(None, '1'), only_contains(1))
        assert_that(int_var('-a', None), equal_to([]))

    def test_enum_var(self):
        assert_that(enum_var('-a', 'r5', VNXRaidType),
                    only_contains('-a', 'r5'))
        assert_that(enum_var(None, 'r5', VNXRaidType), only_contains('r5'))
        assert_that(enum_var('-a', None, VNXRaidType), equal_to([]))

    def test_yes_no_var(self):
        assert_that(yes_no_var('-a', True), only_contains('-a', 'yes'))
        assert_that(yes_no_var('-a', False), only_contains('-a', 'no'))
        assert_that(yes_no_var('-a', None), equal_to([]))


class JsonPrinterDemo(JsonPrinter):
    def __init__(self):
        self.a = 1
        self.b = None

    def _get_properties(self, dec=0):
        return {'a': self.a, 'b': self.b}


class JsonPrinterTest(TestCase):
    def test_str_delete_null(self):
        j = JsonPrinterDemo()
        assert_that(str(j), equal_to('{"JsonPrinterDemo": {"a": 1}}'))


class CommonTest(TestCase):
    def test_get_lock_file(self):
        name = get_lock_file('a.lock')
        assert_that(name, contains_string('.storops'))
        assert_that(name, contains_string('a.lock'))
