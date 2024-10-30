from abc ABC, abstractmethod
from validadorclave.modelo.errores import (NoCumpleLongitudMinimaError, NoTieneLetraMayusculaError, NoTieneLetraMinusculaError, NoTieneNumeroError, NoTieneCaracterEspecialError, NoTienePalabraSecretaError)


@abstractmethod

class ReglaValidacion(ABC):

    def __init__ (self, longitud_esperada: int):
        self.longitud_esperada = longitud_esperada
    
    def _validar_longitud(self, clave: str) -> bool:
        return len(clave) > self.longitud_esperada
    
    def _contiene_mayuscula(self, clave: str) -> bool:
        return any(caracter.isupper() for caracter in clave)
    
    def _contiene_minuscula(self, clave: str) -> bool:
        return any(caracter.islower() for caracter in clave)
    
    def _contiene_numero(self, clave: int) -> bool:
        return any(caracter.isdigit() for caracter in clave)
    
class ReglaValidacionGaminedes(ReglaValidacion):
    def __init__(self):
        super().__init__(longitud_esperada=8)
    
    def _contiene_caracter_especial(self, clave:str) -> bool:
        caracteres_especiales = '@_%$#'
        return any(caracter in caracteres_especiales for caracter in clave)
    
    def es_valida(self, clave:str) -> bool:
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError("La longitud de la clave no es valida")
        if not self._contiene_mayuscula(clave):
            raise NoTieneLetraMayusculaError("La clave debe contener al menos una letra mayuscula")
        if not self._contiene_minuscula(clave):
            raise NoTieneLetraMinusculaError("La clave debe contener al menos una letra minuscula")
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError("La clave debe contener al menos un numero")
        if not self._contiene_caracter_especial(clave):
            raise ExcepcionCaracterEspecialNoEncontrado("La clave debe contener al menos un carácter especial.")
        return True
    
class ReglavalidacionCalisto(ReglaValidacion):
    def es_valida(self):
        super().__init__(longitud_esperada=6)
    
    def contiene_calisto(self, clave:str) -> bool:
        posicion = clave.find("calisto")
        if posicion == -1:
            return False
        
    
        palabra_calisto = clave[posicion:posicion + len("calisto")]
        mayusculas = sum(1 for caracter in palabra_calisto if caracter.issuper())

        return mayusculas >= 2 and mayusculas < len(palabra_calisto)

    def es_valida(self, clave:str) -> bool:
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError("La longitud de la clave no es valida")
    
        if not self._contiene_mayuscula(clave):
            raise NoTieneLetraMayusculaError("La clave debe contener al menos una letra mayuscula")
        
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError("La clave debe contener al menos un numero")

        if not self.contiene_calisto(clave):
            raise NoTienePalabraSecretaError("La clave no cumple con la regla de 'calisto'")
        return True
    
class Validador:
    def __init__(self, regla):
        self.regla = regla

    def es_valida(self, clave: str) -> bool:
        return self.regla.es_valida(clave)    
    