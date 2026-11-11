# Plain-English FAQ

Read this once before Dec 3. Every answer is written so you can say it out loud to someone who has never heard of a supply chain index. Each answer says what our own data shows, and separately what comes from outside sources (linked), so nobody on the team claims more than we can back up.

**Quick rule for Q&A:** if the question is "why did X happen," say what our data shows, then say "other reporting suggests Y, but we did not test that." That is an honest answer and it scores well on the "integrity" part of the grading.

---

## 1. Why only shipments that cross the Pacific or go through the canal? Why not Europe, Latin America, Africa?

Because the question we asked is about a route choice. For cargo coming from Asia to the US, a shipper really does have two options: cross the Pacific to a West Coast port, or go through the Panama Canal to an East or Gulf Coast port. That choice is what a canal drought or a West Coast jam changes.

Cargo from Europe or Africa mostly crosses the Atlantic to East Coast ports. It never faces the Pacific-versus-canal choice, so it would not tell us anything about this question. Latin America is mostly short-haul into Gulf and East Coast ports, again no real Pacific-versus-canal choice.

One nuance to be ready for: our "Panama-dependent" ports (NY-NJ, Savannah, Virginia, Charleston, Houston) are really East and Gulf Coast ports. Asian cargo can reach them through Panama or through Suez. That is why the Red Sea disruption shows up in the same lane share as the canal drought, and why we say we cannot fully separate those two episodes.

## 2. What does the pressure index measure?

It is the New York Fed's Global Supply Chain Pressure Index (GSCPI). In plain words: a single monthly number for how stretched global supply chains are.

It blends two kinds of inputs: shipping costs (container and dry-bulk freight indexes, plus airfreight prices), and survey answers from manufacturers in seven economies (China, the euro area, Japan, South Korea, Taiwan, the UK, the US) about delivery times, order backlogs, and stockpiles. The Fed removes the effect of plain demand swings so the number reflects supply trouble, then combines everything statistically (principal component analysis).

How to read it: **0 is the long-run average. 1 means one standard deviation above average, so clearly stressed. Negative means looser than normal.** Our peak is 4.43 in Dec 2021. Source: [NY Fed, "A New Barometer of Global Supply Chain Pressures"](https://libertystreeteconomics.newyorkfed.org/2022/01/a-new-barometer-of-global-supply-chain-pressures). Note the Fed revises past values with each release, so we record the download date.

What it does not do: it is one global number. It cannot tell you which port or which route is stressed. That is why we need Q2 and Q3.

## 3. Why check whether cargo shifts to different ports? Why does it matter?

Because a disruption does not make cargo disappear. It moves it. If a West Coast jam pushes cargo to the East Coast, the problem moves with it. Knowing where cargo goes tells you which ports and which routes are exposed next.

Worked example from our data: the Los Angeles and Long Beach backlog peaked at 103 ships in January 2022. The East and Gulf share of China imports rose 8.4 points over 2021-22. Then Savannah built its own backlog of 39 ships by August 2022, once the diverted cargo arrived. The jam moved.

This is also what "resilience" means in our question: a lane is resilient if it can absorb cargo when another lane breaks.

## 4. We dropped Mexico. What are we using now?

Mexico was only ever a possible stand-in for Panama Canal traffic. We dropped it because about 90% of US-Mexico trade moves by truck and rail, not ship, so it would have measured the wrong thing.

What we use now measures the route directly. We take Census import records by US port (China-origin, containerized value) and sort the ports into two groups. **Pacific-direct:** Los Angeles, Long Beach, Oakland, Seattle-Tacoma. **Panama-dependent:** NY-NJ, Savannah, Port of Virginia, Charleston, Houston. The "lane share" is the percent of China's containerized import value that lands in each group each month.

## 5. Why China only, instead of all trade?

Three reasons, in order of how solid they are:

1. **The route choice is an Asia story.** See answer 1. China has historically been the largest single Asian source of US container imports, so it is the cleanest test of the Pacific-versus-canal question.
2. **The data pull works one country at a time.** The Census port-level endpoint takes one country code per request (China is 5700), and each request is slow. One clean country beat several rushed ones.
3. **Keeping the comparison clean.** Mixing countries would blend very different routes and trade rules into one line.

How big is China's slice? It was the largest source of US goods imports through 2022, and still $439B in 2024, 13.4% of the total and second behind Mexico. It is shrinking: $215.0B in January to September 2026, 7.8% of US imports and fourth, behind Mexico, Canada and Taiwan. Sources: [Census, US trade with China](https://www.census.gov/foreign-trade/balance/c5700.html) and [Census, top trading partners](https://www.census.gov/foreign-trade/statistics/highlights/topyr.html). So our lens covers a shrinking slice of US trade. We call our result China-origin only and say it is unconfirmed for other countries. The next step we propose is to repeat it for a second origin country, such as Vietnam.

## 6. Were our decisions based on shipment volume? Is there enough data?

Two different measures, so be precise:

- **Lane share (Q2) is based on dollar value, not volume.** Census gives the dollar value of containerized imports by port. It does not give container counts. So Q2 is "share of the dollars," not "share of the boxes."
- **Port throughput (Q3 map and strips) is based on volume.** The Bureau of Transportation Statistics (BTS) publishes loaded import containers (TEUs) by port, and we index each port to its own 2019 level (2019 = 100). Ship-waiting counts are from the same BTS source.

Is there enough data? There is plenty of months (monthly, 2019 to 2026, so 80+ points per series). The real limit is **episodes**, not months. We have four disruption windows, and two of them overlap. That is enough to describe a pattern worth watching. It is not enough to call it a law. We say this on the limits slide.

## 7. Do reroutes happen because too many ships are waiting while the docks are full?

That is the intuitive story, and our data is consistent with it. But we should not claim it is the whole story.

What the data shows: the LA-Long Beach backlog peaked in January 2022 and cleared by about June 2022 (5 months). The East and Gulf share kept rising after the backlog cleared. So waiting ships alone do not explain the shift. Outside reporting also points to worries about West Coast labor disputes as a reason importers moved cargo east ([CNBC, Sep 2022](https://www.cnbc.com/2022/09/24/new-york-now-no-1-port-in-us-as-sea-change-in-trade-hits-west-coast.html)).

What to say: "Congestion is the clearest trigger we can see in the data. Importers also reacted to labor risk. We did not separate those two."

Also worth knowing: shippers book space weeks ahead, so the decision to reroute is made well before a ship reaches a full dock. That is reasoning, not something we measured.

## 8. Why did volume drop at some ports, and how does that relate to wait times?

They are opposite ends of the same cycle, and they are measured differently:

- **Wait time (backlog)** counts ships anchored waiting for a berth. It is high when **too much** arrives at once.
- **Throughput (volume)** counts containers actually moved, indexed to 2019. It is low when **too little** arrives.

In our data the Pacific ports were running above 2019 during the 2021-22 jam (index about 115 to 135, the "congestion window peak" column in `port_throughput_stats.csv`) while ships queued. Volume fell below 2019 later, around spring 2023 (index 71 to 81 at the Pacific ports), when the queues were gone. So the dip in volume came after the waiting ended, not at the same time.

Why volume fell in 2023: our data does not say. A common explanation is that importers had over-ordered during the surge and then bought less, and some cargo moved east. We did not test either, so say "we did not test why."

## 9. Do we know why Seattle-Tacoma is still below 2019?

Our data does not tell us why. It only shows that Seattle-Tacoma fell to a low of 71 in March 2023 (2019 = 100), got back to its 2019 level by July 2024 (16 months), and then fell again to 78 by July 2026. It is the one port of our nine still clearly below its 2019 level. (Oakland also took 16 months to recover, and it sits just under 2019 at 99.)

Outside reporting gives context. Sea-Intelligence reports that the Northwest Seaport Alliance (Seattle and Tacoma) had the steepest decline of any major US West Coast port, with laden import volumes down 18.0% year on year in 2026-Q1, while Vancouver rose 9.0% and Prince Rupert 7.8%. The reasons it lists are trade friction, favourable rail routes from Canadian ports into the US Midwest, and shippers avoiding US West Coast labor and congestion risk. Source: [Sea-Intelligence, TP Realignment: NAWC 2026-Q1 Volume Analysis](https://sea-intelligence.com/press-room/387-tp-realignment-nawc-2026-q1-volume-analysis).

Naming note: our charts and slides say "Seattle-Tacoma", meaning the **seaport** (the Northwest Seaport Alliance), not the airport. The data files and Tableau CSVs still use the short label "Sea-Tac" for the same port. On slides, write "Seattle-Tacoma (the seaport)" the first time.

## 10. Slide 07 explained

**What is congestion?** Too much cargo arriving at the same port at the same time. Ships queue offshore, containers pile up in the yard. The trouble is **at the port**, at the end of the trip. Example: Los Angeles in 2021.

**What is a chokepoint?** A narrow passage that many routes depend on, like the Panama Canal or the Red Sea and Suez Canal. The trouble is **on the route**, in the middle of the trip. Example: the 2023 Panama Canal drought, which limited how many ships could pass.

**How are they different?** Congestion blocks a destination. A chokepoint blocks a path. That is why they push cargo in opposite directions.

**What is the short Pacific route?** A ship leaves China and sails straight across the Pacific to a West Coast port (LA, Long Beach, Oakland, Seattle-Tacoma). No canal needed. On our schematic map it is about 5,600 nautical miles.

**What is the long route?** A ship leaves China, crosses the Pacific, passes through the Panama Canal, and arrives at an East or Gulf Coast port. About 10,900 nautical miles on our schematic, roughly 1.9 times as far. (These are rough great-circle distances between waypoints, not exact shipping lanes.)

**"Congestion favors the long route."** When the West Coast is jammed, cargo takes the longer route to the East and Gulf Coast to avoid the jam. We saw the East and Gulf share rise 8.4 points.

**"A chokepoint favors the short route."** When the canal or the Red Sea is the problem, cargo drifts back to the West Coast where no canal is needed. We saw a small westward drift in 2023-24 and again so far in 2026.

**What are "the two patterns"?** Say them by name, not "first" and "second": the **port-jam pattern** (cargo moves east) and the **chokepoint pattern** (cargo moves west).

**What did shipping rates predict, and why not now?** We tested whether the Shanghai-to-Los Angeles shipping price six months earlier lined up with the East and Gulf share of China imports. Across the whole period the match is moderate (r = 0.48). But splitting the period tells the real story: **r = 0.82 through 2022, r = 0.09 from 2023 on.** The match came from one episode, when the 2021 price spike was followed by the 2021-22 eastward shift. After that, prices stopped being a useful guide. One episode is not a reliable predictor, so we do not use it to forecast. (r is the correlation: 1 means two lines move together perfectly, 0 means no link.)

**What does "three panels" mean?** It was a mistake in our notes. The chart has **four stacked strips** on one shared timeline (pressure, lane share, shipping rate, port backlog). We now call it "stacked strips" and use it only as a backup slide.

**Is there a better way to show whether they move together?** Yes, and we are adding it. The stacked strips make you compare four wiggly lines by eye, which is hard. Two clearer views:

1. **Episode scorecard (main slide).** One row per disruption, one column per measure (pressure, cargo shift, ship backlog), with a bar in each cell. Your eye reads across a row and sees at once whether the three measures rose together. It uses only our own numbers.
2. **Rate scatter (backup).** One dot per month, shipping rate on the x axis, East and Gulf share on the y axis, two colors for "through 2022" and "2023 and later." You can see the tight line through 2022 and the shapeless cloud after it. That makes r = 0.82 versus 0.09 visible instead of just stated.

**What is our conclusion?** In one breath: **"The crisis is not over, but it is a different crisis. 2021 was a port jam: pressure, freight costs and ships waiting all spiked, and cargo moved east. 2026 is a cost shock: pressure and freight rates are up, ports are clear, and cargo is leaning west. That is a pattern from four episodes, so we call it worth watching, not proven."** On freight costs: the Shanghai to Los Angeles rate went from $1,730 in February 2020 (the series starts there) to $11,730 in August 2021. For why 2026 looks this way, see answers 12 to 14: that part is outside reporting and a theory, not something our data tests.

Raul delivers both the limits and the conclusion, so the close flows as one voice.

## 11. Where do we stand against the professor's guidelines?

See [`visualization_decisions.md`](visualization_decisions.md). It walks each chart through the course vocabulary: data and task abstraction, marks and channels, expressiveness and effectiveness, graphical integrity, color, small multiples, narrative structure, and the map rules from the geovisualization lecture (proportional symbols, counts versus ratios).

## 12. Why is pressure high in 2026 but ports are clear?

**What our data shows.** The pressure score peaked at 1.81 in May 2026 and was 1.28 in September. The Shanghai to Los Angeles spot rate rose from $3,112 in April to $7,848 in September (per 40-ft box). But Los Angeles and Long Beach averaged under 1 ship waiting in 2026, against 103 at the January 2022 peak. So 2026 is not a port jam.

**Theory (outside reporting, not tested in our data).** The Middle East war that began on February 28, 2026 effectively closed the Strait of Hormuz, roughly doubled bunker fuel prices, and sent ships the long way around the Cape ([Sea Vantage timeline](https://www.seavantage.com/blog/strait-of-hormuz-crisis-2026-shipping-disruption-timeline)). Higher fuel and longer routes raise costs and delivery times without filling US ports. The NY Fed itself did not say what drove the index ([Reuters, Oct 6 2026](https://finance.yahoo.com/economy/policy/articles/york-fed-says-supply-chain-143658302.html)).

## 13. Do tariffs explain it?

**What our data shows.** US goods imports from China fell from $440.3B in 2024 to $308.7B in 2025, and were $215.0B in January to September 2026 ([Census, US trade with China](https://www.census.gov/foreign-trade/balance/c5700.html)). China's share of US imports fell from 13.4% in 2024 (second, behind Mexico) to 7.8% so far in 2026 (fourth, behind Mexico, Canada and Taiwan) ([Census, top trading partners](https://www.census.gov/foreign-trade/statistics/highlights/topyr.html)). PIIE puts China's share at about 9% by the end of 2025 ([PIIE, Mar 16 2026](https://www.piie.com/blogs/realtime-economics/2026/trump-china-trade-wars-five-takeaways-us-imports-2025)).

**Theory, not a result.** Fewer containers from China would help explain why West Coast ports are clear. Tariffs do not explain why pressure is higher. We did not test either link.

## 14. What is the war's role?

**Outside reporting, a theory, not our result.** Reuters reported that the pressure index hit its highest level in nearly four years in April 2026 (first reported as 1.82; our revised snapshot has 1.78), and that the rise coincides with the war, but the NY Fed did not explain it ([Reuters via PYMNTS, May 6 2026](https://www.pymnts.com/supply-chain/2026/fed-data-shows-global-supply-chain-pressure-hits-4-year-high/)). Xeneta reported Far East to US West Coast spot rates up 192% between February 28 and June 19, 2026, even though that lane does not pass through Hormuz, and expected full recovery no earlier than mid-September ([Xeneta, Jun 19 2026](https://www.xeneta.com/news/us-iran-deal-to-reopen-strait-of-hormuz-but-full-container-shipping-recovery-at-least-three-months-away)).

**What to say if pushed.** The timing fits: our pressure score jumped from 0.63 in March to 1.78 in April. But it was already above zero before the war (0.47 in December 2025), and we have no data that separates the war from tariffs or anything else. Call it a theory.

---

## Two corrections we found while preparing (say so if asked)

- The earlier deck said September 2026's reading of 1.28 was "about 40% of the 2021 peak." Checking the math: 1.28 / 4.43 is about 29%. The **40% figure is the 2026 peak of 1.81** (1.81 / 4.43 is about 41%). The deck and notes now say: peak 1.81 in May, 1.28 in September.
- The earlier deck said "West Coast ports recovered in 2 to 3 months." That is true of Los Angeles (2) and Long Beach (3). **Oakland and Seattle-Tacoma each took 16 months, and Seattle-Tacoma then fell back to 78 by July 2026, the one port clearly below 2019.** The deck now says that.

Catching and fixing our own errors is exactly the "integrity" story the professor asked about. Use it.
