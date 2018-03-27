
# coding: utf-8

# In[1]:

from random import shuffle, choice
import copy

class Card006():
    
    CARD_SCORE = {x: 1 for x in range(1, 105)}
    @staticmethod
    def all_cards(random = False):
        if random:
            deck = list(Card006(num) for num in Card006.CARD_SCORE)
            shuffle(deck)
            return deck
        else:
            return list(Card006(num) for num in Card006.CARD_SCORE)
    
    def __init__(self, number):
        def _det_score(number1):
            if number1 == 55:
                return 7
            elif number1 % 11 == 0:
                return 5
            elif number1 % 10 == 0:
                return 3
            elif number1 % 5 == 0:
                return 2
            else:
                return 1    
        self._validate(number)
        self.card_number = number    
        self.card_score = _det_score(number)

    def _validate(self, number):
        if not (number > 0 and number < 105):
            raise ValueError('Invalid card\'s number')
    
    def __eq__(self, other):                                      #Проверять ли что other - card006???
        if self.card_number == other.card_number:
            return True
        else:
            return False
        
    def __ne__(self, other):
        return not (self == other)
    
    def __lt__(self, other):
        return self.card_number < other.card_number
    
    def __gt__(self, other):
        return self.card_number > other.card_number
    
    def __str__(self):
        return '{}'.format(self.card_number)
    
    def __repr__(self):
        return "Card006 with number {}".format(self.card_number)
    
    def score(self):
        return self.card_score


class Row():
    
    def __init__(self, card, row_id):
        self._validate(card)
        self.list_card = [card]
        self.row_id = row_id
        
    def _validate(self, card):
        if not (isinstance(card, Card006)):
            raise ValueError('Invalid type')
            
    def __str__(self):
        return 'Row №{}: {}'.format(self.row_id, ' '.join(str(card) for card in self.list_card))
    
    def __repr__(self):
        return '<Row object. Row id:{}. Row\'s cards: {}>'.format(self.row_id, self.list_card)
    
    def add(self, card):
        self.list_card.append(card)

        
class Table():
    
    def __init__(self, cards):
        if not all(isinstance(card, Card006) for card in cards):
            raise ValueError(
                'Invalid player: cards must all be Card006 objects'
            )
        if len(cards) != 4:
            raise ValueError(
                'Invalid player: must be initalised with 4 Cards006'
            )
        self.rows = [Row(cards[i], i+1) for i in range(4)]
        
    def __repr__(self):
        cards_of_rows = list(map(str, self.rows))
        return '<CowTable object. Rows:\n{c[0]}\n{c[1]}\n{c[2]}\n{c[3]}>'.format(c = cards_of_rows)
    
    def __str__(self):
        cards_of_rows = list(map(str, self.rows))
        return 'Current table:\n{c[0]}\n{c[1]}\n{c[2]}\n{c[3]}'.format(c = cards_of_rows)
    
    def put_card(self, card, person = False):
        list_comparing = []
        i = 0
        for row in self.rows:
            if card.card_number > row.list_card[-1].card_number:
                list_comparing.append([card.card_number - row.list_card[-1].card_number, i])
            i += 1
        list_comparing.sort()
        if len(list_comparing) > 0:
            if len(self.rows[list_comparing[0][1]].list_card) == 5:
                out_cards = copy.copy(self.rows[list_comparing[0][1]].list_card)
                self.rows[list_comparing[0][1]].list_card.clear()
                self.rows[list_comparing[0][1]].add(card)
                return out_cards
            else:
                self.rows[list_comparing[0][1]].add(card)
        else:
            if person:
                print(self)
                row_index = int(input('Please select row. '))
                if row_index > 4 or row_index < 1:
                    print('Please select an existing row! ')
                out_cards = copy.copy(self.rows[row_index-1].list_card)
                self.rows[row_index-1].list_card.clear()
                self.rows[row_index-1].add(card)
                return out_cards
            else:
                row_index = choice(list(range(1, 5)))
                out_cards = copy.copy(self.rows[row_index-1].list_card)
                self.rows[row_index-1].list_card.clear()
                self.rows[row_index-1].add(card)
                return out_cards
    
        
class CowPlayer():
    
    def __init__(self, cards, player_id=None):
        if len(cards) != 10:
            raise ValueError(
                'Invalid player: must be initalised with 10 Cards006'
            )
        if not all(isinstance(card, Card006) for card in cards):
            raise ValueError(
                'Invalid player: cards must all be Card006 objects'
            )
        self.hand = cards
        self.player_id = player_id
        self.penalty_score = 0
    
    def __repr__(self):
        if self.player_id is not None:
            return '<CowPlayer object: player {}>'.format(self.player_id)
        else:
            return '<CowPlayer object>'

    def __str__(self):
        if self.player_id is not None:
            return str(self.player_id)
        else:
            return repr(self)
    
    def add_cards_to_base(self, penalty_cards):
        if penalty_cards == None:
            return None
        sum = 0
        for card in penalty_cards:
            sum += card.card_score
        self.penalty_score += sum
        
    def print_hand(self):
            print('Your hand: {}'.format(
                ' '.join(str(card) for card in self.hand)
            ))
            
    
class CowGame():
    
    def __init__(self, players):
        if not isinstance(players, int):
            raise ValueError('Invalid game: players must be integer')
        if not 2 <= players <= 10:
            raise ValueError('Invalid game: must be between 2 and 10 players')
        self.deck = Card006.all_cards(True)
        self.players = [
            CowPlayer(self._deal_hand(), n) for n in range(players)
        ]
        self.table = Table([self.deck.pop() for i in range(4)])
        self.playable_cards = []
    
    def _deal_hand(self):
        return [self.deck.pop() for i in range(10)]
    
    @property
    def is_active(self):
        return all((player.penalty_score) < 66 for player in self.players)
    
    def pop_card_player(self, player_id, card_index):
        self.playable_cards.append([self.players[player_id].hand.pop(card_index), player_id])
    
    def play(self):
        My_player = self.players[0]
        print('The game begins. You are Player №0.')  
#         My_player.print_hand()
        while self.is_active:
            counter = 1
            while self.is_active and counter <= 10:
                print()
                next(self)
                counter += 1
            self.clear()
        print()
        print('Game has finished!\n')
        print('Player\'s penalty scores:')
        for player in self.players:
            print(player.penalty_score)
            
    def clear(self):
        self.deck = Card006.all_cards(True)
        for player in self.players:
            player.hand = self._deal_hand()
        self.table = Table([self.deck.pop() for i in range(4)])

    def __next__(self):
        if not self.is_active:
            return 0
        print(self.table)
        print()
        print('Current penalty scores:')
        for player in self.players:
            print('Player №{} has {} penalty scores'.format(player.player_id, player.penalty_score))
        print()
        My_player = self.players[0]
        My_player.print_hand()
        played = False
        while not played:
            card_index = int(input('Which card do you want to play? '))
            if card_index > len(My_player.hand) or card_index < 1:
                print('Please select an existing card! ')
            else:
                self.pop_card_player(self.players.index(My_player), card_index-1)
                played = True

        for i in range(1, len(self.players)):
            card = choice(self.players[i].hand)
            self.pop_card_player(i, choice(list(range(len(self.players[i].hand)))))

        self.playable_cards.sort(reverse = True)
#         print(self.playable_cards)
        for card in self.playable_cards:
            if card[1] == 0:
                self.players[card[1]].add_cards_to_base(self.table.put_card(card[0], True))
            else:
                self.players[card[1]].add_cards_to_base(self.table.put_card(card[0]))
            if not self.is_active:
                break
        self.playable_cards.clear()

if __name__ == '__main__':
    egame = CowGame(4)
    egame.play()


# In[ ]:




# In[ ]:



