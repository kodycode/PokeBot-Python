from cogs import AdminCommands, NightVendorCommands, UserCommands


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
    await bot.add_cog(NightVendorCommands(bot))
    await bot.add_cog(UserCommands(bot))
    print("PokeBot online")
