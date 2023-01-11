class TrainerDAO:
    """
    Accesses, modifies and returns the PokeBot JSON data
    """
    def get_trainer_pokemon_inventory(self) -> dict:
        """
        Gets the inventory of pokemon from the trainer
        """

    def get_trainer_last_catch_time(self) -> float:
        """
        Gets the last catch time of the trainer
        """

    def get_trainer_last_daily_redeemed_time(self) -> float:
        """
        Gets the last daily redeemed time of the trainer
        """

    def get_trainer_lootbox_inventory(self) -> dict:
        """
        Gets the inventory of lootboxes that the trainer has
        """

    def get_trainer_daily_tokens(self) -> int:
        """
        Gets the list of daily tokens that the trainer has
        """

    def set_pokemon_inventory(self, pkmn_name: str, quantity: int) -> None:
        """
        Sets the quantity of a specific trainer's pokemon
        within their inventory
        """

    def set_trainer_last_catch_time(self, time: float) -> None:
        """
        Sets the trainer's last daily redeemed time
        """

    def set_trainer_last_daily_redeemed_time(self, time: float) -> None:
        """
        Sets the trainer's last daily redeemed time
        """

    def set_lootbox_inventory(self, lootbox_tier_name: str, quantity: int) -> None:
        """
        Sets the quantity of a specific lootbox tier within
        the trainer's inventory
        """

    def set_daily_tokens(self, quantity: int) -> None:
        """
        Sets the trainer's daily token amount
        """
