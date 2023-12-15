# nelkut
![GHA workflow badge](https://github.com/EeroAnt/nelkut/workflows/CI/badge.svg)

[![codecov](https://codecov.io/gh/EeroAnt/nelkut/graph/badge.svg?token=QIODCMQO6O)](https://codecov.io/gh/EeroAnt/nelkut)

Ryhmä 4 OhTu miniprojekti 
# Backlog

[Backlog](https://docs.google.com/spreadsheets/d/1923qVBaTEvUpGSOyh8lcoLwEM9oUUErB05xrt4Awjx4/edit#gid=1)

# Sovellus

Sovellus löytyy [täältä](https://nelkut-minit.fly.dev/).

Neljännen sprintin toiminnallisuudet (DOIn ja tagien lisäys) löytyy ainoastaan lokaalista versiosta. Asennusohjeet:

1. Asenna PostgreSQL. PostgreSQL:n oman dokumentaation ohjeet löydät [täältä](https://www.postgresql.org/download/)
2. Kloonaa repo komennolla `git clone git@github.com:EeroAnt/nelkut.git`
3. Asenna riippuvuudet komennolla `poetry install`
4. Määritä .env-tiedostoon haluttu tietokannan osoite sekä `SECRET_KEY` ja aja tietokantaan schema (HUOM! Tietokannan osoite pitää olla siinä muodossa, että kirjoittamalla konsoliin psql [osoite], tietokantaan muodostetaan yhteys suoraan eli ilman, että tarvitsee erikseen kirjoittaa esim. salasanaa. Lisäksi osoitteen alussa pitää olla postgresql eikä pelkkä postgres.)
6. Haluttuun tietokantaan yhdistettynä anna komento `psql < schema.sql` reposition juurikansiossa 
7. Käynnistä sovellus komennolla `flask run`

# Projektin loppuraportti

[report.md](https://github.com/EeroAnt/nelkut/blob/main/report.md)

# Definition of done

Määritellään valmiiksi tehty tarkoittamaan sitä, että vaatimus on analysoitu, suunniteltu, ohjelmoitu, testattu, testaus automatisoitu, dokumentoitu, integroitu muuhun ohjelmistoon ja viety tuotantoympäristöön.

# Lisenssi

[LICENSE](https://github.com/EeroAnt/nelkut/blob/main/LICENSE)-tiedostosta löytyy tarkemmat tiedot lisenssioikeuksista ja -rajoituksista (MIT)
