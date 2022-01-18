import re
import traceback

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from coins import models
from scraper.dtos import DataSet, Exchange, Issue, Trade


class Scraper:
    COIN_PLACEHOLDER = "<COIN_PLACEHOLDER>"

    def __init__(self):
        self.dataset = DataSet()
        self.dB_coins = models.Coin.objects.all()
        self.dB_exchanges = models.Exchange.objects.all()
        self.dB_rules = models.ExceptionRule.objects.all()

    def run(self):
        self._web_scrape()
        self._generate_trades()

    def _web_scrape(self):
        options = Options()
        # options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=options)
        for dbExchange in self.dB_exchanges:
            exchange = Exchange(dbExchange.name)
            driver.get(dbExchange.markets_page)
            try:
                Scraper.wait_on_load(dbExchange, driver)
            except TimeoutException:
                try:
                    driver.delete_all_cookies()
                    driver.refresh()
                    Scraper.wait_on_load(dbExchange, driver)
                except TimeoutException:
                    self.dataset.issues.append(Issue("ANY", dbExchange.name, "timeout on wait xpath"))
                    continue
            for dbCoin in self.dB_coins:
                xpath = dbExchange.base_xpath
                shorthand = dbCoin.shorthand
                skip = False
                for rule in self.dB_rules.filter(forCoin=dbCoin, forExchange=dbExchange):
                    if rule.kind == models.ExceptionRule.ExceptionKind.DIFF_COIN_SHORTHAND:
                        shorthand = rule.value
                    elif rule.kind == models.ExceptionRule.ExceptionKind.DIFF_XPATH:
                        xpath = rule.value
                    elif rule.kind == models.ExceptionRule.ExceptionKind.NOT_TRADED:
                        skip = True
                        break
                if skip: continue
                try:
                    val = driver.find_element(
                        By.XPATH,
                        xpath.replace(Scraper.COIN_PLACEHOLDER, shorthand)
                    ).text
                    if val is None or val == "":
                        issue = Issue(dbCoin.shorthand, dbExchange.name, "empty value")
                        self.dataset.issues.append(issue)
                    else:
                        exchange.add_coin(dbCoin.shorthand, Scraper.parse_float(val))
                except (ValueError, WebDriverException):
                    issue = Issue(dbCoin.shorthand, dbExchange.name, traceback.format_exc())
                    self.dataset.issues.append(issue)
            self.dataset.exchanges.append(exchange)
        driver.close()

    @staticmethod
    # hail mary attempt to catch some double parsing errors
    def parse_float(val) -> float:
        if "," in val and "." in val:
            val = val.replace(",", "")
        elif "," in val:
            val = val.replace(",", ".")
        values = re.findall(r"[-+]?\d*\.*\d+", val)
        if len(values):
            return float(values[0])
        else:
            raise ValueError(f"regex didn't match any floats in {val}")

    @staticmethod
    def wait_on_load(dbExchange, driver):
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, dbExchange.wait_xpath)
            )
        )

    @staticmethod
    def hard_refresh(driver: webdriver.Chrome) -> None:
        driver.execute_script("location.reload(true);")

    def _generate_trades(self):
        for dbCoin in self.dB_coins:
            for buy_exchange in self.dataset.exchanges:
                for sell_exchange in self.dataset.exchanges:
                    # continue if coins are not traded on both exchanges
                    if dbCoin.shorthand not in buy_exchange.coins or dbCoin.shorthand not in sell_exchange.coins:
                        continue
                    # continue is the trade is going to make a loss
                    if buy_exchange.coins[dbCoin.shorthand].value >= sell_exchange.coins[dbCoin.shorthand].value:
                        continue
                    trade = Trade(
                        buy=buy_exchange.coins[dbCoin.shorthand],
                        sell=sell_exchange.coins[dbCoin.shorthand]
                    )
                    self.dataset.trades.append(trade)
        self.dataset.trades.sort(reverse=True, key=lambda x: x.gain)
