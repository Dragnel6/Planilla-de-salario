import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    cargo = request.form['cargo']
    salario = float(request.form['salario'])

    # Cálculo de ISSS (El salario arriba de mil máximo quitar $30)
    ISSS = salario * 0.03 if salario <= 1000 else 30.00

    # Cálculo de AFP (7.25% del salario del empleado)
    AFP = salario * 0.0725

    # Renta imponible
    renta_imponible = salario - ISSS - AFP

    # Cálculo del ISR (Impuesto sobre la renta) - SOLO si la renta imponible es mayor a 472
    if renta_imponible <= 472.00:
        ISR = 0
    elif renta_imponible <= 895.24:
        ISR = (renta_imponible - 472.00) * 0.10 + 17.67
    elif renta_imponible <= 2038.10:
        ISR = (renta_imponible - 895.24) * 0.20 + 60.00
    else:
        ISR = (renta_imponible - 2038.10) * 0.30 + 288.57

    # Salario líquido (después de impuestos)
    salario_neto = renta_imponible - ISR

    # Aportes patronales
    ISSS_patronal = salario * 0.075  # 7.5% del salario
    AFP_patronal = salario * 0.0875  # 8.75% del salario

    # Redondeo de valores a 2 decimales
    ISSS = round(ISSS, 2)
    AFP = round(AFP, 2)
    ISR = round(ISR, 2)
    salario_neto = round(salario_neto, 2)
    ISSS_patronal = round(ISSS_patronal, 2)
    AFP_patronal = round(AFP_patronal, 2)

    # Sumar los aportes del empleado y del patrono
    isss_total = round(ISSS + ISSS_patronal, 2)
    afp_total = round(AFP + AFP_patronal, 2)

    return render_template('index.html', nombre=nombre, apellido=apellido, cargo=cargo, salario=salario, ISSS=ISSS, AFP=AFP, 
    renta_imponible=renta_imponible, ISR=ISR, salario_neto=salario_neto, 
    ISSS_patronal=ISSS_patronal, AFP_patronal=AFP_patronal, 
    isss_total=isss_total, afp_total=afp_total)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


