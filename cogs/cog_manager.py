from cogs.pokemon import PokemonCommands


def setup(bot):
    bot.add_cog(PokemonCommands(bot))
    print("PokeBot online.")
