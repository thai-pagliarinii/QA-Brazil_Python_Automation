from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import data
from helpers import retrieve_phone_code
import time

class UrbanRoutesPage:
    #seção De e Para
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    #seção tarifas
    taxi_option_locator = (By.XPATH, '//button[contains(text(),"Chamar")]')
    comfort_icon_locator = (By.XPATH, '//img[@src="/static/media/kids.075fd8d4.svg"]')
    comfort_active = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    #telefone
    add_phone_number = (By.CCS_SELECTOR, '.np-button')
    phone_number = (By.ID, 'phone')
    phone_number_enter = (By.CCS_SELECTOR, '.button full')
    phone_number_code = (By.ID, 'code')
    code_confirm_button = (By.XPATH, '//button[contains(text(), "Confirmar")]')
    number_finish = (By.CCS_SELECTOR, '.np-text')
    # Pagamento
    payment_method_select = (By.CCS_SELECTOR, '.pp-button.filled')
    add_card = (By.CCS_SELECTOR, '.pp-plus')
    card_number = (By.ID, 'number')
    card_code = (By.CCS_SELECTOR, 'input.card-input#code')
    add_finish_card = (By.XPATH, '//button[contains(text(), "Adicionar")]')
    close_button_card = (By.CCS_SELECTOR, '.payment-picker.open .close-button')
    confirm_card = (By.CCS_SELECTOR, '.pp-value-text')
    #mensagens e opções
    add_comment = (By.ID, 'comment')
    switch_blanket = (By.CSS_SELECTOR, '.switch')
    switch_blanket_active = (By.CSS_SELECTOR,
                             '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div:nth-child(1) > div > div.r-sw > div > input')
    add_ice_cream = (By.XPATH, '.counter-plus' )
    quantity_sorvete = (By.CCS_SELECTOR, '.counter-value')
    # Pedido final
    order_car_button = (By.CSS_SELECTOR, '.smart-button')
    order_pop_up = (By.CSS_SELECTOR, '.order-header-title')

    def __init__(self, driver):
        self.driver = driver

    def enter_from_location(self, from_text):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_text)

    def enter_to_location(self, to_text):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.to_field))
        self.driver.find_element(*self.to_field).send_keys(to_text)

    def enter_locations(self, from_text, to_text):
        self.enter_from_location(from_text)
        self.enter_to_location(to_text)

    def get_from_location_value(self):
        return WebDriverWait(self.driver, 3).until(
        EC.visibility_of_element_located(self.from_field)
            ).get_attribute('value')

    def get_to_location_value(self):
        return WebDriverWait(self.driver, 3).until(
        EC.visibility_of_element_located(self.to_field)
            ).get_attribute('value')

    def click_taxi_option(self):
        self.driver.find_element(*self.taxi_option_locator).click()

    def click_comfort_icon(self):
        self.driver.find_element(*self.comfort_icon_locator).click()

    def click_comfort_active(self):
        try:
            active_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.comfort_active))
            return "active" in active_button.get_attribute("class")
        except:
            return False

    def click_number_text(self, telefone):
        self.driver.find_element(*self.add_phone_number).click()
        time.sleep(2)
        self.driver.find_element(*self.phone_number).send_keys(telefone)
        time.sleep(2)
        self.driver.find_element(*self.phone_number_enter).click()
        time.sleep(2)

        code = retrieve_phone_code(self.driver)  # Digita o código
        code_input = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(*self.phone_number_code)
        )
        code_input.clear()
        code_input.send_keys(code)

        self.driver.find_element(*self.code_confirm_button).click()

    def numero_confirmado(self):
        numero = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.number_finish))
        return numero.text

    def click_add_cartao(self, cartao, code):
        self.driver.find_element(*self.payment_method_select).click()
        self.driver.find_element(*self.add_card).click()
        time.sleep(2)
        self.driver.find_element(*self.card_number).send_keys(cartao)
        time.sleep(2)
        self.driver.find_element(*self.card_code).send_keys(code)
        time.sleep(1)
        self.driver.find_element(*self.add_finish_card).click()
        self.driver.find_element(*self.close_button_card).click()

    def confirm_cartao(self):
        return self.driver.find_element(*self.confirm_card).text

    def add_comentario(self, comentario):
        self.driver.find_element(*self.add_comment).send_keys(comentario)

    def comment_comfirm(self):
        return self.driver.find_element(*self.add_comment).get_attribute('value')

    def switch_cobertor(self):
        switch_ativo = self.driver.find_element(*self.switch_blanket)
        switch_ativo.click()

    def switch_cobertor_active(self):
        switch = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.switch_blanket_active))
        return switch.is_selected()

    def click_add_ice_cream(self):
        #clicar na opcao sortvete
        self.driver.find_element(*self.add_ice_cream).click()

    def quantity_sorvete(self):
        return self.driver.find_element(*self.quantity_sorvete).text

    def click_order_car_button(self):
        #chamar o carro
        self.driver.find_element(*self.order_car_button).click()

    def pop_up_show(self):
        pop_up = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(*self.pop_up_show()))
        return pop_up.text