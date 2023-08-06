import unittest
import mock
from shellfoundry.template_retriever import TemplateRetriever


class TestTemplateRetriever(unittest.TestCase):
    def mock_get_templates_from_github(self):
        return """
        templates:
          switch : https://github.com/QualiSystems/shellfoundry-switch-template
          router : https://github.com/QualiSystems/shellfoundry-router-template
        """

    @mock.patch('shellfoundry.template_retriever.TemplateRetriever._get_templates_from_github',
                mock_get_templates_from_github)
    def test_get_templates(self):
        # Arrange
        template_retriever = TemplateRetriever()

        # Act
        templates = template_retriever.get_templates()

        # Assert
        self.assertSequenceEqual(templates,
                                 {'switch': 'https://github.com/QualiSystems/shellfoundry-switch-template',
                                  'router': 'https://github.com/QualiSystems/shellfoundry-router-template'})
