import math
import random


AllSets = {}


class CardType(object):
    def __init__(self, name):
        self.name = name


class CardList(set):
    def __contains__(self, item):
        if not isinstance(item, Card):
            for card in self:
                if card.name == item:
                    return True
        return super(CardList, self).__contains__(item)

    def __call__(self, *names):
        cards = set()
        for card in self:
            if card.name in names:
                cards.add(card)
        return cards


class Card(object):
    def __init__(self, name, types=None, cardSet=None):
        self.name = name
        self.set = cardSet

        if isinstance(types, set):
            self.types = types
        elif types is None:
            self.types = set()
        else:
            self.types = set(types)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return '<randomizer.Card: {}>'.format(self)

    def __gt__(self, other):
        return str(self) > str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __str__(self):
        if Event in self.types:
            formatStr = '({} Event): {}'
        elif Landmark in self.types:
            formatStr = '({} Landmark): {}'
        elif Project in self.types:
            formatStr = '({} Project): {}'
        elif Way in self.types:
            formatStr = '({} Way): {}'
        else:
            formatStr = '{}: {}'
        return formatStr.format(self.set.name, self.name)


class Set(object):
    def __init__(self, name):
        global AllSets
        self.name = name
        self._cards = CardList()
        self._firstEdition = None
        self._secondEdition = None

        self._events = None
        self._landmarks = None
        self._projects = None
        self._potionCards = None
        self._ways = None

        AllSets[self.name] = self

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '<randomizer.Set: {}>'.format(self.name)

    def _AddCards(self, cardList, cards):
        for cardData in cards:
            if isinstance(cardData, Card):
                cardList.add(cardData)
            elif isinstance(cardData, dict):
                card = Card(**cardData)
                card.set = self
                cardList.add(card)
            else:
                # Assume card data is name for now
                cardList.add(Card(cardData, cardSet=self))

    def AddCards(self, cards):
        self._AddCards(self._cards, cards)

    def RemoveCards(self, cards):
        self._cards -= cards

    @property
    def cards(self):
        return self._cards

    @property
    def firstEdition(self):
        return self._firstEdition

    @firstEdition.setter
    def firstEdition(self, cards):
        if self._firstEdition is None:
            self._firstEdition = CardList()
        self._AddCards(self._firstEdition, cards)

    @property
    def secondEdition(self):
        return self._secondEdition

    @secondEdition.setter
    def secondEdition(self, cards):
        if self._secondEdition is None:
            self._secondEdition = CardList()
        self._AddCards(self._secondEdition, cards)

    @property
    def events(self):
        if self._events is None:
            self._events = CardList(
                card for card in self._cards if card.types & {Event}
            )
        return self._events

    @property
    def landmarks(self):
        if self._landmarks is None:
            self._landmarks = CardList(
                card for card in self._cards if card.types & {Landmark}
            )
        return self._landmarks

    @property
    def projects(self):
        if self._projects is None:
            self._projects = CardList(
                card for card in self._cards if card.types & {Project}
            )
        return self._projects

    @property
    def ways(self):
        if self._ways is None:
            self._ways = CardList(
                card for card in self._cards if card.types & {Way}
            )
        return self._ways

    @property
    def potionCards(self):
        if self._potionCards is None:
            self._potionCards = CardList(
                card for card in self._cards if card.types & {Potion}
            )
        return self._potionCards


# Define card types
Event = CardType('Event')
Landmark = CardType('Landmark')
Project = CardType('Project')
Way = CardType('Way')
Potion = CardType('Potion')

# Define sets
Base = Set('Base')
Base.AddCards([
    'Cellar', 'Chapel', 'Moat', 'Harbinger', 'Merchant', 'Village', 'Workshop',
    'Vassal', 'Bureaucrat', 'Gardens', 'Militia', 'Moneylender', 'Poacher',
    'Remodel', 'Smithy', 'Throne Room', 'Bandit', 'Council Room', 'Festival',
    'Laboratory', 'Library', 'Market', 'Mine', 'Sentry', 'Witch', 'Artisan'
])
Base.firstEdition = [
    'Adventurer', 'Chancellor', 'Feast', 'Spy', 'Thief', 'Woodcutter'
]
Base.secondEdition = Base.cards(
    'Artisan', 'Bandit', 'Harbinger', 'Merchant', 'Poacher', 'Sentry', 'Vassal'
)

Intrigue = Set('Intrigue')
Intrigue.AddCards([
    'Courtyard', 'Lurker', 'Pawn', 'Masquerade', 'Shanty Town', 'Steward',
    'Swindler', 'Wishing Well', 'Baron', 'Bridge', 'Conspirator', 'Diplomat',
    'Ironworks', 'Mill', 'Mining Village', 'Secret Passage', 'Courtier',
    'Duke', 'Minion', 'Patrol', 'Replace', 'Torturer', 'Trading Post',
    'Upgrade', 'Harem', 'Nobles'
])
Intrigue.firstEdition = [
    'Coppersmith', 'Great Hall', 'Saboteur', 'Scout', 'Secret Chamber',
    'Tribute'
]
Intrigue.secondEdition = Intrigue.cards(
    'Courtier', 'Diplomat', 'Lurker', 'Mill', 'Patrol', 'Replace',
    'Secret Passage'
)

Seaside = Set('Seaside')
Seaside.AddCards([
    'Embargo', 'Haven', 'Lighthouse', 'Native Village', 'Pearl Diver',
    'Ambassador', 'Fishing Village', 'Lookout', 'Smugglers', 'Warehouse',
    'Caravan', 'Cutpurse', 'Island', 'Navigator', 'Pirate Ship', 'Salvager',
    'Sea Hag', 'Treasure Map', 'Bazaar', 'Explorer', 'Ghost Ship',
    'Merchant Ship', 'Outpost', 'Tactician', 'Treasury', 'Wharf'
])

Alchemy = Set('Alchemy')
Alchemy.AddCards([
    'Herbalist', 'Apprentice',
    {'name': 'Transmute', 'types': {Potion}},
    {'name': 'Vineyard', 'types': {Potion}},
    {'name': 'Apothecary', 'types': {Potion}},
    {'name': 'Scrying Pool', 'types': {Potion}},
    {'name': 'University', 'types': {Potion}},
    {'name': 'Alchemist', 'types': {Potion}},
    {'name': 'Familiar', 'types': {Potion}},
    {'name': 'Philosopher Stone', 'types': {Potion}},
    {'name': 'Golem', 'types': {Potion}},
    {'name': 'Possession', 'types': {Potion}}
])

Prosperity = Set('Prosperity')
Prosperity.AddCards([
    'Loan', 'Trade Route', 'Watchtower', 'Bishop', 'Monument', 'Quarry',
    'Talisman', 'Worker Village', 'City', 'Contraband', 'Counting House',
    'Mint', 'Mountebank', 'Rabble', 'Royal Seal', 'Vault', 'Venture', 'Goons',
    'Grand Market', 'Hoard', 'Bank', 'Expand', 'Forge', "King's Court",
    'Peddler'
])

Cornucopia = Set('Cornucopia')
Cornucopia.AddCards([
    'Hamlet', 'Fortune Teller', 'Menagerie', 'Farming Village',
    'Horse Traders', 'Remake', 'Tournament', 'Young Witch', 'Harvest',
    'Horn of Plenty', 'Hunting Party', 'Jester', 'Fairgrounds'
])

Hinterlands = Set('Hinterlands')
Hinterlands.AddCards([
    'Crossroads', 'Duchess', 'Fools Gold', 'Develop', 'Oasis', 'Oracle',
    'Scheme', 'Tunnel', 'Jack of all Trades', 'Noble Brigand', 'Nomad Camp',
    'Silk Road', 'Spice Merchant', 'Trader', 'Cache', 'Cartographer',
    'Embassy', 'Haggler', 'Highway', 'Ill-gotten Gains', 'Inn', 'Mandarin',
    'Margrave', 'Stables', 'Border Village', 'Farmland'
])

DarkAges = Set('Dark Ages')
DarkAges.AddCards([
    'Poor House', 'Beggar', 'Squire', 'Vagrant', 'Forager', 'Hermit',
    'Market Square', 'Sage', 'Storeroom', 'Urchin', 'Armory', 'Death Cart',
    'Feodum', 'Fortress', 'Ironmonger', 'Marauder', 'Procession', 'Rats',
    'Scavenger', 'Wandering Minstrel', 'Band of Misfits', 'Bandit Camp',
    'Catacombs', 'Count', 'Counterfeit', 'Cultist', 'Graverobber',
    'Junk Dealer', 'Knights', 'Mystic', 'Pillage', 'Rebuild', 'Rogue', 'Altar',
    'Hunting Grounds'
])

Guilds = Set('Guilds')
Guilds.AddCards([
    'Candlestick Maker', 'Stonemason', 'Doctor', 'Masterpiece', 'Advisor',
    'Plaza', 'Taxman', 'Herald', 'Baker', 'Butcher', 'Journeyman',
    'Merchant Guild', 'Soothsayer'
])

Adventures = Set('Adventures')
Adventures.AddCards([
    'Coin of the Realm', 'Page', 'Peasant', 'Ratcatcher', 'Raze', 'Amulet',
    'Caravan Guard', 'Dungeon', 'Gear', 'Guide', 'Duplicate', 'Magpie',
    'Messenger', 'Miser', 'Port', 'Ranger', 'Transmogrify', 'Artificer',
    'Bridge Troll', 'Distant Lands', 'Giant', 'Haunted Woods', 'Lost City',
    'Relic', 'Royal Carriage', 'Storyteller', 'Swamp Hag', 'Treasure Trove',
    'Wine Merchant', 'Hireling',
    {'name': 'Alms', 'types': {Event}},
    {'name': 'Borrow', 'types': {Event}},
    {'name': 'Quest', 'types': {Event}},
    {'name': 'Save', 'types': {Event}},
    {'name': 'Scouting Party', 'types': {Event}},
    {'name': 'Travelling Fair', 'types': {Event}},
    {'name': 'Bonfire', 'types': {Event}},
    {'name': 'Expedition', 'types': {Event}},
    {'name': 'Ferry', 'types': {Event}},
    {'name': 'Plan', 'types': {Event}},
    {'name': 'Mission', 'types': {Event}},
    {'name': 'Pilgrimage', 'types': {Event}},
    {'name': 'Ball', 'types': {Event}},
    {'name': 'Raid', 'types': {Event}},
    {'name': 'Seaway', 'types': {Event}},
    {'name': 'Lost Arts', 'types': {Event}},
    {'name': 'Training', 'types': {Event}},
    {'name': 'Inheritance', 'types': {Event}},
    {'name': 'Pathfinding', 'types': {Event}}
])

Empires = Set('Empires')
Empires.AddCards([
    'Engineer', 'City Quarter', 'Overlord', 'Royal Blacksmith',
    'Encampment/Plunder', 'Patrician/Emporium', 'Settlers/Bustling Village',
    'Castles', 'Catapult/Rocks', 'Chariot Race', 'Enchantress',
    'Farmers Market', 'Gladiator/Fortune', 'Sacrifice', 'Temple', 'Villa',
    'Archive', 'Capital', 'Charm', 'Crown', 'Forum', 'Groundskeeper',
    'Legionary', 'Wild Hunt',
    {'name': 'Advance', 'types': {Event}},
    {'name': 'Annex', 'types': {Event}},
    {'name': 'Banquet', 'types': {Event}},
    {'name': 'Conquest', 'types': {Event}},
    {'name': 'Delve', 'types': {Event}},
    {'name': 'Dominate', 'types': {Event}},
    {'name': 'Donate', 'types': {Event}},
    {'name': 'Salt the Earth', 'types': {Event}},
    {'name': 'Ritual', 'types': {Event}},
    {'name': 'Tax', 'types': {Event}},
    {'name': 'Trade', 'types': {Event}},
    {'name': 'Triumph', 'types': {Event}},
    {'name': 'Wedding', 'types': {Event}},
    {'name': 'Windfall', 'types': {Event}},
    {'name': 'Aqueduct', 'types': {Landmark}},
    {'name': 'Arena', 'types': {Landmark}},
    {'name': 'Bandit Fort', 'types': {Landmark}},
    {'name': 'Basilica', 'types': {Landmark}},
    {'name': 'Baths', 'types': {Landmark}},
    {'name': 'Battlefield', 'types': {Landmark}},
    {'name': 'Colonnade', 'types': {Landmark}},
    {'name': 'Defiled Shrine', 'types': {Landmark}},
    {'name': 'Fountain', 'types': {Landmark}},
    {'name': 'Keep', 'types': {Landmark}},
    {'name': 'Labyrinth', 'types': {Landmark}},
    {'name': 'Mountain Pass', 'types': {Landmark}},
    {'name': 'Museum', 'types': {Landmark}},
    {'name': 'Obelisk', 'types': {Landmark}},
    {'name': 'Orchard', 'types': {Landmark}},
    {'name': 'Palace', 'types': {Landmark}},
    {'name': 'Tomb', 'types': {Landmark}},
    {'name': 'Tower', 'types': {Landmark}},
    {'name': 'Triumphal Arch', 'types': {Landmark}},
    {'name': 'Wall', 'types': {Landmark}},
    {'name': 'Wolf Den', 'types': {Landmark}},
])

Nocturne = Set('Nocturne')
Nocturne.AddCards([
    'Bard', 'Blessed Village', 'Cemetary + Haunted Mirror (Heirloom)',
    'Changeling', 'Cobbler', 'Conclave', 'Crypt', 'Cursed Village',
    'Den of Sin', 'Devils Workshop', 'Druid', 'Exorcist', 'Faithful Hound',
    'Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)', 'Guardian',
    'Ghost Town', 'Idol', 'Leprechaun', 'Monastery', 'Necromancer + Zombies',
    'Night Watchman', 'Pixie + Goat (Heirloom)',
    'Pooka + Cursed Gold (Heirloom)', 'Sacred Grove',
    'Secret Cave + Magic Lamp (Heirloom)', 'Shepherd + Pasture (Heirloom)',
    'Raider', 'Skulk', 'Tormentor', 'Tracker + Pouch (Heirloom)',
    'Tragic Hero', 'Vampire', 'Werewolf'
])

Renaissance = Set('Renaissance')
Renaissance.AddCards([
    'Border Guard', 'Ducat', 'Lackeys', 'Acting Troupe', 'Cargo Ship',
    'Experiment', 'Improve', 'Flag Bearer', 'Hideout', 'Inventor',
    'Mountain Village', 'Patron', 'Priest', 'Research', 'Silk Merchant',
    'Old Witch', 'Recruiter', 'Scepter', 'Scholar', 'Sculptor', 'Seer',
    'Spices', 'Swashbuckler', 'Treasurer', 'Villain',
    {'name': 'Cathedral', 'types': {Project}},
    {'name': 'City Gate', 'types': {Project}},
    {'name': 'Pageant', 'types': {Project}},
    {'name': 'Sewers', 'types': {Project}},
    {'name': 'Star Chart', 'types': {Project}},
    {'name': 'Exploration', 'types': {Project}},
    {'name': 'Fair', 'types': {Project}},
    {'name': 'Silos', 'types': {Project}},
    {'name': 'Sinister Plot', 'types': {Project}},
    {'name': 'Academy', 'types': {Project}},
    {'name': 'Capitalism', 'types': {Project}},
    {'name': 'Fleet', 'types': {Project}},
    {'name': 'Guildhall', 'types': {Project}},
    {'name': 'Piazza', 'types': {Project}},
    {'name': 'Road Network', 'types': {Project}},
    {'name': 'Barracks', 'types': {Project}},
    {'name': 'Crop Rotation', 'types': {Project}},
    {'name': 'Innovation', 'types': {Project}},
    {'name': 'Canal', 'types': {Project}},
    {'name': 'Citadel', 'types': {Project}},
])

Menagerie = Set('Menagerie')
Menagerie.AddCards([
    'Animal Fair', 'Barge', 'Black Cat', 'Bounty Hunter', 'Camel Train',
    'Cardinal', 'Cavalry', 'Coven', 'Destrier', 'Displace', 'Falconer',
    'Fisherman', 'Gatekeeper', 'Goatherd', 'Groom', 'Hostelry',
    'Hunting Lodge', 'Kiln', 'Livery', 'Mastermind', 'Paddock', 'Sanctuary',
    'Scrap', 'Sheepdog', 'Sleigh', 'Snowy Village', 'Stockpile', 'Supplies',
    'Village Green', 'Wayfarer',
    {'name': 'Alliance', 'types': {Event}},
    {'name': 'Banish', 'types': {Event}},
    {'name': 'Bargain', 'types': {Event}},
    {'name': 'Commerce', 'types': {Event}},
    {'name': 'Delay', 'types': {Event}},
    {'name': 'Demand', 'types': {Event}},
    {'name': 'Desperation', 'types': {Event}},
    {'name': 'Enclave', 'types': {Event}},
    {'name': 'Enhance', 'types': {Event}},
    {'name': 'Gamble', 'types': {Event}},
    {'name': 'Invest', 'types': {Event}},
    {'name': 'March', 'types': {Event}},
    {'name': 'Populate', 'types': {Event}},
    {'name': 'Pursue', 'types': {Event}},
    {'name': 'Reap', 'types': {Event}},
    {'name': 'Ride', 'types': {Event}},
    {'name': 'Seize the Day', 'types': {Event}},
    {'name': 'Stampede', 'types': {Event}},
    {'name': 'Toil', 'types': {Event}},
    {'name': 'Transport', 'types': {Event}},
    {'name': 'Way of the Butterfly', 'types': {Way}},
    {'name': 'Way of the Camel', 'types': {Way}},
    {'name': 'Way of the Chameleon', 'types': {Way}},
    {'name': 'Way of the Frog', 'types': {Way}},
    {'name': 'Way of the Goat', 'types': {Way}},
    {'name': 'Way of the Horse', 'types': {Way}},
    {'name': 'Way of the Mole', 'types': {Way}},
    {'name': 'Way of the Monkey', 'types': {Way}},
    {'name': 'Way of the Mouse', 'types': {Way}},
    {'name': 'Way of the Mule', 'types': {Way}},
    {'name': 'Way of the Otter', 'types': {Way}},
    {'name': 'Way of the Owl', 'types': {Way}},
    {'name': 'Way of the Ox', 'types': {Way}},
    {'name': 'Way of the Pig', 'types': {Way}},
    {'name': 'Way of the Rat', 'types': {Way}},
    {'name': 'Way of the Seal', 'types': {Way}},
    {'name': 'Way of the Sheep', 'types': {Way}},
    {'name': 'Way of the Squirrel', 'types': {Way}},
    {'name': 'Way of the Turtle', 'types': {Way}},
    {'name': 'Way of the Worm', 'types': {Way}}
])

Antiquities = Set('Antiquities')
Antiquities.AddCards([
    'Inscription', 'Agora', 'Discovery', 'Aquifer', 'Tomb Raider', 'Curio',
    'Gamepiece', 'Dig', 'Moundbuilder Village', 'Encroach', 'Stoneworks',
    'Graveyard', 'Inspector', 'Archaeologist', 'Mission House', 'Mendicant',
    'Profiteer', 'Miner', 'Pyramid', 'Mastermind', 'Mausoleum', 'Shipwreck',
    'Collector', 'Pharaoh', 'Grave Watcher', 'Stronghold', 'Snake Charmer'
])

# Define Landscape cards
Events = Adventures.events | Empires.events | Menagerie.events
Landmarks = Empires.landmarks
Projects = Renaissance.projects
Ways = Menagerie.ways
LandscapeCards = Events | Landmarks | Projects | Ways

# Define cards requiring potions
PotionCards = Alchemy.potionCards

# Define randomizer rules
PlatinumLove = Prosperity.cards.union(
    Base.cards('Artisan', 'Council Room', 'Merchant', 'Mine'),
    Intrigue.cards('Harem', 'Nobles'),
    Seaside.cards('Explorer', 'Treasure Map'),
    Alchemy.cards('Philosopher Stone'),
    Cornucopia.cards('Tournament'),
    Hinterlands.cards(
        'Border Village', 'Cache', 'Duchess', 'Embassy', 'Fools Gold'
    ),
    DarkAges.cards('Altar', 'Counterfeit', 'Hunting Grounds', 'Poor House'),
    Guilds.cards('Masterpiece', 'Soothsayer'),
    Adventures.cards('Hireling', 'Lost City', 'Page', 'Treasure Trove'),
    Empires.cards(
        'Capital', 'Castles', 'Chariot Race', 'Crown', 'Encampment/Plunder',
        'Farmers Market', 'Gladiator/Fortune', 'Groundskeeper', 'Legionary',
        'Patrician/Emporium', 'Sacrifice', 'Temple', 'Wild Hunt'
    ),
    Nocturne.cards(
        'Pooka + Cursed Gold (Heirloom)', 'Raider', 'Sacred Grove',
        'Secret Cave + Magic Lamp (Heirloom)', 'Tragic Hero'
    ),
    Renaissance.cards('Ducat', 'Scepter', 'Spices'),
    Antiquities.cards(
        'Archaeologist', 'Collector', 'Dig', 'Discovery', 'Encroach',
        'Gamepiece', 'Mausoleum', 'Mission House', 'Pharaoh', 'Pyramid',
        'Stoneworks', 'Stronghold'
    )
)

ShelterLove = DarkAges.cards.union(
    Base.cards('Remodel', 'Mine'),
    Intrigue.cards('Replace', 'Upgrade'),
    Seaside.cards('Salvager'),
    Alchemy.cards('Apprentice', 'Scrying Pool'),
    Prosperity.cards('Bishop', 'Expand', 'Forge'),
    Cornucopia.cards('Remake'),
    Hinterlands.cards('Develop', 'Farmland', 'Trader'),
    Adventures.cards('Raze', 'Transmogrify'),
    Empires.cards('Catapult/Rocks', 'Sacrifice'),
    Guilds.cards('Butcher', 'Journeyman', 'Stonemason', 'Taxman'),
    Nocturne.cards(
        'Cemetary + Haunted Mirror (Heirloom)', 'Exorcist',
        'Necromancer + Zombies'
    ),
    Renaissance.cards('Priest'),
    Antiquities.cards(
        'Collector', 'Graveyard', 'Pharaoh', 'Profiteer', 'Shipwreck',
        'Snake Charmer', 'Stoneworks', 'Stronghold'
    )
)

LooterCards = DarkAges.cards('Death Cart', 'Marauder', 'Cultist')

SpoilsCards = DarkAges.cards('Bandit Camp', 'Marauder', 'Pillage')

BoonCards = Nocturne.cards(
    'Bard', 'Blessed Village', 'Druid',
    'Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)', 'Idol',
    'Pixie + Goat (Heirloom)', 'Sacred Grove', 'Tracker + Pouch (Heirloom)'
)

HexCards = Nocturne.cards(
    'Cursed Village', 'Leprechaun', 'Skulk', 'Tormentor', 'Vampire', 'Werewolf'
)

WishCards = Nocturne.cards('Leprechaun', 'Secret Cave + Magic Lamp (Heirloom)')

TrapLove = Antiquities.cards.union(
    Base.cards('Cellar', 'Harbinger', 'Vassal', 'Remodel', 'Mine'),
    Intrigue.cards('Lurker', 'Baron', 'Mill', 'Replace', 'Upgrade'),
    Seaside.cards('Treasure Map', 'Tactician'),
    Alchemy.cards('Transmute'),
    Prosperity.cards(
        'Watchtower', 'Bishop', 'Counting House', 'Vault', 'Goons', 'Expand',
        'Forge'
    ),
    Cornucopia.cards('Hamlet', 'Horse Traders', 'Remake', 'Harvest'),
    Hinterlands.cards(
        'Fools Gold', 'Develop', 'Tunnel', 'Jack of all Trades', 'Trader',
        'Inn', 'Stables', 'Farmland'
    ),
    DarkAges.cards(
        'Beggar', 'Squire', 'Hermit', 'Market Square', 'Storeroom', 'Urchin',
        'Feodum', 'Procession', 'Rats', 'Scavenger', 'Catacombs',
        'Graverobber', 'Pillage', 'Rebuild', 'Altar', 'Hunting Grounds'
    ),
    Guilds.cards('Stonemason', 'Herald', 'Plaza', 'Taxman', 'Butcher'),
    Adventures.cards('Guide', 'Transmogrify', 'Artificer'),
    Empires.cards(
        'Engineer', 'Settlers/Bustling Village', 'Chariot Race',
        'Farmers Market', 'Catapult/Rocks', 'Sacrifice', 'Temple',
        'Patrician/Emporium', 'Groundskeeper', 'Encampment/Plunder',
        'Wild Hunt', 'Castles'
    ),
    Nocturne.cards(
        'Changeling', 'Secret Cave + Magic Lamp (Heirloom)', 'Exorcist',
        'Shepherd + Pasture (Heirloom)', 'Tragic Hero', 'Vampire',
        'Necromancer + Zombies', 'Cemetary + Haunted Mirror (Heirloom)'
    ),
    Renaissance.cards(
        'Improve', 'Mountain Village', 'Swashbuckler', 'Border Guard'
    )
)

BaneCards = set().union(
    Adventures.cards(
        'Amulet', 'Caravan Guard', 'Coin of the Realm', 'Dungeon', 'Gear',
        'Guide', 'Page', 'Peasant', 'Ratcatcher', 'Raze'
    ),
    Alchemy.cards('Herbalist'),
    Antiquities.cards(
        'Discovery', 'Gamepiece', 'Grave Watcher', 'Inscription', 'Inspector',
        'Profiteer', 'Shipwreck', 'Tomb Raider', 'Miner'
    ),
    Base.cards(
        'Cellar', 'Chapel', 'Harbinger', 'Merchant', 'Moat', 'Vassal',
        'Village', 'Workshop'
    ),
    Cornucopia.cards('Fortune Teller', 'Hamlet', 'Menagerie'),
    DarkAges.cards(
        'Beggar', 'Forager', 'Hermit', 'Market Square', 'Sage', 'Squire',
        'Storeroom', 'Urchin', 'Vagrant'
    ),
    Empires.cards(
        'Castles', 'Catapult/Rocks', 'Chariot Race', 'Encampment/Plunder',
        'Enchantress', 'Farmers Market', 'Gladiator', 'Gladiator/Forture',
        'Patrician/Emporium', 'Settlers/Bustling Village'
    ),
    Guilds.cards('Candlestick Maker', 'Doctor', 'Masterpiece', 'Stonemason'),
    Hinterlands.cards(
        'Crossroads', 'Develop', 'Duchess', 'Fools Gold', 'Oasis', 'Scheme',
        'Tunnel'
    ),
    Intrigue.cards(
        'Courtyard', 'Lurker', 'Masquerade', 'Pawn', 'Shanty Town', 'Steward',
        'Swindler', 'Wishing Well'
    ),
    Menagerie.cards(
        'Black Cat', 'Camel Train', 'Goatherd', 'Scrap', 'Sheepdog', 'Sleigh',
        'Snowy Village', 'Stockpile', 'Supplies'
    ),
    Nocturne.cards(
        'Changeling', 'Druid', 'Faithful Hound',
        'Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)',
        'Ghost Town', 'Guardian', 'Leprechaun', 'Monastery', 'Night Watchman',
        'Pixie + Goat (Heirloom)', 'Secret Cave + Magic Lamp (Heirloom)',
        'Tracker + Pouch (Heirloom)'
    ),
    Prosperity.cards('Loan', 'Trade Route', 'Watchtower'),
    Renaissance.cards(
        'Acting Troupe', 'Border Guard', 'Cargo Ship', 'Ducat', 'Experiment',
        'Improve', 'Lackeys'
    ),
    Seaside.cards(
        'Ambassador', 'Embargo', 'Fishing Village', 'Haven', 'Lighthouse',
        'Lookout', 'Native Village', 'Pearl Diver', 'Smugglers', 'Warehouse'
    )
)


def RandomizeDominion(setNames=None, options=None):
    # Make full list + Events + Landmarks to determine landmarks
    sets = set()
    if setNames is None:
        sets.update(AllSets.values())
    else:
        for setName in setNames:
            if setName in AllSets:
                sets.add(AllSets[setName])

    if options:
        if Base in sets:
            if options.get("base-first-edition"):
                Base.AddCards(Base.firstEdition)

            if not options.get("base-second-edition", True):
                Base.RemoveCards(Base.secondEdition)

        if Intrigue in sets:
            if options.get("intrigue-first-edition"):
                Intrigue.AddCards(Intrigue.firstEdition)

            if not options.get("intrigue-second-edition", True):
                Intrigue.RemoveCards(Intrigue.secondEdition)

    completeSet = set().union(*(cardSet.cards for cardSet in sets))

    # Randomize landscape cards
    landscapeSet = set()
    oneTenth = math.ceil(len(completeSet) / 10)

    # Check 10% of all cards for Events, add one if an odd number is found
    eventSet = Events.intersection(random.sample(completeSet, oneTenth))
    if len(eventSet) % 2:
        landscapeSet.update(random.sample(eventSet, 1))

    # Check 10% of all cards for Landmarks, add one if an odd number is found
    landmarkSet = Landmarks.intersection(random.sample(completeSet, oneTenth))
    if len(landmarkSet) % 2:
        landscapeSet.update(random.sample(landmarkSet, 1))

    # Check 10% of all cards for Projects, add one if an odd number is found
    projectSet = Projects.intersection(random.sample(completeSet, oneTenth))
    if len(projectSet) % 2:
        landscapeSet.update(random.sample(projectSet, 1))

    # Check 10% of all cards for Ways, add one if an odd number is found
    waySet = Ways.intersection(random.sample(completeSet, oneTenth))
    if len(waySet) % 2:
        landscapeSet.update(random.sample(waySet, 1))

    # Ensure no more than two landscape cards
    landscapeList = random.sample(landscapeSet, len(landscapeSet))[:2]

    # Pull cards
    pullSet = completeSet - LandscapeCards
    resultSet = set(random.sample(pullSet, 10))

    # Enforce Alchemy rule
    alchemyCount = len(Alchemy.cards & resultSet)
    if alchemyCount == 1:
        # If there's only 1 Alchemy card, remove Alchemy from the options and
        # redraw Kingdom cards
        pullSet -= Alchemy.cards
        resultSet = set(random.sample(pullSet, 10))
    elif alchemyCount == 2:
        # If there are only 2 Alchemy cards, pull 3 Alchemy cards and then
        # randomize the rest from not Alchemy
        alchemyList = random.sample(Alchemy.cards, 3)
        pullSet -= Alchemy.cards
        resultSet = set(alchemyList + random.sample(pullSet, 7))
    # If there are 3 or more Alchemy cards, let it lie.

    # Check for Shelters
    includeShelters = DarkAges in sets and ShelterLove.intersection(
        random.sample(resultSet, 2)
    )

    # Check for Colonies and Platinums
    includeColoniesAndPlatinum = (
        Prosperity in sets
        and PlatinumLove.intersection(random.sample(resultSet, 2))
    )

    # Check for Boulder traps
    includeBoulderTraps = Antiquities in sets and TrapLove.intersection(
        random.sample(resultSet, 1)
    )

    # Check for Potions
    includePotions = Alchemy.potionCards & resultSet

    # Check for Looters
    includeLooters = LooterCards & resultSet
    # Check for Madman
    includeMadman = DarkAges.cards('Hermit') & resultSet
    # Check for Mercenary
    includeMercenary = DarkAges.cards('Urchin') & resultSet
    # Check for Spoils
    includeSpoils = SpoilsCards & resultSet

    # add Prizes
    includePrizes = Cornucopia.cards('Tournament') & resultSet

    includeGhost = resultSet & Nocturne.cards(
        'Cemetary + Haunted Mirror (Heirloom)', 'Exorcist'
    )

    includeBoons = resultSet & BoonCards
    includeHex = resultSet & HexCards

    includeWisp = includeBoons or (Nocturne.cards('Exorcist') & resultSet)

    includeBat = Nocturne.cards('Vampire') & resultSet

    includeImp = resultSet & Nocturne.cards(
        'Devils Workshop', 'Exorcist', 'Tormentor'
    )

    includeWish = resultSet & Nocturne.cards(
        'Leprechaun', 'Secret Cave + Magic Lamp (Heirloom)'
    )

    includeHorse = resultSet.union(landscapeList) & Menagerie.cards(
        'Cavalry',
        'Groom',
        'Hostelry',
        'Livery',
        'Paddock',
        'Scrap',
        'Sleigh',
        'Supplies',
        # Events
        'Bargain',
        'Demand',
        'Ride',
        'Stampede',
    )

    # create final list
    additionalCards = set()

    if includePotions:
        additionalCards.add('Alchemy: Potions')
    if includeShelters:
        additionalCards.add('Dark Ages: Shelters')
    if includeLooters:
        additionalCards.add('Dark Ages: Ruins')
    if includeColoniesAndPlatinum:
        additionalCards.update(('Prosperity: Colony', 'Prosperity: Platinum'))
    if includeBoulderTraps:
        additionalCards.add('Antiquities: Boulder Traps')
    if includeMadman:
        additionalCards.add('Dark Ages: Madman')
    if includeMercenary:
        additionalCards.add('Dark Ages: Mercenary')
    if includeSpoils:
        additionalCards.add('Dark Ages: Spoils')
    if includePrizes:
        additionalCards.update((
            'Cornucopia: Bag of Gold',
            'Cornucopia: Diadem',
            'Cornucopia: Followers',
            'Cornucopia: Princess',
            'Cornucopia: Trusty Steed'
        ))
    if includeGhost:
        additionalCards.add('Nocturne: Ghost')
    if includeBoons:
        additionalCards.add('Nocturne: Boons Deck')
    if includeHex:
        additionalCards.add('Nocturne: Hexes Deck')
    if includeWisp:
        additionalCards.add('Nocturne: Will-o-wisp')
    if includeBat:
        additionalCards.add('Nocturne: Bat')
    if includeImp:
        additionalCards.add('Nocturne: Imp')
    if includeWish:
        additionalCards.add('Nocturne: Wish')
    if includeHorse:
        additionalCards.add('Menagerie: Horse')

    finalResult = sorted(resultSet | additionalCards)

    # Young Witch Support
    includeBane = resultSet & Cornucopia.cards('Young Witch')
    if includeBane:
        eligibleBanes = (pullSet & BaneCards) - resultSet
        if not eligibleBanes:
            # All eligible bane cards are already part of the randomized set!
            # Add a new card to the set and pull a bane from the randomized
            # cards.
            resultSet.update(random.sample(pullSet - resultSet, 1))
            baneCard = random.sample(resultSet & BaneCards, 1)[0]
            resultSet.remove(baneCard)
            finalResult = sorted(resultSet | additionalCards)
        else:
            baneCard = random.sample(eligibleBanes, 1)[0]

        finalResult.append('Bane is {}'.format(baneCard))

    finalResult = finalResult + sorted(landscapeList)

    return [str(card) for card in finalResult]


if __name__ == '__main__':
    print('\n'.join(RandomizeDominion()))
