from cogs import AdminCommands, DailyCommands, InventoryCommands, MiscCommands, NightVendorCommands 


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
    await bot.add_cog(DailyCommands(bot))
    await bot.add_cog(InventoryCommands(bot))
    await bot.add_cog(MiscCommands(bot))
    await bot.add_cog(NightVendorCommands(bot))
    print("PokeBot online")
