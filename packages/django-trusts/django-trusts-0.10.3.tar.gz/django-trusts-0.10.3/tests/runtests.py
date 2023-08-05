# see https://docs.djangoproject.com/en/1.9/topics/testing/advanced/#using-the-django-test-runner-to-test-reusable-applications
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
test_dir = os.path.join(os.path.dirname(__file__), 'trusts')
sys.path.insert(0, test_dir)

import django
from django.test.utils import get_runner
from django.conf import settings

def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    if hasattr(django, 'setup'):
        django.setup()
    failures = test_runner.run_tests(['trusts'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
