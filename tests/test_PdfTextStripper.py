import os
import unittest

from pdfminer.high_level import extract_pages

from pdftextstripper import PdfTextStripper


class PdfTextStripperTestCase(unittest.TestCase):
    maxDiff = None

    def test_sample_output(self):
        this_folder_path = os.path.dirname(os.path.realpath(__file__))
        test_file_path = os.path.join(this_folder_path, "assets", "sample.pdf")
        test_file = open(test_file_path, 'rb')

        doc = extract_pages(test_file)
        page = next(doc)

        stripper = PdfTextStripper()
        output = stripper.process_page(page)

        expected_output = """201 | Heure de départ pour le trajet |
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
l | PARTENAIRE SURFCARD:Naville St-Antoine Av. Général Guisan 15 Vevey  |"""

        self.assertEqual(output, expected_output)
        test_file.close()

    def test_sample2_output(self):
        this_folder_path = os.path.dirname(os.path.realpath(__file__))
        test_file_path = os.path.join(this_folder_path, "assets", "sample2.pdf")
        test_file = open(test_file_path, 'rb')

        doc = extract_pages(test_file)
        page = next(doc)

        stripper = PdfTextStripper()
        output = stripper.process_page(page)

        expected_output = """Lcoonresmec itpestuurm a ddiopliosrc isnitg a emlite  | t,  | A1 | 100 000 | Lcoonresmec itpestuurm a ddiopliosrc isnitg a emlite … | t,  | A2 | 200 000 | Laodripeimsc iinpgsu emlit  d… | olor sit amet, consectetur aaa   | A3 | 300 000 |
… |"""

        self.assertEqual(output, expected_output)
        test_file.close()


if __name__ == '__main__':
    unittest.main()
