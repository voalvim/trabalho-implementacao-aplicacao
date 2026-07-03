def calcular_inss(salario_mensal: float):
  if salario_mensal <= 0:
    return 0.0

  faixas_inss = [
      (1621.00, 0.075),
      (2902.84, 0.09),
      (4354.27, 0.12),
      (8475.55, 0.14),
  ]

  desconto_inss = 0.0
  restante = salario_mensal
  limite_anterior = 0.0

  for limite, aliquota in faixas_inss:
    if restante <= 0:
      break

    parte = min(restante, limite - limite_anterior)
    desconto_inss += parte * aliquota
    restante -= parte
    limite_anterior = limite

  return min(desconto_inss, 988.09)


def calcular_imposto(salario_mensal: float):
  if salario_mensal < 0:
      raise ValueError("O salário não pode ser negativo.")

  desconto_inss = calcular_inss(salario_mensal)
  base_irpf = salario_mensal - desconto_inss
  salario_anual = salario_mensal * 12

  faixas_irpf = [
      (2428.80, 0.0),
      (2826.65, 0.075),
      (3751.05, 0.15),
      (4664.68, 0.225),
      (float("inf"), 0.275),
  ]

  imposto_irpf = 0.0
  restante = base_irpf
  limite_anterior = 0.0

  for limite, aliquota in faixas_irpf:
    if restante <= 0:
      break

    if limite == float("inf"):
      parte = restante
    else:
      parte = min(restante, limite - limite_anterior)

    imposto_irpf += parte * aliquota
    restante -= parte
    limite_anterior = limite

  reducao_imposto = 0.0
  if 5000.01 <= salario_mensal <= 7350.0:
    reducao_imposto = 978.62 - 0.133145 * salario_mensal
    if reducao_imposto < 0:
      reducao_imposto = 0.0

  imposto_irpf = max(imposto_irpf - reducao_imposto, 0.0)
  desconto_total = desconto_inss + imposto_irpf
  imposto_anual = imposto_irpf * 12
  liquido_mensal = salario_mensal - desconto_total
  liquido_anual = salario_anual - desconto_total * 12
  percentual_descontado = (desconto_total / salario_mensal * 100) if salario_mensal else 0.0

  if salario_mensal <= 2428.80:
    faixa = "Isento (até R$ 2.428,80)"
  elif salario_mensal <= 2826.65:
    faixa = "7,5%"
  elif salario_mensal <= 3751.05:
    faixa = "15%"
  elif salario_mensal <= 4664.68:
    faixa = "22,5%"
  else:
    faixa = "27,5%"

  return {
    "salario_mensal": salario_mensal,
    "salario_anual": salario_anual,
    "desconto_inss": desconto_inss,
    "base_irpf": base_irpf,
    "imposto_irpf": imposto_irpf,
    "imposto_anual": imposto_anual,
    "reducao_imposto": reducao_imposto,
    "desconto_total": desconto_total,
    "liquido_mensal": liquido_mensal,
    "liquido_anual": liquido_anual,
    "percentual_descontado": percentual_descontado,
    "faixa": faixa,
  }


salario_mensal = float(input("Informe seu salário bruto mensal (R$): "))

resultado = calcular_imposto(salario_mensal)

print(f"Salário bruto mensal: R$ {resultado['salario_mensal']:.2f}")
print(f"Salário bruto anual: R$ {resultado['salario_anual']:.2f}")
print(f"Desconto INSS mensal: R$ {resultado['desconto_inss']:.2f}")
print(f"Base de cálculo do IRPF: R$ {resultado['base_irpf']:.2f}")
print(f"Faixa de imposto: {resultado['faixa']}")
print(f"IRPF mensal: R$ {resultado['imposto_irpf']:.2f}")
print(f"IRPF anual: R$ {resultado['imposto_anual']:.2f}")
print(f"Redução de imposto aplicada: R$ {resultado['reducao_imposto']:.2f}")
print(f"Desconto total mensal: R$ {resultado['desconto_total']:.2f}")
print(f"Salário líquido mensal: R$ {resultado['liquido_mensal']:.2f}")
print(f"Salário líquido anual: R$ {resultado['liquido_anual']:.2f}")
print(f"Percentual descontado: {resultado['percentual_descontado']:.2f}%")