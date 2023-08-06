from grow.pods import locales
from grow.pods import pods
from grow.pods import storage
from grow.testing import testing
import unittest


class RenderedTest(unittest.TestCase):

    def setUp(self):
        self.dir_path = testing.create_test_pod_dir()
        self.pod = pods.Pod(self.dir_path, storage=storage.FileStorage)

    def test_locale(self):
        controller, params = self.pod.match('/fr/about/')
        fr_locale = locales.Locale.parse('fr')
        self.assertEqual(fr_locale, controller.locale)
        controller, params = self.pod.match('/de_alias/about/')
        de_locale = locales.Locale.parse('de')
        self.assertEqual(de_locale, controller.locale)
        self.assertEqual('de_alias', controller.locale.alias)

    def test_mimetype(self):
        controller, params = self.pod.match('/')
        self.assertEqual('text/html', controller.get_mimetype(params))
        controller, params = self.pod.match('/fr/about/')
        self.assertEqual('text/html', controller.get_mimetype(params))

    def test_render(self):
        controller, params = self.pod.match('/')
        controller.render(params)
        controller, params = self.pod.match('/fr/about/')
        controller.render(params)

    def test_custom_jinja_extensions(self):
        controller, params = self.pod.match('/')
        html = controller.render(params)
        # Test pod uses a custom `|triplicate` filter on 'abcabcabc'
        self.assertIn('Custom Jinja Extension: abcabcabc', html)

    def test_list_concrete_paths(self):
        controller, params = self.pod.match('/')
        self.assertEqual(['/'], controller.list_concrete_paths())


if __name__ == '__main__':
    unittest.main()
