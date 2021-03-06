# Built-in
import unittest

# The module we want to test
import blackjack

class TestBlackJack(unittest.TestCase):

    def test_build_deck(self):
        """
        Make sure that build_deck() generates exactly 52 unique cards
        """

        # Build a test deck.
        test_deck = blackjack.build_deck()

        # Need to set both of these to empty lists.
        card_list = []


        # Check if we have 52 cards
        if len(test_deck) == 52:

            # If so, populate card_list.
            for i in test_deck:
                card_list.append("{}-{}".format(i['suit'], i['value']))


            # Make card_list a set to get rid of duplicates.
            card_list = set(card_list)


        # If build_deck() works, there should be 52 cards total, and both
        # lists should have an equal number of elements.
        self.assertEqual(len(test_deck), 52)
        self.assertEqual(len(card_list), len(test_deck))



    def test_display_play_menu(self):
        """
        Displayer the Dealer's hand, the Player's hand, and the Play Menu
        """

        expected_dealer_hand = [{'suit': 'D', 'value': 'A'}]
        expected_player_hand = [{'suit': 'C', 'value': 'A'},{'suit': 'C', 'value': 10}]
        expected_money = 3000

        expected_output = []
        expected_output.append("Dealer's hand: 11")


        expected_output.append("{0}-{1}  ".format(expected_dealer_hand[0]["suit"], expected_dealer_hand[0]["value"]))
        expected_output.append("")

        expected_output.append("Your hand: 21")
        expected_output.append("{0}-{1}  {2}-{3}  ".format(expected_player_hand[0]["suit"], expected_player_hand[0]["value"],expected_player_hand[1]["suit"], expected_player_hand[1]["value"]))

        expected_output.append("")
        expected_output.append("")
        expected_output.append("Money: ${}".format(expected_money))

        expected_output.append("")
        #expected_output.append("1 - Hit")
        #expected_output.append("2 - Stand")
        #expected_output.append("q - Quit")
        #expected_output.append("")


        test_output = blackjack.display_play_menu(expected_dealer_hand, expected_player_hand, expected_money)
        self.assertEqual(test_output, expected_output)





    def test_display_title_menu(self):
        """
        Basically a clone of the display_title_menu function.
        Insures that the output is properly displayed to the user
        """

        expected_title = []
        expected_title.append("Welcome to Blackjack!")
        expected_title.append("")
        expected_title.append("1 - Play game")
        expected_title.append("q - Exit")
        expected_title.append("")

        test_title = blackjack.display_title_menu()

        self.assertEqual(test_title, expected_title)



    def test_remove_from_deck(self):
        """
        Iterates over the cards in a deck and removes them from the deck.
        Returns the modified deck
        """

        hand = [{'suit': 'S', 'value': 'A'}, {'suit': 'D', 'value': 10}]
        deck = blackjack.build_deck()
        deck = blackjack.remove_from_deck(deck, hand)

        # After the operation, there should only be 50 cards left
        self.assertEqual(len(deck), 50)

        # This time, the deck is down to the last 2 cards
        hand = [{'suit': 'S', 'value': 'A'}, {'suit': 'D', 'value': 10}]
        deck = [{'suit': 'S', 'value': 'A'}, {'suit': 'D', 'value': 10}]
        deck = blackjack.remove_from_deck(deck, hand)

        # This time, a new deck should have been generated, so there should be
        # 52 cards.
        self.assertEqual(len(deck), 52)




    def test_draw_card(self):
        """
        Draw cards from a virtual deck.
        If the card exists, this function adds the card to the specified hand
        and returns it.
        This function DOES NOT modify the deck.
        """

        # Build a new deck
        deck = blackjack.build_deck()

        # Set up the hand
        hand = []

        # Draw a card
        card = {'suit': 'S', 'value': 'A'}
        hand = blackjack.draw_card(deck,hand,card)

        # See if the card is in the hand
        self.assertEqual(hand, [{'suit': 'S', 'value': 'A'}])

        # Add another card
        card = {'suit': 'D', 'value': 10}
        hand = blackjack.draw_card(deck,hand,card)

        # See if the hand contains both cards
        self.assertEqual(hand, [{'suit': 'S', 'value': 'A'}, {'suit': 'D', 'value': 10}])


    def test_compare_scores(self):
        """
        Compare scores to see which is higher.
        First one is the player, second one is the dealer.
        Supposed to return a list with 2 elements.
        0 means loss, 1 means win.
        2 means bust.
        """
        self.assertEqual(blackjack.compare_scores(21, 16), [1,0])
        self.assertEqual(blackjack.compare_scores(16, 21), [0,1])
        self.assertEqual(blackjack.compare_scores(22, 16), [2,1])
        self.assertEqual(blackjack.compare_scores(22, 22), [2,2])
        self.assertEqual(blackjack.compare_scores(19, 19), [1,1])

    def test_add_cards(self):
        """
        Adds up a list of cards and displays a point total.
        Aces can be 1 or 11.
        All other face cards are 10.
        """
        hand = []
        hand.append({'suit': 'S','value': 'A'})
        hand.append({'suit': 'C','value': 10 })
        self.assertEqual(blackjack.add_cards(hand), 21)

        hand = []
        hand.append({'suit': 'S','value': 'A'})
        hand.append({'suit': 'C','value': 'K'})
        self.assertEqual(blackjack.add_cards(hand), 21)


        hand = []
        hand.append({'suit': 'S','value': 'J'})
        hand.append({'suit': 'C','value': 'Q'})
        self.assertEqual(blackjack.add_cards(hand), 20)

        hand = []
        hand.append({'suit': 'S','value': 'A'})
        hand.append({'suit': 'C','value': 10})
        hand.append({'suit': 'D','value': 5})
        self.assertEqual(blackjack.add_cards(hand), 16)

#    def test_divide(self):
#        self.assertEqual(calc.divide(10, 5), 2)
#        self.assertEqual(calc.divide(-1, 1), -1)
#        self.assertEqual(calc.divide(-1, -1), 1)
#
#        # Detect floor division
#        self.assertEqual(calc.divide(5, 2), 2.5)
#
#        # Test if division by zero raises the correct error
#        #self.assertRaises(ValueError, calc.divide, 10, 0)
#
#        # Context manager that does the same thing
#        with self.assertRaises(ValueError):
#            calc.divide(10,0)


# Allow tests to be run with 'python test_calc.py'
if __name__ == '__main__':
    unittest.main()
