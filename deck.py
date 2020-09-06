import random

# Deck Object to build UNO Card deck
class Deck:

    def __init__(self):
        self.cards = []
        self.build()


    def build(self):
        """Function to build the UNO Card deck
        """
        colors = ['Red', 'Green', 'Yellow', 'Blue']
        values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'Draw Two', 'Skip', 'Reverse']
        wild_cards = ['Wild', 'Wild Draw Four']

        for color in colors:
            for val in values:
                card_num = f'{color} {val}'
                self.cards.append(card_num)
                if not val == 0:
                    self.cards.append(card_num)
        count = 0
        while count < 4:
            for wild in wild_cards:
                self.cards.append(wild)
            count += 1

    def shuffle_cards(self):
        """Function to shuffle the UNO Cards
        """
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            # Shuffling the cards position
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def show(self):
        """Function to show the UNO Cards
        """
        print(self.cards)

    def draw_cards(self, num_cards):
        """Function to draw card from the UNO Card deck
        """
        selected_cards = []

        for x in range(num_cards):
            selected_cards.append(self.cards.pop(0))
        return selected_cards


def show_player_hand(player_num, player_cards):
    """Function to print out the player's cards

    Args:
        player_num (int): The index of the player on the player list
        player_cards (list): The card list for the player

    """
    print(f'----------   Player #{player_num + 1}   ----------\n\nYou have the following cards:\n')

    count = 1

    for card in player_cards:
        print(f'\t{count}.  {card}')
        count += 1
    print(' ')


def can_card_play(card_color, card_value, player_cards):
    """To check if there is any card on hand can be played on certain round.

    Args:
        card_color (str): The color of the card
        card_value (str): The value of the card
        player_cards(list): The card list of one player

    Return:
        bool: If there is a card can be played on that round, it will return True. Otherwise, False

    """
    for card in player_cards:
        if card.startswith('Wild'):
            return True
        elif card_color in card or card_value in card:
            return True

    return False


def main():
    print('++++++++++   WELCOME TO THE UNO GAME   ++++++++++\n')

    uno_deck = Deck()
    uno_deck.shuffle_cards()
    uno_deck.shuffle_cards()

    # A list of card that is being displayed
    display_cards = []

    players_cards = list()

    players_counts = int(input('How many players are there? '))

    # To limit the number of players
    while players_counts < 2 or players_counts > 5:
        players_counts = int(input('Error. You have to enter a number between 2-5 only. How many players are there? '))

    for player in range(players_counts):
        player_cards = uno_deck.draw_cards(5)
        players_cards.append(player_cards)

    # Start from the first player on the list
    player_turn = 0
    game_direction = 1
    still_can_play = True

    # Grab the first card from UNO deck
    display_cards.append(uno_deck.cards.pop(0))

    # Split the first display card value
    split_display_card = display_cards[-1].split(' ', 1)
    display_card_color = split_display_card[0]
    if display_card_color.startswith('Wild'):
        display_card_value = '- Any color or value is acceptable'
    else:
        display_card_value = split_display_card[1]

    # Game starts here
    print('\n**********   Game Started   **********\n')

    while still_can_play:
        # First show the player their cards
        show_player_hand(player_turn, players_cards[player_turn])

        print(f'Card on display is: {display_cards[-1]}')

        # If there is any card that they can play
        if can_card_play(display_card_color, display_card_value, players_cards[player_turn]):
            chosen_card = int(input('Please key-in the card number that you wish to play in this round. '))
            while chosen_card < 1 or chosen_card > len(players_cards[player_turn]):
                chosen_card = int(
                    input(f'Please key-in the card number between 1 to {len(players_cards[player_turn])}:  '))
            # To check if the chosen card is the right card
            while not can_card_play(display_card_color, display_card_value,
                                    [players_cards[player_turn][chosen_card - 1]]):
                chosen_card = int(input('Error. Please key-in the card number that you wish to play in this round. '))
                # Check if the user enter the right number
                while chosen_card < 1 or chosen_card > len(players_cards[player_turn]):
                    chosen_card = int(
                        input(f'Please key-in the card number between 1 to {len(players_cards[player_turn])}'))

            print(f'\nPlayer #{player_turn + 1} played {players_cards[player_turn][chosen_card - 1]} \n')
            # Put the card on the display cards pile
            display_cards.append(players_cards[player_turn].pop(chosen_card - 1))

            # Check if the player has no more card after their action on the round
            if len(players_cards[player_turn]) == 0:
                still_can_play = False
                winner_player = f'***** Player {player_turn + 1}  has won *****'

            else:
                # To check if the next card is a special card
                split_card = display_cards[-1].split(' ', 1)
                display_card_color = split_card[0]

                card_color_list = ['Red', 'Green', 'Yellow', 'Blue']

                # When it is only 'Wild'
                if len(split_card) == 1:
                    # When the card is only Wild
                    display_card_value = 'Any'
                else:
                    display_card_value = split_card[1]

                # When card is a Wild card
                if display_card_color == 'Wild':
                    print('List of Color Available: ')
                    for i in range(len(card_color_list)):
                        print(f'\t{i + 1}) {card_color_list[i]}')
                    updated_color = int(input('Which color you want to choose? '))
                    while updated_color < 1 or updated_color > len(card_color_list):
                        updated_color = int(
                            input(
                                f'Please enter the color number between 1 to {len(card_color_list)}. Enter here again: '))
                    print(f'You have chosen {card_color_list[updated_color - 1]} color. ')
                    display_card_color = card_color_list[updated_color - 1]
                    display_cards[-1] = display_card_color + ' ' + display_card_value

                # Other special card
                if display_card_value == 'Reverse':
                    # Change the direction of the turn - to switch direction
                    game_direction = game_direction * -1
                elif display_card_value == 'Draw Two':
                    # Get the next player in line
                    next_player = player_turn + game_direction

                    if next_player >= players_counts:
                        next_player = 0
                    elif next_player < 0:
                        next_player = players_counts - 1

                    players_cards[next_player].extend(uno_deck.draw_cards(2))

                elif display_card_value == 'Draw Four':
                    # Get the next player in line
                    next_player = player_turn + game_direction
                    if next_player >= players_counts:
                        next_player = 0
                    elif next_player < 0:
                        next_player = players_counts - 1

                    players_cards[next_player].extend(uno_deck.draw_cards(4))

                elif display_card_value == 'Skip':
                    # Add one more player turn
                    player_turn += game_direction

                    if player_turn >= players_counts:
                        player_turn = 0
                    elif player_turn < 0:
                        player_turn = players_counts - 1



        else:
            print('\nSorry, you can\'t play this round. You can only draw a card.')

            players_cards[player_turn].extend(uno_deck.draw_cards(1))

        print('\n+++++++++++++++++      NEXT PLAYER      +++++++++++++++++\n')

        player_turn += game_direction

        if player_turn >= players_counts:
            player_turn = 0
        elif player_turn < 0:
            player_turn = players_counts - 1

    print(' ')
    print('_________GAME OVER_________')
    print(f'The winner of this game is {winner_player}')


main()
