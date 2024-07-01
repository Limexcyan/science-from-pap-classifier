from pypdf import PdfWriter

merger = PdfWriter()

r1 = "raports_with_rodo/raportyczlowiek-vs.pdf"
r2 = "raports_with_rodo/raportykosmos-vs.pdf"
r3 = "raports_with_rodo/raportymateria-i-energia-vs.pdf"
r4 = "raports_with_rodo/raportytechnologia-vs.pdf"
r5 = "raports_with_rodo/raportyzdrowie-vs.pdf"
r6 = "raports_with_rodo/raportyziemia-vs.pdf"
r7 = "raports_with_rodo/raportyzycie-vs.pdf"

list_of_pdfs = [r1, r2, r3, r4, r5, r6, r7]

for pdf in list_of_pdfs:
    merger.append(pdf)

merger.write('raports-merged.pdf')
merger.close()