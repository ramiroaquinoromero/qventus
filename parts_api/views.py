from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3
from rest_framework.viewsets import ReadOnlyModelViewSet

connection = sqlite3.connect("db.sqlite3", check_same_thread=False)


def home(request):
    return render(request, "index.html")


@csrf_exempt
def update_part(request, part_id):
    part = ""
    if len(request.body) > 0:
        part = json.loads(request.body)
    if request.method == "GET":
        try:
            result = get_by_id_part_process(part_id)
        except Exception as ex:
            print(ex)
            return send_response(False, "The part wasn't listed.", {}, 500)

        return send_response(True, "The part was listed correctly.", result, 200)
    if request.method == "PUT":
        value_pairs = create_values_pairs_query(part, "UPDATE")
        try:
            result = update_part_process(value_pairs, part_id)
        except Exception as ex:
            print(ex)
            return send_response(False, "The part wasn't updated.", {}, 500)

        return send_response(True, "The part was updated correctly.", result, 200)

    if request.method == "DELETE":
        try:
            result = delete_part_process(part_id)
        except Exception as ex:
            print(ex)
            return send_response(False, "The part wasn't deleted.", {}, 500)

        return send_response(True, "The part was deleted correctly.", result, 200)

    """
    This is only the code if only I was just doing the put method
    The error was related to the query execution returned 200 but not updated on database,
    only needs execute the commit method after the update.
    """
    # value_pairs = create_values_pairs_query(part, "UPDATE")
    # try:
    #     result = update_part_process(value_pairs, part_id)
    # except Exception as ex:
    #     print(ex)
    #     return send_response(False, "The part wasn't updated.", {}, 500)
    #
    # return send_response(True, "The part was updated correctly.", result, 200)

    """
    These methods is related CRUD with the same way to update
    """

    # if request.method == "GET":
    #     try:
    #         result = list_part_process()
    #     except Exception as ex:
    #         print(ex)
    #         return send_response(False, "The part wasn't listed.", {}, 500)
    #
    #     return send_response(True, "The part was listed correctly.", result, 200)
    # if request.method == "POST":
    #     value_pairs = create_values_pairs_query(part, "INSERT")
    #     try:
    #         result = create_part_process(value_pairs)
    #     except Exception as ex:
    #         print(ex)
    #         return send_response(False, "The part wasn't created.", {}, 500)
    #
    #     return send_response(True, "The part was created correctly.", result, 200)
    #
    # if request.method == "PUT":
    #     value_pairs = create_values_pairs_query(part, "UPDATE")
    #     try:
    #         result = update_part_process(value_pairs, part_id)
    #     except Exception as ex:
    #         print(ex)
    #         return send_response(False, "The part wasn't updated.", {}, 500)
    #
    #     return send_response(True, "The part was updated correctly.", result, 200)
    #
    # if request.method == "DELETE":
    #     try:
    #         result = delete_part_process(part_id)
    #     except Exception as ex:
    #         print(ex)
    #         return send_response(False, "The part wasn't deleted.", {}, 500)
    #
    #     return send_response(True, "The part was deleted correctly.", result, 200)


"""
I split these methods because is better readable 
"""


def create_values_pairs_query(part: dict, type_query: str):
    value_pairs = ""
    if type_query == "UPDATE":
        value_pairs = ",".join(
            (
                "{key}='{value}'".format(key=key, value=value)
                if isinstance(value, (str, bool))
                else "{key}={value}".format(key=key, value=value)
                for key, value in part.items()
            )
        )
    elif type_query == "INSERT":
        value_pairs = ",".join(
            (
                "'{value}'".format(key=key, value=value)
                if isinstance(value, (str, bool))
                else "{value}".format(key=key, value=value)
                for key, value in part.items()
            )
        )

    return value_pairs


def update_part_process(value_pairs: str, part_id: int):
    try:
        cursor = connection.cursor()
        sql_update = "UPDATE part SET {value_pairs} WHERE id={part_id}".format(
            value_pairs=value_pairs, part_id=part_id
        )
        cursor.execute(sql_update)
        connection.commit()
        sql_get = "SELECT * FROM part WHERE id={part_id}".format(part_id=part_id)
        cursor.execute(sql_get)
        row = cursor.fetchone()
        result = dict(zip([c[0] for c in cursor.description], row))
        cursor.close()
        return result
    except Exception as ex:
        print(ex)


def create_part_process(value_pairs: str):
    try:
        cursor = connection.cursor()

        sql_insert = "INSERT INTO part(name,sku,description,weight_ounces,is_active) VALUES({value_pairs})".format(
            value_pairs=value_pairs
        )
        cursor.execute(sql_insert)

        connection.commit()
        part_id = cursor.lastrowid

        sql_get = "SELECT * FROM part WHERE id={part_id}".format(part_id=part_id)
        cursor.execute(sql_get)
        row = cursor.fetchone()
        result = dict(zip([c[0] for c in cursor.description], row))
        cursor.close()
        return result
    except Exception as ex:
        print(ex)


def delete_part_process(part_id: int):
    try:
        cursor = connection.cursor()

        sql_delete = "DELETE FROM part WHERE id={part_id}".format(part_id=part_id)
        cursor.execute(sql_delete)
        connection.commit()
        cursor.close()
        return {}
    except Exception as ex:
        print(ex)


def list_part_process():
    try:
        cursor = connection.cursor()

        sql_list = "SELECT * FROM part "
        cursor.execute(sql_list)
        records = cursor.fetchall()
        result = []
        for row in records:
            result.append(dict(zip([c[0] for c in cursor.description], row)))
        cursor.close()
        return result
    except Exception as ex:
        print(ex)


def get_by_id_part_process(part_id: int):
    try:
        cursor = connection.cursor()

        sql_get_by_id = "SELECT * FROM part WHERE id={part_id}".format(part_id=part_id)
        cursor.execute(sql_get_by_id)
        row = cursor.fetchone()
        result = dict(zip([c[0] for c in cursor.description], row))
        cursor.close()
        return result
    except Exception as ex:
        print(ex)


def send_response(status: bool, message: str, data: dict, status_code: int):
    response = {
        "status": status,
        "message": message,
        "data": data,
    }

    return HttpResponse(
        json.dumps(response), content_type="application/json", status=status_code
    )
