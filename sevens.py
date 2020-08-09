# Laying Out Sevens
# 排七

import random


def main():
    print("WELCOME TO SEVENS!")
    selection()


def selection():
    """
    Displays the game menu and ask the user whether they would play game or exit.
    """

    print("======MENU======")
    print("1) Play game")
    print("2) Exit")
    print("================\n")

    status = 0
    while not (status in [1, 2]):
        status = int(input("Enter your choice: "))

    if status == 1:
        game()
    else:
        print("Goodbye!")


def game():
    """
    The main game.
    """

    deck = genDeck()  # Generates the game deck
    # print(deck)

    players_cards = ["", "", "", ""]  # Storing the cards in hand of 4 players
    sevens_pos = []  # Storing the position of the 4 SEVENS

    for i in range(4):
        players_cards[i], deck = distributeCards(deck)
        # print("Player", i + 1, ":", end=" ")

        #printDeck(players_cards[i])  # Prints the cards in a human reading-friendly way

        for card in range(13):
            number = players_cards[i][card][1]

            if number == 6:  # Index of sevens is 6
                sevens_pos.append([i, card])

        #print("\n\n")

    # Take away Sevens from players
    for x in range(3, -1, -1):
        players_cards[sevens_pos[x][0]].pop(sevens_pos[x][1])

    # Starting rounds

    winning_status = [False, False, False, False]  # Winning status of each player
    passes = [0, 0, 0, 0]  # Number of passes of each player
    cards_on_table = initializeCardsOnTable()  # Initial status of the table
    cards_in_hand = []  # Number of cards in each player's hand
    for i in range(4):
        cards_in_hand.append(len(players_cards[i]))



    turn = 0  # Initial turn: Player 1's turn
    while not (winning_status[0] or winning_status[1] or winning_status[2] or winning_status[3]):
        # Take turns while none of the players win

        displayTableCards(cards_on_table)

        print("Player {}'s turn".format(turn))

        if turn == 0:  # Player's turn
            print("Cards in hand:", end=" ")
            printDeck(players_cards[turn])
            #print(players_cards[turn])
            print("\n")

            # Check for cards on player's hand that can be placed on the table
            placeable_cards = checkAvailable(players_cards[turn], cards_on_table)
            print("Placeable cards: ", end=" ")
            printDeck(placeable_cards)

            # Ask the player which card to place (if there are placeable cards)
            if len(placeable_cards) >= 1:

                # Ask the player whether they would place a card or pass the round
                pass_or_place = -1
                while not (pass_or_place in [1, 2]):
                    print("\nWould you like to place a card or pass this round?")
                    print("1) Place a card\t\t2) Pass this round")

                    pass_or_place = int(input(">> "))


                if pass_or_place == 1:      # Place a card

                    players_choice = 0
                    while not (1 <= players_choice <= len(placeable_cards)):
                        players_choice = int(input("Which card would you like to place on the table? "))

                    # Place the card on the table
                    suit_chosen = placeable_cards[players_choice - 1][0]        # Suit of the card to be placed
                    number_chosen = placeable_cards[players_choice - 1][1]      # Number of the card to be placed

                    cards_on_table = placeCard(cards_on_table, suit_chosen, number_chosen)
                    # print(cards_on_table)
                    print("Card placed.")


                    # Remove the card on player's hand


                else:                       #
                    print("")


            #else:   # No placeable cards

            break   # delete later

        # else:           # Bots' turn

        # Check number of cards in hand of each player
        for i in range(4):
            if cards_in_hand[i] == 0:
                winning_status[i] = True

        # After checking the winning status of each player, decides whether the game should continue
        if not (winning_status[0] or winning_status[1] or winning_status[2] or winning_status[3]):
            if turn != 3:
                turn += 1
            else:
                turn = 0


def checkAvailable(cards_on_hand, cards_on_table):
    """
    Looks for the cards that can be placed based on the cards on the table.
    """

    available_cards = []    # This will store the cards that can be placed on table
    choice_of_cards = []    # This will store the cards on player's hand that can be placed on table

    #print("Cards on the table: ", cards_on_table)

    # Look for cards that can be placed on table
    for suit in range(4):
        for number in range(13):
            if 1 <= number <= 11:       # Check adjacent indices for indices 1 to 11
                if (cards_on_table[suit][number + 1] == 1) or (cards_on_table[suit][number - 1] == 1):
                    available_cards.append([suit, number])

            elif number == 0:
                if cards_on_table[suit][number + 1] == 1:
                    available_cards.append([suit, number])

            else:
                if cards_on_table[suit][number - 1] == 1:
                    available_cards.append([suit, number])

    #print("AVAILABLE CARDS: ", available_cards)

    # Look for the cards that the user can place on the table
    for card in range(len(cards_on_hand)):
        if cards_on_hand[card] in available_cards:
            choice_of_cards.append(cards_on_hand[card])


    #print("Choice of cards: ", choice_of_cards)

    return choice_of_cards


def placeCard(cards_on_table, suit, number):
    """
    Places a card on the table.
    """

    cards_on_table[suit][number] = 1

    return cards_on_table


def displayTableCards(cards):
    suits = ("Spades", "Hearts", "Clubs", "Diamonds")
    numbers = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

    print("Cards on table: ")

    for i in range(4):
        print(suits[i])

        for j in range(13):
            if cards[i][j] == 1:
                print(numbers[j], end=" ")
            else:
                print(" ", end=" ")

        print("\n")


def initializeCardsOnTable():
    """
    Initializes the cards on table (Only Seven of each suit on the table).
    """

    cards_on_table = []

    for suit in range(4):
        suit_list = []

        for number in range(13):
            if number == 6:
                suit_list.append(1)
            else:
                suit_list.append(0)

        cards_on_table.append(suit_list)

    return cards_on_table


def printDeck(deck):
    """
    Prints the deck in a human reading-friendly way.
    """

    for card in range(len(deck)):
        suit = deck[card][0]
        number = deck[card][1]

        display_name = printCard(suit, number)
        print(display_name, end="\t")


def printCard(suit, number):
    """
    This function converts the suit index and number into a human reading-friendly format.

    Input: Suit index and number index of the card
    Output: The human reading-friendly format of the card (e.g. Clubs King, Heart 3)
    """

    if suit == -1 and number == -1:
        return "Empty"

    else:
        display_name = ""

        suit_name = ("Spades", "Hearts", "Clubs", "Diamonds")
        number_name = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

        display_name = suit_name[suit] + " " + number_name[number]

        return display_name


def distributeCards(deck):
    """
    This function randomly selects 13 cards from the deck.

    Input: A deck of cards
    Output: 13 randomly selected cards and the deck without the 13 cards.
    """

    selected_cards = []  # This list will store the 13 randomly selected cards

    for i in range(13):
        card_already_selected = True
        while card_already_selected:
            suit = getRandomNum(0, 3)
            card_number = getRandomNum(0, 12)

            if deck[suit][card_number] == 1:
                # 1 means that the card is not yet distributed to any player
                card_already_selected = False

                selected_cards.append([suit, card_number])
                deck[suit][card_number] = 0

    return selected_cards, deck


def genDeck():
    """
    Generates the deck.
    """

    deck = []

    for suit in range(4):
        suit_cards = []  # Storing cards of the same suit
        for card in range(13):
            suit_cards.append(1)  # 1 means that the card is not taken by any player

        deck.append(suit_cards)

    return deck


def getRandomNum(minimum, maximum):
    """Returns a random integer from range(minimum, maximum). """
    return random.randint(minimum, maximum)


# main()
game()
