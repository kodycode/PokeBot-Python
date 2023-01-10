def get_ctx_user_id(ctx):
    """
    Gets context author user_id returned as string
    """
    return str(ctx.message.author.id)
