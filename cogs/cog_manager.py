from cogs.pokemon import PokemonCommands


async def setup(bot):
    await bot.add_cog(PokemonCommands(bot))
    print("PokeBot online")
