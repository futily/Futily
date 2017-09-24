import json
import os

from django.conf import settings

from futily.utils.list import find_dict_by_value


class EaAssetCreatorCommand(object):
    def __init__(self):
        super(EaAssetCreatorCommand, self).__init__()

        self.base_dir = '{}/data/players'.format(settings.BASE_ROOT)
        self.teamConfig = '{}/data/teamconfig.json'.format(settings.BASE_ROOT)
        self.messages_en = 'https://www.easports.com/iframe/fut17/bundles/futweb/web/flash/xml/localization/messages' \
                           '.en_GB.xml?cl=164521'

    @staticmethod
    def get_object(item, obj):
        return item[obj]

    def get_items(self):
        items = []
        files = os.listdir(self.base_dir)

        for json_file in files:
            with open(f'{self.base_dir}/{json_file}', 'r') as open_file:
                try:
                    data = json.load(open_file)
                    items.append(data['items'])
                except Exception as e:  # pylint: disable=broad-except
                    print(e)

        return [item for sublist in items for item in sublist]

    def get_team_config(self, year='2018'):
        with open(self.teamConfig) as json_file:
            data = json.load(json_file)

            return find_dict_by_value(data['Years'], 'Year', year)
