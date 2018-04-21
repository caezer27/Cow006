# coding: utf-8

from random import shuffle, choice
import pickle
import copy
import json


class Card006():

    MAX_CARD_NUMBER = 104
    CARD_SCORE = {x: 1 for x in range(1, MAX_CARD_NUMBER+1)}

    @staticmethod
    def all_cards(random = False):
        if random:
            deck = list(Card006(num) for num in Card006.CARD_SCORE)
            shuffle(deck)
            return deck
        else:
            return list(Card006(num) for num in Card006.CARD_SCORE)

    @staticmethod
    def redict(card_dict):
        return Card006(card_dict['Card'][0])

    def dict(self):
        return {'Card': [self.card_number,self.card_score]}
    
    def __init__(self, number):
        def _det_score(number1):
            if number1 % 55 == 0:
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
        if not (number > 0 and number < Card006.MAX_CARD_NUMBER+1):
            raise ValueError('Invalid card\'s number')
    
    def __eq__(self, other):
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

    MAX_LEN_OF_ROW = 6

    def __init__(self, card, row_id):
        self._validate(card, row_id)
        self.list_card = [card]
        self.row_id = row_id

    @staticmethod
    def redict(row_dict):
        list_cards = [Card006.redict(card) for card in row_dict['cards']]
        row = Row(list_cards.pop(0), row_dict['id'])
        for card in list_cards:
            row.add(card)
        return row

    def dict(self):
        return {'id': self.row_id, 'cards': [card.dict() for card in self.list_card]}

    def _validate(self, card, row_id):
        if not (isinstance(card, Card006)):
            raise ValueError('Invalid row: must be initalised with Card006')
        if not (isinstance(row_id, int)):
            raise ValueError('Invalid row: row_id must be integer')
            
    def __str__(self):
        return 'Row №{}: {}'.format(self.row_id+1, ' '.join(str(card) for card in self.list_card))
    
    def __repr__(self):
        return '<Row object. Row id:{}. Row\'s cards: {}>'.format(self.row_id, self.list_card)
    
    def add(self, card):
        self.list_card.append(card)

    def accept_card(self, card):
        self._validate(card, 1)
        if self.list_card[-1] < card:
            return True
        else:
            return False

    def check6(self):
        if len(self.list_card) == Row.MAX_LEN_OF_ROW-1:
            return True
        else:
            return False


class Table():

    NUMBER_OF_ROWS = 4
    
    def __init__(self, cards, reinit = False):
        if reinit:
            self.rows = [row for row in cards]
        else:
            if not all(isinstance(card, Card006) for card in cards):
                raise ValueError(
                    'Invalid table: all cards must be Card006 objects'
                )
            if len(cards) != Table.NUMBER_OF_ROWS:
                raise ValueError(
                    'Invalid table: must be initalised with {} Cards006'.format(Table.NUMBER_OF_ROWS)
                )
            self.rows = [Row(cards[i], i) for i in range(Table.NUMBER_OF_ROWS)]

    def dict(self):
        return {'rows': [row.dict() for row in self.rows]}

    @staticmethod
    def redict(table_dict):
        list_of_rows = [Row.redict(row) for row in table_dict['rows']]
        return Table(list_of_rows, reinit = True)

    def __repr__(self):
        cards_of_rows = list(map(str, self.rows))
        return '<CowTable object. Rows:\n{}>'.format('\n'.join(cards for cards in cards_of_rows))
    
    def __str__(self):
        cards_of_rows = list(map(str, self.rows))
        return 'Current table:\n{}'.format('\n'.join(cards for cards in cards_of_rows))


class CowPlayer():

    INITIAL_NUMBER_OF_CARDS = 10

    def __init__(self, cards, player_id=None, human=False, penalty=0, reinit=False):
        if not reinit:
            if len(cards) != CowPlayer.INITIAL_NUMBER_OF_CARDS:
                raise ValueError(
                    'Invalid player: must be initalised with {} Cards006'.format(CowPlayer.INITIAL_NUMBER_OF_CARDS))
            if not all(isinstance(card, Card006) for card in cards):
                raise ValueError('Invalid player: cards must all be Card006 objects')
        self.hand = cards
        self.player_id = player_id
        self.penalty_score = penalty
        self.human = human

    def dict(self):
        return {'hand': [card.dict() for card in self.hand],
                'id': self.player_id,
                'penalty_score': self.penalty_score,
                'human': self.human}

    @staticmethod
    def redict(player_dict):
        hand = [Card006.redict(card) for card in player_dict['hand']]
        return CowPlayer(hand, player_dict['id'], player_dict['human'], player_dict['penalty_score'],
                         reinit=True)


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

    MIN_NUMBER_OF_PLAYERS = 2
    TOTAL_NUMBER_OF_PLAYERS = 10
    CRITICIAL_PENALTY_SCORE = 66

    def __init__(self, human_players, ii_players):
        if not (isinstance(human_players, int) and isinstance(ii_players, int)):
            raise ValueError('Invalid game: number of players must be integer')
        if not CowGame.MIN_NUMBER_OF_PLAYERS <= human_players + ii_players <= CowGame.TOTAL_NUMBER_OF_PLAYERS:
            raise ValueError(
                'Invalid game: total number of players must be between {} and {} players'
                .format(CowGame.MIN_NUMBER_OF_PLAYERS, CowGame.TOTAL_NUMBER_OF_PLAYERS))
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
        self.table = Table([self.deck.pop() for i in range(Table.NUMBER_OF_ROWS)])

    def dict(self):
        return {'playable_cards': [[card[0].dict(), card[1]] for card in self.playable_cards],
                'players': [player.dict() for player in self.players],
                'table': self.table.dict()}

    def deal_hand(self):
        return [self.deck.pop() for i in range(CowPlayer.INITIAL_NUMBER_OF_CARDS)]
    
    @property
    def is_active(self):
        return all((player.penalty_score) < CowGame.CRITICIAL_PENALTY_SCORE for player in self.players)
    
    def pop_card_player(self, player_id, card_index):
        self.playable_cards.append([self.players[player_id].hand.pop(card_index), player_id])

    def take_row(self, player_id, row_id, card):
        self.players[player_id].add_cards_to_base(self.table.rows[row_id].list_card)
        self.table.rows[row_id].list_card.clear()
        self.table.rows[row_id].add(card)
        self.print_take_row(player_id, row_id, card)

    def human_put_card(self, player_id, card):
        list_comparing = [rows.row_id for rows in self.table.rows if rows.accept_card(card)]
        if list_comparing:
            self.put_card_to_row(list_comparing, player_id, card)
        else:
            print(self.table)
            choosed = False
            while not choosed:
                input_from_player = input('Please select row. ')
                if input_from_player == 'save':
                    if self.save():
                        print('Game saved successfully!')
                else:
                    row_id = int(input_from_player) - 1
                    if row_id > Table.NUMBER_OF_ROWS - 1 or row_id < 0:
                        print('Please select an existing row! ')
                    else:
                        self.take_row(player_id, row_id, card)
                        choosed = True

    def save(self):
        data = self.creat_data_to_save()
        with open('save.cow.json', 'w') as f:
            json.dump(data, f)
        return True

    def creat_data_to_save(self):
        data = self.dict()
        return data

    def load(self):
        with open('save.cow.json', 'r') as f:
            data_new = json.load(f)
            self.players = [CowPlayer.redict(player) for player in data_new['players']]
            self.table = Table.redict(data_new['table'])
            self.playable_cards = [[Card006.redict(card[0]), card[1]] for card in data_new['playable_cards']]
            self.next_step(load=True)

    def put_card(self, player_id, card):
        list_comparing = [rows.row_id for rows in self.table.rows if rows.accept_card(card)]
        if list_comparing:
            self.put_card_to_row(list_comparing, player_id, card)
        else:
            row_id = choice(list(range(Table.NUMBER_OF_ROWS)))
            self.take_row(player_id, row_id, card)

    def put_card_to_row(self, list_comparing, player_id, card):
        row_id = min([(card - self.table.rows[row].list_card[-1], row) for row in list_comparing])[1]
        if self.table.rows[row_id].check6():
            self.take_row(player_id, row_id, card)
        else:
            self.table.rows[row_id].add(card)
            self.print_put_card(player_id, card, row_id)

    def print_take_row(self, player_id, row_id, card):
        print('Player№{} take row№{} and put card {}'.format(player_id+1, row_id+1, card))

    def print_put_card(self, player_id, card, row_id):
        print('Player№{} put card {} to row№{}'.format(player_id+1, card, row_id+1))

    def play(self):
        print('The game begins.')
        choosed = False
        while not choosed:
            input_from_player = input('Would you like load previous game? ')
            if input_from_player == 'yes':
                print('Game loaded.')
                self.load()
                choosed = True
            elif input_from_player == 'no':
                print('Game continues.')
                choosed = True
            else:
                print('I cannot understand you! Please, repeat!')

        while self.is_active:
            counter = len(self.players[0].hand)
            while self.is_active and counter > 0:
                print()
                self.next_step()
                counter = len(self.players[0].hand)
            self.clear()
        print()
        print('Game has finished!\n')
        print('Player\'s penalty scores:')
        for player in self.players:
            print('Player №{} - {}'.format(player.player_id+1, player.penalty_score))

    def next_step(self, load = False):
        if (load == False):
            print(self.table)
            print()
            print('Current penalty scores:')
            for player in self.players:
                print('Player №{} has {} penalty scores'.format(player.player_id+1, player.penalty_score))
            print()

            #Выбор карт для игры
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

            #Разложение карт по строкам
            self.playable_cards.sort()
            #print(self.playable_cards)
        if (load == True) or (load == False):
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

    # a = Card006(50)
    # b = a.dict()
    # print(b)
    # c = Card006.redict(b)
    # print(repr(c))

    # a = Card006(50)
    # c = Card006(51)
    # b = Row(a, 1)
    # b.add(c)
    # print(b.dict())
    # f = b.dict()
    # e = Row.redict(f)
    # print(repr(e))

    # a = Card006(50)
    # b = Card006(92)
    # c = Card006(51)
    # d = Card006(58)
    # tab = Table([a,b,c,d])
    # dic = tab.dict()
    # tab1 = Table.redict(dic)
    # print(repr(tab))
    # print(repr(tab1))

