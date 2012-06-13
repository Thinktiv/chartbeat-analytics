from setuptools import setup, find_packages

setup(name="chartbeat_analytics",
           version="0.1",
           description="chartbeat_analytics",
           author="Thinktiv",
           author_email="rahul.kashyap@joshlabs.in",
           packages=['chartbeat_analytics','chartbeat_analytics.templatetags'],
           package_data={'chartbeat_analytics': ['templates/chartbeat_analytics/*.html']},
           include_package_data=True,
)
