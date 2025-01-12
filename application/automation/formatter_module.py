def format_number(input_number):
    """
    Formatea un número al estilo nn.nnn,mm
    :param input_number: Número (int o float) a formatear
    :return: Cadena con el número formateado
    """
    # Asegurarse de que sea un número flotante
    number = float(input_number)
    
    # Separar la parte entera y decimal
    integer_part, decimal_part = f"{number:.2f}".split(".")
    
    # Formatear la parte entera con separadores de miles
    formatted_integer = "{:,}".format(int(integer_part)).replace(",", ".")
    
    # Combinar las partes con coma como separador decimal
    return f"{formatted_integer},{decimal_part}"


if __name__ == "__main__":
    print(format_number(13123123120.00))