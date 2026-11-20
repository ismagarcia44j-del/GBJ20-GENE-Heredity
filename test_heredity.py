import pytest
from heredity import finding_out_parent, PROBS

def test_finding_out_parent():
    one_gene = {"Alice"}
    two_genes = {"Bob"}

    assert finding_out_parent("Bob", one_gene, two_genes) == 0.99
    assert finding_out_parent("Alice", one_gene, two_genes) == 0.5
    assert finding_out_parent("Carol", one_gene, two_genes) == 0.01
    assert 0 < finding_out_parent("Dave", set(), set()) < 1