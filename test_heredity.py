import pytest
from heredity import finding_out_parent, PROBS, n_gene_odd, parent_child, no_parents_odd, joint_probability, update, normalize

def test_finding_out_parent():
    one_gene = {"Alice"}
    two_genes = {"Bob"}
    # how likely is that apparent passes 1 depending on the parent genes' number
    assert finding_out_parent("Bob", one_gene, two_genes) == 0.99
    assert finding_out_parent("Alice", one_gene, two_genes) == 0.5
    assert finding_out_parent("Carol", one_gene, two_genes) == 0.01
    assert 0 < finding_out_parent("Dave", set(), set()) < 1

def test_n_gene_odd():
    one = {"Harry"}
    two = {"James"}

    # Textbook case: two carriers (0.5 / 0.5) -> 25% / 50% / 25%
    assert n_gene_odd("K", {"K"}, set(), 0.5, 0.5) == 0.5
    assert n_gene_odd("K", set(), {"K"}, 0.5, 0.5) == 0.25
    assert n_gene_odd("K", set(), set(), 0.5, 0.5) == 0.25

    # CS50 spec example: 0.99 / 0.01 -> 1-gene chance is 0.99^2 + 0.01^2
    assert n_gene_odd("K", {"K"}, set(), 0.99, 0.01) == pytest.approx(0.9802)

    # The three outcomes must sum to 1 for any parent odds
    for m in (0, 0.01, 0.5, 0.99, 1):
        for f in (0, 0.01, 0.5, 0.99, 1):
            total = (n_gene_odd("K", set(), set(), m, f)
                     + n_gene_odd("K", {"K"}, set(), m, f)
                     + n_gene_odd("K", set(), {"K"}, m, f))
            assert total == pytest.approx(1), (m, f)

def test_parent_child():
    PROBS = {"mutation": 0.01}

    # 3 generations: roots -> Daisy/Elton -> Gina
    PEOPLE = {
        "Zena":   {"mother": None,     "father": None},
        "Arthur": {"mother": None,     "father": None},
        "Claire": {"mother": None,     "father": None},
        "Barry":  {"mother": None,     "father": None},
        "Daisy":  {"mother": "Zena",   "father": "Arthur"},
        "Elton":  {"mother": "Claire", "father": "Barry"},
        "Gina":   {"mother": "Daisy",  "father": "Elton"},
    }
    ONE_GENE = {"Daisy", "Gina"}
    TWO_GENES = {"Elton"}

    
    # Daisy has 1 gene; parents Zena and Arthur have 0 -> both pass-on odds = 0.01
    # P = 0.01*0.99 + 0.01*0.99 = 0.0198
    assert parent_child("Daisy", "Zena", "Arthur", ONE_GENE, TWO_GENES) == pytest.approx(0.0198)


    # In this world Daisy IS a 1-gene carrier (odd 0.5), Elton IS 2-gene (odd 0.99)
    # Gina has 1 gene -> P = 0.5*0.01 + 0.99*0.5 = 0.5
    assert parent_child("Gina", "Daisy", "Elton", ONE_GENE, TWO_GENES) == pytest.approx(0.5)


    # Same world, but Gina assumed to have 0 genes -> (1-0.5)*(1-0.99) = 0.005
    assert parent_child("Gina", "Daisy", "Elton", {"Daisy"}, TWO_GENES) == pytest.approx(0.005)

def test_no_parent_odd():
    empty_set = set()
    # 3% of the population carries one copy
    assert no_parents_odd("Zena", {"Zena"}, empty_set) == pytest.approx(0.03)

    
    # 1% of the population carries two copies
    assert no_parents_odd("Zena", empty_set, {"Zena"}) == pytest.approx(0.01)


    # In neither set -> 96%
    assert no_parents_odd("Zena", empty_set, empty_set) == pytest.approx(0.96)


    # The three values are the population prior: they must sum to 1
    assert (no_parents_odd("X", empty_set, empty_set)
        + no_parents_odd("X", {"X"}, empty_set)
        + no_parents_odd("X", empty_set, {"X"}) == pytest.approx(1.0))

def test_joint_probability():
    people = {
        "Zena":   {"mother": None,     "father": None},
        "Arthur": {"mother": None,     "father": None},
        "Daisy":  {"mother": "Zena",   "father": "Arthur"},
    }
    one_gene = {"Daisy"}            # Zena: 0 genes, Arthur: 2 genes
    two_genes = {"Arthur"}
    have_trait = {"Zena", "Daisy"}  # Arthur does NOT have the trait

    # Zena   0 genes + trait:  0.96 * 0.01
    # Arthur 2 genes - trait:  0.01 * 0.35
    # Daisy  1 gene  + trait:  (0.01*0.01 + 0.99*0.99) * 0.56 = 0.9802 * 0.56
    # joint = 0.0096 * 0.0035 * 0.548912
    assert joint_probability(people, one_gene, two_genes, have_trait) == pytest.approx(1.84434432e-05)

    # Sanity: lone founder, 0 genes, no trait -> 0.96 * 0.99
    assert joint_probability({"Zena": {"mother": None, "father": None}}, set(), set(), set()) == pytest.approx(0.9504)


def test_update():
    NAMES = ("Harry", "James", "Lily")
    ALL = set(NAMES)

    CASE2 = ({"Harry"}, {"James"}, {"Harry", "James"}, 0.1)
    CASE3 = (set(), ALL, set(), 0.5)

    # expected per person: (gene2, gene1, gene0, trait_True, trait_False)
    cases = [
        # 1. nobody has gene or trait
        ([(set(), set(), set(), 0.2)],
         {n: (0, 0, 0.2, 0, 0.2) for n in NAMES}),
        # 2. mixed
        ([CASE2],
         {"Harry": (0, 0.1, 0, 0.1, 0),
          "James": (0.1, 0, 0, 0.1, 0),
          "Lily":  (0, 0, 0.1, 0, 0.1)}),
        # 3. everyone has 2 genes
        ([CASE3],
         {n: (0.5, 0, 0, 0, 0.5) for n in NAMES}),
        # 4. p = 0 changes nothing
        ([({"Lily"}, set(), {"Lily"}, 0.0)],
         {n: (0, 0, 0, 0, 0) for n in NAMES}),
        # 5. accumulation: two calls on the same dict
        ([CASE2, CASE3],
         {"Harry": (0.5, 0.1, 0, 0.1, 0.5),
          "James": (0.6, 0, 0, 0.1, 0.5),
          "Lily":  (0.5, 0, 0.1, 0, 0.6)}),
    ]

    for calls, expected in cases:
        # fresh dict for every case
        probabilities = {
            n: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
            for n in NAMES
        }
        for one_gene, two_genes, have_trait, p in calls:
            assert update(probabilities, one_gene, two_genes, have_trait, p) is None
        for name, (g2, g1, g0, tt, tf) in expected.items():
            assert probabilities[name]["gene"][2] == pytest.approx(g2)
            assert probabilities[name]["gene"][1] == pytest.approx(g1)
            assert probabilities[name]["gene"][0] == pytest.approx(g0)
            assert probabilities[name]["trait"][True] == pytest.approx(tt)
            assert probabilities[name]["trait"][False] == pytest.approx(tf)


def test_normalize():
    probabilities = {
        "Harry": {
            "gene": {2: 2, 1: 6, 0: 2},          # sums to 10
            "trait": {True: 1, False: 3},        # sums to 4
        },
        "Lily": {
            "gene": {2: 0.1, 1: 0.3, 0: 0.6},    # already normalized
            "trait": {True: 0.25, False: 0.75},  # already normalized
        },
    }

    normalize(probabilities)

    # Case 1: unnormalized values keep their proportions
    assert probabilities["Harry"]["gene"] == pytest.approx({2: 0.2, 1: 0.6, 0: 0.2})
    assert probabilities["Harry"]["trait"] == pytest.approx({True: 0.25, False: 0.75})

    # Case 2: already normalized values stay the same
    assert probabilities["Lily"]["gene"] == pytest.approx({2: 0.1, 1: 0.3, 0: 0.6})
    assert probabilities["Lily"]["trait"] == pytest.approx({True: 0.25, False: 0.75})

    # Case 3: every distribution of every person sums to 1
    for person in probabilities.values():
        for distribution in person.values():
            assert sum(distribution.values()) == pytest.approx(1)
