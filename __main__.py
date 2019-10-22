from hsbcpdfreader import HSBCPdfReader
from hsbccreditcardpdfreader import HSBCCreditCardPdfReader

hpr = HSBCCreditCardPdfReader('/Users/j.waterschoot/Downloads/Statement-3.pdf')
df = hpr.get_dataframe()
print(df)