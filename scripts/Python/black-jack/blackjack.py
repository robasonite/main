# Copyright 2020 Robert Kight
#
# A small text-based blackjack game.
# NOTE: This program is just for fun. No real world money is won or lost.
import secrets
import os
# A simple blackjack game


def draw_card(deck, hand, card):
    if card in deck:
        hand.append(card)

    return hand


def remove_from_deck(deck, hand):
    for c in hand:

        # Check if the card is in the deck first
        if c in deck:
            deck.remove(c)

    # Prevent deck depletion
    if len(deck) == 0:
        deck = build_deck()

    return deck


def build_deck():
    suits = ['D','C','H','S']
    values = [1,2,3,4,5,6,7,8,9,10,'J','Q','K','A']
    deck = []

    for s in suits:
        for v in values:
            card = {'suit': s, 'value': v}
            deck.append(card)

    return deck


def compare_scores(a,b):

    # Double bust
    if a > 21 and b > 21:
        return [2,2]

    else:
        if a < 22 and b < 22:

            # Draw
            if a == b:
                return [1,1]

            # Player wins
            elif a > b:
                return [1,0]

            # Player loses
            elif a < b:
                return [0,1]

        # Player busts and loses
        elif a > 21:
            return [2,1]

        # Dealer busts and player loses
        elif b > 21:
            return [1,2]




def add_cards(cards):
    total = 0
    ace = False
    for c in cards:
        # Check if the value is a string.
        value = c["value"]
        if isinstance(value, str):
            if value == 'A':

                # If an Ace was already counted, increase total by 1.
                if ace == False:
                    total += 11
                    ace = True

                # If this is the first ace, add 11 and set 'ace' to true.
                else:
                    total += 1

            # For all other face cards, add 10:
            else:
                total += 10

        # If not, it must be an int, so add it:
        else:
            total += value

    # Before returning the total, see if it's over 21
    if total > 21 and ace == True:
        total -= 10
    return total

def display_title_menu():
    title = []
    title.append("Welcome to Blackjack!")
    title.append("")
    title.append("1 - Play game")
    title.append("q - Exit")
    title.append("")

    return title


def display_play_menu(dealerHand,playerHand,playerMoney):
    # Get the point value for both hands
    playerScore = add_cards(playerHand)
    dealerScore = add_cards(dealerHand)

    menu = []

    # Display dealer's hand
    menu.append("Dealer's hand: {}".format(dealerScore))
    handString = ""
    for d in dealerHand:
        handString += "{0}-{1}  ".format(d["suit"], d["value"])

    menu.append(handString)
    menu.append("")

    # Display player's hand
    menu.append("Your hand: {}".format(playerScore))
    handString = ""
    for p in playerHand:
        handString += "{0}-{1}  ".format(p["suit"], p["value"])

    menu.append(handString)

    # Player's money
    menu.append("")
    menu.append("")
    menu.append("Money: ${}".format(playerMoney))
    menu.append("")

    # Display option menu
    #menu.append("")
    #menu.append("1 - Hit")
    #menu.append("2 - Stand")
    #menu.append("q - Quit")
    #menu.append("")

    return menu




#print(build_deck())

# The main game loop
def gameLoop(Deck, PlayerMoney, PlayerHand, DealerHand):
    user_input = ""

    # Set up initial hands
    PlayerHand = draw_card(Deck,PlayerHand,secrets.choice(Deck))
    DealerHand = draw_card(Deck,DealerHand,secrets.choice(Deck))

    # Update the deck
    Deck = remove_from_deck(Deck, PlayerHand)
    Deck = remove_from_deck(Deck, DealerHand)

    # Track whether the user is standing
    userStanding = False

    # Track whether the dealer is standing
    dealerStanding = False

    # Track the hand scores
    playerScore = 0
    dealerScore = 0

    resultMessage = ""
    roundOver = False

    while user_input != "q":
        os.system("clear")

        # Display current game status
        play_screen = display_play_menu(DealerHand, PlayerHand, PlayerMoney)
        for line in play_screen:
            print(line)


        # If the player isn't standing, it's their turn
        if userStanding == False and roundOver == False:

            # Player menu
            print("1 - Hit")
            print("2 - Stand")
            print("q - Quit")
            print("")

            # Get input from users
            user_input = input("> ")

            # Player draws card when Hit is selected
            if user_input == "1":
                PlayerHand = draw_card(Deck,PlayerHand,secrets.choice(Deck))
                Deck = remove_from_deck(Deck, PlayerHand)
                playerScore = add_cards(PlayerHand)

                # If the player's hand score is greater 20, the user must stand.
                if playerScore > 20:
                    userStanding = True


            # If the user chooses to stand, it's the Dealer's turn
            elif user_input == "2":
                userStanding = True

        # Dealer's turn
        elif dealerStanding == False and roundOver == False:
            dealerScore = add_cards(DealerHand)

            # If the Player busts or has 21, there's no point in drawing
            if playerScore > 20:
                dealerStanding = True

            elif dealerScore < playerScore and dealerScore < 21:
                DealerHand = draw_card(Deck, DealerHand, secrets.choice(Deck))
                Deck = remove_from_deck(Deck, DealerHand)

            # The Dealer's turn is over
            else:
                dealerStanding = True

        # After both Dealer and Player have ended their turns, evaluate the
        # results.
        elif dealerStanding == True and userStanding == True and roundOver == False:
            results = compare_scores(playerScore, dealerScore)

            if results == [1,0]:
                resultMessage = "Round won!"
                PlayerMoney += 100
            elif results == [0,1]:
                resultMessage = "Round lost!"
                PlayerMoney -= 100
            elif results == [2,1]:
                resultMessage = "Bust! Round lost!"
                PlayerMoney -= 100
            elif results == [1,2]:
                resultMessage = "Dealer busts! Round won!"
                PlayerMoney += 100
            elif results == [2,2]:
                resultMessage = "DOUBLE BUST!"
            elif results == [1,1]:
                resultMessage = "Push!"
            
            roundOver = True

        elif roundOver == True:
            print(resultMessage)

            # Print a new options menu for the player
            print("")
            print("1 - New round")
            print("q - Quit")
            print("")
            user_input = input("> ")

            # If the user wants to continue, set up new round
            if user_input == "1":
                # Set up new hands
                PlayerHand = []
                DealerHand = []
                PlayerHand = draw_card(Deck,PlayerHand,secrets.choice(Deck))
                DealerHand = draw_card(Deck,DealerHand,secrets.choice(Deck))

                # Update the deck
                Deck = remove_from_deck(Deck, PlayerHand)
                Deck = remove_from_deck(Deck, DealerHand)

                # Set both standing values to false so play can continue
                userStanding = False
                dealerStanding = False
                roundOver = False
                resultMessage = ""


    # When the loop is broken, quit game
    print("Goodbye!")


# Run game
def startGame():
    Deck = build_deck()
    PlayerMoney = 1000
    PlayerHand = []
    DealerHand = []

    # Display the title screen
    os.system("clear")

    title = display_title_menu()
    for line in title:
        print(line)

    user_input = input("> ")

    # If the player chooses "Quit", exit.
    if (user_input == "q"):
        print("Goodbye!")

    elif (user_input == "1"):
        # If the player chooses Play, start game loop.
        gameLoop(Deck, PlayerMoney, PlayerHand, DealerHand)

# If the program is run like 'python blackjack.py', start the game.
if __name__ == '__main__':
    startGame()

# Else, the program is being tested.
