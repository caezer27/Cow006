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

    def __sub__(self, other):
        return self.card_number - other.card_number
    
    def score(self):
        return self.card_score


class Row():
    
    def __init__(self, card, row_id):
        self._validate(card)
        self.list_card = [card]
        self.row_id = row_id

    def _validate(self, card):
        if not (isinstance(card, Card006)):
            raise ValueError('Invalid row: must be initalised with Card006')
            
    def __str__(self):
        return 'Row №{}: {}'.format(self.row_id+1, ' '.join(str(card) for card in self.list_card))
    
    def __repr__(self):
        return '<Row object. Row id:{}. Row\'s cards: {}>'.format(self.row_id, self.list_card)
    
    def add(self, card):
        self.list_card.append(card)

    def accept_card(self, card):
        self._validate(card)
        if self.list_card[-1] < card:
            return True
        else:
            return False

    def check6(self):
        if len(self.list_card) == 5:
            return True
        else:
            return False


class Table():
    
    def __init__(self, cards):
        if not all(isinstance(card, Card006) for card in cards):
            raise ValueError(
                'Invalid table: all cards must be Card006 objects'
            )
        if len(cards) != 4:
            raise ValueError(
                'Invalid table: must be initalised with 4 Cards006'
            )
        self.rows = [Row(cards[i], i) for i in range(4)]
        
    def __repr__(self):
        cards_of_rows = list(map(str, self.rows))
        return '<CowTable object. Rows:\n{c[0]}\n{c[1]}\n{c[2]}\n{c[3]}>'.format(c = cards_of_rows)
    
    def __str__(self):
        cards_of_rows = list(map(str, self.rows))
        return 'Current table:\n{c[0]}\n{c[1]}\n{c[2]}\n{c[3]}'.format(c = cards_of_rows)


class CowPlayer():
    
    def __init__(self, cards, player_id=None, human=False):
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
        self.human = human
    
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
        for card in penalty_cards:
            self.penalty_score += card.card_score
        
    def print_hand(self):
            print('Player №{}, your hand: {}'.format(
                self.player_id+1,
                ' '.join(str(card) for card in self.hand)
            ))
            
    
class CowGame():

    CRITICIAL_PENALTY_SCORE = 66

    def __init__(self, human_players, ii_players):
        if not (isinstance(human_players, int) and isinstance(ii_players, int)):
            raise ValueError('Invalid game: number of players must be integer')
        if not 2 <= human_players + ii_players <= 10:
            raise ValueError('Invalid game: total number of players must be between 2 and 10 players')
        self.clear(True, human_players, ii_players)
        self.playable_cards = []

    def clear(self, initial = False, human_players = None, ii_players = None):
        self.deck = Card006.all_cards(random=True)
        if initial:
            self.players = [CowPlayer(self.deal_hand(), n, True) for n in range(human_players)]
            self.players.extend([CowPlayer(self.deal_hand(), n+human_players) for n in range(ii_players)])
        else:
            for player in self.players:
                player.hand = self.deal_hand()
        self.table = Table([self.deck.pop() for i in range(4)])
    
    def deal_hand(self):
        return [self.deck.pop() for i in range(10)]
    
    @property
    def is_active(self):
        return all((player.penalty_score) < CowGame.CRITICIAL_PENALTY_SCORE for player in self.players)
    
    def pop_card_player(self, player_id, card_index):
        self.playable_cards.append([self.players[player_id].hand.pop(card_index), player_id])

    def human_put_card(self, player_id, card):
        list_comparing = [rows.row_id for rows in self.table.rows if rows.accept_card(card)]
        if len(list_comparing) == 0:
            print(self.table)
            choosed = False
            while not choosed:
                row_index = int(input('Please select row. ')) - 1
                if row_index > 3 or row_index < 0:
                    print('Please select an existing row! ')
                else:
                    self.players[player_id].add_cards_to_base(self.table.rows[row_index].list_card)
                    self.table.rows[row_index].list_card.clear()
                    self.table.rows[row_index].add(card)
                    choosed = True
        else:
            row_id = min([(card - self.table.rows[row].list_card[-1],row) for row in list_comparing])[1]
            if self.table.rows[row_id].check6():
                self.players[player_id].add_cards_to_base(self.table.rows[row_id].list_card)
                self.table.rows[row_id].list_card.clear()
                self.table.rows[row_id].add(card)
            else:
                self.table.rows[row_id].add(card)

    def put_card(self, player_id, card):
        list_comparing = [rows.row_id for rows in self.table.rows if rows.accept_card(card)]
        if len(list_comparing) == 0:
            row_index = choice(list(range(4)))
            self.players[player_id].add_cards_to_base(self.table.rows[row_index].list_card)
            self.table.rows[row_index].list_card.clear()
            self.table.rows[row_index].add(card)
        else:
            row_id = min([(card - self.table.rows[row].list_card[-1],row) for row in list_comparing])[1]
            if self.table.rows[row_id].check6():
                self.players[player_id].add_cards_to_base(self.table.rows[row_id].list_card)
                self.table.rows[row_id].list_card.clear()
                self.table.rows[row_id].add(card)
            else:
                self.table.rows[row_id].add(card)

    def play(self):
        print('The game begins.')
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
            print('Player №{} - {}'.format(player.player_id+1, player.penalty_score))

    def __next__(self):
        print(self.table)
        print()
        print('Current penalty scores:')
        for player in self.players:
            print('Player №{} has {} penalty scores'.format(player.player_id+1, player.penalty_score))
        print()

        for player in self.players:
            if player.human:
                player.print_hand()
                played = False
                while not played:
                    card_index = int(input('Which card do you want to play? '))
                    for card in player.hand:
                        if card.card_number == card_index:
                            self.pop_card_player(player.player_id, player.hand.index(card))
                            played = True
                            break
                    if not played:
                        print('Please select an existing card! ')
            else:
                card = choice(player.hand)
                self.pop_card_player(player.player_id, player.hand.index(card))

        self.playable_cards.sort()
        print(self.playable_cards)

        for card_and_player_id in self.playable_cards:
            player_ids = card_and_player_id[1]
            card = card_and_player_id[0]
            if self.players[player_ids].human:
                self.human_put_card(player_ids, card)
            else:
                self.put_card(player_ids, card)
            if not self.is_active:
                break
        self.playable_cards.clear()


if __name__ == '__main__':
    egame = CowGame(1,3)
    egame.play()