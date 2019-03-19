""" 
Blackjack
Player vs. Computer (Dealer)
Winner- higer total value and <= 21.
Each speacial card equal to 10, Ace equalto 11 or 1.

Taly Kishon                                               16/03/2019
"""

#Imports
import random

#Global variables#
#Tuples:
SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
#Dictionary for card values:
VALUES = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

#Classes decleration:
class Card():  
    def __init__(self,suit,rank):        
        try:                
            if suit in SUITS:
                self.suit = suit
            else:
                raise ValueError("Given suit is not Hearts, Diamonds, Spades or Clubs")
            if rank in RANKS:
                self.rank = rank            
            else:
                raise ValueError("Given rank is not part of Ranks")
        except ValueError as exp:
            print('Error: '+ exp)
        except:
            print('Undefined error')

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck():
#Contains all cards
    def __init__(self):
        self.deck = []
        #Set all cards
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))
        self.Shuffle()

    #Shuffle all cards in deck
    def Shuffle(self):
        random.shuffle(self.deck)

    #Pop card from deck
    def PopCard(self):
        return self.deck.pop()

    #Returns string of all cards
    def __str__(self):
        str_deck = ''
        for card in self.deck:
            str_deck += card.__str__() + '\n'        
        return str_deck

class Hand():
    def __init__(self):
        self.cards = []
        self.total = 0
        self.acesNum = 0

    #Returns str of hand
    def __str__(self):
        str_hand = ''
        str_hand += 'Cards in hand: \n'
        for card in self.cards:
            str_hand += card.__str__() + '\n'        
        str_hand += 'Total ' + str(self.total) + '\n'
        return str_hand

    #Returns first card in hand
    def FirstCard(self):
        return self.cards[0].__str__()

    #Add card to hand
    def AddCard(self, card):
        self.cards.append(card)
        self.total += VALUES[card.rank]
        if (card.rank == 'Ace'):
            self.acesNum +=1
            if self.total == 21:
                return
            else:
                self.CheckAces()
        return                            

    #Deal 2 cards, for first round
    def FirstRoundDealCards(self, card1, card2):
        self.AddCard(card1)
        self.AddCard(card2)
        return

    #Check sum of Aces and decide which value to use
    def CheckAces(self):
        aces = self.acesNum
        while (self.total > 21) and (aces > 0):
            #Ace will be equal to 1
            self.total -= 10
            aces -= 1       
  

class Player():
    def __init__(self, name, cash=100, bet=0):
        self.name = name
        self.cash = int(cash)
        self.bet = int(bet)
        self.hand = Hand()

    def __str__(self):
        str_player = ''
        str_player += self.name + '\n'
        str_player += 'Your current balance is: ' + str(self.cash) + '$ \n'
        if len(self.hand.cards) > 0:
            str_player += self.hand.__str__() + '\n'
        else:
            str_player += 'No cards in hand \n'
        return str_player

    def PlayerWinsGame(self):
        self.cash += (self.bet * 2)
        self.bet = 0

    def PlayerBustGame(self):
        self.cash -= self.bet
        self.bet = 0

    def UpdateBet(self,bet):
        try:
            intBet = int(bet)
            if (
                (intBet > int(self.cash)) and (int(self.cash)-intBet > 0)):
                raise ValueError("You don't have enough money!")
            elif intBet < 0:
                raise ValueError("Bet must be a possitive number!")
            else:
                self.bet = intBet
                self.cash -= intBet
        except ValueError as exp:
            print(exp)
        except:
            print('Error!')

    def ClearHand(self):
        self.hand = Hand()

def WinGame(playerWinner, playerloser):
    print (playerloser.hand.__str__())
    print (playerWinner.hand.__str__())
    print(playerloser.name + " BUST! \n")
    print(playerWinner.name + " WON!!!\n")


def main():
    playOn = True

    print("Lets play BlackJack!!")
    #Create Dealar player
    playerDealer = Player('Dealer')    
    #Create Player
    player1Name = input("Player 1 please enter your name:")
    player1 = Player(player1Name)

    #Play Game
    while playOn:        

        #Create deck and shuffle
        playDeck = Deck()   

        print('Hello ' + player1.__str__())

        player1.UpdateBet(input("Please enter your bet:"))
        print("Dealing cards..")
        #Deal 2 card to player
        player1.hand.FirstRoundDealCards(playDeck.PopCard(),playDeck.PopCard())
        print(player1.hand)

        #Deal 2 cards to dealer
        print("Dealing 2 cards to delar..")
        playerDealer.hand.FirstRoundDealCards(playDeck.PopCard(),playDeck.PopCard())
        print(playerDealer.name + "'s first card: "+ playerDealer.hand.FirstCard() + "\n")
        
        playerMove=True

        #Player's move:         
        while playerMove :
            try:
                move= int(input("Press 1 for 'Hit' or 2 for 'Stand':"))
                if (move!=1 or move!=2):
                    raise ValueError("Invalid choise, please retry.")

                #Player move--> Hit (recive another card)
                if move == 1 :
                    print("Hit me!")
                    player1.hand.AddCard(playDeck.PopCard())
                    print(player1.hand)
                    #Player hand is more then 21
                    if (player1.hand.total > 21):                                               
                        player1.PlayerBustGame()
                        WinGame(playerDealer, player1)
                        playerMove=False
                    #Player hand is equal to 21
                    elif player1.hand.total == 21:                        
                        player1.PlayerWinsGame()
                        WinGame(player1, playerDealer) 
                        playerMove=False

                #Player move--> Stand (stop receving cards, Dealer turn)
                elif move == 2:
                    print("Stand! \nDealer is taking cards till wining, 17 or bust..")                    

                    while playerMove == 2:                                                
                        #Case player win (21 or dealer bust)
                        if ((player1.hand.total == 21) or (playerDealer.hand.total > 21)):
                            WinGame(player1, playerDealer)                      
                            player1.PlayerWinsGame()
                            playerMove=False                          
                        #Case player bust or dealer win
                        elif ((player1.hand.total > 21) or ((playerDealer.hand.total > player1.hand.total) or (playerDealer.hand.total==21))):
                            WinGame(playerDealer, player1)
                            player1.PlayerBustGame()
                            playerMove=False                          
                        #Case player win: 17<dealer<21 and player>dealer
                        elif ((playerDealer.hand.total >= 17) and (playerDealer.hand.total < 21) and (player1.hand.total >= playerDealer.hand.total)) :
                            WinGame(player1, playerDealer) 
                            player1.PlayerWinsGame()
                            playerMove=False                          
                        #Dealer recive another card
                        else:  
                            playerDealer.hand.AddCard(playDeck.PopCard())
            except ValueError as exp:
                print(exp)
            except:
                print("Ilegal move")

        #Play again?
        playAgain = (input("Press Y to play again or any other key to drop: \n")).lower()
        if playAgain=='y':
            player1.ClearHand()
            playerDealer.ClearHand()
            print("Lets play!!")
        else:            
            playOn = False
            print("Thanks for playing. Bye! \n")


if __name__ == "__main__":
    main()

