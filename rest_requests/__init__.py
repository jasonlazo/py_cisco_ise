def get_path(path_template: str, path_parms: dict):
    try:
        path_template = path_template.format(**path_parms)
    except KeyError:
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


def iterate_over_pages(rest_client, *args, **kwargs):
    run = True
    kwargs["path_params"] = kwargs.get("path_params", {})
    kwargs["path_params"]["size"] = 20
    kwargs["path_params"]["page"] = 1

    while run:
        response = rest_client.send_request(
            *args,
            **kwargs
        )["SearchResult"]

        for response_item in response["resources"]:
            yield response_item

        run = bool(response["nextPage"]["href"])
        kwargs["path_params"]["page"] += 1
