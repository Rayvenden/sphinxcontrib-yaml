import unittest
import warnings
import os

from sphinx_testing import with_app

from sphinxcontrib.autoyaml import AutoYAMLException


CONFIG = {
    'master_doc': 'index',
    'extensions': ['sphinxcontrib.autoyaml'],
    'autoyaml_root': '.',
}


def patch_config(delta):
    r = CONFIG.copy()
    r.update(delta)
    return r


def build(app, path):
    """Build and return documents without known warnings"""
    with warnings.catch_warnings():
        # Ignore warnings emitted by docutils internals.
        warnings.filterwarnings(
            "ignore",
            "'U' mode is deprecated",
            DeprecationWarning)
        app.build()
        with open(os.path.join(app.outdir, path),
                  encoding='utf-8') as rendered:
            return rendered.read()


class TestAutoYAML(unittest.TestCase):

    @with_app(
        confoverrides=patch_config({'autoyaml_level': 0}),
        buildername="text",
        srcdir="tests/examples/output",
        copy_srcdir_to_tmpdir=True)
    def test_output(self, app, status, warning):
        output = build(app, "index.txt")
        with open("tests/examples/output/index.txt") as f:
            correct = f.read()
        self.assertEqual(correct, output + '\n')

    @with_app(
        confoverrides=CONFIG,
        buildername="text",
        srcdir="tests/examples/output",
        copy_srcdir_to_tmpdir=True)
    def test_output(self, app, status, warning):
        output = build(app, "index.txt")
        with open("tests/examples/output/index2.txt") as f:
            correct = f.read()
        self.assertEqual(correct, output + '\n')

    @with_app(
        confoverrides=CONFIG,
        buildername="html",
        srcdir="tests/examples/wrong_location1",
        copy_srcdir_to_tmpdir=True)
    def test_missing_file(self, app, status, warning):
        ret = None
        with self.assertRaises(AutoYAMLException):
            build(app, "index.txt")

    @with_app(
        confoverrides=CONFIG,
        buildername="html",
        srcdir="tests/examples/wrong_location2",
        copy_srcdir_to_tmpdir=True)
    def test_directory_argument(self, app, status, warning):
        ret = None
        with self.assertRaises(AutoYAMLException):
            build(app, "index.txt")


if __name__ == '__main__':
    unittest.main()
