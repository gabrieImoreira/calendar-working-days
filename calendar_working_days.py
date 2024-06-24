from datetime import timedelta
import requests

class CalendarWorkingDays:
    """ Classe para trabalhar com o calendário de São Paulo, Brasil """

    def __init__(self):
        # Dicionário para armazenar os feriados já obtidos
        self.lista_feriados = {}

    def get_holidays(self, year):
        """
        Obtem os feriados para o ano especificado

        Parameters:
        year (int): Ano para obter os feriados

        Returns:
        list: Lista de feriados no formato 'YYYY-MM-DD'
        """
        # Verifica se já temos os feriados para o ano solicitado
        if year in self.lista_feriados:
            return self.lista_feriados[year]

        # Se não tiver, faz a requisição à API BrasilAPI para obter os feriados
        next_year = year + 1
        url = f"https://brasilapi.com.br/api/feriados/v1/{year}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            holidays = response.json()
            list_holidays = [holiday['date'] for holiday in holidays]
            # feriado de aniversário de São Paulo
            list_holidays.append(f'{year}-01-25')

            # Armazena os feriados no dicionário para reuso futuro
            self.lista_feriados[year] = list_holidays
            return list_holidays

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Erro ao obter feriados: {e}")

    def is_working_day(self, date):
        """
        Verifica se a data é um dia útil
        
        Parameters:
        date (datetime): Data a ser verificada

        Returns:
        bool: True se for um dia útil, False caso contrário
        """
        year = date.year
        if year not in self.lista_feriados:
            self.get_holidays(year)

        if date.weekday() >= 5:  # 5 e 6 são sábado e domingo
            return False
        
        date_str = date.strftime('%Y-%m-%d')
        for holiday in self.lista_feriados[year]:
            if holiday == date_str:
                return False
        
        return True

    def add_working_days(self, date, days):
        """
        Adiciona um número de dias úteis à data especificada
        
        Parameters:
        date (datetime): Data base
        days (int): Número de dias úteis a serem adicionados
        
        Returns:
        datetime: Data resultante após adicionar os dias úteis
        """
        current_date = date
        count_days = 0

        while count_days < days:
            current_date += timedelta(days=1)
            if self.is_working_day(current_date):
                count_days += 1

        return current_date
