import json
import os

from pynamodb.exceptions import DoesNotExist, DeleteError

from todos.todo_model import TodoModel


def delete(event, context):
    try:
        TodoModel.Meta.table_name = os.environ['DYNAMODB_TABLE']
    except KeyError:
        return {'statusCode': 500,
                'body': json.dumps({'error': 'ENV_VAR_NOT_SET'})}

    try:
        todo_id = event['path']['todo_id']
    except KeyError:
        return {'statusCode': 422,
                'body': json.dumps({'error': 'URL_PARAMETER_MISSING',
                                    'error_message': 'TODO was not found'})}
    try:
        found_todo = TodoModel.get(hash_key=todo_id)
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error': 'NOT_FOUND',
                                    'error_message': 'TODO was not found'})}
    try:
        found_todo.delete()
    except DeleteError:
        return {'statusCode': 400,
                'body': json.dumps({'error': 'DELETE_FAILED',
                                    'error_message': 'Unable to delete the TODO'})}

    # create a response
    return {'statusCode': 204}
