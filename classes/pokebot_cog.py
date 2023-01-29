from discord.ext import commands


class PokeBotCog(commands.Cog):
    def __init__(self):
        super().__init__()
        print(f"Added {type(self).__name__} Cog")

    async def post_catch_cooldown_incomplete_msg(
        self,
        ctx: commands.Context, 
        e: Exception
    ) -> None:
        """
        Sends the exception message for when catch cooldown
        has not finished
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       f" please wait **{str(e)}** second(s) to catch" \
                       " another pokemon")

    async def post_daily_cooldown_incomplete_msg(
        self,
        ctx: commands.Context
    ) -> None:
        """
        Sends the exception message for when the daily cooldown
        hasn't passed yet for the user to claim the daily
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       f" you've already claimed the daily for today")

    async def post_higher_quantity_specified_exception_msg(
        self,
        ctx: commands.Context,
        e: Exception
    ) -> None:
        """
        Sends the exception message for when a higher quantity is
        specified over the max quantity of a pokemon to release
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       " please specify a pokemon quantity less than the" \
                       f" max pokemon quantity number: **{str(e)}**")

    async def post_higher_page_specified_exception_msg(
        self, 
        ctx: commands.Context,
        e: Exception
    ) -> None:
        """
        Sends the exception message for when a higher page is
        given than the max page for a trainer's inventory
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       " please specify a page number less than the" \
                       f" max page number: **{str(e)}**")

    async def post_improper_daily_shop_item_number_exception_msg(
        self,
        ctx: commands.Context,
        e: Exception
    ) -> None:
        """
        Sends the exception message for when an improper daily shop item
        is given (less than zero or higher than the number of available)
        daily shop items
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       " please specify an item from the daily shop menu" \
                       f" from **1** to **{str(e)}**")

    async def post_no_egg_count_msg(
        self,
        ctx: commands.Context,
        e: Exception
    ) -> None:
        """
        Sends the exception message for when theres no eggs to hatch
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       f" you have no {str(e)} eggs to hatch")

    async def post_not_enough_daily_shop_tokens_exception_msg(
        self,
        ctx: commands.Context,
        e: Exception
    ) -> None:
        """
        Sends the exception message for when not the trainer doesn't
        have enough daily shop tokens to spend on a daily shop item
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       f" you need **{str(e)}** daily tokens to buy this item")

    async def post_not_enough_exchange_pokemon_quantity_exception_msg(
        self,
        ctx: commands.Context
    ) -> None:
        """
        Sends the exception message for when not enough pokemon
        exists to exchange 
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       " please specify a valid amount of" \
                       " pokemon to exchange that have enough" \
                       " quantity to release")

    async def post_not_enough_exchange_pokemon_specified_exception(
        self,
        ctx: commands.Context
    ) -> None:
        """
        Sends the exception message for when not enough pokemon
        is specified to exchange
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       " please specify five pokemon to exchange")

    async def post_not_enough_lootbox_quantity_exception_msg(
        self,
        ctx: commands.Context,
        e: Exception
    ) -> None:
        """
        Sends the exception message for when there's no quantity available
        for a specified lootbox
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       " please make sure you have enough" \
                       f" {str(e)} lootboxes to open")

    async def post_page_quantity_too_low_msg(
        self,
        ctx: commands.Context
    ) -> None:
        """
        Sends the exception message for when a page number given
        is less than or equal to 0
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       " please specify an inventory page number greater" \
                       " than 0")

    async def post_release_quantity_too_low_msg(
        self,
        ctx: commands.Context
    ) -> None:
        """
        Sends the exception message for when a release quantity less
        than or equal to 0 is given by the user
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       " please specify a pokemon quantity greater than 0" \
                       " to release")

    async def post_too_many_exchange_pokemon_specified_exception_msg(
        self,
        ctx: commands.Context
    ) -> None:
        """
        Sends the exception message for when more than the minimum number
        of pokemon is specified to exchange
        """
        await ctx.send(f"{ctx.message.author.mention}," \
                       " please specify only 5 pokemon to exchange")

    async def post_unregistered_trainer_exception_msg(
        self, 
        ctx: commands.Context
    ) -> None:
        """
        Sends the exception message for an unregistered trainer
        """
        await ctx.send(f"{ctx.message.author.mention}," 
                       " hasn't set off on his journey to"
                       " catch 'em all yet. (Trainer must catch"
                       " a pokemon first in order to use this"
                       " bot command)"
        )
