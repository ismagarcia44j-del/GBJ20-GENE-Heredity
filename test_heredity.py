import pytest
from heredity import finding_out_parent, PROBS, n_gene_odd, parent_child

def test_finding_out_parent():
    one_gene = {"Alice"}
    two_genes = {"Bob"}

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
