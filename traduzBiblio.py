#utf-8
import ast,re
# Carregando dicionario e montando obeto dict
dicioTxt = open("dicioTermos.txt", "r",encoding='utf8')
conteudo = dicioTxt.read()
dicioTxt.close()
dicioTermos = ast.literal_eval('{' + conteudo[:-1] + '}')
# Carregando dicionario e montando obeto dict
aTraduzir = open("aTraduzir.txt", "r",encoding='utf8')
conteudo = aTraduzir.read()
aTraduzir.close()
dicioNovos = ast.literal_eval('{' + conteudo[:-1] + '}')
#
novosTermos = []
arquivos = [
#    'Sor Dante do Vale.gcs'
#    'Basic Set Advantages.adq',
#    'Basic Set Enhancement Modifiers.adm',
#    'Basic Set Limitation Modifiers.adm',
#    'Basic Set Skills.skl',
    'Basic Set Equipment.eqp'
]
#
def dict2txt(dicionario):
    txt = ''
    for key, value in iter(dicionario.items()):
        txt += '\'' + key.replace('\\"','\\\\"').replace('\'','\\\'') + '\':\'' + value.replace('\\"','\\\\"').replace('\'','\\\'') + '\','+ '\n'
    return txt[:-1]
#
def atualizaArquivosFontes ():
    incluidos = []
    dicioTermosAlterados = False
    for key, value in iter(dicioNovos.items()):
        if key != value:
            dicioTermos[key] = value
            incluidos.append(key)
            dicioTermosAlterados = True
    for key in incluidos:
        del dicioNovos[key]
    with open ('aTraduzir.txt','w',encoding='utf8') as main:
        main.write(dict2txt(dicioNovos))
#
    if dicioTermosAlterados: 
        with open ('dicioTermos.txt','w',encoding='utf8') as main:
            main.write(dict2txt(dicioTermos))
#
def buscaNovosTermos(texto):
    for linha in texto.splitlines():
        if any (termo in linha for termo in ('"name": "','"qualifier": "','"specialization": "','"description": "')):
            if re.search('(?<=": )(.*")',linha).group(1) not in dicioTermos.values():
                novaLinha = '\'' + re.search('(?<=": )(.*")',linha).group(1).replace('\'','\\\'') + '\':\'' + re.search('(?<=": )(.*")',linha).group(1).replace('\'','\\\'') + '\','
                novosTermos.append(novaLinha) if novaLinha not in novosTermos else novosTermos
#
def atualizaATraduzir():
    listaCompleta = dict2txt(dicioNovos).splitlines()
    listaCompleta.append(novosTermos)
#    txt = '\n'.join(sorted(novosTermos))
    txt = '\n'.join(novosTermos)
    with open ('aTraduzir.txt','w',encoding='utf8') as main:
        main.write(txt) 
#
atualizaArquivosFontes()
#
for arquivo in arquivos:
#    with open(r'.\\' + arquivo,'r',encoding='utf8') as main:
    with open(arquivo,'r',encoding='utf8') as main:
        input_data = main.read()
    input_data = input_data.replace('"type": "Skill"','"type": "skill"')
    for key, value in iter(dicioTermos.items()):
#        if key not in ('total','multiplier','percentage','points','true','skill','advantage','burn','cor','cut','fat','modifier')
        input_data = input_data.replace(key,value)
#    with open(r'.\\' + arquivo,'w', encoding='utf8') as new_main:
    with open(arquivo,'w', encoding='utf8') as new_main:
        new_main.write(input_data)
    buscaNovosTermos(input_data)
#
atualizaATraduzir()
#