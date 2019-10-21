from hsbcpdfreader import HSBCPdfReader

hpr = HSBCPdfReader('/Users/j.waterschoot/Downloads/statements.pdf')
df = hpr.get_dataframe()
print(df)