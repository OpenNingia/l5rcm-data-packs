# Modificatori di statistiche del personaggio

Elenco di **tecniche di scuola, kata, kiho, tattoo, ancestri, percorsi (path), merit, flaw ed effetti di armi/armature** presenti nei data pack di L5RCM il cui effetto meccanico **modifica una statistica del personaggio** (Anelli, Tratti, Armor TN, Reduction/RD, Iniziativa, Ferite/penalità da ferita, Onore/Gloria/Status, Insight, Punti Vuoto, bonus/malus persistenti a tiri di attacco/danno/abilità/tratto, Movimento).

> **Note metodologiche**
> - Sono stati **esclusi** gli effetti puramente narrativi, le azioni extra, i ri-tiri e le abilità senza una variazione numerica di statistica. In caso di dubbio su una variazione numerica, la voce è stata inclusa.
> - Gli **incantesimi (spells)** non sono stati inclusi (effetti magici temporanei, fuori ambito).
> - Lo `slug` è l'attributo `id` del record; quando esiste un attributo `rule=` riconosciuto dal motore dell'app è indicato come `id (rule=...)`.
> - Molti effetti sono descritti in testo libero nei `<Description>`: il "Bonus/Malus" è una sintesi, fare riferimento al testo originale per i dettagli e le condizioni.

**Abbreviazioni dei pack:** Core = `core_pack` · BoA = Book of Air · BoE = Book of Earth · BoF = Book of Fire · BoV = Book of Void · BoW = Book of Water · GC = Great Clan · EE = Emerald Empire · SF = Sword & Fan · SH = Strongholds · LBS = Little Book of Sin · CDP = Community Data Pack · IH = Imperial Histories

---

## 1. Kata

| Fonte | Nome | slug/rule | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|
| Core | Breath of Wind Style | breath_of_wind_style | Iniziativa | +2 Iniziativa (Reactions Stage, stacca) |
| Core | Striking as Air | striking_as_air | Armor TN | +Air Ring (Defense Stance) |
| Core | Iron Forest Style | iron_forest_style | Tiri attacco (Air al posto di Agility) | usa Air Ring invece di Agility (attacco con lancia/asta) |
| Core | Veiled Menace Style | veiled_menace_style | Armor TN | +Stealth Skill Rank (1/turno, singolo attacco) |
| Core | Iron in the Mountains Style | iron_in_the_mountains_style | Armor TN (Defense Stance) | usa Earth Ring invece di Air Ring |
| Core | Striking as Earth | striking_as_earth | Reduction (Earth) | +Earth Ring RD (Full Defense, cumulativo) |
| Core | Indomitable Warrior Style | indomitable_warrior_style | Penalità TN da Wound Rank | −Earth Ring alle penalità TN da ferite |
| Core | Striking as Fire | striking_as_fire | Tiri attacco | +Fire Ring a un attacco/round (Full Attack) |
| Core | Disappearing World Style | disappearing_world_style | Tiri danno (Agility al posto di Strength) | usa Agility invece di Strength per il danno (1/turno) |
| Core | Reckless Abandon Style | reckless_abandon_style | Armor TN | +Fire Ring (Full Attack Stance) |
| Core | Balance The Elements Style | balance_the_elements_style | Iniziativa (Void al posto di Reflexes) | usa Void Ring invece di Reflexes per l'Iniziativa |
| Core | Striking as Void | striking_as_void | Armor TN | +Void Ring (Center Stance) |
| Core | Strength Of Purity Style | strength_of_purity_style | Tiri danno (Honor al posto di Strength) | tira Honor Rank invece di Strength+DF (1/turno) |
| Core | Strength In Arms Style | strength_in_arms_style | Tiri attacco (Strength al posto di Agility) | usa Strength invece di Agility (arma pesante, 1/turno) |
| Core | Striking as Water | striking_as_water | Movimento | +5 ft di movimento (Attack Stance, Free Action) |
| BoA | North Wind Style | north_wind_style | Tiro attacco (Increased Damage Maneuver) | +Air Ring al totale |
| BoA | South Wind Style | south_wind_style | Tiro attacco (Called Shot/Knockdown) | +Air Ring al totale |
| BoE | The Power of the Mountain | the_power_of_the_mountain | Armor TN / Tiri danno | −fino a Earth Ring Armor TN; +stesso valore a tutti i danni |
| BoE | The Strength of the Mountain | the_strength_of_the_mountain | Iniziativa / Armor TN | −fino a Earth Ring Iniziativa; +stesso valore Armor TN |
| BoE | Lee of the Stone | lee_of_the_stone | Armor TN (Defense/Full Defense) | +Earth Ring Armor TN |
| BoE | Strike as the Avalanche | strike_as_the_avalanche | Strength (danno Heavy Weapons) | +1 Rank Strength effettivo |
| BoE | Weathered and Unbroken | weathered_and_unbroken | Water (movimento) | Water contato 2 Rank in meno (min 1) per il movimento |
| BoW | Waves upon the Breakers | waves_upon_the_breakers | Danno (arma con 3+ rank) | +1k0 |
| BoW | Leaves in the Stream | leaves_in_the_stream | Armor TN / Movimento | −fino a 5×Water Armor TN, +stesso al Movimento |
| BoW | Power of the Tsunami | power_of_the_tsunami | Reduction nemica ignorata | ignora RD = Water Ring, 1/round |
| GC | Strength Of The Crab | strength_of_the_crab | Reduction (in armatura, Attack Stance) | +2 RD |
| GC | Strength Of The Crane | strength_of_the_crane | Armor TN (spada/lancia) | +(Honor Rank − 3, min 1) |
| GC | Strength Of The Dragon | strength_of_the_dragon | Armor TN (katana + wakizashi) | +3 |
| GC | Strength Of The Lion | strength_of_the_lion | Iniziativa (alleato) | +3 |
| GC | Son Of Storms | son_of_storms | Reduction nemica (arma Small) | −1 RD |
| GC | Strength of The Mantis | strength_of_the_mantis | Penalità attacco a distanza (nemico in mischia) | −3 alla penalità |
| GC | Dance Of The Winds | dance_of_the_winds | Iniziativa (asta/lancia) | +3 |
| GC | Strength Of The Phoenix | strength_of_the_phoenix | Armor TN (persona protetta) | +3 |
| GC | Strength Of The Scorpion | strength_of_the_scorpion | Danno (dopo Feint) | +3 Ferite |
| GC | Strength Of The Unicorn | strength_of_the_unicorn | Armor TN + Reduction (cavalcatura) | +3 Armor TN, +3 RD |
| GC | Strength Of The Spider | strength_of_the_spider | Tutti i tiri nemici (dopo 15+ Ferite) | −3 al Turno successivo |

---

## 2. Kiho

| Fonte | Nome | slug/rule | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|
| Core | Air Fist | air_fist | Iniziativa / danno disarmato | +5 Iniziativa; −Air Ring danno disarmato |
| Core | Soul of the Four Winds | soul_of_the_four_winds | Armor TN | +Insight Rank + Air Ring |
| Core | Stain Upon the Soul | stain_upon_the_soul | Penalità TN (bersaglio) | bersaglio subisce penalità TN come Wound Ranks = Air Ring |
| Core | Steal the Air Dragon | steal_the_air_dragon | Tiri Stealth | +Air Ring dadi tirati e tenuti su Stealth |
| Core | Cleansing Spirit | cleansing_spirit | Tiri resistenza veleno/malattia | +metà Earth Ring dadi |
| Core | Embrace the Stone | embrace_the_stone | Reduction | +2× Earth Ring RD (stacca) |
| Core | Grasp of the Earth Dragon | grasp_of_the_earth_dragon | Penalità TN da Wound Rank | −Earth Ring alle penalità TN da ferite |
| Core | Speed of the Mountains | speed_of_the_mountains | Movimento (Water Ring bersaglio) | Water Ring del bersaglio −2 per il movimento |
| Core | Fire's Fleeting Speed | fires_fleeting_speed | Movimento | +5 ft alle Move Action |
| Core | Flame Fist | flame_fist | Penalità TN (bersaglio) | bersaglio −3× Fire Ring TN a tutte le azioni |
| Core | Partaking the Waves | partaking_the_waves | Reduction | +Water Ring RD (stacca) |
| Core | Song of the World | song_of_the_world | Iniziativa | bersaglio −5 Iniziativa, self +5 Iniziativa |
| Core | Death Touch | death_touch | Tutti gli Anelli (bersaglio) | Anelli del bersaglio −1/ora, max −Insight Rank |
| Core | Touch the Void Dragon | touch_the_void_dragon | Un Anello + Tratti | +1 Rank a un Anello ambientale e ai suoi Tratti |
| BoA | Calling the East Wind | calling_the_east_wind | Tiro danno (calcio) | +1k0 danno |
| BoE | The Rolling Avalanche | the_rolling_avalanche | Tiro danno (atemi) | +Earth Ring k0 |
| BoE | Earth Palm | earth_palm | Tiro danno/attacco nemico (malus) | −4k0 danno al bersaglio (Water), o 2 Raise forzate (Fire) |
| BoE | Rising Mountain | rising_mountain | Reduction | +2× Raise RD per Raise nemica (max Earth ×5) |
| BoF | The Mind's Fire | the_minds_fire | Tiri abilità basati su Intelligence | +2k2 (poi Fatigued) |
| BoV | Rebuke of the Heavens | rebuke_of_the_heavens | Tutti i tiri del bersaglio (X = Monk School Ranks) | −Xk1 |
| BoW | Musubi | musubi | Armor TN | +Water Ring + Staves Rank (+Water per Simple Action) |

---

## 3. Tattoo

| Fonte | Nome | slug/rule | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|
| Core | Bamboo | tattoo_bamboo | Armor TN | +2× School Rank + 5 |
| Core | Blaze | tattoo_blaze | Danno disarmato | +Fire Ring + School Rank danno da fuoco |
| Core | Centipede | tattoo_centipede | Movimento | muovi Water Ring ×100' (Complex Action) |
| Core | Crab | tattoo_crab | Reduction | +Earth Ring RD |
| Core | Crane | tattoo_crane | Tiri abilità sociali | +School Rank + Air Ring dadi bonus |
| Core | Hawk | tattoo_hawk | Movimento (salto) | salta Water Ring ×25' |
| Core | Lion | tattoo_lion | Rank abilità Bugei | +School Rank rank in una Bugei Skill |
| Core | Mountain | tattoo_mountain | Penalità da ferita | −School Rank + 2 a tutte le penalità da ferita |
| Core | Scorpion | tattoo_scorpion | Tiri Stealth | +School Rank dadi su Stealth |
| Core | Phoenix | tattoo_phoenix | Ferite (cura) | cura School Rank ×10 Ferite (auto a Down) |
| Core | Wind | tattoo_wind | Movimento | nessun cap di movimento Water Ring ×20 |
| Core | Wolf | tattoo_wolf | Tiri caccia (Tracking) | +School Rank Free Raise |
| BoE | Bear | tattoo_bear | Stamina / Strength | +School Rank Stamina, o +½ School Rank (arr. su) Strength |
| BoF | Volcano | tattoo_volcano | Reduction (vs infiammabili) | RD 5 vs armi/frecce in legno |
| BoW | Wave | tattoo_wave | Tiro contrapposto Strength Knockdown (+/resist) | +Xk0 (X = Insight Rank) |
| CDP | Bat | tattoo_bat | Iniziativa | +1 dado + School Rank |
| CDP | Butterfly | tattoo_butterfly | Void Ring (req. kiho); attacco atemi disarmato | Void +1 rank; +School Rank attacco disarmato |
| CDP | Cricket | tattoo_cricket | Water Ring (req. kiho); attacco atemi disarmato | Water +1 rank; +School Rank attacco disarmato |
| CDP | Hurricane-Tsunami | tattoo_hurricane | Air Ring (req. kiho); attacco atemi disarmato | Air +1 rank; +School Rank attacco disarmato |
| CDP | Hare | tattoo_hare | Water Ring (movimento) | +2× School Rank a Water Ring per il movimento |
| CDP | Orichi | tattoo_orichi | TN da colpire (in lotta); tiri di lotta | +2× School Rank TN; +1 dado non tenuto |
| CDP | Panther | tattoo_panther | Tiri Stealth/Hunting | +School Rank dadi |
| CDP | Crow | tattoo_crow | Tiri resistenza al Taint | +2× School Rank dadi |
| CDP | Snow Crane | tattoo_snowcrane | Punti Vuoto; tiri abilità duello | +1 Void (solo duello); +School Rank a tiri duello |
| CDP | Torii | tattoo_torii | TN tiro assessment avversario (duello) | +School Rank ×5 |
| CDP | Nightingale | tattoo_nightingale | TN proprio tiro assessment (duello) | −10 |

---

## 4. Effetti di armi e armature

| Fonte | Nome | slug/rule | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|
| Core | Daikyu rule | daikyu_rule | TN tiri attacco | +10 TN se usato a piedi |
| Core | Lance special rule | lance_special_rule | TN tiri attacco | +5 TN (a cavallo) / +10 TN (a piedi) in mischia senza movimento |
| Core | No shoot horseback | no_shoot_horseback_rule | TN tiri attacco | +10 TN da cavallo |
| Core | Light armor rule | light_armor_rule | TN tiri Athletics/Stealth | +5 TN |
| Core | Heavy armor rule | heavy_armor_rule | TN tiri Agility/Reflexes | +5 TN |
| Core | Riding armor rule | riding_armor_rule | Armor TN / TN tiri Agility-Reflexes | +12 Armor TN (a cavallo); +5 TN Agility/Reflexes (a piedi) |
| BoF | Blade of Truths | blade_of_truths | Tiro danno nemico vs portatore (malus) | +1k1 danno nemico vs portatore (quando maledetta) |
| BoF | Bloodsword Ambition | bloodsword_ambition | Tiri Sincerity (Deceit)/Stealth | +2k2 continuo |
| BoF | Bloodsword Judgement | bloodsword_judgement | Tiri attacco (Handan) | +2k0 continuo |
| BoF | Bloodsword Passion | bloodsword_passion | Tiri Kenjutsu | +1k0 continuo |
| BoF | Bloodsword Revenge | bloodsword_revenge | Tiri Kenjutsu (Fukushu) | +3k0 continuo; concede Combat Reflexes + Quick |
| LBS | Large Wooden Shield | (Armor) large_shield_rule | Armor TN; tiri Agility/Reflexes | +5 TN base; +15 vs distanza, +5 vs mischia; +8/+12 TN penalità a tiri Agi/Ref |
| LBS | Senpet Chain Shirt | (Armor) senpet_chain_shirt | Armor TN; tiri Agility/Reflexes | +5 TN (nessuno vs perforanti); +3 TN penalità a tiri Agi/Ref |
| LBS | Khopesh (Str bonus) | heavy_weapon_khopesh | Danno (DR) | +bonus Strength al DR (come ascia/arma pesante) |

---

## 5. Merit (Vantaggi)

| Fonte | Nome | slug/rule | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|
| Core | Inheritance | inheritance | Tiri abilità (con oggetto ereditato) | +1k1 su tiri abilità non combattivi |
| Core | Balance | balance | Tiri resistenza Intimidazione/Tentazione | +1k0 |
| Core | Clear Thinker | clear_thinker | Tiri contrapposti vs manipolazione | +1k0 |
| Core | Daredevil | daredevil | Tiro Athletics (spesa Void) | +3k1 invece di +1k1 |
| Core | Dark Paragon (Control) | dark_paragon_control | Tiro abilità sociale | ri-tiro + (+5) |
| Core | Dark Paragon (Determination) | dark_paragon_determination | Penalità TN/ferita | annulla su un tiro abilità/incantesimo |
| Core | Dark Paragon (Insight) | dark_paragon_insight | Tiri Awareness | ri-tiro + (+5) |
| Core | Dark Paragon (Knowledge) | dark_paragon_knowledge | Tiri Intelligence | ri-tiro + (+5) |
| Core | Dark Paragon (Strength) | dark_paragon_strength | Tiro danno | ri-tiro + (+5) |
| Core | Dark Paragon (Will) | dark_paragon_will | Ferite | annulla 10 Ferite |
| Core | Forbidden Knowledge (Gozoku) | forbidden_knowledge_gozoku (rule=fk_gozoku) | Tiri abilità sociali (vs Gozoku) | +1k1 |
| Core | Forbidden Knowledge (Kolat) | forbidden_knowledge_kolat (rule=fk_kolat) | Tiri abilità sociali (vs Kolat) | +1k1 |
| Core | Irreproachable | irreproachable | Tiro contrapposto vs Tentazione | +1k0 |
| Core | Paragon (Compassion) | paragon_compassion | Tiro per aiutare inferiori (spesa Void) | +2k2 invece di +1k1 |
| Core | Paragon (Courage) | paragon_courage | Tiri vs Intimidazione/Paura | +1k1 |
| Core | Paragon (Courtesy) | paragon_courtesy | Tiro Etiquette | +2k0 |
| Core | Paragon (Duty) | paragon_duty | Penalità TN/ferita | annulla su tiro abilità/incantesimo (spesa Void) |
| Core | Paragon (Honesty) | paragon_honesty | Tiro Sincerity (Honesty) | +1k1 |
| Core | Paragon (Honor) | paragon_honor | Tiri vs Tentazione/Intimidazione | +2× Honor Rank |
| Core | Paragon (Sincerity) | paragon_sincerity | Tiri Sincerity contrapposti | +2k0 |
| Core | Precise Memory | precise_memory | Tiro Tratto Intelligence | +1k1 |
| Core | Tactician | tactician | Tiro Mass Battle Table | +/−5 |
| Core | Virtuous | virtuous (rule=virtuous) | Onore | +1 Honor Rank |
| Core | Wary | wary | Tiro Investigation (Notice) | +1k1 |
| Core | Crab Hands | crab_hands | Abilità arma (non addestrato) | trattata come rank 1 |
| Core | Dangerous Beauty | dangerous_beauty | Tiri Temptation | +1k0 |
| Core | Hands of Stone | hands_of_stone | Tiri danno disarmato | +0k1 |
| Core | Large | large (rule=large) | Tiri danno (arma da mischia grande) | +1k0 |
| Core | Prodigy | prodigy (rule=prodigy) | Tiro School Skill | +1k0 |
| Core | Quick | quick | Iniziativa | +Reflexes Trait |
| Core | Quick Healer | quick_healer | Stamina (per recupero ferite) | +2 rank |
| Core | Strength of the Earth | strength_of_the_earth (rule=strength_of_earth) | Penalità TN da Wound Rank | ridotte di 3 |
| Core | Voice | voice | Tiro Perform (voce) | +1k1 |
| Core | Fame | fame (rule=fame) | Gloria | +1 Glory Rank |
| Core | Heart of Vengeance | heart_of_vengeance | Tiri contrapposti vs fazione bersaglio | +1k1 |
| Core | Hero of the People | hero_of_the_people | TN riconoscimento (popolani) | −10 TN |
| Core | Imperial Spouse | imperial_spouse (rule=imperial_spouse) | Status; tiri sociali (Imperiali) | +0.5 Status; +1k1 |
| Core | Leadership | leadership | Iniziativa (alleato) | +School Rank +1k1 |
| Core | Perceived Honor | perceived_honor | Onore (percepito) | +1 rank/livello |
| Core | Social Position | social_position (rule=social_position) | Status | +1 Status Rank |
| Core | Benten's Blessing | bentens_blessing | Tiro abilità sociale (persuasione) | +0k1 |
| Core | Bishamon's Blessing | bishamons_blessing | Tiri Tratto Strength | +1k0 (e Raise bonus) |
| Core | Blood of Osano-Wo | blood_of_osanowo | Danno da incantesimi di forze naturali | −1k1 |
| Core | Chosen by the Oracles (Air) | chosen_by_the_oracles_air_ | Tiri Air Ring | +1k1 |
| Core | Chosen by the Oracles (Earth) | chosen_by_the_oracles_earth_ | Tiri Earth Ring | +1k1 |
| Core | Chosen by the Oracles (Fire) | chosen_by_the_oracles_fire_ | Tiri Fire Ring | +1k1 |
| Core | Chosen by the Oracles (Void) | chosen_by_the_oracles_void_ | Tiri Void Ring | +1k1 |
| Core | Chosen by the Oracles (Water) | chosen_by_the_oracles_water_ | Tiri Water Ring | +1k1 |
| Core | Daikoku's Blessing | daikokus_blessing | Tiri Commerce | +1k1 |
| Core | Ebisu's Blessing | ebisus_blessing | Tiri abilità sociali (non-samurai) | +1k1 |
| Core | Enlightened | enlightened (rule=enlightened) | Void Ring (costo XP) | −2 XP per incremento |
| Core | Friend of the Elements (Air) | friend_of_the_elements_air | Tiri Tratto Air | +1 Free Raise |
| Core | Friend of the Elements (Earth) | friend_of_the_elements_earth | Tiri Tratto Earth | +1 Free Raise |
| Core | Friend of the Elements (Fire) | friend_of_the_elements_fire | Tiri Tratto Fire | +1 Free Raise |
| Core | Friend of the Elements (Void) | friend_of_the_elements_void | Tiri Tratto Void | +1 Free Raise |
| Core | Friend of the Elements (Water) | friend_of_the_elements_water | Tiri Tratto Water | +1 Free Raise |
| Core | Friendly Kami (Air) | friendly_kami_air | Tiri lancio incantesimi (Air Sense/Commune/Summon) | +1k1 |
| Core | Friendly Kami (Earth) | friendly_kami_earth | Tiri lancio incantesimi (Earth Sense/Commune/Summon) | +1k1 |
| Core | Friendly Kami (Fire) | friendly_kami_fire | Tiri lancio incantesimi (Fire Sense/Commune/Summon) | +1k1 |
| Core | Friendly Kami (Void) | friendly_kami_void | Tiri lancio incantesimi (Void Sense/Commune/Summon) | +1k1 |
| Core | Friendly Kami (Water) | friendly_kami_water | Tiri lancio incantesimi (Water Sense/Commune/Summon) | +1k1 |
| Core | Fukurokujin's Blessing | fukurokujins_blessing | Tiro Lore scelto | +1k1 |
| Core | Great Destiny | great_destiny | Ferite | ridotte a 1 invece della morte (1/sessione) |
| Core | Jurojin's Blessing | jurojins_blessing | Tiri resistenza malattia/veleno | +2k0 |
| Core | Kharmic Tie 1 | kharmic_tie_1 | Tiri attacco (proteggendo il legato) | +1k1 per livello (1/sessione) |
| Core | Magic Resistance | magic_resistance | TN incantesimi elementali su di te | +3 per rank |
| Core | Touch of the Spirit Realms (Chikushudo) | touch_of_the_spirit_realms_chikushudo | Tiri Animal Handling | +1k1 |
| Core | Touch of the Spirit Realms (Gaki-do) | touch_of_the_spirit_realms_gakido | Ferite | recupera 5 all'uccisione |
| Core | Touch of the Spirit Realms (Jigoku) | touch_of_the_spirit_realms_jigoku | Attacco/tiri Tratto e abilità fisiche | +Taint Rank (×2 se Lost) |
| Core | Touch of the Spirit Realms (Maigo no Musha) | touch_of_the_spirit_realms_maigo_no_musha | Gloria | +1 (quando il premio >3) |
| Core | Touch of the Spirit Realms (Meido) | touch_of_the_spirit_realms_meido | Tiri sociali contrapposti di manipolazione | +2k0 |
| Core | Touch of the Spirit Realms (Sakkaku) | touch_of_the_spirit_realms_sakkaku | Tiri Sincerity (Deceit) | +1k1 |
| Core | Touch of the Spirit Realms (Tengoku) | touch_of_the_spirit_realms_tengoku | Tiri Earth Ring vs Taint | +2k0 |
| Core | Touch of the Spirit Realms (Toshigoku) | touch_of_the_spirit_realms_toshigoku | Movimento (Move per attaccare) | +5 ft |
| Core | Touch of the Spirit Realms (Yomi) | touch_of_the_spirit_realms_yomi | Tiri School Skill scelti | +1k0 |
| BoV | Reincarnated | reincarnated | Tiri abilità (3 abilità non di Scuola) | +1k0 |
| BoV | Watanu-Trained | watanu_trained | Tiri Craft (una lavorazione metallica) | +1k1 |
| BoV | Iron Heart Native | iron_heart_native | Tiri Stamina / tiri Strength non da danno | +1k0 |
| BoV | Laughing Plains Native | laughing_plains_native | Tiri resistenza alla Paura | +5 |
| BoV | Sacred Forest Native | sacred_forest_native | Tiri Lore: Theology / Lore: Spirit Realms | +1k0 |

---

## 6. Flaw (Svantaggi)

| Fonte | Nome | slug/rule | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|
| Core | Consumed (Control) | consumed_control | Tiri Etiquette/Sincerity | −1k1 |
| Core | Consumed (Determination) | consumed_determination | Punti Vuoto (potenziamento dadi) | non può spenderli sui tiri di dado |
| Core | Consumed (Strength) | consumed_strength | Tiro Etiquette | −1k0 |
| Core | Consumed (Will) | consumed_will | Tiri Courtier/Temptation | −1k1 |
| Core | Disbeliever | disbeliever | Tiri abilità sociali (shugenja/monaci) | +5 TN |
| Core | Failure of Bushido (Courage) | failure_of_bushido_courage | Tutti i tiri (vs Gloria/Status/Shadowlands superiori) | +5 TN |
| Core | Failure of Bushido (Duty) | failure_of_bushido_duty | Ferite (Void) | non può spendere Void per annullare ferite |
| Core | Failure of Bushido (Honesty) | failure_of_bushido_honesty | Tiri vs Intimidazione/Tentazione | non può aggiungere Honor Rank |
| Core | Failure of Bushido (Honor) | failure_of_bushido_honor | Tiri vs Intimidazione/Tentazione | non può aggiungere Honor Rank |
| Core | Frail Mind | frail_mind | Tiri Willpower contrapposti | avversario +2k0 |
| Core | Greedy | greedy | Temptation (Bribery) avversario | avversario +1k1 |
| Core | Gullible | gullible | Sincerity (Deceit) avversario | avversario +1k1 |
| Core | Idealistic | idealistic | Onore (perdita) | perdita di Onore +1 |
| Core | Lost Love | lost_love | Tutti i TN (quando ricordato) | +5 TN |
| Core | Obtuse | obtuse (rule=obtuse) | Costo XP High Skill | raddoppiato |
| Core | Phobia | phobia | Tutti i TN (vs la fobia) | +5 per rank |
| Core | Soft-Hearted | softhearted | Tutti i TN (dopo aver ucciso) | +10 per un giorno |
| Core | Bad Eyesight | bad_eyesight (rule=bad_eyesight) | Tiri attacco a distanza e Perception | −1k1 |
| Core | Bad Health | bad_health (rule=bad_health) | Earth Ring (ferite/malattia) | −1 rank |
| Core | Blind | blind (rule=blind) | Attacco a distanza/mischia; Armor TN; Water Ring (mov.) | −3k3 distanza, −1k1 mischia; TN=Reflexes+5; Water −2 rank |
| Core | Disturbing Countenance | disturbing_countenance | Tiri abilità sociali | +5 TN |
| Core | Lame | lame | Water Ring (movimento); tiri Agility (gambe) | Water Ring=1; +10 TN |
| Core | Low Pain Threshold | low_pain_threshold | Penalità TN da Wound Rank | +5 per ogni rank |
| Core | Missing Limb | missing_limb | TN che coinvolgono l'arto | +10 TN |
| Core | Permanent Wound | permanent_wound | Ferite (primo Wound Rank) | il primo rank è sempre pieno |
| Core | Small | small (rule=small) | Water Ring (movimento); tiri danno mischia | Water −1 rank; −1k0 danno |
| Core | Weakness (Agility) | weakness_agility (rule=weak_agility) | Agility | −1 rank |
| Core | Weakness (Awareness) | weakness_awareness (rule=weak_awareness) | Awareness | −1 rank |
| Core | Weakness (Intelligence) | weakness_intelligence (rule=weak_intelligence) | Intelligence | −1 rank |
| Core | Weakness (Perception) | weakness_perception (rule=weak_perception) | Perception | −1 rank |
| Core | Weakness (Reflexes) | weakness_reflexes (rule=weak_reflexes) | Reflexes | −1 rank |
| Core | Weakness (Stamina) | weakness_stamina (rule=weak_stamina) | Stamina | −1 rank |
| Core | Weakness (Strength) | weakness_strength (rule=weak_strength) | Strength | −1 rank |
| Core | Weakness (Willpower) | weakness_willpower (rule=weak_willpower) | Willpower | −1 rank |
| Core | Antisocial | antisocial | Tiri abilità sociali | −1k0 (rank1) / −1k1 (rank2) |
| Core | Dishonored | dishonored | Status | Status Rank 1, non può guadagnarne |
| Core | Gaijin Name | gaijin_name | Tiri abilità sociali (esplosioni dadi) | i dadi esplodono solo una volta |
| Core | Infamous | infamous | Gloria | sostituita da Infamy Rank |
| Core | Lechery | lechery | Temptation (Seduction) avversario | avversario +1k1 |
| Core | Social Disadvantage | social_disadvantage (rule=social_disadvantage) | Status | Status Rank 0 |
| Core | Benten's Curse | bentens_curse | TN tiro Etiquette | +10 TN |
| Core | Bishamon's Curse | bishamons_curse (rule=bishamon_curse) | Strength (per tiri danno) | −1 rank |
| Core | Cursed by the Realm (Chikushudo) | cursed_by_the_realm_chikushudo | Tiri Animal Handling | −1k1 |
| Core | Cursed by the Realm (Jigoku) | cursed_by_the_realm_jigoku | Tiri resistenza al Taint | −1k1 |
| Core | Cursed by the Realm (Maigo no Musha) | cursed_by_the_realm_maigo_no_musha | Tiri vs spiriti | −1k1 |
| Core | Cursed by the Realm (Meido) | cursed_by_the_realm_meido | Tiri basati su Perception | −1k0 |
| Core | Cursed by the Realm (Tengoku) | cursed_by_the_realm_tengoku | Tutti i TN (nei templi del Cielo) | +10 TN |
| Core | Daikoku's Curse | daikokus_curse | Tiri Commerce; koku iniziali | −1k1; koku −1 |
| Core | Dark Fate | dark_fate | Ferite | ridotte a 1 invece della morte (1/sessione) |
| Core | Ebisu's Curse | ebisus_curse | Tiri abilità sociali (non-samurai) | −1k1 |
| Core | Fukurokujin's Curse | fukurokujins_curse | TN tiro Lore | +5 TN |
| Core | Haunted | haunted | Un tiro di dado (1/sessione) | −1k1 |
| Core | Hotei's Curse | hoteis_curse | Costo attivazione Punto Vuoto | richiede 2 Punti Vuoto |
| Core | Jurojin's Curse | jurojins_curse | Tiri resistenza veleno/malattia | −2k0 |
| Core | Lord Moon's Curse | lord_moons_curse | Punti Vuoto (max) | +1 Punto Vuoto durante la luna piena |
| Core | Touch of the Void | touch_of_the_void | Bonus spesa Void | +2k1 invece di +1k1 |
| Core | Wrath of the Kami | wrath_of_the_kami | Lancio incantesimi (vs di te) | nemico +1 Free Raise |

---

## 7. Tecniche di Scuola (Core)

Include il bonus `+1` al Tratto di Scuola (assegnato alla creazione) e le tecniche con effetto sulle statistiche.

| Scuola | Nome | slug | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|
| Ichiro Bushi | School Trait | badger_ichiro_bushi_school | Strength | +1 |
| Ichiro Bushi | Crushing Blow | badger_crushing_blow | Armor TN nemica / Reduction | ignora armatura su TN; ignora 1 Rank RD (disarmato) |
| Ichiro Bushi | Return The Strike | badger_return_the_strike | Iniziativa / attacco / danno | −20 Init; +Strength dadi non tenuti ad attacco e danno (2 round) |
| Komori Shugenja | School Trait | bat_komori_shugenja_school | Awareness | +1 |
| Heichi Bushi | School Trait | boar_heichi_bushi_school | Strength | +1 |
| Heichi Bushi | The Charge Of The Boar | boar_the_charge_of_the_boar | Danno (lancia) | +0k1 |
| Heichi Bushi | The Anger Of The Boar | boar_the_anger_of_the_boar | Penalità da ferita | −1 Wound Rank di penalità TN |
| Heichi Bushi | Beyond The Mountains | boar_beyond_the_mountains | Attacco | +2k0 (attacco gratuito da Full Defense) |
| Hida Bushi | School Trait | crab_hida_bushi_school | Stamina | +1 |
| Hida Bushi | The Way Of The Crab | crab_the_way_of_the_crab | Danno (arma pesante) / TN | +1k0 danno; ignora penalità TN armatura pesante |
| Hida Bushi | The Mountain Does Not Move | crab_the_mountain_does_not_move | Reduction | +RD = Earth Ring |
| Hida Bushi | Devastating Blow | crab_devastating_blow | Reduction nemica | −4 RD (un attacco) |
| Kuni Shugenja | School Trait | crab_kuni_shugenja_school | Willpower | +1 |
| Yasuki Courtier | School Trait | crab_yasuki_courtier_school | Perception | +1 |
| Yasuki Courtier | Wiles Of The Carp | crab_wiles_of_the_carp | TN nemico (ingannarti) | +5 × School Rank al suo TN |
| Yasuki Courtier | What Is Yours Is Mine | crab_what_is_yours_is_mine | Tiri sociali contrapposti | +5k0 (24h) |
| Hiruma Bushi | School Trait | crab_hiruma_bushi_school | Willpower | +1 |
| Hiruma Bushi | Torch's Flame Flickers | crab_torchs_flame_flickers | Attacco | +1k0 (Attack Stance) |
| Hiruma Bushi | Wolf's Little Lesson | crab_wolfs_little_lesson | Armor TN | +5 per colpo (stacca fino a School Rank) |
| Hiruma Bushi | Hummingbird Wings | crab_hummingbird_wings | Armor TN | +2 × School Rank (un attacco) |
| Toritaka Bushi | School Trait | crab_toritaka_bushi_school | Strength | +1 |
| Toritaka Bushi | The Falcon's Eyes | crab_the_falcons_eyes | Tiri Perception / danno | +1k0 Perception; +1k0 danno vs spirit-realm |
| Toritaka Bushi | Claws Of The Falcon | crab_claws_of_the_falcon | Reduction nemica | ignora 5 RD; −10 RD vs spirito (Void) |
| Hiruma Scout | School Trait | crab_ob_hiruma_scout_school | Reflexes | +1 |
| Hiruma Scout | Dance the Razor's Edge | crab_dance_the_razors_edge | Iniziativa | +Stealth Skill Rank |
| Hiruma Scout | Strike of the Stalker | crab_strike_of_the_stalker | Reduction nemica | ignora 10 RD |
| Defender of the Wall | Hida's Strength | crab_hidas_strength | Reduction | +RD 8 |
| Kakita Bushi | School Trait | crane_kakita_bushi_school | Reflexes | +1 |
| Kakita Bushi | The Way Of The Crane | crane_the_way_of_the_crane | Iniziativa / attacco | +2× Iaijutsu a Init; +1k1+School Rank attacco (Center) |
| Kakita Bushi | Speed Of Lightning | crane_speed_of_lightning | Attacco | +2k0 vs Iniziativa inferiore |
| Asahina Shugenja | School Trait | crane_asahina_shugenja_school | Awareness | +1 |
| Asahina Shugenja | The Soul's Grace | crane_the_souls_grace | Danno nemico | −0k1 ai nemici entro 20' (Void) |
| Doji Courtier | School Trait | crane_doji_courtier_school | Awareness | +1 |
| Doji Courtier | The Gift Of The Lady | crane_the_gift_of_the_lady | Tiro sociale contrapposto | +5k0 vs Alleato |
| Daidoji Iron Warriors | School Trait | crane_daidoji_iron_warriors | Agility | +1 |
| Daidoji Iron Warriors | The Force Of Honor | crane_the_force_of_honor | Ferite / attacco | +(Honor−4, min 1) Ferite per Rank; +1k0 attacco (Attack Stance) |
| Daidoji Iron Warriors | The Shield Of Faith | crane_the_shield_of_faith | Armor TN (Guard) | bonus Guard +5 (bersaglio +15 invece di +10) |
| Daidoji Iron Warriors | Vigilance Of Mind | crane_vigilance_of_mind | Attacco / danno | +2k1 vs avversario scelto (Void) |
| Kenshinzen | Drawing The Void | crane_drawing_the_void | Armor TN | +10 (Center Stance) |
| Tonbo Shugenja | School Trait | dragonfly_tonbo_shugenja_school | Perception | +1 |
| Mirumoto Bushi | School Trait | dragon_mirumoto_bushi_school | Stamina | +1 |
| Mirumoto Bushi | Way Of The Dragon | dragon_way_of_the_dragon | Armor TN | +School Rank (katana+wakizashi) |
| Mirumoto Bushi | Furious Retaliation | dragon_furious_retaliation | Attacco | +3k0 vs avversario scelto |
| Tamori Shugenja | School Trait | dragon_tamori_shugenja_school | Stamina | +1 |
| Kitsuki Investigator | School Trait | dragon_kitsuki_investigator_school | Perception | +1 |
| Kitsuki Investigator | Kitsuki's Method | dragon_kitsukis_method | Armor TN | +Perception Trait Rank |
| Kitsuki Investigator | Wisdom The Wind Brings | dragon_wisdom_the_wind_brings | TN nemico (inganno/Feint/Disarm) | +5 per School Rank |
| Togashi Tattooed | School Trait | dragon_togashi_tattooed_order | Void | +1 |
| Togashi Tattooed | Body Of Stone | dragon_body_of_stone | Attacco / danno disarmato | +1k1 |
| Hoshi Tsurui Zumi | School Trait | dragon_ob_hoshi_tsurui_zumi | Void | +1 |
| Hitomi Kikage Zumi | School Trait | dragon_ob_hitomi_kikage_zumi | Reflexes | +1 |
| Swordsmasters | Harmony And Precision | dragon_harmony_and_precision | Reduction nemica | ignora la RD dell'avversario |
| Tamori Master of Mts | Inner Fortitude | dragon_inner_fortitude | Reduction / Armor TN | +RD 2 e +10 Armor TN (spell slot) |
| Toritaka Bushi (Falcon) | School Trait | falcon_toritaka_bushi_school | Strength | +1 |
| Toritaka (Falcon) | The Falcon's Eyes | falcon_the_falcons_eyes | Tiri Perception / danno | +1k0 Perception; +1k0 danno vs spirit-realm |
| Toritaka (Falcon) | Claws Of The Falcon | falcon_claws_of_the_falcon | Reduction nemica | ignora 5 RD; −10 RD vs spirito (Void) |
| Kitsune Shugenja (Fox) | School Trait | fox_kitsune_shugenja_school | Stamina | +1 |
| Usagi Bushi | School Trait | hare_usagi_bushi_school | Reflexes | +1 |
| Usagi Bushi | Speed Of The Hare | hare_speed_of_the_hare | Armor TN / Movimento | +Athletics a TN; Water Ring +1 per movimento |
| Usagi Bushi (ACW) | School Trait | hare_usagi_bushi_school_after_clan_war | Reflexes | +1 |
| Seppun Guardsman | School Trait | imperial_seppun_guardsman_school | Perception | +1 |
| Seppun Guardsman | Never In Darkness | imperial_never_in_darkness | Tiro Investigation | +1k1 (rileva imboscata/sorpresa) |
| Seppun Guardsman | The Clouds Part | imperial_the_clouds_part | Attacco / danno | +Honor Rank (Void) |
| Seppun Shugenja | School Trait | imperial_seppun_shugenja_school | Intelligence | +1 |
| Otomo Courtier | School Trait | imperial_otomo_courtier_school | Awareness | +1 |
| Otomo Courtier | The Emperor's Protection | imperial_the_emperors_protection | Onore nemico | bersaglio perde 5 Onore |
| Otomo Courtier | The Virtues Of Command | imperial_the_virtues_of_command | Tiro sociale contrapposto | +5k0 |
| Miya Herald | School Trait | imperial_miya_herald_school | Awareness | +1 |
| Miya Herald | Voice Of The Emperor | imperial_voice_of_the_emperor | Onore nemico | l'attaccante perde 2× School Rank Onore |
| Miya Herald | Eyes Of The Emperor | imperial_eyes_of_the_emperor | Tiri Etiquette (resistere) | +Honor Rank |
| Miya Herald | Glory Of The Emperor | imperial_glory_of_the_emperor | Tiro Courtier/Etiquette | +5k0 |
| Akodo Bushi | School Trait | lion_akodo_bushi_school | Perception | +1 |
| Akodo Bushi | The Way Of The Lion | lion_the_way_of_the_lion | Armor TN nemica / attacco | ignora porzione armatura del TN; +1k0 attacco |
| Akodo Bushi | Strength Of Purity | lion_strength_of_purity | Un tiro (skirmish) | +Honor Rank |
| Kitsu Shugenja | School Trait | lion_kitsu_shugenja_school | Perception | +1 |
| Ikoma Bard | School Trait | lion_ikoma_bard_school | Intelligence | +1 |
| Ikoma Bard | The Heart Of The Lion | lion_the_heart_of_the_lion | TN nemico (Intimidazione/Tentazione) | +5 per School Rank |
| Ikoma Bard | The Voice Of The Ancestors | lion_the_voice_of_the_ancestors | Un tiro abilità (alleati) | +Honor Rank |
| Matsu Berserker | School Trait | lion_matsu_berserker_school | Strength | +1 |
| Matsu Berserker | The Lion's Roar | lion_the_lions_roar | Danno / Movimento | +Honor Rank danno; +5 ft movimento (Full Attack) |
| Matsu Berserker | Matsu's Courage | lion_matsus_courage | Penalità da ferita | ignora penalità TN = Honor Rank (×2 in Full Attack) |
| Lion's Pride | The Fury Of Matsu | lion_the_fury_of_matsu | Armor TN | +10 (Full Attack Stance) |
| Yoritomo Bushi | School Trait | mantis_yoritomo_bushi_school | Strength | +1 |
| Yoritomo Bushi | The Way Of The Mantis | mantis_the_way_of_the_mantis | Attacco | +1k0 a tutti gli attacchi |
| Yoritomo Bushi | Voice Of The Storm | mantis_voice_of_the_storm | Armor TN nemica | −5 per colpo (stacca fino a School Rank) |
| Yoritomo Bushi | The Rolling Wave | mantis_the_rolling_wave | Armor TN | +10 se ti sei mosso di 5 ft |
| Yoritomo Bushi | Hand Of Osano-Wo | mantis_hand_of_osanowo | Danno | +Strength dadi tenuti; +0k2 vs Prone (Void) |
| Moshi Shugenja | School Trait | mantis_moshi_shugenja_school | Awareness | +1 |
| Yoritomo Courtier | School Trait | mantis_yoritomo_courtier_school | Willpower | +1 |
| Yoritomo Courtier | Storm Heart | mantis_storm_heart | Willpower (Intimidazione) | +1 Rank (+2 vs Status inferiore) |
| Yoritomo Courtier | Will Of The Storm | mantis_will_of_the_storm | Tiri sociali nemici | −3k0 ai tiri del bersaglio vs te |
| Yoritomo Courtier | Strength In All Things | mantis_strength_in_all_things | Tiro Intimidazione/resistenza | +5k0 |
| Tsuruchi Archer | School Trait | mantis_tsuruchi_archer_school | Reflexes | +1 |
| Tsuruchi Archer | Always Be Ready | mantis_always_be_ready | Attacco (arco) / Iniziativa | +1k0 attacco; +3 Iniziativa |
| Tsuruchi Archer | The Arrow Knows The Way | mantis_the_arrow_knows_the_way | Danno (arco) | +2k0 |
| Tsuruchi Archer | Tsuruchi's Eye | mantis_tsuruchis_eye | Attacco / danno | +4k1 |
| Kitsune Shugenja (Mantis) | School Trait | mantis_kitsune_shugenja_school | Stamina | +1 |
| Storm Riders | The Raging Ocean | mantis_the_raging_ocean | School Rank | +1 Shugenja School Rank |
| Toku Bushi | School Trait | monkey_toku_bushi_school | Willpower | +1 |
| Toku Bushi | Toku's Lesson | monkey_tokus_lesson | Tiri abilità / penalità da ferita | +1k0 vs TN 25+; −penalità ferite = Willpower + 2× School Rank |
| Toku Bushi | The Strength Of One Man | monkey_the_strength_of_one_man | Attacco / danno | +1k1 (più nemici / Insight superiore) |
| Four Temples Monk | School Trait | monks_four_temples_monk_school | Awareness | +1 |
| Order of Heroes Monk | School Trait | monks_order_of_heroes_monk_school | Perception | +1 |
| Shrine of Seven Thunders Monk | School Trait | shine_of_the_seven_thunders_monk_school | Stamina | +1 |
| Temple of Kaimetsu-Uo | School Trait | temple_of_the_kaimetsu_uo_monk_school | Willpower | +1 |
| Temple of Osano-Wo Monk | School Trait | monks_the_temple_of_osanowo_monk_school | Strength | +1 |
| Temple of Osano-Wo Monk | The Hand of Thunder | monks_the_hand_of_thunder | Danno disarmato | +0k1 |
| Thousand Fortunes Monk | School Trait | monks_the_temples_of_the_thousand_fortunes_monk_school | Agility | +1 |
| Tsi Smith | School Trait | oriole_tsi_smith_school | Intelligence | +1 |
| Morito Bushi (Ox) | School Trait | ox_morito_bushi_school | Agility | +1 |
| Morito Bushi (Ox) | Legacy Of The Four Winds | ox_legacy_of_the_four_winds | Iniziativa / attacco | +1k0 Init (montato); +1k0 attacco (montato) |
| Morito Bushi (Ox) | The Wind Blows Many Ways | ox_the_wind_blows_many_ways | Tiri abilità | +1k0 a Bugei skill scelte |
| Morito Bushi (Ox) | Fast And Furious | ox_fast_and_furious | Attacco / danno | +2k2 vs Iniziativa inferiore |
| Shiba Bushi | School Trait | phoenix_shiba_bushi_school | Agility | +1 |
| Isawa Shugenja | School Trait | phoenix_isawa_shugenja_school | Intelligence | +1 |
| Asako Loremaster | School Trait | phoenix_asako_loremaster_school | Intelligence | +1 |
| Asako Loremaster | From The Ashes | phoenix_from_the_ashes | Tiri sociali | +2k0 (2 giorni, corte) |
| Asako Loremaster | Voice Of The Universe | phoenix_voice_of_the_universe | Tiri sociali (alleato) | +Lore:History Rank (24h) |
| Asako Loremaster | Wisdom Of The Ages | phoenix_wisdom_of_the_ages | Tiro Lore | +5k0 |
| Agasha Shugenja | School Trait | phoenix_agasha_shugenja_school | Intelligence | +1 |
| Disciples of Sun Tao | School Trait | ronin_disciples_of_sun_tao | Reflexes | +1 |
| Disciples of Sun Tao | Gaze of Sun Tao | ronin_gaze_of_sun_tao | Tiri Iaijutsu | +Honor Rank |
| Forest Killers | School Trait | ronin_forest_killers | Agility | +1 |
| Forest Killers | Strength Of The Forest | ronin_strength_of_the_forest | Ferite / danno | +Stamina Ferite per Rank; +Stamina danno mischia |
| Tawagoto's Army | School Trait | ronin_tawagotos_army | Agility | +1 |
| Tengoku's Justice | School Trait | ronin_tengokus_justice | Strength | +1 |
| Tengoku's Justice | Heaven's Curse | ronin_heavens_curse | Danno (Strength) | raddoppia i dadi Strength a sorpresa |
| The Tessen | School Trait | ronin_the_tessen | Stamina | +1 |
| The Tessen | Folds Of The Iron Fan | ronin_folds_of_the_iron_fan | Armor TN | +War Fan Rank (impugnando il war fan) |
| Bayushi Bushi | School Trait | scorpion_bayushi_bushi_school | Intelligence | +1 |
| Bayushi Bushi | The Way Of The Scorpion | scorpion_the_way_of_the_scorpion | Iniziativa / Armor TN | +1k1 Init; +5 TN vs Iniziativa inferiore |
| Soshi Shugenja | School Trait | scorpion_soshi_shugenja_school | Awareness | +1 |
| Bayushi Courtier | School Trait | scorpion_bayushi_courtier_school | Awareness | +1 |
| Shosuro Infiltrator | School Trait | scorpion_shosuro_infiltrator_school | Reflexes | +1 |
| Shosuro Infiltrator | The Path Of Shadows | scorpion_the_path_of_shadows | Tiri Stealth | +2k0 |
| Chuda Shugenja (Snake) | School Trait | snake_chuda_shugenja_school | Willpower | +1 |
| Chuda Shugenja (Snake) | To Punish The Wicked | snake_to_punish_the_wicked | Reduction nemica / danno incant. | −RD = School Rank (Void); +School Rank danno incant. vs Tainted |
| Suzume Bushi | School Trait | sparrow_suzume_bushi_school | Willpower | +1 |
| Suzume Bushi | All Things In Time | sparrow_all_things_in_time | Iniziativa / attacco / danno | −5 Init; +1k0 attacco e danno |
| Suzume Bushi | Purity Of Chi | sparrow_purity_of_chi | Armor TN | +5 vs creature / Onore inferiore |
| Suzume Bushi | Wisdom Is Greatest Weapon | sparrow_wisdom_is_the_greatest_weapon | Tiro Perform/Lore | +Honor Rank (Void) |
| Suzume Bushi | Slow And Deadly | sparrow_slow_and_deadly | Attacco / danno | +10 (round dopo Center Stance) |
| Daigotsu Bushi | School Trait | spider_daigotsu_bushi_school | Strength | +1 |
| Daigotsu Bushi | The Way Of The Spider | spider_the_way_of_the_spider | Penalità ferita / danno | riduce penalità ferite OPPURE +danno = Strength+Taint |
| Daigotsu Bushi | Aura Of Blood | spider_aura_of_blood | Danno (self + alleati) | +2k0 (Void) |
| Daigotsu Bushi | Devouring Wrath | spider_devouring_wrath | Ferite | recupera 5 Ferite per colpo mischia (max +20) |
| Daigotsu Bushi | Inhuman Assault | spider_inhuman_assault | Armor TN nemica / Reduction | ignora armatura e bonus Stance al TN; ignora RD armatura |
| Chuda Shugenja (Spider) | School Trait | spider_chuda_shugenja_school | Willpower | +1 |
| Daigotsu Courtier | School Trait | spider_daigotsu_courtier_school | Perception | +1 |
| Daigotsu Courtier | Insidious Whispers | spider_insidious_whispers | Onore (percepito) | +School Rank all'Onore apparente |
| Daigotsu Courtier | Cracks In The Wall | spider_cracks_in_the_wall | Tiri Etiquette/Perform nemici | −1k1 a quelli entro 20' (Void) |
| Order of the Spider Monk | School Trait | spider_order_of_the_spider_monk | Agility | +1 |
| Order of the Spider Monk | The Dark Path | spider_the_dark_path | Attacco / Armor TN | +1k0 attacco (disarmato/asta); +2× School Rank TN vs mischia |
| Order of the Spider Monk | Drawing In The Strike | spider_drawing_in_the_strike | Reduction | +RD = Anello scelto + Taint |
| Order of the Spider Monk | Guarded By Chi | spider_guarded_by_chi | TN incantesimo nemico | +2× Anello scelto + Taint al TN incant. vs te |
| Order of the Spider Monk | Darkness Unleashed | spider_darkness_unleashed | Punti Vuoto / danno | +Void Points = Taint o Earth; può aggiungere +1k1 danno |
| Kasuga Smuggler | School Trait | tortoise_kasuga_smuggler_school | Awareness | +1 |
| Kasuga Smuggler | Way Of The Tortoise | tortoise_way_of_the_tortoise | Tiri sociali | +2k0 vs heimin/hinin |
| Kasuga Smuggler | The Shell Of The Tortoise | tortoise_the_shell_of_the_tortoise | Onore nemico | attaccante/calunniatore perde 2× School Rank Onore |
| Moto Bushi | School Trait | unicorn_moto_bushi_school | Strength | +1 |
| Moto Bushi | The Way Of The Unicorn | unicorn_the_way_of_the_unicorn | Danno | +1k0 (montato/scimitarra/due mani) |
| Moto Bushi | Shinsei's Smile | unicorn_shinseis_smile | Attacco | +½ penalità ferita nemica all'attacco |
| Moto Bushi | Moto Cannot Yield | unicorn_moto_cannot_yield | Danno | +½ Strength dadi tenuti (montato/Full Attack) |
| Iuchi Shugenja | School Trait | unicorn_iuchi_shugenja_school | Perception | +1 |
| Ide Emissary | School Trait | unicorn_ide_emissary_school | Awareness | +1 |
| Utaku Battle Maiden | School Trait | unicorn_utaku_battle_maiden | Reflexes | +1 |
| Utaku Battle Maiden | Riding In Harmony | unicorn_riding_in_harmony | Attacco / danno / Horsemanship | +Honor a un attacco (o danno montato); +Honor a Horsemanship |
| Utaku Battle Maiden | The Void Of War | unicorn_the_void_of_war | Iniziativa / Armor TN | +5 a Iniziativa o Armor TN |
| Utaku Battle Maiden | Wind Never Stops | unicorn_wind_never_stops | Danno | +2k1 (carica, Void) |
| Utaku Battle Maiden | Otaku's Blessing | unicorn_otakus_blessing | Danno / tiri Bugei | +Honor Rank (Void) |

---

## 8. Tecniche di Scuola (espansioni)

| Fonte / Scuola | Nome | slug | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|
| BoA Fukurokujin's Eyes | Way of the Closed Eye | way_of_the_closed_eye | Iniziativa | +20 Iniziativa (dopo VP + Perception TN20) |
| BoA Wind's Grace Order | Pillars of the Mind's Eye | pillars_of_the_minds_eye | Attacco archery | +1k0 per Kiho attivo |
| BoA Crab Defender | Warrior of Earth | crab_warrior_of_earth | Reduction (durante iaijutsu Strike) | +Earth ×3 RD |
| BoA Asahina Archer | No Regrets | crane_no_regrets | Attacco archery | +½ Air (arr. giù) dadi non tenuti |
| BoA Kaze-Do Fighter | The Way of Air | monks_the_way_of_air | Tiro abilità attacco nemico (malus) | −(Air Ring nemico)k0 all'attaccante |
| BoA Unicorn Yomanri Archer | The Way of Yomanri | the_way_of_yomanri | Attacco/danno (mira) | +1k1 attacco o +1k0 danno per Simple Action (max Agility) |
| BoA Taoist Archer | Flight of Innocence | flight_of_innocence | Danno arco | +1k1 danno (spesa VP) |
| BoE Order of the Nameless Gift | Shinsei's Gift | shinseis_gift | Punti Vuoto / Armor TN / Reduction | +Earth Ring VP/giorno (solo per ridurre danno o alzare Armor TN) |
| BoE Temple of Persistence | Unyielding Spirit | unyielding_spirit | Tiro bonus (Contrapposto/Attacco) | +Earth Ring k0 (spesa VP) |
| BoE Defender of the Brotherhood | Harmony in Chaos | harmony_in_chaos | Tiro Etiquette/Courtier | +Willpower k1 (spesa VP) |
| BoE Hiruma Slayers | Deny the Horde | crab_deny_the_horde | Danno (masakari) | +3k0 danno (Full Attack / vs Tainted) |
| BoE Crab Sumai Wrestler | Way of Sumai | way_of_sumai | Tiro lotta / danno; Taglia | +1k0 (+2k0 se Large) controllo; +1k1 danno; rimuove Small/concede Large |
| BoE Daidoji Heavy Regulars | Way of the Iron Crane | crane_way_of_the_iron_crane | Attacco / Armor TN | +1k1 attacco vs Attack-stance; +Heavy Weapons Rank Armor TN (Defense) |
| BoE Yoritomo Sculptors | Watanabe's Legacy | watanabes_legacy | Tiri Sculpture | +1k1 |
| BoE Yoritomo Emissaries | Intrepid Negotiator | intrepid_negotiator | Tiro Etiquette/Sincerity | +Willpower dadi non tenuti (spesa VP) |
| BoE Shiba Armorsmiths | Brilliant Steel | brilliant_steel | Armor TN; Craft (armatura) | +2× Earth Ring Armor TN extra (su VP +10); +1k0 Craft |
| BoE Unicorn Bariqu Wrestler | Way of the Ujik-Hai | way_of_the_ujikhai | Tiro controllo lotta | +1k1 (vs non-Bariqu); +2k0 (se Agility superiore) |
| BoF Tengoku's Fist | The Hand of the Heavens | monks_the_hand_of_the_heavens | Tiro attacco | Free Raise se Fire > Fire nemico |
| BoF Student of Hitsu-Do | The Way of Fire | dragon_the_way_of_fire / monks_the_way_of_fire / phoenix_the_way_of_fire | DR danno disarmato; Fire Ring (per Kiho) | base DR 0k[Fire] vs 0k1 (subisci Fire ×2 Ferite); Fire +1 Rank per apprendere Fire Kiho |
| BoF Crab Knife-Fighters | One Blade, Both Hands | crab_one_blade_both_hands | Tiro danno tanto | +3k1 danno; ignora armatura/5 RD |
| BoF The Transcendent Brotherhood | Apotheosis of Fire | dragon_apotheosis_of_fire | Tiri Awareness/Perception/Intelligence | +Fire Ring ai totali (mentre/dopo bruciare) |
| BoF Ujina Skirmishers | Master of the Quick Blade | hare_master_of_the_quick_blade | Iniziativa / danno coltello | +1k0 Iniziativa; +1k1 danno (coltelli) |
| BoF Mantis Whirlwind Fighters | Waves Rush to Shore | mantis_waves_rush_to_shore | Armor TN / danno kama | +Knives Rank Armor TN; +3k0 danno |
| BoF Saigo's Blades | Saigo's Technique | saigos_technique | Tiro Duel Assessment | +5 al totale (post-Intimidazione) |
| GC Kaiu Engineer | The Kaiu Method | crab_the_kaiu_method | Tiri School Skill (e spesa Void) | +1k0 (+2k2 su Void) |
| GC Kaiu Engineer | The Path Of The Shell | crab_the_path_of_the_shell | Reduction + Armor TN armatura forgiata | +School Rank RD, +½ School Rank Armor TN |
| GC Kaiu Engineer | The Path Of Steel | crab_the_path_of_steel | Attacco o danno arma forgiata | +1k0 attacco / +0k1 danno |
| GC Kuni Witch Hunter | To See The Darkness | crab_to_see_the_darkness | Resistenza Taint; attacco vs Tainted/Shadowlands | +1k1 |
| GC Kuni Witch Hunter | To Repel The Darkness | crab_to_repel_the_darkness | Tiri rilevamento Taint | +3k0 |
| GC Kuni Witch Hunter | To Shatter The Darkness | crab_to_shatter_the_darkness | Attacco/danno vs Shadowlands/Tainted | +4k1 |
| GC Daidoji Scout | Surveying The Land | crane_surveying_the_land | Tiri Stealth/Hunting; danno trappola | +1k0; +1k1 danno trappola |
| GC Daidoji Scout | Scouring The Shadows | crane_scouring_the_shadows | Tiro attacco (nemico ignaro) | +2k0 |
| GC Daidoji Scout | Weaken The Resistance | crane_weaken_the_resistance | Ignora Reduction armatura; danno se no RD | ignora RD; +1k0 danno |
| GC Daidoji Scout | Strike And Move | crane_strike_and_move | Danno trappola | +2k1 |
| GC Daidoji Scout | Cunning Of Daidoji | crane_cunning_of_daidoji | Tiro danno (colpo di precisione) | +1k1 |
| GC Kakita Artisan | Soul Of The Artisan | crane_soul_of_the_artisan | Tiri arte scelta | +2k0 |
| GC Kakita Artisan | Free The Spirit | crane_free_the_spirit | Tiri arte scelta | +2k1 |
| GC Matsu Beastmaster | Heart Of The Beast | lion_heart_of_the_beast | Leoni: tratto Swift + Wound Rank | Swift 2; +1 Wound Rank |
| GC Matsu Beastmaster | All As One | lion_all_as_one | Tiri danno (branco insieme) | +2k1 |
| GC Matsu Beastmaster | With The Soul Of A Lion | lion_with_the_soul_of_a_lion | Warcat: Armor TN, Reduction, Paura | +10 Armor TN, +2 RD, +2 Paura |
| GC Mantis Brawler | Way Of The Drunken Fist | mantis_way_of_the_drunken_fist | Controllo lotta & danno (disarmato/small/improvv.); penalità Prone | +1k0; nessuna penalità Armor TN da Prone |
| GC Mantis Brawler | Drunk Loses His Sandal | mantis_drunk_loses_his_sandal | Armor TN (scambia danno Feint) | +5 (+10 se Prone) |
| GC Mantis Brawler | Drunk Pounds A Door | mantis_drunk_pounds_a_door | Attacco & danno (spesa Void) | +4k1 (+4k2 se Prone) |
| GC Tsuruchi Bounty Hunter | A Hunter's Sense | mantis_a_hunters_sense | Tiri Intimidazione/sociali | +1k1 (+1k0 vs samurai) |
| GC Yoritomo Shugenja | Child Of The Sea | mantis_child_of_the_sea | Tiri incantesimi Thunder | Free Raise |
| GC Asako Henshin | The Four Mysteries | phoenix_the_four_mysteries | Due Tratti di un Anello (self/altri) | +/− School Rank (½ per altri) |
| GC Asako Henshin | The Riddle Of Fire | phoenix_the_riddle_of_fire | Dadi tenuti danno disarmato; riduce dadi danno nemico | tenuti = Fire Ring; −Fire Ring dadi danno nemico |
| GC Shosuro Actors | The First Face | scorpion_the_first_face | Tiri Acting/Sincerity (Deceit) (spesa Void) | +3k1 invece di +1k1 |
| GC Shosuro Actors | The Subtle Sting | scorpion_the_subtle_sting | Tiri attacco (arma Small) | +2k0 |
| GC Goju Ninja | The Cloak Of Night | spider_the_cloak_of_night | Armor TN (+ TN propri tiri non-Ath/Def/Stealth) | +fino a School Rank×5 (penalità ai propri tiri stessa entità) |
| GC Goju Ninja | Melting Into Shadow | spider_melting_into_shadow | Tiri Stealth (dadi); attacco vs ignaro | +School Rank dadi; +1 Free Raise |
| GC Goju Ninja | Shadow Upon The Moon | spider_shadow_upon_the_moon | Iniziativa (primo round dopo ri-corporeizzare) | +5 |
| GC Ninube Shugenja | Mask of the Nothing | spider_mask_of_the_nothing | Tiri Stealth (forma ombra); incant. Nothing | +5k0; Free Raise |
| GC Moto Vindicator | Purity of the Breath | unicorn_purity_of_the_breath | Riduzione penalità ferita OPPURE Armor TN | ±(School Rank + Willpower), ×2 vs Shadowlands |
| GC Moto Vindicator | Facing the Dark Within | unicorn_facing_the_dark_within | Tiri Investigation | +2k0 (+2k1 Taint) |
| GC Moto Vindicator | Avenging our Own | unicorn_avenging_our_own | Attacco & danno (vs attaccante/Tainted) | +2k0 |
| GC Moto Vindicator | Bloodied but Unbowed | unicorn_bloodied_but_unbowed | Danno mischia (= penalità da ferita) | +totale penalità ferita |
| GC Kitsuki Debater | The Ebb and Flow of Deception | dragon_the_ebb_and_flow_of_deception | Prossimo tiro sociale avversario | −1k1 |
| GC The Dragon's Flame | Rain of Death | dragon_rain_of_death | Tiri attacco (+arco) | +1k0 (+2k2 arco) |
| GC Togashi Defender | Power Within and Without | dragon_power_within_and_without | Reduction (senza armatura, no Kiho/Tattoo) | RD = 3 + Void Ring |
| GC Akodo Kensai | The Heart of the Sword | lion_the_heart_of_the_sword | Armor TN (spada, Attack Stance, vs 1° attacco) | +Honor Rank |
| GC Lion Scout | Shadow Unseen | lion_shadow_unseen | Tiri Stealth e Bugei basate su Agility | +1k0 |
| GC Lion Paragon | Pure and Dedicated | lion_pure_and_dedicated | Honor Rank (raddoppiato per le tecniche) | ×2 Honor Rank |
| GC Kitsune Ranger | One With the Wild | mantis_one_with_the_wild | Tiri di rilevamento contrapposti | +2k0 |
| GC Moshi Guardian of the Sun | Defender as the Sun | mantis_defender_as_the_sun | Tiro attacco OPPURE Armor TN protetto | +1k0 / +1k1 |
| GC Moto Fanatic | Reckless Abandon | unicorn_recless_abandon | Reduction (Full Attack Stance) | +School Rank RD |
| GC Utaku Horse Master | Master of the Open Plains | unicorn_master_of_the_open_plains | Tiri Animal Handling/Horsemanship/Hunting | +2k0 |
| GC Kakita Master Artisan | Mastery Unbounded | crane_mastery_unbounded | Tiri arte scelta | +2k0 |
| GC Mirumoto Master Sensei | The Sword And The Soul | dragon_the_sword_and_the_soul | Punti Vuoto (recupera all'uccisione) | +1 Punto Vuoto |
| GC Mirumoto Master Sensei | The Body Is Illusion | dragon_the_body_is_illusion | Penalità da ferita (spesa Void) | ignora penalità da ferita |
| GC Akodo Tactical Masters | The Soul Of The Army | lion_the_soul_of_the_army | Tiri Battle / Bugei (spesa Void) | +5k1 Battle / +2k2 Bugei |
| BoV Order of Eternity | The Touch of Eternity | the_touch_of_eternity | Tiri abilità (situazionale) | +1k1 +Void |
| BoV Abbot | The Reverence of Wisdom | the_reverence_of_wisdom | Status; tiri sociali | Status 4.0; +1k1 (proprio Ordine) / +1k0 (altri) |
| BoV Koga Ninja | The People's Vengeance | the_peoples_vengeance | Tiri abilità vs samurai | +1k1 |
| BoV Sesai Ninja | Anything for the Phoenix | anything_for_the_phoenix | Tiri Stealth | +1k1 |
| BoV Hateru Ninja | The False Dragon | the_false_dragon | Tiri Acting (come samurai Dragon) | +2k1 |
| BoV Ghosts of the Forest | Walk Among the Trees | walk_among_the_trees | Tiri Tratto Perception (vicino Nazo Mori) | +1k0 |
| BoW Order of Jurojin's Blessing | Blessings of Longevity | monks_blessings_of_longevity | Tiri Medicine (malattia / ferite) | +1k1 / +1k0 |
| BoW Shrine of Heaven's Mirror | Gaze Into the Mirror | monks_gaze_into_the_mirror | Tiri Divination | +1k0 (+1k1 presagi) |
| BoW Servants of Mercy | Mercy's Touch | monks_mercys_touch | Ferite curate (Medicine) | +2k1 Ferite |
| BoW Daidoji Spy Master | Truth in Shadows | crane_truth_in_shadows | Tiri Stealth/Investigation/Temptation | +2k0 |
| BoW Kitsuki's Eye | The Eye Sees All | dragon_the_eye_sees_all | Tiri per evitare la sorpresa | +2k2 |
| BoW Student of Cliff's Edge | Howl of the Cliff's Edge | howl_of_the_cliffs_edge_3 / _4 | Tiro attacco (kusarigama Knockdown/Disarm) | +2k1 |
| BoW The Scorpion's Tail | The Tail's Reach | scorpion_the_tails_reach_3 / _4 | Tiri Athletics (arma a catena, arrampicata) | +1k1 |
| BoW The Scales of the Carp | Swimming Beneath the Waves | ronin_swimming_beneath_the_waves | Tiri Temptation (Bribery) | +1k0 (+1k1 vs Crab/Crane) |
| EE The Diamond Sutra | The Diamond Sutra | monks_shinmaki_diamond_sutra | Tiri Meditation/Fear/sociali | +1k0 |
| SF Ikoma Tactician | The Commander's Fan | the_commanders_fan | Armor TN; tiri Battle (Mass Battle) | Armor TN +½/+full Warfans Rank; +1k1 Battle |
| SF Tsuru's Legion | Overrun | tsurus_legion_overrun | Tiro attacco (spesa Void, montato) | +Xk0 (X = Strength cavalcatura) |
| SH Yasuki Enforcer | Gentle Encouragement | yasuki_enforcer_gentle_encouragement | Tiri attacco vs bersaglio (1° round) | +1k0 (+1k0 per Raise) |
| SH Hiruma Yojimbo | The Crab's Shell | hiruma_yojimbo_crabs_shell | Armor TN del protetto | +(eccedenza attacco oltre il TN) |
| SH Doji Warrior-Poet | Fan & Sword | crane_fan_and_sword | Iaijutsu/Perform:Poetry (Void); Gloria | +2k1 invece di +1k1; +1 Gloria alla vittoria |
| SH Mirumoto Sentinel | Master the Land (R3/R4) | dragon_master_the_land_rank3 / _rank4 | 3 abilità Bugei scelte; Water Ring nemico | +1k0 abilità; Water Ring nemico −1 (movimento) |
| SH Water Hammer Smith | Child of the Water | dragon_child_of_the_water | Tiri Craft (Void) | +2× Water Ring |
| SH Kitsune Artisan | The Beauty of the World | kitsune_artisan_beauty_of_the_world | Tiri Artisan/Craft (spell slot) | +1k0 |
| SH Ikoma Warden | To Race the Wind | lion_to_race_the_wind | Tiri Bugei (montato); Horsemanship/Investigation (Void) | +1k0; +2k2 invece di +1k1 |
| SH Lioness Legion | Charge of the Pride | lion_charge_of_the_pride | Movimento | +5 ft (Full Attack); Move = Water Ring ×25 ft |
| SH Asako Philosopher | The Winds of Rhetoric | the_winds_of_rhetoric | Tiri sociali Etiquette contrapposti | +1k1 |
| SH Provincial Guard | Maintaining the Peace | phoenix_maintaining_the_peace | Armor TN (Defense/Full Defense + Void) | +Etiquette Skill |
| SH Shadow Blades | Never Beyond My Reach | scorpion_never_beyond_my_reach | Tiri attacco & danno (arma Ninja) | +1k1 |
| SH Daigotsu Scout | The Cloak of Shadows | spider_the_cloak_of_shadows | Movimento (Stealth) | Move non ridotto; ignora penalità terreno |
| SH Calm Heart Duelist | The Calm Heart Conquers | unicorn_calm_heart_conquers | Tiro Iaijutsu (non letale) | +1k0 |
| SH Ide Caravan Master | The Gilded Road | unicorn_ide_the_gilded_road | Tiri Commerce/sociali (cliente) | +1k1 |
| SH Minor Clan Alliance Diplomat | The Courts of Kudo Mura | the_courts_of_kudo_mura | Tiri Etiquette/Sincerity contrapposti | +3k0 |

---

## 9. Ancestri (Ancestors)

| Fonte | Nome | slug | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|
| Core | Hida | ancestor_crab_hida | Tiri danno / Reduction nemica | +1k0 danno; ignora 4 RD nemica |
| Core | Doji | ancestor_crane_doji | Tiri Courtier/Etiquette/Perform/Sincerity | +1k0 |
| Core | Akodo | ancestor_lion_akodo | Tiri abilità Bugei (eccetto Iaijutsu) | +1k0 (e +1k1 Mass Battle) |
| Core | Ikoma | ancestor_lion_ikoma | Tiri Intelligence / danno disarmato | +1k0 Intelligence; +2k0 danno disarmato |
| Core | Kaimetsu-Uo | ancestor_mantis_kaimetsu_uo | Tiri Willpower / danno arma improvv. | +1k1 Willpower; +1k1 danno (improvvisata) |
| Core | Asako | ancestor_phoenix_asako | Tiri abilità sociali (vs Alleato) | +1k0 |
| Core | Shiba | ancestor_phoenix_shiba | Tiri Intelligence / Armor TN | +1k1 Intelligence; +Intelligence Rank ad Armor TN |
| Core | Mirumoto | ancestor_dragon_mirumoto | Tiri abilità basate su Agility | +1k1 (+3k1 per abilità della Scuola Mirumoto) |
| Core | Kitsuki | ancestor_dragon_agasha_kitsuki | Sostituzione Tratto | usa Perception invece di Awareness per i tiri |
| GC | Hiruma | ancestor_crab_hiruma | Tiri Stealth/Kenjutsu/Kyujutsu | +1k0 |
| GC | Kaiu | ancestor_crab_kaiu | Tiri Craft/Engineering (spesa Void) | +3k1 invece di +1k1 |
| GC | Doji Hayaku | ancestor_crane_doji_hayaku | Tiri Lore: Shadowlands | +1k1 |
| GC | Asahina | ancestor_crane_asahina | Tiri Meditation; lancio incant. (Craft/Defense non da danno) | +1k0 / +1k1 |
| GC | Agasha | ancestor_dragon_agasha_gc | Lancio incant. (non-Void); tiri Spellcraft | +1k0 / +1k1 |
| GC | Togashi Yamatsu | ancestor_dragon_togashi_yamatsu | Magic Resistance (vs maho); Willpower (vs possessione) | 2 Rank MR; +2k2 |
| GC | Kitsu | ancestor_lion_kitsu | Tiri Lore: Spirit Realms | +1k1 |
| GC | Matsu Hitomi | ancestor_lion_matsu_hitomi | Tiri resistenza Tentazione/Intimidazione/Paura | +1k1 |
| GC | Moshi Azami | ancestor_mantis_moshi_azami | Reduction vs fuoco | RD 5 |
| GC | Isawa | ancestor_phoenix_isawa | Tiri Spellcraft (Spell Research) | +1k1 |
| GC | Yogo | ancestor_scorpion_yogo | Lancio incant. (Wards) | +1k1 |
| GC | Soshi Saibankan | ancestor_scorpion_soshi_saibankan | Tiri Perception/Lore: Law (spesa Void) | +3k1 invece di +1k1 |
| GC | Otaku | ancestor_unicorn_otaku | Tiri Horsemanship; attacco vs avversari maschi | +1k1 / +1k0 |
| GC | Iuchi | ancestor_unicorn_iuchi | Elemento Deficiente (rimosso) | nessuna Deficiency |
| GC | Chuda Bikimi | ancestor_spider_chuda_bikimi | Tiri Stealth | +1k0 (+1k1 via spell slot) |
| GC | Yogo Junzo | ancestor_spider_yogo_junzo | Totale lancio incant. (per Forbidden Knowledge / Taint Rank) | +2 (+4 maho) ciascuno |

---

## 10. Percorsi (Paths)

| Fonte | Nome | slug | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|
| Core | Honor Is My Shield (Emerald Magistrate) | honor_is_my_shield | Reduction | +½ Honor Rank (arr. su, cumulativo) |
| Core | Purity in Purpose & Deed (Jade Legionnaire) | purity_in_purpose_and_deed | Tiri attacco e danno | +differenza di Onore vs avversario |
| Core | The Emperor's Hand (Emerald Champion) | the_emperors_hand | Tiri abilità High/Bugei | +1k1 (e +1k0 School Skills) |
| Core | Berserker's Rage (Crab Berserker) | crab_berserkers_rage | Attacco e danno / penalità ferita | +2k1 attacco e danno; ignora penalità ferite |
| Core | To Defend Unto Death (Empress Guard R3) | crane_to_defend_unto_death_rank3 | Attacco & Perception / Armor TN | +½ Honor ad attacco e Perception; +10 Armor TN (difesa Imperiali) |
| Core | To Defend Unto Death (Empress Guard R4) | crane_to_defend_unto_death_rank4 | Attacco & Perception / Armor TN | +½ Honor ad attacco e Perception; +10 Armor TN (difesa Imperiali) |
| Core | Heart of the Mountain (Mirumoto Mountaineer) | dragon_heart_of_the_mountain | Tiri attacco a distanza | +½ Athletics Rank (arr. su) |
| Core | Strength of the Soul (Tamori Warrior Priest) | dragon_strength_of_the_soul | Tiri abilità Bugei | +1k0 (per spell slot, max School Rank) |
| Core | Honor of the Lion (Deathseeker) | lion_heart_of_the_lion | Danno / Armor TN / attacco | +Honor a un danno (poi −5 Armor TN); +1k0 attacco (Full Attack) |
| Core | Scion of Strength (Bishamon's Chosen) | lion_scion_of_strength | Tiri basati su Strength (incl. danno) | +1k0 |
| Core | Revel in Villainy (Yoritomo Scoundrel) | mantis_revel_in_villany | Tiri Athletics/Commerce/Sailing/Sincerity/Low | +2× School Rank (su spesa Void) |
| Core | Strength in Terror (Obsidian Magistrate) | spider_strength_in_terror | Tiri High/Bugei / attacco | +Perception + Taint Rank (High/Bugei, no Weapon); +diff. Onore all'attacco |
| Core | The Swift Soul (Shinjo Scout) | unicorn_swift_soul | Tiri attacco | +1k0 mentre Montato |

---

## 11. Skill Mastery (abilità di maestria)

Abilità di maestria delle abilità (`MasteryAbilities`) che concedono una modifica numerica a una statistica. Sono escluse le maestrie che cambiano solo l'economia delle azioni (ready come Free/Simple Action, attacchi extra), le Free Raise verso manovre e le modifiche all'esplosione dei dadi.
Solo `core_pack/skills.xml` e `lbs_pack/lbsskills.xml` definiscono mastery; i `SkillDef` di Great Clan e Strongholds hanno `<MasteryAbilities/>` vuoto.

| Fonte | Skill | slug/rule | Rank | Caratteristica modificata | Bonus/Malus |
|---|---|---|---|---|---|
| Core | Athletics | athletics | 7 | Movimento | +5 ft a un Move Action per round |
| Core | Battle | battle (rule=ma_battle_5) | 5 | Iniziativa | +Battle Rank all'Initiative Score |
| Core | Defense | defense | 5 | Armor TN | +3 Armor TN in posa Defense/Full Defense |
| Core | Hunting | hunting | 5 | Tiro Stealth | +1k0 a Stealth in ambienti selvaggi |
| Core | Iaijutsu | iaijutsu | 7 | Tiri Focus (duello) | +2k2 ai Focus Roll se l'Assessment supera l'avversario di 10+ |
| Core | Jiujutsu | jiujutsu | 3 | Danno disarmato | +1k0 |
| Core | Jiujutsu | jiujutsu | 7 | Danno disarmato | +0k1 |
| Core | Chain Weapons | chain_weapons | 5 | Tiro contrapposto | +1k0 vs avversari in lotta (grapple) |
| Core | Heavy Weapons | heavy_weapons | 3 | Reduction avversario | −2 RD |
| Core | Kenjutsu | kenjutsu (rule=ma_kenjutsu_3) | 3 | Danno (spada) | +1k0 |
| Core | Kyujutsu | kyujutsu (rule=ma_kyujutsu_5) | 5 | Gittata arco | +50% gittata massima |
| Core | Kyujutsu | kyujutsu (rule=ma_kyujutsu_7) | 7 | Forza arco | +1 Strength di qualsiasi arco |
| Core | Polearms | polearms | 3 | Iniziativa | +5 nel primo round |
| Core | Polearms | polearms | 5 | Danno (polearm) | +1k0 vs avversari montati o più grandi |
| Core | Spears | spears | 3 | Reduction avversario | ignora 3 RD nel primo round |
| Core | Spears | spears | 5 | Gittata | +5 ft agli attacchi a distanza |
| Core | Staves | staves | 7 | Danno (small staves) | +1k0 |
| Core | War Fan | war_fan | 5 | Armor TN | +1 |
| Core | War Fan | war_fan | 7 | Armor TN | +3 |
| Core | Calligraphy | calligraphy | 5 | Tiro (rompere codici) | +10 per decifrare un codice/cifrario |
| Core | Courtier | courtier (rule=ma_insight_plus_3) | 3 | Insight | +3 |
| Core | Courtier | courtier | 5 | Tiri Courtier contrapposti | +1k0 |
| Core | Courtier | courtier (rule=ma_insight_plus_7) | 7 | Insight | +7 (cumulabile col Rank 3) |
| Core | Etiquette | etiquette (rule=ma_insight_plus_3) | 3 | Insight | +3 |
| Core | Etiquette | etiquette | 5 | Tiri Etiquette contrapposti | +1k0 |
| Core | Etiquette | etiquette (rule=ma_insight_plus_7) | 7 | Insight | +7 (cumulabile col Rank 3) |
| Core | Investigation | investigation | 5 | Tiri Investigation contrapposti | +5 |
| Core | Medicine | medicine | 5 | Ferite curate | +1k0 |
| Core | Meditation | meditation | 3 | Punti Vuoto | recupera fino a 2 Void Points |
| Core | Meditation | meditation | 7 | Punti Vuoto | recupera fino a 3 Void Points |
| Core | Sincerity | sincerity | 5 | Tiri Sincerity contrapposti | +5 |
| Core | Spellcraft | spellcraft | 5 | Tiri lancio incantesimi | +1k0 |
| Core | Tea Ceremony | tea_ceremony | 5 | Punti Vuoto | i partecipanti recuperano 2 Void Points invece di 1 |
| Core | Ninjutsu | ninjutsu (rule=ma_ninjutsu_3) | 3 | Danno (armi ninjutsu) | +1k0 |
| Core | Ninjutsu | ninjutsu (rule=ma_ninjutsu_7) | 7 | Danno (armi ninjutsu) | +0k1 |
| Core | Forgery | forgery | 3 | Tiro Forgery | +1k0 vs Investigation/Perception |
| Core | Forgery | forgery | 5 | Tiro per rilevare falsi | +1k0 |
| Core | Forgery | forgery | 7 | Tiro Forgery | +0k1 vs Investigation/Perception |
| Core | Intimidation | intimidation | 5 | Tiri Intimidation contrapposti | +5 |
| Core | Stealth | stealth | 3 | Movimento | Simple Move Action = Water ×5 ft |
| Core | Stealth | stealth | 5 | Movimento | Simple Move Action = Water ×10 ft |
| Core | Temptation | temptation | 5 | Tiri Temptation contrapposti | +5 |
| Core | Engineering | engineering | 5 | Tiri Engineering coop./cumulativi | +5 |
| Core | Sailing | sailing | 5 | Tiri Sailing coop./cumulativi | +5 |
| LBS | Storytelling | storytelling | 5 | Insight | +2 |
| LBS | Storytelling | storytelling | 10 | Insight | +2 |
| LBS | Tahaddi | tahaddi | 7 | Tiri Focus (duello) | +2k2 se l'Assessment supera l'avversario di 10+ |
| LBS | Swordmanship | swordmanship (rule=ma_kenjutsu_3) | 3 | Danno (spada) | +1k0 |

---

*Documento generato dall'analisi dei data pack in `packs/`. Per i dettagli completi di ciascun effetto (condizioni, stance, costi in Punti Vuoto) consultare il `<Description>` del record corrispondente nel file XML di origine.*
