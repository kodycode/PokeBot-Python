from cogs.modules.pokemon_functionality import PokemonFunctionality
from discord.ext import commands


class PokemonCommands:
    """Handles Pokemon related commands"""

    def __init__(self, bot):
        self.cmd_function = PokemonFunctionality(bot)

    @commands.command(name='give', pass_context=True, hidden=True)
    async def give(self, ctx, user_id, pkmn_name, shiny=False):
        """
        Gives a pokemon to a trainer (admin only cmd)

        @param ctx - context of the command sent
        @param user_id - user to give pokemon to
        @param pkmn_name - name of the pokemon to give to user
        @param shiny - 's' or 'shiny' if shiny
        """
        await self.cmd_function.give_trainer_pokemon(ctx,
                                                     user_id,
                                                     pkmn_name,
                                                     shiny)

    @commands.command(name='delete', pass_context=True, hidden=True)
    async def delete(self, ctx, user_id, pkmn_name, shiny=False):
        """
        Deletes a pokemon from the trainer (admin only cmd)

        @param ctx - context of the command sent
        @param user_id - user to give pokemon to
        @param pkmn_name - name of the pokemon to delete from the user
        @param shiny - 's' or 'shiny' if shiny
        """
        await self.cmd_function.delete_trainer_pokemon(ctx,
                                                       user_id,
                                                       pkmn_name,
                                                       shiny)

    @commands.command(name='giveloot', pass_context=True, hidden=True)
    async def giveloot(self, ctx, user_id, lootbox):
        """
        Deletes a pokemon from the trainer (admin only cmd)

        @param ctx - context of the command sent
        @param user_id - user to give pokemon to
        @param lootbox - lootbox to give to the user
        """
        await self.cmd_function.give_trainer_lootbox(ctx,
                                                     user_id,
                                                     lootbox)

    @commands.command(name='deleteloot', pass_context=True, hidden=True)
    async def deleteloot(self, ctx, user_id, lootbox):
        """
        Deletes a pokemon from the trainer (admin only cmd)

        @param ctx - context of the command sent
        @param user_id - user to give pokemon to
        @param lootbox - lootbox to remove
        """
        await self.cmd_function.delete_trainer_lootbox(ctx,
                                                       user_id,
                                                       lootbox)

    @commands.command(name='reload', pass_context=True, hidden=True)
    async def reload(self, ctx):
        """
        Reloads pokemon data (admin only cmd)
        """
        await self.cmd_function.reload_data(ctx)

    @commands.command(name='catch', pass_context=True)
    async def catch(self, ctx):
        """
        Catches a random pokemon

        @param ctx - context of the command sent
        """
        await self.cmd_function.catch_pokemon(ctx)

    @commands.command(name='c', pass_context=True, hidden=True)
    async def c(self, ctx):
        """
        Shortcut to catch a random pokemon

        @param ctx - context of the command sent
        """
        await self.cmd_function.catch_pokemon(ctx)

    @commands.command(name='inventory', pass_context=True)
    async def pinventory(self, ctx, page_number=0):
        """
        Displays the trainer's pokemon inventory

        @param ctx - context of the command sent
        @param page_number - page number in inventory
        """
        await self.cmd_function.display_pinventory(ctx, page_number)

    @commands.command(name='i', pass_context=True, hidden=True)
    async def i(self, ctx, page_number=0):
        """
        Shortcut to display inventory

        @param ctx - context of the command sent
        @param page_number - page number in inventory
        """
        await self.cmd_function.display_pinventory(ctx, page_number)

    @commands.command(name='gif')
    async def gif(self, pkmn_name: str, shiny=None):
        """
        Display a gif of the pokemon

        @param pkmn_name - name of the pokemon to find a gif of
        @param shiny - specify if pkmn is shiny or not
        """
        await self.cmd_function.display_gif(pkmn_name, shiny)

    @commands.command(name='profile')
    async def profile(self, trainer):
        """
        Obtains the profile of a trainer specified

        @param trainer - trainer profile to search for
        """
        await self.cmd_function.display_trainer_profile(trainer)

    @commands.command(name='ranking')
    async def ranking(self, option="t"):
        """
        Displays ranking of all the trainers

        @param option - options are:
                        l - legendary
                        s - shiny
                        t - total (default)
                        u - ultra
        """
        await self.cmd_function.display_ranking(option)

    @commands.command(name='release', pass_context=True)
    async def release(self, ctx, pkmn: str, quantity=1):
        """
        Releases a pokemon from your inventory

        @param pkmn - pkmn to be released
        """
        await self.cmd_function.release_pokemon(ctx, pkmn, quantity)

    @commands.command(name='r', pass_context=True, hidden=True)
    async def r(self, ctx, pkmn: str, quantity=1):
        """
        Shortcut to release pokemon from your inventory

        @param pkmn - pkmn to be released
        """
        await self.cmd_function.release_pokemon(ctx, pkmn, quantity)

    @commands.command(name='hatch', pass_context=True)
    async def hatch(self, ctx):
        """
        Hatches an egg from your inventory

        @param pkmn - pkmn to be released
        """
        await self.cmd_function.hatch_egg(ctx)

    @commands.command(name='h', pass_context=True, hidden=True)
    async def h(self, ctx):
        """
        Shortcut to hatch an egg from your invertory

        @param pkmn - pkmn to be released
        """
        await self.cmd_function.hatch_egg(ctx)

    @commands.command(name='fuse', pass_context=True)
    async def fuse(self, ctx, pkmn, *args):
        """
        Fuses all type-specific forms of a pokemon to get the original

        @param pkmn - pokemon to fuse into
        @param args - enter 5 pokemon to fuse to get to the original
                      (valid for only pokemon with over 5 known forms)
        """
        await self.cmd_function.fuse_pokemon(ctx, pkmn, args)

    @commands.command(name='f', pass_context=True, hidden=True)
    async def f(self, ctx, pkmn, *args):
        """
        Shortcut to fuse all type-specific forms of a pokemon
        to get the original

        @param pkmn - pokemon to fuse into
        """
        await self.cmd_function.fuse_pokemon(ctx, pkmn, args)

    @commands.command(name='exchange', pass_context=True)
    async def exchange(self, ctx, *args):
        """
        Exchanges 5 pokemon for a pokemon with a 5x shiny chance

        @param pkmn - pkmn to be released
        """
        await self.cmd_function.exchange_pokemon(ctx, args)

    @commands.command(name='e', pass_context=True, hidden=True)
    async def e(self, ctx, *args):
        """
        Shortcut to exchange 5 pokemon for a pokemon with a 5x shiny chance

        @param pkmn - pkmn to be released
        """
        await self.cmd_function.exchange_pokemon(ctx, args)

    @commands.command(name='open', pass_context=True)
    async def open(self, ctx, lootbox: str):
        """
        Opens a lootbox in the inventory

        @param lootbox - choices are:
                         b - bronze
                         s - silver
                         g - gold
                         l - legendary
        """
        await self.cmd_function.open_lootbox(ctx, lootbox)

    @commands.command(name='o', pass_context=True, hidden=True)
    async def o(self, ctx, lootbox: str):
        """
        Shortcut to open a lootbox in the inventory

        @param lootbox - choices are:
                         b - bronze
                         s - silver
                         g - gold
                         l - legendary
        """
        await self.cmd_function.open_lootbox(ctx, lootbox)

    @commands.command(name='loot', pass_context=True)
    async def loot(self, ctx):
        """
        Displays the number of lootboxes the trainer has
        """
        await self.cmd_function.display_lootbox_inventory(ctx)

    @commands.command(name='l', pass_context=True, hidden=True)
    async def l(self, ctx):
        """
        Shortcut to display the number of lootboxes the trainer has
        """
        await self.cmd_function.display_lootbox_inventory(ctx)

    @commands.command(name='vendor', pass_context=True)
    async def vendor(self, ctx, option: str):
        """
        Command to communicate with the night vendor

        @param options - options include:
                         i - info to see what's for sale
                         r - re-roll what's for sale
                         t - trade the vendor
        """
        await self.cmd_function.vendor_options(ctx, option)

    @commands.command(name='v', pass_context=True, hidden=True)
    async def v(self, ctx, option: str):
        """
        Shortcut to communicate with the night vendor

        @param options - options include:
                         i - info to see what's for sale
                         r - re-roll what's for sale
                         t - trade the vendor
        """
        await self.cmd_function.vendor_options(ctx, option)

    @commands.command(name='daily', pass_context=True)
    async def daily(self, ctx):
        """
        Claim a daily lootbox as well as a daily token
        """
        await self.cmd_function.claim_daily(ctx)

    @commands.command(name='gift', pass_context=True)
    async def gift(self, ctx):
        """
        Claims an available gift
        """
        await self.cmd_function.claim_gift(ctx)

    @commands.command(name='d', pass_context=True, hidden=True)
    async def d(self, ctx):
        """
        Shortcut to claim a daily lootbox as well as a daily token
        """
        await self.cmd_function.claim_daily(ctx)
