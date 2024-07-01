from dzial import *

df_to_repear = pd.read_csv('articles.csv')

rodo = '''Zgodnie z Rozporządzeniem Parlamentu Europejskiego i Rady (UE) z dnia  27 kwietnia 2016  r. w sprawie ochrony osób fizycznych w związku z przetwarzaniem danych osobowych i w sprawie swobodnego przepływu takich danych oraz uchylenia dyrektywy 95/46/WE (ogólne rozporządzenie o ochronie danych) informujemy Cię o przetwarzaniu Twoich danych. Administratorem danych jest Fundacja PAP,z siedzibą w Warszawie przy ulicy Bracka 6/8, 00-502 Warszawa. Chodzi o dane, które są zbierane w ramach korzystania przez Ciebie z naszych usług, w tym stron internetowych, serwisów i innych funkcjonalności udostępnianych przez Fundację PAP, głównie zapisanych w plikach cookies i innych identyfikatorach internetowych, które są instalowane na naszych stronach przez nas oraz naszych zaufanych partnerów Fundacji PAP.

Gromadzone dane są wykorzystywane wyłącznie w celach:
• świadczenia usług drogą elektroniczną
• wykrywania nadużyć w usługach
• pomiarów statystycznych i udoskonalenia usług Podstawą prawną przetwarzania danych jest świadczenie usługi i jej doskonalenie, a także zapewnienie bezpieczeństwa co stanowi prawnie uzasadniony interes administratora Dane mogą być udostępniane na zlecenie administratora danych podmiotom uprawnionym do uzyskania danych na podstawie obowiązującego prawa.

Osoba, której dane dotyczą, ma prawo dostępu do danych, sprostowania i usunięcia danych, ograniczenia ich przetwarzania. Osoba może też wycofać zgodę na przetwarzanie danych osobowych.
Wszelkie zgłoszenia dotyczące ochrony danych osobowych prosimy kierować na adres fundacja@pap.pl lub pisemnie na adres Fundacja PAP, ul. Bracka 6/8, 00-502 Warszawa z dopiskiem "ochrona danych osobowych"

Więcej o zasadach przetwarzania danych osobowych i przysługujących Użytkownikowi prawach znajduje się w Polityce prywatności. Dowiedz się więcej. Wyrażam zgodę FUNDACJA PAPBracka 6/800-502, Warszawanaukawpolsce@pap.pl(+48 22) 509 27 07(+48 22) 509 23 88'''


for i in range(len(df_to_repear)):
    df_to_repear['content'][i] = df_to_repear['content'][i].replace(rodo, '')
    print(i)

df_to_repear.to_csv('articles_without_rodo.csv', index=False)


