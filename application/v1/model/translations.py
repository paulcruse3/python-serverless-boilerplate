from functools import lru_cache
import os

import boto3

class Translations:

    def __init__(self):
        self.table = self._get_dynamo_table(os.environ['DYNAMODB_TRANSLATIONS'], os.environ['DYNAMODB_ENDPOINT'])

    @lru_cache(maxsize=128)
    def _get_dynamo_table(self, table, endpoint=None):
        return boto3.resource('dynamodb', endpoint_url=endpoint).Table(table)

    def create_translation(self, **kwargs):
        self.table.put_item(Item=kwargs);
        return kwargs

    def translate_english(self, english):
        result = self.table.get_item(
            Key={
               'english': english
            }
        )
        return result.get('Item', {});

    def translate_spanish(self, spanish):
        results = self.table.query(
            IndexName='spanish',
            Limit=1,
            KeyConditionExpression='spanish = :spanish',
            ExpressionAttributeValues={
                ':spanish': spanish
            }
        )
        return results['Items'][0] if len(results['Items']) else {}

    def delete_translation(self, english):
        self.table.delete_item(
            Key={
               'english': english
            }
        )
