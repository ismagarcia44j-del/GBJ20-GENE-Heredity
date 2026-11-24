# Heredity

**Estimate the chance that someone carries a genetic trait, using only their family tree.**

You list who the parents are and who is known to show the trait (for example, hearing loss). Heredity tells you, for every person:

- the chance they have **0, 1, or 2 copies** of the gene
- the chance they **show the trait**

> ⚠️ This is an educational probability model, not a medical test. Only a genetic test and a doctor can confirm anything.

🔒 It runs on your computer. Your family data never leaves it.

## Quick start

```
pip install -r requirements.txt
python heredity.py data/family0.csv
```

## 1. Describe your family

Create a CSV file with four columns:

```
name,mother,father,trait
Harry,Lily,James,
James,,,1
Lily,,,0
```

| Column | What to write |
|---|---|
| `name` | A unique name for each person |
| `mother`, `father` | Their parents' names, as written in the same file. If you don't know the parents, leave **both** blank |
| `trait` | `1` = has the trait, `0` = doesn't, blank = unknown |

The more `trait` values you know, the sharper the results.

## 2. Read the results

```
Harry:
  Gene:
    2: 0.0092
    1: 0.4557
    0: 0.5351
  Trait:
    True: 0.2665
    False: 0.7335
```

Reading this: Harry has about a 27% chance of showing the trait, and about a 46% chance of carrying exactly one copy of the gene.

## 3. Use it for another disease

Open `heredity.py` and edit the `PROBS` block at the top. These are the only numbers you need to change:

| Setting | What it means | Rule |
|---|---|---|
| `gene` | How common are 0, 1, or 2 copies in the general population? | The 3 values add up to 1 |
| `trait` | If someone has 0, 1, or 2 copies, what is the chance they show symptoms? | Each True/False pair adds up to 1 |
| `mutation` | The chance a copy flips when passed from parent to child | Keep it small (e.g. 0.01) |

Rule of thumb for the `trait` values:
- **Recessive disease** (needs 2 copies): high chance only for 2 copies, near 0 for 0 and 1.
- **Dominant disease** (1 copy is enough): high chance for both 1 and 2 copies.

Get your numbers from published medical sources or a genetic counselor. Don't guess them.

### Which diseases fit?

- ✅ **Fits:** conditions driven by a single gene, where symptoms depend on how many copies you have (hearing impairment from GJB2, cystic fibrosis, sickle cell disease, Huntington's disease).
- ❌ **Doesn't fit:** conditions caused by many genes or by lifestyle (type 2 diabetes, heart disease), and sex-linked conditions (hemophilia, color blindness).

## Limits

- Results are probabilities, not diagnoses.
- Keep families small (about 10 people or fewer). The computation grows very fast with each extra person.
- It assumes one gene, one trait, and parent information that is either complete or fully blank.
