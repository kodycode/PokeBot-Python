from cogs import AdminCommands, DailyCommands, InventoryCommands, MiscCommands, NightVendorCommands, PokeBotTasks


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
    await bot.add_cog(DailyCommands(bot))
    await bot.add_cog(InventoryCommands(bot))
    await bot.add_cog(MiscCommands(bot))
    await bot.add_cog(NightVendorCommands(bot))
    await bot.add_cog(PokeBotTasks(bot))
    print("PokeBot online")
