# pdftextstripper

A simple tool built on top of [pdfminer.six](https://pdfminersix.readthedocs.io) to extract the content of a pdf keeping together information on the same line.

Inspired by the Java's library [PDFLayoutTextStripper](https://github.com/JonathanLink/PDFLayoutTextStripper). The result are not visually as good as this library, but they tend to keep the full content, especially when there are different font sizes and lots of text in the document.

It can be helpful to parse PDF tables.

## Install

Clone this repository, go in its root folder and run:

```bash
pip install .
```

## Use

```python
from pdfminer.high_level import extract_pages
from pdftextstripper import PdfTextStripper

test_file = open(insert_your_path_here, 'rb')

doc = extract_pages(test_file)
page = next(doc)

stripper = PdfTextStripper()
text = stripper.process_page(page)
print(text)
```

## Example

### Use case 1: Not many characters on one line

#### Results if you use [PDFLayoutTextStripper](https://github.com/JonathanLink/PDFLayoutTextStripper)

![example](sample.png)

#### Results if you use pdftextstripper

```
201 | Heure de départ pour le trajet |
sfi |  |  | 02'' |  | VL'eUvneioyn |  Gare | VH | illeneLUuNvDeI  A-U V VeENvDeRy | EDI | SAMEDI | DIMAgNénCéHrEa leets |  fêtes  |
tamixor |  |  |  |  |  |  | 34'' |  | BVeervgeèyr e | Funiculaire | 0056 |  |   1442  2530 |  39 49 59 |   4124  5203 |  39 49 59 |  10 30 50 |
pp |  |
asr |  |  | 07 |  04 19 29 39 49 59 |  04 19 29 39 49 59 |  10 30 50 |
u |
ocr |  |  | 08 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |  10 30 50 |
a |
p |
e | 09 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |  10 30 50 |
d |
s |
pme |  |  | 10 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |  10 32 52 |
T | 11 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |  12 32 52 |
12 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |  12 32 42 52 |
13 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |  02 12 22 29 39 49 59 |
14 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |
15 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |
16 |  09 19 29 41 51 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |
17 |  01 11 21 31 41 51 |  09 19 29 39 49 59 |  09 19 29 39 49 59 |
18 |  01 11 21 31 39 49 59 |  09 19 29 39 49 59 |  09 19 29 39 49 |
19 |  09 19 39 58 |  09 19 38 58 |  09 19 38 58 |
Arrêt sur demande | 20 |  18 40 |  18 40 |  18 40 |
SFOETNETS :CNOoNuSvIeDl-EARnE, S2 C jaOnMviMerE,  VJOenUdRrSe dDiE  |   | 21 |  00 20 40 |  00 20 40 |  00 20 40 |
SLuainndti,  dLuen Pdein dtee cPôâtqeu, e1se,r A asocûetn,s Liounn,d  | i du  | 22 |  00 20 40 |  00 20 40 |  00 20 40 |
Jeûne Fédéral, Noël | 23 |  00 20 40 56 |  00 20 40 56 |  00 20 40 56 |
Abonnement Voie 7 non valable | 24 |  36 |  36 |
01 |  05X |  05X |
Horaire valable dès le 11 décembre 2016 |
l | X Circule durant les nuits du vendredi au samedi, du samedi au |
dimanche et du 31.12 au 01.01 |
l | INFO-VENTE:Montreux-Vevey Tourisme Grand-Place 29 Vevey  |
l | PARTENAIRE SURFCARD:Naville St-Antoine Av. Général Guisan 15 Vevey  |
```

### Use case 2: Many characters on one line

![example](sample2.png)


#### Results if you use [PDFLayoutTextStripper](https://github.com/JonathanLink/PDFLayoutTextStripper)

```
     Lorem ipsum dolor  sit amet,  A1 100  000 Lorem  ipsum  dolor  sit  amet, A2 200 000 Lorem  ipsum  dolor sit  amet,  consectetur  aaa    A3300
     consectetur  adipiscing  elit           consectetur  adipiscing  elit …           adipiscing  elit  …
     …
```

#### Results if you use pdftextstripper

```
Lcoonresmec itpestuurm a ddiopliosrc isnitg a emlite  | t,  | A1 | 100 000 | Lcoonresmec itpestuurm a ddiopliosrc isnitg a emlite … | t,  | A2 | 200 000 | Laodripeimsc iinpgsu emlit  d… | olor sit amet, consectetur aaa   | A3 | 300 000 |
… |
```

## Notes

While [PDFLayoutTextStripper](https://github.com/JonathanLink/PDFLayoutTextStripper) is great, it is not written in Python, and trying to convert it to Python did not work well for me. I needed to use pdfminer.six to get the position of every glyph in the document. However, the results were not very good because PDFLayoutTextStripper uses a fixed length for the line, which does not allow all content to be displayed correctly when there are different font sizes or simply lots of text.

This library instead tries to keep all the content of the lines intact.

## How does it work ?

1. We get all characters of the document with their positions, replacing spaces ` ` and newlines `\n` with pipes `|` for better visualization.
2. We sort the characters in the Y-direction.
3. We build the output line by line by adding the characters.
4. We start a new line when the new character's Y-position is more than the previous one's Y-position plus its height.
5. Once a new line is detected, we sort the elements on this line in the X-direction.

## Support

Please [open an issue](https://github.com/thomassimmer/pdftextstripper/issues/new/) for
support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/thomassimmer/pdftextstripper/compare).

## License

pdftextstripper is released under the MIT License. See the LICENSE file for more details.
