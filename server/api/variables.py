from __future__ import annotations
import requests
import socket
import math
import tldextract
import time
from time import monotonic
import json
import os
import asyncio
import feedparser
from shapely.geometry import MultiPoint
from pathlib import Path
import statistics
import aiohttp





data_1 = [
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/india/shah-banos-daughter-sends-legal-notice-to-emraan-hashmi-yami-gautams-haq/articleshow/125047347.cms",
    "title": "Shah Bano's daughter sends legal notice to Emraan Hashmi, Yami Gautam's 'HAQ'",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/new-updates/indians-went-crazy-after-south-africa-captain-laura-wolvaardt-thanks-team-india-on-twitter-it-turned-out-to-be-fake/articleshow/125047331.cms",
    "title": "Indians went crazy after South Africa Captain Laura Wolvaardt thanks Team India on Twitter, it turned out to be fake",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Ashburn",
    "url": "https://m.economictimes.com/markets/stocks/news/a-measured-move-opec-balances-growth-with-caution/opec-balances-expectations-and-caution/slideshow/125047485.cms",
    "title": "A Measured Move: OPEC+ balances growth with caution",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/tech/technology/pine-labs-ipo-could-unlock-esops-worth-rs-1360-crore/articleshow/125047189.cms",
    "title": "Pine Labs IPO could unlock Esops worth Rs 1,360 crore",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "New Delhi",
    "url": "https://indianexpress.com/article/cities/delhi/breakthrough-gurgaon-police-arrest-fugitive-gangster-deepak-nandal-rohtak-10342837/",
    "title": "In another breakthrough, Gurgaon police arrest key associate of fugitive gangster Deepak Nandal in Rohtak",
    "country": "India",
    "latitude": 28.6419,
    "longitude": 77.2217
  },
  {
    "city": "Mumbai",
    "url": "https://www.indiatimes.com/trending/haq-real-story-shah-bano-fight-for-justice-after-husband-abandoned-her-yami-gautam-emraan-hashmi/articleshow/125046584.html",
    "title": "Haq real story: Shah Bano’s historic fight for justice after her husband abandoned her",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Chennai",
    "url": "https://www.thehindubusinessline.com/markets/stock-markets/markets-open-flat-amid-mixed-global-cues-shriram-finance-leads-gainers-with-5-rally/article70234957.ece",
    "title": "Markets open flat amid mixed global cues; Shriram Finance leads gainers with 5% rally",
    "country": "India",
    "latitude": 13.0837,
    "longitude": 80.2702
  },
  {
    "city": "Mumbai",
    "url": "https://www.rediff.com/movies/report/revealed-when-juhi-met-shah-rukh-for-the-first-time/20251103.htm",
    "title": "REVEALED! When Juhi Met SRK For 1st Time!",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/science/pm-modi-launches-rs-1-lakh-crore-rdi-fund-to-spur-private-investment-in-research-development/articleshow/125047079.cms",
    "title": "PM Modi launches Rs 1 lakh crore RDI Fund to spur private investment in research & development",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Melbourne",
    "url": "https://berwicknews.starcommunity.com.au/sport/2025-11-03/cricket-world-rallies-together/",
    "title": "Cricket world rallies together",
    "country": "AU",
    "latitude": -37.814,
    "longitude": 144.9633
  },
  {
    "city": "New Delhi",
    "url": "https://www.livemint.com/companies/start-ups/pine-labs-ipo-shares-stock-valuation-investors-peak-xv-temasek-paypal-11762139485331.html",
    "title": "Pine Labs’ early investors set to bag stellar gains from IPO",
    "country": "India",
    "latitude": 28.6419,
    "longitude": 77.2217
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/new-updates/icai-ca-january-2026-exam-registration-begins-november-3-check-how-to-apply-exam-schedule-last-date-and-fees/articleshow/125046888.cms",
    "title": "ICAI CA January 2026 exam registration begins November 3: Check how to apply, exam schedule, last date and fees",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Seattle",
    "url": "https://www.bloomberg.com/news/articles/2025-11-03/rothschild-sees-more-global-firms-listing-indian-units-next-year",
    "title": "Rothschild sees more global firms listing Indian units next year",
    "country": "US",
    "latitude": 47.6339,
    "longitude": -122.3476
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/markets/ipos/fpos/groww-ipo-fintech-brokers-changed-investing-for-12-crore-indians-but-now-staring-at-a-structural-reset/articleshow/125046618.cms",
    "title": "Groww IPO: Fintech brokers changed investing for 12 crore Indians, but now staring at a structural reset",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "New York",
    "url": "https://www.yahoo.com/news/articles/minibus-rams-parked-truck-indias-042834276.html",
    "title": "Truck rams into bus in southern India, killing at least 20",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "New Delhi",
    "url": "https://www.livemint.com/money/personal-finance/these-5-premium-credit-cards-can-lift-your-lifestyle-a-great-deal-11762129080146.html",
    "title": "THESE 5 premium credit cards can lift your lifestyle a great deal",
    "country": "India",
    "latitude": 28.6419,
    "longitude": 77.2217
  },
  {
    "city": "Mumbai",
    "url": "https://timesofindia.indiatimes.com/auto/cars/2025-tata-sierra-teased-iconic-suv-to-return-on-november-25/articleshow/125046597.cms",
    "title": "2025 Tata Sierra teased: Iconic SUV to return on November 25",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://timesofindia.indiatimes.com/education/news/jee-main-2026-nta-confirms-no-calculator-allowed-clarifies-typo-error-in-bulletin/articleshow/125046491.cms",
    "title": "JEE Main 2026: NTA confirms calculators not allowed; clarifies typo error in bulletin",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/tech/technology/sequoia-us-crossover-fund-may-join-growws-anchor-book-ahead-of-ipo/articleshow/125046720.cms",
    "title": "Sequoia US crossover fund may join Groww’s anchor book ahead of IPO",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/tech/technology/sequoia-capital-us-may-join-growws-anchor-book-ahead-of-ipo/articleshow/125046720.cms",
    "title": "Sequoia Capital US may join Groww’s anchor book ahead of IPO",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Los Angeles",
    "url": "https://variety.com/2025/film/box-office/china-box-office-her-turn-evangelion-1236568170/",
    "title": "China Box Office: ‘Her Turn’ Debuts at No. 1, ‘Evangelion: 3.0+1.0’ Opens Strong",
    "country": "United States",
    "latitude": 34.0537,
    "longitude": -118.2428
  },
  {
    "city": "Richardson",
    "url": "https://freerepublic.com/focus/f-news/4350350/posts",
    "title": "The Nigerian government agrees to accept Trump’s help against Islamic terrorists",
    "country": "US",
    "latitude": 32.9482,
    "longitude": -96.7297
  },
  {
    "city": "Ashburn",
    "url": "https://m.economictimes.com/markets/stocks/news/a-measured-move-opec-balances-growth-with-caution/opec-balances-expectations-and-caution/slideshow/125047485.cms",
    "title": "A Measured Move: OPEC+ balances growth with caution",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/e38f4fb7d5ad1fc8",
    "title": "Baidu says its Apollo Go robotaxi hit 250,000 weekly orders globally as of October 31, matching Waymo's 250,000 weekly paid US rides reported in April 2025",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/tech/artificial-intelligence/trump-says-china-other-countries-cant-have-nvidias-top-ai-chips/articleshow/125047216.cms",
    "title": "Trump says China, other countries can't have Nvidia's top AI chips",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/markets/expert-view/fertilizer-stocks-poised-for-growth-amid-policy-push-siddhartha-khemka/articleshow/125047116.cms",
    "title": "Fertilizer stocks poised for growth amid policy push: Siddhartha Khemka",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "New York",
    "url": "https://finance.yahoo.com/news/high-growth-tech-stocks-asia-043757046.html",
    "title": "High Growth Tech Stocks In Asia Including Sichuan Jiuyuan Yinhai Software Co Ltd",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "New York",
    "url": "https://finance.yahoo.com/news/3-asian-stocks-estimated-trading-043751117.html",
    "title": "3 Asian Stocks Estimated To Be Trading At Discounts Up To 39.2%",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/16d049beaa088b7b",
    "title": "Gold Dips After China Ends Tax Incentive | Bloomberg: The Asia Trade, 11/3/25",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "New York",
    "url": "https://finance.yahoo.com/news/asian-growth-stocks-high-insider-043537474.html",
    "title": "Asian Growth Stocks With High Insider Ownership To Watch",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "Dublin",
    "url": "https://www.irishtimes.com/culture/books/review/2025/11/03/paschal-donohoe-reviews-the-worlds-worst-bet-how-the-globalisation-gamble-went-wrong/",
    "title": "Paschal Donohoe reviews The World’s Worst Bet: How The Globalisation Gamble Went Wrong",
    "country": "Ireland",
    "latitude": 53.3494,
    "longitude": -6.2606
  },
  {
    "city": "Toronto",
    "url": "https://financialpost.com/pmn/shares-in-asia-advance-led-by-tech-stocks-after-another-week-of-gains-for-wall-st",
    "title": "Shares in Asia advance, led by tech stocks, after another week of gains for Wall St",
    "country": "Canada",
    "latitude": 43.6535,
    "longitude": -79.3839
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/tech/technology/sequoia-capital-us-may-join-growws-anchor-book-ahead-of-ipo/articleshow/125046720.cms",
    "title": "Sequoia Capital US may join Groww’s anchor book ahead of IPO",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "New York",
    "url": "https://finance.yahoo.com/news/shares-asia-advance-led-tech-042354013.html",
    "title": "Shares in Asia advance, led by tech stocks, after another week of gains for Wall St",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "New York",
    "url": "https://finance.yahoo.com/news/shares-asia-advance-led-tech-042354838.html",
    "title": "Shares in Asia advance, led by tech stocks, after another week of gains for Wall St",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "Moscow",
    "url": "https://sputnikglobe.com/20251103/russias-mishustin-arrives-in-china-for-2-day-visit-1123055481.html",
    "title": "Russia's Mishustin Arrives in China for 2-Day Visit",
    "country": "Russia",
    "latitude": 55.6256,
    "longitude": 37.6064
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/94bb6388b09213ac",
    "title": "At APEC, Xi Jinping proposed a World Artificial Intelligence Cooperation Organization for global AI regulation; state media says it could be based in Shanghai",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/markets/commodities/news/gold-price-today-yellow-metal-near-3-week-low-down-rs-11k-from-peak-is-this-just-a-dip-or-start-of-a-bigger-slide/articleshow/125046580.cms",
    "title": "Gold Price Today: Yellow metal near 3-week low, down Rs 11K from peak. Is this just a dip or start of a bigger slide?",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "New York",
    "url": "https://www.huffpost.com/entry/supreme-court-trump-tariffs-diplomacy_n_69082893e4b00afef15f4d88",
    "title": "Tariffs Are Trump's Favorite Foreign Policy Tool. The Supreme Court Could Change How He Uses Them.",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "New Delhi",
    "url": "https://indianexpress.com/article/world/trump-says-no-tomahawk-missiles-for-ukraine-leaves-door-open-10342697/",
    "title": "‘No, not really’: Trump says on Tomahawk missiles for Ukraine, but leaves door open",
    "country": "India",
    "latitude": 28.6419,
    "longitude": 77.2217
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/507a07f943f8a50e",
    "title": "USPS & all major banks to close for 24 hours in days for first November shutdown",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/32d012aab5a000cc",
    "title": "5.3-magnitude earthquake strikes Philippines",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Beit El",
    "url": "https://www.israelnationalnews.com/news/417205",
    "title": "Pennsylvania diocese condemns 'profoundly offensive' Holocaust imagery on parade float",
    "country": "State of Palestine",
    "latitude": 31.942,
    "longitude": 35.222
  },
  {
    "city": "Toronto",
    "url": "https://www.digitaljournal.com/entertainment/review-catherine-curtin-and-marcia-cross-star-in-pen-pals-off-broadway-production/article",
    "title": "Review: Catherine Curtin and Marcia Cross star in ‘Pen Pals’ Off-Broadway production",
    "country": "Canada",
    "latitude": 43.6535,
    "longitude": -79.3839
  },
  {
    "city": "San Francisco",
    "url": "https://dailycaller.com/2025/11/02/ufo-tracker-enigma-9000-sightings-underwater-us-coast/",
    "title": "‘Technology Is Picking Up Ghosts Underwater’: UFO Tracker Shows Thousands Of Objects Hovering Around US Coasts",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/tech/artificial-intelligence/trump-says-china-other-countries-cant-have-nvidias-top-ai-chips/articleshow/125047216.cms",
    "title": "Trump says China, other countries can't have Nvidia's top AI chips",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Sydney",
    "url": "https://www.abc.net.au/news/2025-11-03/labor-retreats-from-nuclear-weapons-ban-pledge-four-corners/105959312",
    "title": "The PM once championed a nuclear weapons ban. What happened?",
    "country": "Australia",
    "latitude": -33.8698,
    "longitude": 151.2083
  },
  {
    "city": "New York",
    "url": "https://finance.yahoo.com/news/3-asian-stocks-estimated-trading-043751117.html",
    "title": "3 Asian Stocks Estimated To Be Trading At Discounts Up To 39.2%",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "Dublin",
    "url": "https://www.irishtimes.com/culture/books/review/2025/11/03/paschal-donohoe-reviews-the-worlds-worst-bet-how-the-globalisation-gamble-went-wrong/",
    "title": "Paschal Donohoe reviews The World’s Worst Bet: How The Globalisation Gamble Went Wrong",
    "country": "Ireland",
    "latitude": 53.3494,
    "longitude": -6.2606
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/50f1631adb5a3cd5",
    "title": "In Practice, 'Net Zero' Was Exactly How Much Such Pledges Were Worth",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Stockholm",
    "url": "https://www.aljazeera.com/news/2025/11/3/calls-for-justice-after-mexico-mayor-killed-during-day-of-the-dead-festival",
    "title": "Calls for justice after Mexico mayor killed during Day of the Dead festival",
    "country": "SE",
    "latitude": 59.3294,
    "longitude": 18.0687
  },
  {
    "city": "Beit El",
    "url": "https://www.israelnationalnews.com/news/417203",
    "title": "Iran vows to rebuild nuclear sites 'stronger than before'",
    "country": "State of Palestine",
    "latitude": 31.942,
    "longitude": 35.222
  },
  {
    "city": "San Francisco",
    "url": "https://www.nzherald.co.nz/northern-advocate/news/mpi-finds-fourth-yellow-legged-hornet-queen-and-says-traps-will-be-used/2QLUEEODFJFH7OPJRJ3ZWAAYRI/",
    "title": "MPI finds fourth yellow-legged hornet queen and says traps will be used",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "New York",
    "url": "https://www.huffpost.com/entry/supreme-court-trump-tariffs-diplomacy_n_69082893e4b00afef15f4d88",
    "title": "Tariffs Are Trump's Favorite Foreign Policy Tool. The Supreme Court Could Change How He Uses Them.",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "Seattle",
    "url": "https://www.thestar.com.my/news/nation/2025/11/03/msias-ree-processing-head-start-safeguards-mineral-sovereignty-says-chang",
    "title": "Msia’s REE processing head start safeguards mineral sovereignty, says Chang",
    "country": "US",
    "latitude": 47.6339,
    "longitude": -122.3476
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/d82ad46657f89d3c",
    "title": "Trump calls for the end to the filibuster",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://www.animenewsnetwork.com/daily-briefs/2025-11-02/godzilla-minus-one-film-follow-up-unveils-title/.230580",
    "title": "Godzilla Minus One Film's Follow-Up Unveils Title",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Austin",
    "url": "https://www.lewrockwell.com/2025/11/jacob-hornberger/another-regime-change-war-will-accelerate-americas-slide-into-authoritarianism/",
    "title": "Another Regime-Change War Will Accelerate America’s Slide Into Authoritarianism",
    "country": "US",
    "latitude": 30.2672,
    "longitude": -97.7431
  },
  {
    "city": "Austin",
    "url": "https://www.lewrockwell.com/2025/11/no_author/gold-is-the-canary-in-the-coal-mine/",
    "title": "Gold Is the Canary in the Coal Mine",
    "country": "US",
    "latitude": 30.2672,
    "longitude": -97.7431
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/markets/stocks/news/godrej-consumer-shares-rally-6-after-q2-results-should-you-buy-sell-or-hold/articleshow/125046689.cms",
    "title": "Godrej Consumer shares rally 6% as Goldman Sachs raises target after Q2 show. Should you invest?",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "New York",
    "url": "https://finance.yahoo.com/news/asias-factories-stumble-us-tariffs-035604528.html",
    "title": "Asia's factories stumble as US tariffs hit order books",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/5cdcfb7c32d77ad7",
    "title": "Foreigners Buy Most Indonesia Shares in Year as Outlook Improves",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "South Tangerang",
    "url": "https://katalogpromosi.com/promo-chatime-welcome-november-2-minuman-reguler-mulai-rp-40-000/",
    "title": "Promo Chatime Welcome November 2 Minuman Reguler Mulai Rp. 40.000",
    "country": "ID",
    "latitude": -6.2886,
    "longitude": 106.7179
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/defence/pakistan-eyes-2026-launch-for-first-chinese-submarine-in-5-billion-arms-deal/articleshow/125045444.cms",
    "title": "Pakistan eyes 2026 launch for first Chinese submarine in $5 billion arms deal",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/95828a06b5b84496",
    "title": "Bali deadly floods highlight Indonesian island's overtourism struggles",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Chennai",
    "url": "https://www.thehindubusinessline.com/business-tech/reinforcements-for-the-cyber-frontline/article70233666.ece",
    "title": "Reinforcements for the cyber frontline",
    "country": "India",
    "latitude": 13.0837,
    "longitude": 80.2702
  },
  {
    "city": "Ashburn",
    "url": "https://bmcmededuc.biomedcentral.com/articles/10.1186/s12909-025-07970-6",
    "title": "Student experiences and learning outcomes of an interprofessional and international service-learning program: an exploratory study",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "Los Angeles",
    "url": "https://www.globenewswire.com/news-release/2025/11/02/3178815/0/en/Alvotech-Provides-Update-on-the-Status-of-U-S-Biologics-License-Application-for-AVT05.html",
    "title": "Alvotech Provides Update on the Status of U.S. Biologics License Application for AVT05",
    "country": "United States",
    "latitude": 34.0522,
    "longitude": -118.2437
  },
  {
    "city": "Ashburn",
    "url": "https://www.globenewswire.com/news-release/2025/11/02/3178814/0/en/Alvotech-Provides-Update-on-the-Status-of-U-S-Biologics-License-Application-for-AVT05.html",
    "title": "Alvotech Provides Update on the Status of U.S. Biologics License Application for AVT05",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "Jersey City",
    "url": "https://www.forbes.com/sites/scotttravers/2025/11/02/10-forms-of-art-in-nature-from-the-natures-best-photography-2025-awards/",
    "title": "10 Forms Of ‘Art In Nature’ From The Nature’s Best Photography 2025 Awards",
    "country": "United States",
    "latitude": 40.7216,
    "longitude": -74.0475
  },
  {
    "city": "Elk Grove Village",
    "url": "https://www.foxnews.com/sports/new-york-city-marathon-mens-race-features-photo-finish",
    "title": "New York City Marathon men's race features photo finish",
    "country": "US",
    "latitude": 42.0039,
    "longitude": -87.9703
  },
  {
    "city": "New York",
    "url": "https://finance.yahoo.com/news/see-high-tariff-rates-toys-164406001.html",
    "title": "See the High Tariff Rates on Toys, Video Games and 7 Other Popular Holiday Gifts",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/economy/foreign-trade/canadian-pm-carney-refers-to-progress-with-india-amid-tariff-strains-with-us/articleshow/125036939.cms",
    "title": "Canadian PM Carney refers to 'progress' with India amid tariff strains with US",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Jakarta",
    "url": "https://en.antaranews.com/news/389541/realizing-child-friendly-pesantrens-for-excellent-generations",
    "title": "Realizing child-friendly pesantrens for excellent generations",
    "country": "Indonesia",
    "latitude": -6.1753,
    "longitude": 106.8269
  },
  {
    "city": "Columbus",
    "url": "https://oilprice.com/Energy/Energy-General/Why-the-Worlds-Coal-Addiction-Wont-End-Anytime-Soon.html",
    "title": "Why the World’s Coal Addiction Won’t End Anytime Soon",
    "country": "US",
    "latitude": 39.9612,
    "longitude": -82.9988
  },
  {
    "city": "New York",
    "url": "https://finance.yahoo.com/news/boe-set-hold-rates-uk-200000131.html",
    "title": "BOE Set to Hold Rates as UK Budget Looms Over Decision",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "Euless",
    "url": "https://www.autosport.com/motogp/news/joan-mir-admits-honda-not-ready-to-win-in-motogp-we-have-to-walk-before-we-can-run/10773280/",
    "title": "Mir calls for consistency at Honda: ‘We finish on the podium, or on the ground’",
    "country": "US",
    "latitude": 32.8371,
    "longitude": -97.082
  },
  {
    "city": "Mumbai",
    "url": "https://www.rediff.com/sports/report/pramod-sukant-nitesh-manisha-win-golds-at-indonesia-para-badminton/20251102.htm",
    "title": "Pramod-Sukant, Nitesh, Manisha win Para golds at Indonesia",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Euless",
    "url": "https://dpa-international.com/economics/urn:newsml:dpa.com:20090101:251102-99-513587/",
    "title": "World Economic Forum head predicts AI and cryptocurrency bubbles",
    "country": "US",
    "latitude": 32.8371,
    "longitude": -97.082
  },
  {
    "city": "San Francisco",
    "url": "https://www.rte.ie/news/world/2025/1103/1541816-afghanistan-earthquake/",
    "title": "Afghanistan earthquake kills 20, injures over 300",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://www.rte.ie/news/world/2025/1103/1541816-at-least-9-dead-in-afghanistan-earthquake/",
    "title": "At least 9 dead in Afghanistan earthquake",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Bonn",
    "url": "https://www.dw.com/en/trump-says-there-could-be-us-military-action-in-nigeria/a-74592286",
    "title": "Trump says there 'could be' US military action in Nigeria",
    "country": "DE",
    "latitude": 50.7344,
    "longitude": 7.0955
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/international/world-news/why-is-afghanistan-so-prone-to-earthquakes/articleshow/125045866.cms",
    "title": "Why is Afghanistan so prone to earthquakes?",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/2dcc1ccca037f165",
    "title": "Afghanistan, Pakistan have been hit by a spate of quakes in recent years",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/defence/trump-says-russia-china-have-secretly-tested-nuclear-weapons/articleshow/125045741.cms",
    "title": "Trump says Russia, China have secretly tested nuclear weapons",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/defence/pakistan-eyes-2026-launch-for-first-chinese-submarine-in-5-billion-arms-deal/articleshow/125045444.cms",
    "title": "Pakistan eyes 2026 launch for first Chinese submarine in $5 billion arms deal",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/international/world-news/afghanistan-earthquake-magnitude-6-3-earthquake-shakes-afghanistans-mazar-e-sharif-city-several-casualties-feared/articleshow/125045307.cms",
    "title": "Afghanistan earthquake: Magnitude 6.3 earthquake shakes Afghanistan's Mazar-e Sharif city, several casualties feared",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "El Segundo",
    "url": "https://www.cbc.ca/news/world/afghanistan-earthquake-9.6964015",
    "title": "Deadly 6.3 magnitude earthquake hits northern Afghanistan",
    "country": "US",
    "latitude": 33.9192,
    "longitude": -118.4165
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/defence/trump-says-there-could-be-us-troops-on-the-ground-in-nigeria-or-air-strikes/articleshow/125045083.cms",
    "title": "Trump says there 'could be' US troops on the ground in Nigeria, or air strikes",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "London",
    "url": "https://news.sky.com/story/at-least-seven-dead-and-150-injured-after-magnitude-6-3-earthquake-in-north-afghanistan-13463004",
    "title": "At least seven dead in Afghanistan earthquake",
    "country": "GB",
    "latitude": 51.5085,
    "longitude": -0.1257
  },
  {
    "city": "Jersey City",
    "url": "https://www.forbes.com/sites/brucelee/2025/11/02/how-trump-administration-actions-might-affect-polio-eradication/",
    "title": "How Trump Administration Actions Might Affect Polio Eradication",
    "country": "United States",
    "latitude": 40.7216,
    "longitude": -74.0475
  },
  {
    "city": "Seattle",
    "url": "https://www.thestar.com.my/news/world/2025/11/03/magnitude-63-earthquake-shakes-afghanistan039s-mazar-e-sharif-city-casualties-feared",
    "title": "Magnitude 6.3 earthquake shakes Afghanistan's Mazar-e Sharif city, casualties feared",
    "country": "US",
    "latitude": 47.6339,
    "longitude": -122.3476
  },
  {
    "city": "San Francisco",
    "url": "https://line25.com/articles/mostbet-apk-download-recognized-app/",
    "title": "Mostbet Apk Download Recognized App",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Chennai",
    "url": "https://www.thehindubusinessline.com/business-tech/reinforcements-for-the-cyber-frontline/article70233666.ece",
    "title": "Reinforcements for the cyber frontline",
    "country": "India",
    "latitude": 13.0837,
    "longitude": 80.2702
  },
  {
    "city": "New Delhi",
    "url": "https://indianexpress.com/article/opinion/columns/as-global-consensus-against-nuclear-testing-frays-india-should-re-evaluate-its-options-10342216/",
    "title": "As global consensus against nuclear testing frays, India should re-evaluate its options",
    "country": "India",
    "latitude": 28.6419,
    "longitude": 77.2217
  },
  {
    "city": "Chennai",
    "url": "https://www.thehindubusinessline.com/specials/pulse/no-child-left-behind-closing-indias-immunisation-gap/article70219871.ece",
    "title": "No child left behind: Closing India’s immunisation gap",
    "country": "India",
    "latitude": 13.0837,
    "longitude": 80.2702
  },
  {
    "city": "San Francisco",
    "url": "https://www.cbsnews.com/news/read-full-transcript-norah-odonnell-60-minutes-interview-with-president-trump/",
    "title": "Read the full transcript of 60 Minutes' interview with President Trump",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Sydney",
    "url": "https://www.abc.net.au/news/2025-11-03/afghanistan-earthquake/105964078",
    "title": "Magnitude-6.3 earthquake hits Afghanistan",
    "country": "Australia",
    "latitude": -33.8698,
    "longitude": 151.2083
  },
  {
    "city": "Richardson",
    "url": "https://freerepublic.com/focus/f-news/4350350/posts",
    "title": "The Nigerian government agrees to accept Trump’s help against Islamic terrorists",
    "country": "US",
    "latitude": 32.9482,
    "longitude": -96.7297
  },
  {
    "city": "Bonn",
    "url": "https://www.dw.com/en/trump-says-there-could-be-us-military-action-in-nigeria/a-74592286",
    "title": "Trump says there 'could be' US military action in Nigeria",
    "country": "DE",
    "latitude": 50.7344,
    "longitude": 7.0955
  }
]


data_2 = [
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/international/world-news/what-to-know-as-nigeria-rejects-us-military-threat-over-alleged-christian-killings/articleshow/125045849.cms",
    "title": "What to know as Nigeria rejects US military threat over alleged Christian killings",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Seattle",
    "url": "https://abcnews.go.com/International/wireStory/nigeria-rejects-us-military-threat-alleged-christian-killings-127108565",
    "title": "What to know as Nigeria rejects US military threat over alleged Christian killings",
    "country": "US",
    "latitude": 47.5413,
    "longitude": -122.3129
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/defence/trump-says-there-could-be-us-troops-on-the-ground-in-nigeria-or-air-strikes/articleshow/125045083.cms",
    "title": "Trump says there 'could be' US troops on the ground in Nigeria, or air strikes",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Elk Grove Village",
    "url": "https://www.foxnews.com/politics/trump-says-tariffs-critical-national-security-supreme-court-prepares-landmark-decision",
    "title": "Trump says tariffs critical to national security as Supreme Court prepares landmark decision",
    "country": "US",
    "latitude": 42.0039,
    "longitude": -87.9703
  },
  {
    "city": "San Francisco",
    "url": "https://slashdot.org/firehose.pl?op=view&amp;id=179945238",
    "title": "Trump threat of military action in Nigeria prompts confusion and alarm - The Washington Post",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://www.japantimes.co.jp/news/2025/11/03/world/politics/nigeria-us-islamist-sovereignty/",
    "title": "Nigeria says U.S. help against Islamist insurgents must respect its sovereignty",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Columbus",
    "url": "https://oilprice.com/Latest-Energy-News/World-News/Oil-Prices-Edge-Higher-After-OPEC-Pauses-Output-Hikes-in-Early-2026.html",
    "title": "Oil Prices Edge Higher After OPEC+ Pauses Output Hikes in Early 2026",
    "country": "US",
    "latitude": 39.9612,
    "longitude": -82.9988
  },
  {
    "city": "Seattle",
    "url": "https://abcnews.go.com/International/wireStory/trump-threatens-nigeria-potential-military-action-escalates-claim-127092170",
    "title": "Trump threatens Nigeria with potential military action, escalates claim of Christian persecution",
    "country": "US",
    "latitude": 47.5413,
    "longitude": -122.3129
  },
  {
    "city": "San Francisco",
    "url": "https://decider.com/2025/11/02/real-housewives-of-potomac-tia-glover-interview/",
    "title": "‘Real Housewives Of Potomac’ Star Tia Glover Thinks Stacey Rusch Is Always In The Hot Seat Because “That’s Where She Likes To Be”: “Nothing Is Too Far Fetched For Her”",
    "country": "US",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  {
    "city": "Atlanta",
    "url": "https://www.nature.com/articles/s41598-025-22000-7",
    "title": "Risk assessment of heavy metals in north of Iran (Sari) rice and implications for human health",
    "country": "US",
    "latitude": 33.749,
    "longitude": -84.388
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/d20a067ffd5528f2",
    "title": "Trump says 'could be' US boots on ground in Nigeria",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Ashburn",
    "url": "https://www.nbcnews.com/news/us-news/weekend-rundown-november-2-rcna241207",
    "title": "Here's the biggest news you missed this weekend",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "New York",
    "url": "https://www.huffpost.com/entry/nicki-minaj-trump-nigeria-christian-killings_n_690785c9e4b05a8637e7e2f8",
    "title": "Nicki Minaj Sings Trump’s Praises For His Nigeria Comments",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "Osaka",
    "url": "https://japantoday.com/category/world/nigeria-says-u.s.-help-against-islamist-insurgents-must-respect-its-sovereignty",
    "title": "Nigeria says U.S. help against Islamist insurgents must respect its sovereignty",
    "country": "JP",
    "latitude": 34.6938,
    "longitude": 135.5011
  },
  {
    "city": "Richardson",
    "url": "https://freerepublic.com/focus/f-bloggers/4350292/posts",
    "title": "Trump Warns Nigeria: US 'Guns-a-Blazing' if Christian Killings Continue",
    "country": "US",
    "latitude": 32.9482,
    "longitude": -96.7297
  },
  {
    "city": "Abuja",
    "url": "https://www.premiumtimesng.com/health/health-news/832416-federal-govt-condemns-abduction-of-neurosurgeon-calls-for-urgent-rescue.html",
    "title": "Federal govt condemns abduction of neurosurgeon, calls for urgent rescue",
    "country": "Nigeria",
    "latitude": 9.0556,
    "longitude": 7.4914
  },
  {
    "city": "San Francisco",
    "url": "https://biztoc.com/x/d90625fc20f5c6c5",
    "title": "Trump Threatens US Military Action In Nigeria Over 'Killing Of Christians'",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://www.japantimes.co.jp/environment/2025/11/03/climate-change/trump-pivot-climate-eu-hoekstra/",
    "title": "Trump pivot is a ‘watershed moment’ for climate, says EU’s Hoekstra",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Seattle",
    "url": "https://www.thestar.com.my/news/world/2025/11/03/brazil-kicks-off-cop30-climate-events-in-year-of-distractions",
    "title": "Brazil kicks off COP30 climate events in year of distractions",
    "country": "US",
    "latitude": 47.6339,
    "longitude": -122.3476
  },
  {
    "city": "Ashburn",
    "url": "https://www.justjared.com/2025/11/02/wicked-director-jon-m-chu-reacts-to-ariana-grande-cynthia-erivos-matching-tattoos/",
    "title": "'Wicked' Director Jon M Chu Reacts to Ariana Grande & Cynthia Erivo's Matching Tattoos",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "San Francisco",
    "url": "https://nypost.com/2025/11/02/opinion/bill-gates-finally-got-to-right-answer-on-climate-change-but-not-before-immense-harm/",
    "title": "Bill Gates finally got to right answer on climate change — but not before immense harm",
    "country": "US",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  {
    "city": "New York",
    "url": "https://finance.yahoo.com/news/bofa-lifts-sea-limited-se-031041680.html",
    "title": "BofA Lifts Sea Limited (SE) Price Target, Cites Strong Growth Momentum",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "San Francisco",
    "url": "https://www.thegatewaypundit.com/2025/11/newsoms-latest-anti-trump-talking-point-just-got/",
    "title": "Newsom’s Latest Anti-Trump Talking Point Just Got DESTOYED by Facts",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://www.usmagazine.com/celebrity-news/news/prince-william-says-he-is-excited-for-first-visit-to-brazil/#article",
    "title": "Prince William Says He's 'Excited' for 1st Ever Visit to Brazil",
    "country": "US",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  {
    "city": "Jersey City",
    "url": "https://www.forbes.com/sites/trentreinsmith/2025/11/02/ufc-announces-ufc-322-full-fight-card-order/",
    "title": "UFC Announces UFC 322 Full Fight Card Order",
    "country": "United States",
    "latitude": 40.7216,
    "longitude": -74.0475
  },
  {
    "city": "San Francisco",
    "url": "https://theconversation.com/cop30-nzs-lack-of-climate-ambition-undermines-global-goals-and-free-trade-agreements-267727",
    "title": "COP30: NZ’s lack of climate ambition undermines global goals and free-trade agreements",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/markets/stocks/news/asian-stocks-trade-mixed-gold-dips-on-china-move/articleshow/125044465.cms",
    "title": "Asian stocks trade mixed, gold dips on China move",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "New Delhi",
    "url": "https://www.ndtvprofit.com/markets/stock-market-today-all-you-need-to-know-going-into-trade-on-november-3-2025",
    "title": "All You Need To Know Going Into Trade On Monday",
    "country": "India",
    "latitude": 28.6139,
    "longitude": 77.2089
  },
  {
    "city": "Ashburn",
    "url": "https://www.justjared.com/2025/11/02/charles-leclerc-dating-history-revealed-meet-his-fiancee-see-the-full-list-of-his-exes/",
    "title": "Charles Leclerc Dating History Revealed: Meet His Fiancée & See the Full List of His Exes",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "Washington",
    "url": "https://publishingperspectives.com/2025/11/at-frankfurt-a-quick-talk-on-the-uns-act-now-campaign/",
    "title": "At Frankfurt: A Quick Talk on the UN’s ‘Act Now’ Campaign",
    "country": "US",
    "latitude": 38.8951,
    "longitude": -77.0364
  },
  {
    "city": "Toronto",
    "url": "https://financialpost.com/pmn/business-pmn/pimco-lg-among-managers-supporting-more-investment-in-mining",
    "title": "Pimco, L&G Among Managers Supporting More Investment in Mining",
    "country": "Canada",
    "latitude": 43.6535,
    "longitude": -79.3839
  },
  {
    "city": "London",
    "url": "https://news.sky.com/story/prince-william-to-attend-earthshot-prize-and-cop30-in-brazil-with-his-team-hoping-to-refocus-attention-away-from-andrew-13463000",
    "title": "Can Prince William drag attention away from Andrew during Brazil visit?",
    "country": "GB",
    "latitude": 51.5085,
    "longitude": -0.1257
  },
  {
    "city": "Atlanta",
    "url": "https://www.nature.com/articles/s41598-025-22139-3",
    "title": "Violence against female sex workers in the state of Piauí, Brazil – a cross-sectional study",
    "country": "US",
    "latitude": 33.749,
    "longitude": -84.388
  },
  {
    "city": "Dublin",
    "url": "https://pubs.rsc.org/en/content/articlelanding/2025/tc/d5tc03197d",
    "title": "Structure–property coupling in lead-free halides Rb3Sb2Br9 and Rb3Sb2Br6I3 obtained by mechanochemistry",
    "country": "IE",
    "latitude": 53.3331,
    "longitude": -6.2489
  },
  {
    "city": "Columbus",
    "url": "https://oilprice.com/Energy/Energy-General/Energy-Transition-Stalls-10-Years-After-Paris-Agreement.html",
    "title": "Energy Transition Stalls 10 Years After Paris Agreement",
    "country": "US",
    "latitude": 39.9612,
    "longitude": -82.9988
  },
  {
    "city": "San Francisco",
    "url": "https://www.snopes.com//fact-check/bill-gates-climate-change/",
    "title": "Bill Gates said climate change 'will not lead to humanity's demise'?",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Ashburn",
    "url": "https://www.nature.com/articles/d41586-025-03571-x",
    "title": "How to fight climate change without the US: a guide to global action",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "Nürnberg",
    "url": "https://mypeoplesreview.com/2025/11/03/peak-tourist-season-sees-128443-arrivals-in-a-month/",
    "title": "Peak tourist season sees 128,443 arrivals in a month",
    "country": "DE",
    "latitude": 49.4542,
    "longitude": 11.0775
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/defence/pakistan-eyes-2026-launch-for-first-chinese-submarine-in-5-billion-arms-deal/articleshow/125045444.cms",
    "title": "Pakistan eyes 2026 launch for first Chinese submarine in $5 billion arms deal",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/markets/stocks/news/jayesh-logistics-ipo-listing-today-gmp-suggests-modest-premium-likely/articleshow/125045068.cms",
    "title": "Jayesh Logistics IPO listing today. GMP suggests modest premium likely",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "San Francisco",
    "url": "https://english.khabarhub.com/2025/03/504069/",
    "title": "Economic Digest: Nepal’s Business News in a Snap",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "New Delhi",
    "url": "https://indianexpress.com/article/political-pulse/no-barbed-wire-bangladesh-bengal-bjp-mps-remark-put-party-10342663/",
    "title": "‘No barbed wire with Bangladesh’: Why Bengal BJP MP’s remark has put the party in a bind",
    "country": "India",
    "latitude": 28.6419,
    "longitude": 77.2217
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/sports/a-47-year-wait-ends-how-indian-womens-cricket-found-its-own-1983-moment/articleshow/125044668.cms",
    "title": "A 47-year wait ends: How Indian Women’s Cricket found its own ‘1983 moment’",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Chicago",
    "url": "https://make.wordpress.org/community/2025/11/03/monthly-education-buzz-report-october-2025/",
    "title": "Monthly Education Buzz Report – October 2025",
    "country": "US",
    "latitude": 41.85,
    "longitude": -87.65
  },
  {
    "city": "San Francisco",
    "url": "https://line25.com/articles/mostbet-apk-download-recognized-app/",
    "title": "Mostbet Apk Download Recognized App",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Nürnberg",
    "url": "https://mypeoplesreview.com/2025/11/03/sc-issues-interim-order-halting-ambassador-recall-2/",
    "title": "SC issues interim order halting ambassador recall",
    "country": "DE",
    "latitude": 49.4542,
    "longitude": 11.0775
  },
  {
    "city": "Dublin",
    "url": "https://pubs.rsc.org/en/content/articlelanding/2025/ra/d5ra02952j",
    "title": "Integrated biodiesel and biopolymer production from Nannochloropsis biomass: a closed-loop biorefinery approach",
    "country": "IE",
    "latitude": 53.3331,
    "longitude": -6.2489
  },
  {
    "city": "Ashburn",
    "url": "https://www.globenewswire.com/news-release/2025/11/02/3178815/0/en/Alvotech-Provides-Update-on-the-Status-of-U-S-Biologics-License-Application-for-AVT05.html",
    "title": "Alvotech Provides Update on the Status of U.S. Biologics License Application for AVT05",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "Ashburn",
    "url": "https://www.globenewswire.com/news-release/2025/11/02/3178814/0/en/Alvotech-Provides-Update-on-the-Status-of-U-S-Biologics-License-Application-for-AVT05.html",
    "title": "Alvotech Provides Update on the Status of U.S. Biologics License Application for AVT05",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "San Francisco",
    "url": "https://www.bbc.com/sport/cricket/articles/c7813dw7189o",
    "title": "Who made your World Cup team of the tournament?",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Sydney",
    "url": "https://www.abc.net.au/news/2025-11-03/house-prices-increase-again-mortgages-rba-interest-rate-decision/105962246",
    "title": "Social and economic consequences of rising house prices are here to stay",
    "country": "Australia",
    "latitude": -33.8698,
    "longitude": 151.2083
  },
  {
    "city": "Mumbai",
    "url": "https://timesofindia.indiatimes.com/city/guwahati/bangla-national-anthem-case-under-examination-cops-say/articleshow/125038552.cms",
    "title": "Bangla national anthem case under examination, cops say",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "New Delhi",
    "url": "https://indianexpress.com/elections/rjd-put-gun-to-cong-head-for-cm-face-says-pm-modi-rahul-says-op-sindoor-was-stopped-under-us-pressure-10342276/",
    "title": "RJD put gun to Cong head for CM face, says PM Modi; Rahul says Op Sindoor was stopped under US pressure",
    "country": "India",
    "latitude": 28.6419,
    "longitude": 77.2217
  },
  {
    "city": "San Francisco",
    "url": "https://www.notebookcheck.net/Realme-C85-Pro-launches-with-a-7-000-mAh-battery-and-is-well-protected-against-water-even-for-weeks-of-diving.1153441.0.html",
    "title": "Realme C85 Pro launches with a 7,000 mAh battery and is well protected against water, even for weeks of diving",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/sports/ind-w-vs-sa-w-shafali-verma-smashes-half-century-in-womens-world-cup-final-gives-india-a-flying-start-with-smrti-mandhana/articleshow/125034076.cms",
    "title": "Ind W vs SA W: Shafali Verma smashes half-century in Women's World Cup final, gives India a flying start with Smrti Mandhana",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/new-updates/school-assembly-news-headlines-for-3rd-november-top-national-international-business-and-sports-update/articleshow/125034097.cms",
    "title": "School Assembly News Headlines for 3rd November: Top national, international, business and sports update",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "New Delhi",
    "url": "https://indianexpress.com/article/world/trump-says-no-tomahawk-missiles-for-ukraine-leaves-door-open-10342697/",
    "title": "‘No, not really’: Trump says on Tomahawk missiles for Ukraine, but leaves door open",
    "country": "India",
    "latitude": 28.6419,
    "longitude": 77.2217
  },
  {
    "city": "Ashburn",
    "url": "https://m.economictimes.com/markets/stocks/news/a-measured-move-opec-balances-growth-with-caution/opec-balances-expectations-and-caution/slideshow/125047485.cms",
    "title": "A Measured Move: OPEC+ balances growth with caution",
    "country": "US",
    "latitude": 39.0437,
    "longitude": -77.4875
  },
  {
    "city": "Dublin",
    "url": "https://www.irishtimes.com/culture/books/review/2025/11/03/paschal-donohoe-reviews-the-worlds-worst-bet-how-the-globalisation-gamble-went-wrong/",
    "title": "Paschal Donohoe reviews The World’s Worst Bet: How The Globalisation Gamble Went Wrong",
    "country": "Ireland",
    "latitude": 53.3494,
    "longitude": -6.2606
  },
  {
    "city": "Chennai",
    "url": "https://www.thehindubusinessline.com/companies/bpcl-buys-upper-zakum-crude-for-december-to-replace-russian-oil-sources-say/article70234864.ece",
    "title": "BPCL buys Upper Zakum crude for December to replace Russian oil, sources say",
    "country": "India",
    "latitude": 13.0837,
    "longitude": 80.2702
  },
  {
    "city": "Moscow",
    "url": "https://sputnikglobe.com/20251103/russias-mishustin-arrives-in-china-for-2-day-visit-1123055481.html",
    "title": "Russia's Mishustin Arrives in China for 2-Day Visit",
    "country": "Russia",
    "latitude": 55.6256,
    "longitude": 37.6064
  },
  {
    "city": "Chennai",
    "url": "https://www.thehindubusinessline.com/markets/commodities/crude-oil-futures-gain-as-opec-halts-production-hikes-in-q1-2026/article70234886.ece",
    "title": "Crude oil futures gain as OPEC+ halts production hikes in Q1 2026",
    "country": "India",
    "latitude": 13.0837,
    "longitude": 80.2702
  },
  {
    "city": "New York",
    "url": "https://www.huffpost.com/entry/supreme-court-trump-tariffs-diplomacy_n_69082893e4b00afef15f4d88",
    "title": "Tariffs Are Trump's Favorite Foreign Policy Tool. The Supreme Court Could Change How He Uses Them.",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "Austin",
    "url": "https://www.lewrockwell.com/2025/11/jacob-hornberger/another-regime-change-war-will-accelerate-americas-slide-into-authoritarianism/",
    "title": "Another Regime-Change War Will Accelerate America’s Slide Into Authoritarianism",
    "country": "US",
    "latitude": 30.2672,
    "longitude": -97.7431
  },
  {
    "city": "Austin",
    "url": "https://www.lewrockwell.com/2025/11/no_author/ukraine-hail-mary-operation-to-unblock-pokrovsk-has-failed/",
    "title": "Ukraine – Hail Mary Operation To Unblock Pokrovsk Has Failed",
    "country": "US",
    "latitude": 30.2672,
    "longitude": -97.7431
  },
  {
    "city": "Mumbai",
    "url": "https://timesofindia.indiatimes.com/education/news/gate-application-correction-window-2026-closing-today-check-key-details-and-direct-link-here/articleshow/125046086.cms",
    "title": "GATE application correction window 2026 closing today: Check key details and direct link here",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://timesofindia.indiatimes.com/tv/news/malayalam/bigg-boss-malayalam-7-wildcard-entrant-sabuman-gets-evicted-says-i-just-tried-to-be-genuine-throughout-the-show/articleshow/125046153.cms",
    "title": "Bigg Boss Malayalam 7: Wildcard entrant Sabuman gets evicted, says 'I just tried to be genuine throughout the show'",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/international/global-trends/why-trump-can-do-no-wrong/articleshow/125046136.cms",
    "title": "Why Trump can do no wrong",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://timesofindia.indiatimes.com/entertainment/hindi/bollywood/news/amitabh-bachchan-showers-praise-on-india-womens-cricket-team-after-world-cup-gloryworld-champions-/articleshow/125046031.cms",
    "title": "Amitabh Bachchan showers praise on India Women's Cricket Team after World Cup glory:'WORLD CHAMPIONS !!'",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Bonn",
    "url": "https://www.dw.com/en/trump-says-there-could-be-us-military-action-in-nigeria/a-74592286",
    "title": "Trump says there 'could be' US military action in Nigeria",
    "country": "DE",
    "latitude": 50.7344,
    "longitude": 7.0955
  },
  {
    "city": "Mumbai",
    "url": "https://timesofindia.indiatimes.com/entertainment/hindi/bollywood/news/venice-film-festival-2025-director-anuparna-roy-on-historic-win-it-changed-our-life/articleshow/125045988.cms",
    "title": "Venice Film Festival 2025: Director Anuparna Roy on historic win, 'It changed our life'",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Mumbai",
    "url": "https://timesofindia.indiatimes.com/sports/mlb/news/shohei-ohtanis-world-series-post-sets-the-internet-buzzing-as-nfl-legend-tom-brady-drops-a-fiery-reaction-after-los-angeles-dodgers-dramatic-game-7-win/articleshow/125045840.cms",
    "title": "Shohei Ohtani's World Series post sets the internet buzzing as NFL legend Tom Brady drops a fiery reaction after Los Angeles Dodgers' dramatic Game 7 win",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "Toronto",
    "url": "https://www.digitaljournal.com/life/tehran-toy-museum-brings-old-childhood-memories-to-life/article",
    "title": "Tehran toy museum brings old childhood memories to life",
    "country": "Canada",
    "latitude": 43.6535,
    "longitude": -79.3839
  },
  {
    "city": "Toronto",
    "url": "https://www.digitaljournal.com/world/tehran-toy-museum-brings-old-childhood-memories-to-life/article",
    "title": "Tehran toy museum brings old childhood memories to life",
    "country": "Canada",
    "latitude": 43.6535,
    "longitude": -79.3839
  },
  {
    "city": "San Francisco",
    "url": "https://www.thegatewaypundit.com/2025/11/mic-drop-president-trump-goes-after-60-minutes/",
    "title": "MIC DROP: President Trump Goes Off After ’60 Minutes’ Host Norah O’Donnell Asks if Indictments Against Comey and Letitia James Are “Political Retribution” (VIDEO)",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://www.cbsnews.com/news/read-full-transcript-norah-odonnell-60-minutes-interview-with-president-trump/",
    "title": "Read the full transcript of 60 Minutes' interview with President Trump",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Atlanta",
    "url": "https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-025-02203-w",
    "title": "Host clustering of Campylobacter species and enteric pathogens in a longitudinal cohort of infants, family members and livestock in rural Eastern Ethiopia",
    "country": "US",
    "latitude": 33.749,
    "longitude": -84.388
  },
  {
    "city": "San Francisco",
    "url": "https://www.r-bloggers.com/2025/11/country-codes/",
    "title": "Country codes",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://nypost.com/2025/11/02/opinion/trump-has-already-put-bidens-record-to-shame-after-just-9-months/",
    "title": "Trump has already put Biden’s record to shame after just 9 months",
    "country": "US",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  {
    "city": "Chennai",
    "url": "https://www.thehindubusinessline.com/news/kashmir-hosts-international-marathon-as-tourism-officials-eye-global-spotlight/article70232830.ece",
    "title": "Kashmir hosts international marathon as tourism officials eye global spotlight",
    "country": "India",
    "latitude": 13.0837,
    "longitude": 80.2702
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/industry/transportation/airlines-/-aviation/akasa-air-will-consider-flights-to-kenya-egypt-other-countries-feels-very-good-about-boeing-delivery-schedule-ceo/articleshow/125032140.cms",
    "title": "Akasa Air will consider flights to Kenya, Egypt, other countries; feels 'very good' about Boeing delivery schedule: CEO",
    "country": "India",
    "latitude": 19.055,
    "longitude": 72.8692
  },
  {
    "city": "San Francisco",
    "url": "https://theconversation.com/starvation-as-a-weapon-of-war-how-ethiopia-created-a-famine-in-tigray-268395",
    "title": "Starvation as a weapon of war: how Ethiopia created a famine in Tigray",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Richardson",
    "url": "https://www.juancole.com/2025/11/dockworker-strikes-solidarity.html",
    "title": "Dockworker strikes in solidarity with Gaza have a long legacy",
    "country": "US",
    "latitude": 32.9482,
    "longitude": -96.7297
  },
  {
    "city": "Richardson",
    "url": "https://freerepublic.com/focus/f-news/4350156/posts",
    "title": "Pledging Allegiance to Somalia Is Becoming Common Among Democratic Candidates in Some Blue Cities",
    "country": "US",
    "latitude": 32.9482,
    "longitude": -96.7297
  },
  {
    "city": "San Francisco",
    "url": "https://www.thegatewaypundit.com/2025/11/libertarian-journalist-john-stossel-dismantles-zohran-mamdanis-socialist/",
    "title": "Libertarian Journalist John Stossel Dismantles Zohran Mamdani’s Socialist Plans for New York City (VIDEO)",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://time.com/7330421/sudan-el-fasher-rsf-darfur/",
    "title": "Reports of Mass Killings by Militia After Key City Falls in Sudan",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Seattle",
    "url": "https://www.noahpinion.blog/p/the-giant-basket-case-countries",
    "title": "The giant basket case countries",
    "country": "US",
    "latitude": 47.6339,
    "longitude": -122.3476
  },
  {
    "city": "San Francisco",
    "url": "https://www.techradar.com/how-to-watch/football/liverpool-vs-aston-villa-premier-league-2025-26",
    "title": "Liverpool vs Aston Villa live stream: How to watch Premier League 2025/26, TV channels, broadcasters",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://www.techradar.com/how-to-watch/football/tottenham-hotspur-vs-chelsea-premier-league-2025-26",
    "title": "Tottenham vs Chelsea Live Stream: How to watch Premier League 2025/26 London Derby on TV and online",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Washington",
    "url": "https://www.dailysignal.com/2025/11/01/are-americans-better-or-worse-off-since-january/",
    "title": "Are Americans Better or Worse Off Since January?",
    "country": "Unknown",
    "latitude": 39.7837,
    "longitude": -100.4459
  },
  {
    "city": "San Francisco",
    "url": "http://electrek.co/2025/11/01/we-tested-these-4-chinese-evs-in-the-us-but-dont-ask-us-how/",
    "title": "We tested these 4 Chinese EVs in the US (but don’t ask us how)",
    "country": "US",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  {
    "city": "Moscow",
    "url": "https://sputnikglobe.com/20251101/sputnik-launches-radio-broadcasts-in-burkina-faso-1123049174.html",
    "title": "Sputnik Launches Radio Broadcasts in Burkina Faso",
    "country": "Russia",
    "latitude": 55.6256,
    "longitude": 37.6064
  },
  {
    "city": "San Francisco",
    "url": "https://www.loudersound.com/bands-artists/even-my-dental-hygienist-sent-me-something-the-other-day-to-say-they-were-all-singing-it-at-some-wedding-reception-how-a-british-boogie-rock-band-turned-a-minor-john-fogerty-hit-into-an-all-time-classic-that-kicked-off-the-biggest-gig-in-history",
    "title": "“Even my dental hygienist sent me something the other day to say they were all singing it at some wedding reception”: How a British boogie-rock band turned a minor John Fogerty hit into an all-time classic that kicked off the biggest gig in history",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://www.wmur.com/article/trump-extorted-democrats-shutdown-drags-on/69230565",
    "title": "Trump shuns negotiations as shutdown drags on",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "San Francisco",
    "url": "https://www.wbaltv.com/article/trump-extorted-democrats-shutdown-drags-on/69230565",
    "title": "Trump shuns negotiations as shutdown drags on",
    "country": "US",
    "latitude": 37.7621,
    "longitude": -122.3971
  },
  {
    "city": "Sacramento",
    "url": "https://www.kcra.com/article/trump-extorted-democrats-shutdown-drags-on/69230565",
    "title": "Trump shuns negotiations as shutdown drags on",
    "country": "United States",
    "latitude": 38.5753,
    "longitude": -121.4861
  },
  {
    "city": "New York",
    "url": "https://www.huffpost.com/entry/government-shutdown-trump_n_6908332de4b0ad5446e0843f",
    "title": "Trump Says He 'Won't Be Extorted' By Democrats, Shuns Negotiations As Shutdown Drags On",
    "country": "United States",
    "latitude": 40.7127,
    "longitude": -74.006
  },
  {
    "city": "Columbus",
    "url": "https://www.aljazeera.com/news/2025/11/3/calls-for-justice-after-mexico-mayor-killed-during-day-of-the-dead-festival",
    "title": "Calls for justice after Mexico mayor killed during Day of the Dead festival",
    "country": "US",
    "latitude": 39.9612,
    "longitude": -82.9988
  },
  {
    "city": "Richardson",
    "url": "https://freerepublic.com/focus/f-news/4350346/posts",
    "title": "The water war Trump hasn’t blown up",
    "country": "US",
    "latitude": 32.9482,
    "longitude": -96.7297
  },
  {
    "city": "Sydney",
    "url": "https://www.abc.net.au/news/2025-11-03/carlos-alberto-manzo-rodriguez-killed-during-festivities/105965498",
    "title": "Anti-crime mayor killed during Mexico's Day of the Dead festivities",
    "country": "Australia",
    "latitude": -33.8698,
    "longitude": 151.2083
  }
]

