import re
from langchain.evaluation import RegexMatchStringEvaluator

# Define the transaction text and regex patterns
s = 'Transferência Recebida *** Larissa Soares Carvalho 360.855.938-80 NU *** 900.00'
TRANSACTION_REGEX = r'(Compra no débito|Transferência|Pagamento de boleto|Estorno|Total de entradas|Total de saídas|Pagamento da fatura)'
DATE_REGEX = r'(\d{2} [A-Z]{3} \d{4})'
TRANSACTION_LABELS = [
    'Total de saídas',
    'Compra no',
    'Transferência enviada',
    'Pagamento',
    'Pagamento de boleto efetuado',
    'Pagamento da fatura',
    'Pagamento de boleto'
]

# Create a function to find monetary values
def find_monetary_values(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    pattern = r"\b[R$€£¥]?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)\b"
    matches = re.findall(pattern, text)
    monetary_values = [match for match in matches if len(match.split('.')) == 2]
    return monetary_values

# Create a function to format transaction values using LangChain evaluators
def format_transaction_values(transaction_text):
    if transaction_text is not None:
        monetary_values = find_monetary_values(transaction_text)

        # Use a RegexMatchStringEvaluator to check if the transaction text matches the TRANSACTION_REGEX
        regex_evaluator = RegexMatchStringEvaluator(pattern=TRANSACTION_REGEX)
        regex_result = regex_evaluator.evaluate_strings(prediction=transaction_text)

        if regex_result['score'] > 0:
            # If there's a match with the TRANSACTION_REGEX, check for specific labels
            for label in TRANSACTION_LABELS:
                if label in transaction_text and 'Estorno' not in transaction_text:
                    return '-' + monetary_values[0] if monetary_values else None

        return monetary_values[0] if monetary_values else None

# Use the LangChain evaluator to format and evaluate the transaction text
result = format_transaction_values(s)
print(result)
print("-----")
