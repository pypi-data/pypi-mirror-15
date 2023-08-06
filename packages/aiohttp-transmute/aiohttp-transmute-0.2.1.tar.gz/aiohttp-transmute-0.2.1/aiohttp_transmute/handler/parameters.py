from transmute_core.exceptions import APIException


async def extract_params(request, context, signature, parameters):
    args = {}
    if signature.get_argument("request"):
        args["request"] = request

    empty_args = []

    for name, arginfo in parameters.query.items():
        if name in request.GET:
            args[name] = context.serializers.load(arginfo.type, request.GET[name])
        else:
            empty_args.append(arginfo)

    for name, arginfo in parameters.header.items():
        if name in request.headers:
            args[name] = context.serializers.load(arginfo.type, request.headers[name])
        else:
            empty_args.append(arginfo)

    if len(parameters.body) > 0:
        # we don't want to try to read the body, if we don't need to.
        # in these cases, an empty body will usually be passed
        content = await request.content.read()
        serializer = context.contenttype_serializers[request.content_type]
        body_dict = serializer.load(content)
        for name, arginfo in parameters.body.items():
            if name in body_dict:
                args[name] = context.serializers.load(arginfo.type, body_dict[name])
            else:
                empty_args.append(arginfo)

    for name, arginfo in parameters.path.items():
        if name in request.match_info:
            args[name] = context.serializers.load(arginfo.type, request.match_info[name])
        else:
            empty_args.append(arginfo)

    required_params_not_passed = []

    for arg in empty_args:
        if arg.default is None:
            required_params_not_passed.append(arg.name)
        else:
            args[arg.name] = arg.default

    if len(required_params_not_passed) > 0:
        raise APIException(
            "required arguments {0} not passed".format(required_params_not_passed)
        )

    pos_args = []
    for arg in signature.args:
        pos_args.append(args[arg.name])
        del args[arg.name]
    return pos_args, args
