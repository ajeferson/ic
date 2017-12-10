from collections import namedtuple
from itertools import combinations
import pandas as pd


def apriori(transactions, **kwargs):

    min_support = kwargs.get('min_support', 0.1)
    min_confidence = kwargs.get('min_confidence', 0.0)
    min_lift = kwargs.get('min_lift', 0.0)
    max_length = kwargs.get('max_length', None)

    if min_support <= 0:
        raise ValueError('minimum support must be > 0')

    _gen_support_records = kwargs.get(
        '_gen_support_records', generate_support_records)
    _gen_ordered_statistics = kwargs.get(
        '_gen_ordered_statistics', generate_ordered_statistics)
    _filter_ordered_statistics = kwargs.get(
        '_filter_ordered_statistics', filter_statistics)

    transaction_manager = Manager.create_transactions(transactions)
    support_records = _gen_support_records(
        transaction_manager, min_support, max_length=max_length)

    for support_record in support_records:
        ordered_statistics = list(
            _filter_ordered_statistics(
                _gen_ordered_statistics(transaction_manager, support_record),
                min_confidence=min_confidence,
                min_lift=min_lift,
            )
        )
        if not ordered_statistics:
            continue
        yield RelationRecord(
            support_record.items, support_record.support, ordered_statistics)


SupportRecord = namedtuple(
    'SupportRecord', ('items', 'support'))
RelationRecord = namedtuple(
    'RelationRecord', SupportRecord._fields + ('ordered_statistics',))
OrderedStatistic = namedtuple(
    'OrderedStatistic', ('items_base', 'items_add', 'confidence', 'lift',))


def filter_statistics(ordered_statistics, **kwargs):
    min_conf = kwargs.get('min_confidence', 0.0)
    min_lift = kwargs.get('min_lift', 0.0)

    for ordered_statistic in ordered_statistics:
        if ordered_statistic.confidence < min_conf:
            continue
        if ordered_statistic.lift < min_lift:
            continue
        yield ordered_statistic


def generate_support_records(transaction_manager, min_support, **kwargs):
    max_length = kwargs.get('max_length')

    _create_next_candidates = kwargs.get(
        '_create_next_candidates', create_next_candidates)

    candidates = transaction_manager.candidates_at_beginning()
    length = 1
    while candidates:
        relations = set()
        for relation_candidate in candidates:
            support = transaction_manager.make_support_calculations(relation_candidate)
            if support < min_support:
                continue
            candidate_set = frozenset(relation_candidate)
            relations.add(candidate_set)
            yield SupportRecord(candidate_set, support)
        length += 1
        if max_length and length > max_length:
            break
        candidates = _create_next_candidates(relations, length)


def generate_ordered_statistics(transaction_manager, record):
    items = record.items
    for combines in combinations(sorted(items), len(items) - 1):
        items_base = frozenset(combines)
        items_add = frozenset(items.difference(items_base))
        conf = (
            record.support / transaction_manager.make_support_calculations(items_base))
        lift = conf / transaction_manager.make_support_calculations(items_add)
        yield OrderedStatistic(
            frozenset(items_base), frozenset(items_add), conf, lift)


def create_next_candidates(previous, length):

    item_set = set()
    for candidate in previous:
        for item in candidate:
            item_set.add(item)
    items = sorted(item_set)

    tmp_next_candidates = (frozenset(x) for x in combinations(items, length))

    if length < 3:
        return list(tmp_next_candidates)

    next_candidates = [
        candidate for candidate in tmp_next_candidates
        if all(
            True if frozenset(x) in previous else False
            for x in combinations(candidate, length - 1))
    ]
    return next_candidates


class Manager(object):

    def __init__(self, transactions):
        self.__num_transaction = 0
        self.__items = []
        self.__transaction_index_map = {}

        for transaction in transactions:
            self.new_transaction(transaction)

    def new_transaction(self, transaction):
        for item in transaction:
            if item not in self.__transaction_index_map:
                self.__items.append(item)
                self.__transaction_index_map[item] = set()
            self.__transaction_index_map[item].add(self.__num_transaction)
        self.__num_transaction += 1

    def make_support_calculations(self, items):

        if not items:
            return 1.0

        if not self.num_transaction:
            return 0.0

        s = None
        for item in items:
            indexes = self.__transaction_index_map.get(item)
            if indexes is None:
                return 0.0

            if s is None:
                s = indexes
            else:
                s = s.intersection(indexes)

        return float(len(s)) / self.__num_transaction

    def candidates_at_beginning(self):
        return [frozenset([item]) for item in self.items]

    @property
    def num_transaction(self):
        return self.__num_transaction

    @property
    def items(self):
        return sorted(self.__items)

    @staticmethod
    def create_transactions(transactions):
        if isinstance(transactions, Manager):
            return transactions
        return Manager(transactions)


dataset = pd.read_csv('Market_Basket_Optimisation.csv', header=None)
transactions = []
for i in range(0, 7501):
    transactions.append([str(dataset.values[i,j]) for j in range(0, 20)])

# Training
rules = apriori(transactions, min_support=0.003, min_confidence=0.2, min_lift=3, min_length=2)

# Get the results
results = list(rules)

for result in results:
    print result