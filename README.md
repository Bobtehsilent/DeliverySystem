### README

# Paketoptimering med Genetisk Algoritm

Detta projekt implementerar ett optimeringssystem för leveranser av paket baserat på genetiska algoritmer. Syftet är att maximera den totala förtjänsten genom att balansera vikt, förtjänst och leveranstider, samtidigt som straffavgifter för ej levererade paket minimeras.

## Funktioner
- **Genetisk Algoritm:** Algoritmen använder mekanismer som initialisering, fitness-beräkning, selektion, crossover och mutation för att iterativt förbättra lösningarna.
- **Visualisering:** Resultaten presenteras genom:
  - Fitness-utveckling över generationer.
  - Histogram för vikt och förtjänst fördelat på lastbilar.
  - Histogram över vikten och förtjänsten för paket kvar i lager.
- **Schemaläggning och GUI:** En enkel app låter användaren köra optimeringen manuellt eller schemalagt vid en bestämd tidpunkt.

## Användning

### 1. **Installera nödvändiga bibliotek**
Installera beroenden med pip:
```bash
pip install -r requirements.txt
```

### 2. **Köra applikationen**
Starta huvudapplikationen:
```bash
python run.py
```

- **Run Now:** Välj en specifik fil från en dialogruta eller bearbeta en fil i `data/to_process`-mappen om den finns. Kan ta några sekunder innan den startar igång på riktigt.
- **View Results:** Visa resultaten från tidigare körningar, inklusive visualiseringar och textfiler.

### 3. **Filstrukturer**
- **`data/to_process/`:** Lägg till CSV-filer som ska bearbetas. Kan också placeras i data om dom inte ska schemaläggas.
- **`results/`:** Resultat från körningar, inklusive textfiler och visualiseringar.
- **`logs/`:** Temporära loggfiler som flyttas till resultatsmappen efter körning.
- **`src/`:** Här ligger all kod för algoritmen, appen och alla dess funktionalitet.
- **`logs/`:** Här hamnar alla loggar när filer körs igenom. Vid specifika körningar genom appen flyttas dom till results när dom är klara.

### 4. **Filformat**
Ingående datafiler ska vara i CSV-format med följande kolumnrubriker:
- `Paket_id`
- `Vikt`
- `Förtjänst`
- `Deadline`

Exempel på en korrekt formaterad rad:
```
1,5.2,8,2
```

### 5. **Jupyter Notebooks**
Två notebooks finns tillgängliga i repot:
- **optimization.ipynb:** Testar olika inställningar för algoritmen för att optimera parametrar
- **delivery_use.ipynb:** Demonstrerar resultat för ett urval av filer.

## Visualiseringar
- **Fitness-utveckling:** Visar hur algoritmen förbättrar fitnessvärden över generationer.
- **Lastbilsfördelning:** Histogram för vikten och förtjänsten per lastbil.
- **Restlager:** Histogram för ej levererade paket.

## Resultat
Resultatfiler inkluderar:
- **`run_xxx_results.txt`:** En sammanfattning av optimeringsresultaten.
- **`run_xxx_truck_details.txt`:** Detaljerad fördelning av paket per lastbil.
- **`fitness_evolution.png`:** En graf på förbättringar på fitness genom generationer
- **`leftover_distribution.png`:** Ett histogram för vad som är kvar på lagret.
- **`truck_distribution.png`:** Ett histogram på fördelningen av förtjänst per lastbil.
- **`run_xxx.log`:** Loggnings historiken när filen kördes igenom. Fitness genom alla generationer.

Exempel:
```
--- Resultat för Optimering ---
Truck(Truck_1, Total Weight: 799.50, Packages: 248, Total Profit: 1188.00)
Truck(Truck_2, Total Weight: 798.20, Packages: 232, Total Profit: 1099.00)
Truck(Truck_3, Total Weight: 799.90, Packages: 232, Total Profit: 1092.00)
Truck(Truck_4, Total Weight: 799.70, Packages: 225, Total Profit: 1089.00)
Truck(Truck_5, Total Weight: 796.50, Packages: 246, Total Profit: 1218.00)
Truck(Truck_6, Total Weight: 799.80, Packages: 220, Total Profit: 1065.00)
Truck(Truck_7, Total Weight: 798.60, Packages: 222, Total Profit: 992.00)
Truck(Truck_8, Total Weight: 799.80, Packages: 203, Total Profit: 938.00)
Truck(Truck_9, Total Weight: 797.60, Packages: 212, Total Profit: 992.00)
Truck(Truck_10, Total Weight: 799.70, Packages: 217, Total Profit: 927.00)

Totalt antal paket kvar i lager: 7743
Total Förtjänst (paket i lager): 37580.0
Totala Straffavgifter (paket i lager): -9950.0
Total Förtjänst (levererade paket): 10600.0
Totala Straffavgifter (levererade paket): -957.0
Total förtjänst för levererade paket: 9643.0
```

## Avslutande Kommentarer
Detta projekt kombinerar en optimeringsalgoritm med visualiseringar och användarvänlighet genom ett GUI. Genom att utforska både algoritmens logik och resultaten erbjuder systemet ett robust verktyg för att hantera paketleveranser. För mer detaljer och exempel, se projektets Jupyter-notebooks.