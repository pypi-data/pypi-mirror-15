import time
from unittest import skipIf

from django.utils import six
from django.utils.text import slugify

from nested_admin.tests.base import BaseNestedAdminTestCase
from .models import (
    TestAdminWidgetsRoot, TestAdminWidgetsA, TestAdminWidgetsB,
    TestAdminWidgetsC0, TestAdminWidgetsC1)


class TestAdminWidgets(BaseNestedAdminTestCase):

    fixtures = ['admin-widgets.xml']

    root_model = TestAdminWidgetsRoot
    nested_models = (TestAdminWidgetsA, TestAdminWidgetsB,
        (TestAdminWidgetsC0, TestAdminWidgetsC1))

    @classmethod
    def setUpClass(cls):
        super(TestAdminWidgets, cls).setUpClass()
        cls.a_model, cls.b_model, (cls.c0_model, cls.c1_model) = cls.nested_models

    def check_prepopulated(self, indexes):
        name = "Item %s" % (" ABC"[len(indexes)])
        if name == 'Item C':
            name += "%d%d" % (indexes[-1][0], indexes[-1][1])
        else:
            name += "%d" % indexes[-1]

        name += " (%s)" % " > ".join(["%s" % i[1] for i in self._normalize_indexes(indexes)])

        expected_slug = slugify(six.text_type(name))

        slug_sel = self.get_form_field_selector('slug', indexes)

        self.set_field('name', name, indexes)
        time.sleep(0.2)
        slug_val = self.selenium.execute_script(
            'return $("%s").val()' % slug_sel)
        self.assertEqual(slug_val, expected_slug, "prepopulated slug field did not sync")

    def check_datetime(self, indexes):
        date_el = self.get_field('date_0', indexes)
        time_el = self.get_field('date_1', indexes)

        if self.has_grappelli:
            now_link_xpath = "following-sibling::*[1]"
        else:
            now_link_xpath = "following-sibling::*[1]/a[1]"
        date_el.clear()
        time_el.clear()
        date_el.find_element_by_xpath(now_link_xpath).click()
        if self.has_grappelli:
            with self.clickable_selector('#ui-datepicker-div .ui-state-highlight') as el:
                el.click()
        time.sleep(0.1)
        time_el.find_element_by_xpath(now_link_xpath).click()
        if self.has_grappelli:
            with self.clickable_selector('#ui-timepicker .ui-state-active') as el:
                el.click()
        time.sleep(0.10)
        self.assertNotEqual(date_el.get_attribute('value'), '', 'Date was not set')
        self.assertNotEqual(time_el.get_attribute('value'), '', 'Time was not set')

    def check_m2m(self, indexes):
        add_all_link = self.get_field('m2m_add_all_link', indexes)
        remove_all_link = self.get_field('m2m_remove_all_link', indexes)
        remove_all_link.click()
        add_all_link.click()
        m2m_to_sel = self.get_form_field_selector('m2m_to', indexes)
        time.sleep(0.2)
        selected = self.selenium.execute_script(
            'return $("%s").find("option").toArray().map(function(el) { return parseInt(el.value, 10); })'
                % m2m_to_sel)
        self.assertEqual(selected, [1, 2, 3])

    def check_widgets(self, indexes, skip_m2m=False):
        self.check_prepopulated(indexes)
        self.check_datetime(indexes)
        if not skip_m2m:
            self.check_m2m(indexes)

    def test_initial_extra_prepopulated(self):
        self.load_admin()
        self.check_prepopulated([0])
        self.check_prepopulated([0, 0])

    def test_initial_extra_m2m(self):
        self.load_admin()
        self.check_m2m([0])
        self.check_m2m([0, 0])

    def test_initial_extra_datetime(self):
        self.load_admin()
        self.check_datetime([0])
        self.check_datetime([0, 0])

    @skipIf(BaseNestedAdminTestCase.has_grappelli,
        "Known bug with prepopulated fields and grappelli")
    @skipIf(BaseNestedAdminTestCase.has_suit,
        "Known bug with prepopulated fields and django-suit")
    def test_add_prepopulated(self):
        self.load_admin()
        self.add_inline()
        self.check_prepopulated([1])

    @skipIf(BaseNestedAdminTestCase.has_grappelli,
        "Known bug with prepopulated fields and grappelli")
    @skipIf(BaseNestedAdminTestCase.has_suit,
        "Known bug with prepopulated fields and django-suit")
    def test_add_initial_extra_prepopulated(self):
        self.load_admin()
        self.add_inline()
        self.check_prepopulated([1, 0])

    def test_add_m2m(self):
        self.load_admin()
        self.add_inline()
        self.check_m2m([1])

    @skipIf(True, "Known bug")
    def test_add_initial_extra_m2m(self):
        self.load_admin()
        self.add_inline()
        self.check_m2m([1, 0])

    def test_add_datetime(self):
        self.load_admin()
        self.add_inline()
        self.check_datetime([1])

    @skipIf(BaseNestedAdminTestCase.has_grappelli,
        "Known bug with datetime fields and grappelli")
    def test_add_initial_extra_datetime(self):
        self.load_admin()
        self.add_inline()
        self.check_datetime([1, 0])

    def test_add_two_deep_m2m(self):
        self.load_admin()
        self.add_inline()
        self.add_inline([1])
        self.check_m2m([1, 1])

    @skipIf(BaseNestedAdminTestCase.has_grappelli,
        "Known bug with prepopulated fields and grappelli")
    @skipIf(BaseNestedAdminTestCase.has_suit,
        "Known bug with prepopulated fields and django-suit")
    def test_add_two_deep_prepopulated(self):
        self.load_admin()
        self.add_inline()
        self.add_inline([1])
        self.check_prepopulated([1, 1])

    @skipIf(BaseNestedAdminTestCase.has_grappelli,
        "Known bug with datetime fields and grappelli")
    def test_add_two_deep_datetime(self):
        self.load_admin()
        self.add_inline()
        self.add_inline([1])
        self.check_datetime([1, 1])

    def test_add_three_deep_m2m(self):
        self.load_admin()
        self.add_inline()
        self.add_inline([1])
        self.add_inline([1, 0, [1]])
        self.check_m2m([1, 0, [1, 0]])

    @skipIf(BaseNestedAdminTestCase.has_grappelli,
        "Known bug with prepopulated fields and grappelli")
    @skipIf(BaseNestedAdminTestCase.has_suit,
        "Known bug with prepopulated fields and django-suit")
    def test_add_three_deep_prepopulated(self):
        self.load_admin()
        self.add_inline()
        self.add_inline([1])
        self.add_inline([1, 0, [1]])
        self.check_prepopulated([1, 0, [1, 0]])

    @skipIf(BaseNestedAdminTestCase.has_grappelli,
        "Known bug with datetime fields and grappelli")
    def test_add_three_deep_datetime(self):
        self.load_admin()
        self.add_inline()
        self.add_inline([1])
        self.add_inline([1, 0, [1]])
        self.check_datetime([1, 0, [1, 0]])
