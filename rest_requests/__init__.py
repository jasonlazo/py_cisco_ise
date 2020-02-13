from rest_requests.base import CiscoIseRequest


def get_path(path_template: str, path_parms: list):
    try:
        path_template = path_template.format(*path_parms)
    except IndexError:
        raise Exception(
            "Less params than required: path [{}] params[{}]".format(path_template, path_parms)
        )
    return path_template


def get_body(body_template: dict, body_params: dict):
    for k, v in body_params.items():
        if k in body_template:
            if isinstance(body_template[k], dict):
                if isinstance(body_params[k], dict):
                    body_template[k] = get_body(body_template[k], body_params[k])
                else:
                    raise Exception("Bad recursion")
            else:
                body_template[k] = body_params[k]
        else:
            raise Exception("Not allowed key")

    return body_template
