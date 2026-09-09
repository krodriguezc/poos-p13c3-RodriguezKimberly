class RegistroTiempo:
    def __init__(self, fecha: str, horas: float):
        self.fecha = fecha
        self.horas = horas

    def mostrardatos(self)->str:
        return f"{self.fecha} {self.horas}"

    def mostrardatos2(self, hola:str)->str:
        return f"///////  {self.fecha} {hola}"