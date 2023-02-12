# Projektna_naloga

Projekt pri predmetu __Programiranje 1__. 
Analizirala bom prvih 24 strani (~1000 vzorcev) najbolj prodajanih avdioknjig v angleškem jeziku na spletni strani [Audible](https://www.audible.com/search) .

## Podatki

Za vsako avdio knjigo bom pokrila:
* naslov
* id knjige
* datum izida
* dolžina
* opis
* avtor in bralec
* cena
* ocena
* kategorije

Najprej bom iz spletne strani pobrala omenjene podatke in jih spravila v audiobooks.csv. Pri tem posamezne ocene in kategorije pobiram ločene strani dane knjige.

## Hipoteze in ugotovitve

1) Cena je odvisna od leta izida
  
  <sup>To hipotezo lahko hitro ovržemo. Že iz korelacijskega grafa se hitro vidi, da je cena praktično neodvisna od datuma izida. Še največjo povezavo ima z dolžino. </sup>

2) Iz opisa znamo napovedati kategorijo

  <sup>Za to sem napisala naivni bayesov klasifikator, v pomoč so mi bili zapiski iz predavanj. Več se nahaja v category_bayes.ipynb</sup>

3) Iz ostalih podatkov znamo napovedati ceno knjige

  <sup>Z različnimi modeli strojnega učenja sem iz ostalih podatkov poskušala predvideti ceno knjig. Pri tem me je začela bolj zanimati primerjava uspešnosti med njimi. Več o tem je zapisano v predict_price.ipynb</sup>

## Viri

[Baza podatkov z imeni](https://archive.ics.uci.edu/ml/datasets.php)
[Zapiski iz predavanj](https://matija.pretnar.info/programiranje-1/00-uvod.html)

