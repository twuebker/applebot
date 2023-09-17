import coc


async def print_war(tag):
    async with coc.Client() as coc_client:
        try:
            war = await coc_client.get_current_war(tag)
            return f"{war.clan_tag} is currently in {war.state} state."
        except coc.privatewarlog:
            return "uh oh, they have a private war log!"


